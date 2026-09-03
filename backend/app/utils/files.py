"""File utilities: safe filenames, size limits, path-traversal protection."""
import re
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import settings


def validate_upload_file(file: UploadFile) -> str:
    """Validate extension and read the file into memory if within size limit.

    Returns the safe stored filename. Raises HTTPException(400/413) on failure.
    """
    original_name = file.filename or ""
    ext = Path(original_name).suffix.lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {sorted(settings.ALLOWED_IMAGE_EXTENSIONS)}",
        )

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    data = file.file.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB} MB limit.")
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    file.file.seek(0)
    safe_stem = re.sub(r"[^A-Za-z0-9_-]", "_", Path(original_name).stem)[:80] or "image"
    return f"{safe_stem}_{uuid.uuid4().hex[:12]}{ext}"


def resolve_safe_path(base_dir: Path, relative_name: str) -> Path:
    """Resolve a path under base_dir, blocking path traversal."""
    candidate = (base_dir / relative_name).resolve()
    base_resolved = base_dir.resolve()
    if not candidate.is_relative_to(base_resolved):
        raise HTTPException(status_code=400, detail="Invalid path.")
    return candidate
