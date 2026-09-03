from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.detection import DetectionSummary


class SonarMetadata(BaseModel):
    """Optional metadata attached to an upload."""
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    depth: float | None = Field(None, ge=0)
    timestamp: str | None = None
    sonar_frequency_khz: float | None = None
    swath_width_m: float | None = None
    vessel_name: str | None = None
    heave: float | None = None
    pitch: float | None = None
    roll: float | None = None
    notes: str | None = None


class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    storage_path: str
    processed_path: str | None
    latitude: float | None
    longitude: float | None
    depth: float | None
    timestamp: str | None
    sonar_info: dict | None
    notes: str | None
    created_at: datetime


class ImageWithDetections(ImageOut):
    detections: list[DetectionSummary] = []
