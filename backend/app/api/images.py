from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.detection import Detection as DetectionModel
from app.models.image import Image as ImageModel
from app.schemas.detection import DetectionSummary
from app.schemas.image import ImageOut, ImageWithDetections

router = APIRouter(prefix="/api/images", tags=["images"])


@router.get("", response_model=list[ImageOut])
def list_images(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    rows = db.query(ImageModel).order_by(ImageModel.created_at.desc()).limit(limit).offset(offset).all()
    return rows


@router.get("/{image_id}", response_model=ImageWithDetections)
def get_image(image_id: str, db: Session = Depends(get_db)):
    record = db.get(ImageModel, image_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Image not found.")
    dets = db.query(DetectionModel).filter(DetectionModel.image_id == image_id).all()
    payload = ImageOut.model_validate(record).model_dump()
    payload["detections"] = [DetectionSummary.model_validate(d).model_dump() for d in dets]
    return payload


def _serve_file(path_str, not_found_msg: str) -> FileResponse:
    if not path_str:
        raise HTTPException(status_code=404, detail=not_found_msg)
    p = Path(path_str)
    base = settings.UPLOAD_DIR.resolve()
    alt_base = settings.PROCESSED_DIR.resolve()
    resolved = p.resolve()
    if not (resolved.is_relative_to(base) or resolved.is_relative_to(alt_base)):
        raise HTTPException(status_code=400, detail="Invalid path.")
    if not resolved.exists():
        raise HTTPException(status_code=404, detail=not_found_msg)
    return FileResponse(resolved)


@router.get("/{image_id}/original")
def serve_original(image_id: str, db: Session = Depends(get_db)):
    record = db.get(ImageModel, image_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Image not found.")
    return _serve_file(record.storage_path, "Original file missing on disk.")


@router.get("/{image_id}/processed")
def serve_processed(image_id: str, db: Session = Depends(get_db)):
    record = db.get(ImageModel, image_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Image not found.")
    return _serve_file(record.processed_path, "Processed file missing - analysis may not have completed preprocessing.")
