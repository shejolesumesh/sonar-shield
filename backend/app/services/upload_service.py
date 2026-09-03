"""Upload service: validate file, preserve original on disk, create DB record,
run preprocessing and store the processed copy separately."""
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.models.image import Image as ImageModel
from app.preprocessing.preprocessor import preprocess_sonar_image, save_processed_image
from app.quality.engine import assess_sonar_quality
from app.preprocessing.validator import validate_image_bytes
from app.schemas.image import SonarMetadata
from app.utils.files import validate_upload_file


def handle_upload(file: UploadFile, metadata: SonarMetadata | None, db: Session) -> ImageModel:
    safe_name = validate_upload_file(file)
    data = file.file.read()
    validate_image_bytes(data)  # raises 400 if not decodable

    settings.ensure_dirs()
    original_path = settings.UPLOAD_DIR / safe_name
    original_path.write_bytes(data)  # never overwrite existing uploads thanks to uuid suffix

    record = ImageModel(
        filename=file.filename or safe_name,
        storage_path=str(original_path),
        latitude=metadata.latitude if metadata else None,
        longitude=metadata.longitude if metadata else None,
        depth=metadata.depth if metadata else None,
        timestamp=metadata.timestamp if metadata else None,
        sonar_info={
            k: v
            for k, v in (
                ("sonar_frequency_khz", metadata.sonar_frequency_khz if metadata else None),
                ("swath_width_m", metadata.swath_width_m if metadata else None),
                ("vessel_name", metadata.vessel_name if metadata else None),
                ("motion_metadata", {k: v for k, v in (("heave", metadata.heave if metadata else None), ("pitch", metadata.pitch if metadata else None), ("roll", metadata.roll if metadata else None)) if v is not None} or None),
            )
            if v is not None
        } or None,
        notes=metadata.notes if metadata else None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    try:
        import cv2
        import numpy as np

        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        processed = preprocess_sonar_image(img)
        proc_path = save_processed_image(processed, settings.PROCESSED_DIR, safe_name)
        record.processed_path = str(proc_path)
        info = dict(record.sonar_info or {})
        info["quality"] = assess_sonar_quality(img)
        motion = info.get("motion_metadata")
        info["motion_status"] = ("Motion metadata supplied; no validated correction algorithm is applied."
                                 if motion else "Motion compensation unavailable — motion metadata not provided.")
        record.sonar_info = info
        db.commit()
        db.refresh(record)
    except Exception:
        db.rollback()
        record.processed_path = None
        db.commit()
        db.refresh(record)

    return record
