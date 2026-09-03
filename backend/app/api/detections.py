import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.detection import Detection as DetectionModel
from app.models.image import Image as ImageModel
from app.priority.engine import sort_priority_items
from app.schemas.detection import DetectionDetail, DetectionSummary, PriorityItem
from app.services.detection_service import (
    priority_rationale,
    run_detection_for_image,
    to_detail_joined,
)

router = APIRouter(prefix="/api/detections", tags=["detections"])


@router.post("/run", response_model=list[DetectionSummary], status_code=201)
def run_detections(image_id: str = Query(...), db: Session = Depends(get_db)):
    image = db.get(ImageModel, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail=f"Image {image_id} not found.")
    try:
        created = run_detection_for_image(image_id, db=db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")
    if not created:
        return []
    return [DetectionSummary.model_validate(d) for d in created]


@router.get("", response_model=list[DetectionDetail])
def list_detections(
    unknown_only: bool = Query(False),
    min_risk: float | None = Query(None, ge=0, le=100),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = (
        db.query(DetectionModel)
        .join(ImageModel)
        .options(joinedload(DetectionModel.evidence), joinedload(DetectionModel.feedback_items))
        .order_by(DetectionModel.created_at.desc())
    )
    if unknown_only:
        q = q.filter(DetectionModel.is_unknown_anomaly.is_(True))
    if min_risk is not None:
        q = q.filter(DetectionModel.risk_score >= min_risk)
    rows = q.limit(limit).offset(offset).all()
    out = []
    for det in rows:
        img = db.get(ImageModel, det.image_id)
        out.append(to_detail_joined(det, img))
    return out


@router.get("/priority-queue", response_model=list[PriorityItem])
def recovery_priority(db: Session = Depends(get_db)):
    rows = (
        db.query(DetectionModel)
        .join(ImageModel)
        .filter(DetectionModel.status != "REJECTED")
        .all()
    )
    items = []
    for det in rows:
        img = db.get(ImageModel, det.image_id)
        detail = to_detail_joined(det, img)
        detail["rationale"] = priority_rationale(det, img)
        items.append(PriorityItem(**detail))
    return sort_priority_items(items)


@router.get("/{detection_id}", response_model=DetectionDetail)
def get_detection(detection_id: str, db: Session = Depends(get_db)):
    det = (
        db.query(DetectionModel)
        .options(joinedload(DetectionModel.evidence), joinedload(DetectionModel.feedback_items))
        .filter(DetectionModel.id == detection_id)
        .first()
    )
    if det is None:
        # Guard against non-uuid lookups hitting DB errors
        try:
            uuid.UUID(detection_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid detection id format.")
        raise HTTPException(status_code=404, detail="Detection not found.")
    img = db.get(ImageModel, det.image_id)
    return to_detail_joined(det, img)
