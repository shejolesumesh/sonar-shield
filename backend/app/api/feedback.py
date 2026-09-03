from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.detection import Detection as DetectionModel
from app.models.feedback import ExpertFeedback as FeedbackModel
from app.schemas.feedback import FeedbackCreate, FeedbackOut

router = APIRouter(tags=["feedback"])

_STATUS_MAP = {"CONFIRM": "CONFIRMED", "REJECT": "REJECTED", "RECLASSIFY": "RECLASSIFIED"}


@router.post("/api/feedback", response_model=FeedbackOut, status_code=201)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    det = db.get(DetectionModel, payload.detection_id)
    if det is None:
        raise HTTPException(status_code=404, detail="Detection not found.")

    fb = FeedbackModel(
        detection_id=det.id,
        ai_label=det.object_type,   # preserve original AI prediction
        expert_label=payload.expert_label,
        action=payload.action,
        comment=payload.comment,
    )

    # Update detection status; NEVER overwrite object_type/raw_label/confidence
    # (the original AI prediction is preserved for audit purposes).
    det.status = _STATUS_MAP[payload.action]
    if payload.action == "RECLASSIFY":
        det.expert_reclassified_label = payload.expert_label

    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


@router.get("/api/feedback", response_model=list[FeedbackOut])
def list_feedback(detection_id: str | None = None, limit: int = 200, db: Session = Depends(get_db)):
    q = db.query(FeedbackModel).order_by(FeedbackModel.created_at.desc())
    if detection_id:
        q = q.filter(FeedbackModel.detection_id == detection_id)
    return q.limit(limit).all()
