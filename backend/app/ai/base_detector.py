"""Detector abstraction layer. Real detectors plug in here without changing API or UI."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class DetectionCandidate:
    bbox: list                          # [x1, y1, x2, y2] in pixel coords
    label: str                           # raw class label from detector
    confidence: float                    # 0..1
    estimated_size_m2: float | None = None
    shadow_strength: float | None = None  # 0..1 measurable shadow indicator, None if not computable
    extras: dict = field(default_factory=dict)
    # Populated by inference_service.apply_unknown_anomaly_policy()
    is_known: bool = True
    final_label: str = ""

    def __post_init__(self):
        if not self.final_label:
            self.final_label = self.label


class BaseDetector(ABC):
    name: str = "base"
    is_demo: bool = False

    @abstractmethod
    def load(self) -> None:
        """Load model weights / resources. Must be idempotent."""

    @abstractmethod
    def detect(self, image_rgb_or_gray) -> list:
        """Run inference over a preprocessed image array (HxW or HxWx3)."""

    @property
    @abstractmethod
    def version(self) -> str:
        ...
