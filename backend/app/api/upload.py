import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.image import ImageOut, SonarMetadata
from app.services.upload_service import handle_upload

router = APIRouter(prefix="/api/sonar", tags=["upload"])


@router.post("/upload", response_model=ImageOut, status_code=201)
def upload_sonar_image(
    file: UploadFile = File(...),
    metadata_json: str | None = Form(None),
    db: Session = Depends(get_db),
):
    metadata: SonarMetadata | None = None
    if metadata_json:
        try:
            raw = json.loads(metadata_json)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="metadata_json is not valid JSON.")
        if not isinstance(raw, dict):
            raise HTTPException(status_code=400, detail="metadata_json must be a JSON object.")
        try:
            metadata = SonarMetadata(**raw)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=exc.errors())

    try:
        record = handle_upload(file, metadata, db)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}")
    return record
