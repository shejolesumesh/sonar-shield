import uuid

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    detection_id: Mapped[str] = mapped_column(ForeignKey("detections.id", ondelete="CASCADE"), index=True)
    confidence_evidence: Mapped[list | None] = mapped_column(JSON, nullable=True)   # list[str]
    visual_evidence: Mapped[list | None] = mapped_column(JSON, nullable=True)       # list[str]
    shadow_evidence: Mapped[list | None] = mapped_column(JSON, nullable=True)       # list[str]
    explanation: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    created_at = mapped_column(DateTime, server_default=func.now())

    detection = relationship("Detection", back_populates="evidence")
