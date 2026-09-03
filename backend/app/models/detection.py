import uuid

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    image_id: Mapped[str] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), index=True)
    object_type: Mapped[str] = mapped_column(String(128), nullable=False)  # raw detector class; see is_unknown_anomaly for low-confidence flag
    raw_label: Mapped[str] = mapped_column(String(128), nullable=False)  # label before thresholding
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    is_unknown_anomaly: Mapped[bool] = mapped_column(default=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False, default="LOW")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    bbox: Mapped[list | None] = mapped_column(JSON, nullable=True)  # [x1, y1, x2, y2]
    mask_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    estimated_size_m2: Mapped[float | None] = mapped_column(Float, nullable=True)
    severity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    location_factor: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    model_version: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")  # PENDING/CONFIRMED/REJECTED/RECLASSIFIED
    expert_reclassified_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at = mapped_column(DateTime, server_default=func.now())

    evidence = relationship("Evidence", back_populates="detection", uselist=False, cascade="all, delete-orphan")
    feedback_items = relationship("ExpertFeedback", back_populates="detection", cascade="all, delete-orphan")
