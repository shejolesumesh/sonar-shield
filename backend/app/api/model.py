from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.inference_service import get_detector
from app.config import settings
from app.database import get_db
from app.models.feedback import ExpertFeedback as FeedbackModel
from app.models.model_version import ModelVersion as ModelVersionModel

router = APIRouter(prefix="/api/model", tags=["model"])


@router.get("")
def model_info(db: Session = Depends(get_db)):
    detector, info = get_detector()
    versions = db.query(ModelVersionModel).order_by(ModelVersionModel.created_at.desc()).all()
    feedback_count = db.query(FeedbackModel).count()

    return {
        "active_mode": info.get("mode"),
        "is_demo_model": info.get("demo", True),
        "fallback_reason": info.get("fallback_reason"),
        "configured_detector_type": settings.DETECTOR_TYPE,
        "model_name": info.get("model_name", detector.name),
        "model_format": info.get("model_format"),
        "model_version": detector.version,
        "supported_classes": info.get("supported_classes", []),
        "model_path": info.get("model_path"),
        "input_shape": info.get("input_shape"),
        "output_shape": info.get("output_shape"),
        "nms_in_model": info.get("nms_in_model"),
        "class_metadata_note": ("ONNX stores a numeric class-index placeholder; supplied class_names.txt maps index 0 to Crab-Pot."
                                if info.get("embedded_class_metadata") == "{0: '0'}" else None),
        "known_class_threshold": settings.KNOWN_CLASS_THRESHOLD,
        "min_detection_confidence": settings.MIN_DETECTION_CONFIDENCE,
        "risk_formula": {
            "expression": ("risk = W_CONF*confidence + W_SEV*severity + "
                           "W_SIZE*normalized_size + W_LOC*location_factor"),
            "weights": {
                "confidence": settings.RISK_W_CONFIDENCE,
                "severity": settings.RISK_W_SEVERITY,
                "size": settings.RISK_W_SIZE,
                "location": settings.RISK_W_LOCATION,
            },
            "label": "PROTOTYPE RISK SCORE - not a scientifically validated environmental risk model.",
        },
        "versions": [
            {
                "version": v.version,
                "model_name": v.model_name,
                "description": v.description,
                "metrics": v.metrics,
                "is_active": v.is_active,
                "created_at": str(v.created_at),
            }
            for v in versions
        ],
        "feedback_collected": feedback_count,
        "retraining_note": ("Expert feedback is stored as a validated dataset for future "
                            "training. No automatic production retraining occurs."),
    }
