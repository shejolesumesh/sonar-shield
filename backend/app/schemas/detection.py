from pydantic import BaseModel, ConfigDict


class DetectionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: str
    object_type: str
    confidence: float
    is_unknown_anomaly: bool
    risk_level: str
    risk_score: float
    priority: int
    bbox: list | None
    estimated_size_m2: float | None
    model_version: str
    status: str


class EvidenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    confidence_evidence: list | None
    visual_evidence: list | None
    shadow_evidence: list | None
    explanation: str | None


class FeedbackItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    action: str
    comment: str | None


class DetectionDetail(DetectionSummary):
    raw_label: str
    severity_score: float
    location_factor: float
    evidence: EvidenceOut | None = None
    feedback: list[FeedbackItem] = []
    image_id: str | None = None
    image_filename: str | None = None
    image_storage_path: str | None = None
    image_processed_path: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    depth: float | None = None
    timestamp: str | None = None


class MapPoint(BaseModel):
    detection_id: str
    latitude: float
    longitude: float
    object_type: str
    confidence: float
    risk_level: str
    priority: int
    status: str


class HeatmapResponse(BaseModel):
    has_data: bool
    points: list[MapPoint]
    message: str | None = None


class PriorityItem(DetectionSummary):
    latitude: float | None = None
    longitude: float | None = None
    depth: float | None = None
    image_id: str
    rationale: str
