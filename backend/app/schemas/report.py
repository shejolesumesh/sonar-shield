from pydantic import BaseModel, ConfigDict


class ReportRow(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    detection_id: str
    object_type: str
    confidence: float
    risk_level: str
    risk_score: float
    priority: int
    latitude: float | None
    longitude: float | None
    timestamp: str | None
    model_version: str
    expert_status: str


class ReportMeta(BaseModel):
    generated_at_utc: str
    disclaimer: str
    total_rows: int
    format: str
