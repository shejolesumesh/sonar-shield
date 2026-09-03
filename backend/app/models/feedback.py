import uuid

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ExpertFeedback(Base):
    __tablename__ = "expert_feedback"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    detection_id: Mapped[str] = mapped_column(ForeignKey("detections.id", ondelete="CASCADE"), index=True)
    ai_label: Mapped[str] = mapped_column(String(128), nullable=False)
    expert_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    action: Mapped[str] = mapped_column(String(32), nullable=False)  # CONFIRM / REJECT / RECLASSIFY
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at = mapped_column(DateTime, server_default=func.now())

    detection = relationship("Detection", back_populates="feedback_items")
