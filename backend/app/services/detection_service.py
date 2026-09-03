"""Detection service: orchestrates preprocessing output -> inference -> evidence ->
risk -> priority -> database persistence."""
from sqlalchemy.orm import Session

from app.ai.inference_service import apply_unknown_anomaly_policy, get_detector
from app.database import SessionLocal
from app.evidence.engine import build_evidence, location_factor
from app.models.detection import Detection as DetectionModel
from app.models.evidence import Evidence as EvidenceModel
from app.models.image import Image as ImageModel
from app.models.model_version import ModelVersion as ModelVersionModel
from app.priority.engine import rationale_text
from app.preprocessing.preprocessor import letterbox_transform, unletterbox_bbox
from app.risk.engine import RiskInput, compute_risk, priority_from_risk


def _ensure_model_version(db: Session, version: str, model_name: str, demo: bool) -> None:
    exists = db.query(ModelVersionModel).filter_by(version=version).first()
    if exists:
        exists.is_active = True
        db.commit()
        return
    db.add(ModelVersionModel(
        version=version,
        model_name=model_name,
        description=("Development DEMO MODEL producing deterministic heuristic "
                     "pseudo-detections. Not scientifically validated." if demo
                     else "Real ONNX object detector; boxes and confidence come from model inference."),
        is_active=True,
    ))
    db.commit()


def run_detection_for_image(image_id: str, db: Session | None = None) -> list:
    own_db = db is None
    db = db or SessionLocal()
    try:
        record = db.get(ImageModel, image_id)
        if record is None:
            raise ValueError(f"Image {image_id} not found")

        detector, info = get_detector()
        # Keep this list before inserting a new run.  A re-run must replace an
        # earlier result even when the current model correctly returns no boxes.
        previous_detections = db.query(DetectionModel).filter(
            DetectionModel.image_id == record.id,
        ).all()

        import cv2
        processed = cv2.imread(record.processed_path or record.storage_path)
        original = cv2.imread(record.storage_path)
        if processed is None or original is None:
            raise ValueError("Stored image could not be read")

        raw_candidates = detector.detect(processed)
        transform = letterbox_transform(original.shape)
        for candidate in raw_candidates:
            candidate.bbox = unletterbox_bbox(candidate.bbox, transform)
        kept = apply_unknown_anomaly_policy(raw_candidates)

        _ensure_model_version(db, detector.version, detector.name, info.get("demo", True))

        created = []
        for cand in kept:
            final_label = cand.final_label
            loc_factor = location_factor(record.latitude, record.longitude)
            ev_data = build_evidence(cand, original.shape)
            sev = ev_data["severity_score"]

            risk = compute_risk(RiskInput(
                confidence=cand.confidence,
                severity_score=sev,
                estimated_size_m2=cand.estimated_size_m2,
                location_factor=loc_factor,
            ))
            prio = priority_from_risk(risk.risk_score, final_label, cand.confidence,
                                      cand.estimated_size_m2)

            det = DetectionModel(
                image_id=record.id,
                object_type=final_label,
                raw_label=cand.label,
                confidence=cand.confidence,
                is_unknown_anomaly=(not cand.is_known),
                risk_score=risk.risk_score,
                risk_level=risk.risk_level,
                priority=prio,
                bbox=cand.bbox,
                mask_path=None,
                estimated_size_m2=cand.estimated_size_m2,
                severity_score=sev,
                location_factor=loc_factor,
                model_version=detector.version,
                status="PENDING",
            )
            db.add(det)
            db.flush()
            db.add(EvidenceModel(
                detection_id=det.id,
                confidence_evidence=ev_data["confidence_evidence"],
                visual_evidence=ev_data["visual_evidence"],
                shadow_evidence=ev_data["shadow_evidence"],
                explanation=ev_data["explanation"],
            ))
            created.append(det)

        # Remove previous detections when re-running analysis on the same image.
        # ORM deletion is deliberate: it also removes evidence and expert-feedback
        # children through the model relationships rather than leaving orphans.
        for old in previous_detections:
            db.delete(old)

        db.commit()
        for d in created:
            db.refresh(d)
        return created
    finally:
        if own_db:
            db.close()


def to_detail(det: DetectionModel) -> dict:
    """Serialize a Detection ORM row into the DetectionDetail payload shape."""
    return {
        "id": det.id,
        "object_type": det.object_type,
        "raw_label": det.raw_label,
        "confidence": det.confidence,
        "is_unknown_anomaly": det.is_unknown_anomaly,
        "risk_score": det.risk_score,
        "risk_level": det.risk_level,
        "priority": det.priority,
        "bbox": det.bbox,
        "estimated_size_m2": det.estimated_size_m2,
        "model_version": det.model_version,
        "status": det.status,
        "severity_score": det.severity_score,
        "location_factor": det.location_factor,
        "evidence": det.evidence,
        "feedback": det.feedback_items,
        "image_id": det.image_id,
        "image_filename": None,
        "image_storage_path": None,
        "image_processed_path": None,
        "latitude": None,
        "longitude": None,
        "depth": None,
        "timestamp": None,
    }


def to_detail_joined(det: DetectionModel, image: ImageModel) -> dict:
    base = to_detail(det)
    base.update({
        "image_id": image.id,
        "image_filename": image.filename,
        "image_storage_path": image.storage_path,
        "image_processed_path": image.processed_path,
        "latitude": image.latitude,
        "longitude": image.longitude,
        "depth": image.depth,
        "timestamp": image.timestamp,
    })
    return base


def priority_rationale(det: DetectionModel, image: ImageModel) -> str:
    return rationale_text(
        det.object_type, det.risk_score, det.confidence, det.priority,
        image.latitude is not None and image.longitude is not None,
    )
