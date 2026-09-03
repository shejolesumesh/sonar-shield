"""Real PyTorch/YOLO adapter. Optional dependency: torch/torchvision.

Loads weights from settings.PYTORCH_MODEL_PATH. If torch is unavailable or the
weights file does not exist, loading fails gracefully and inference_service falls
back to the demo detector. Replace `detect` internals with your trained model's
inference code without touching any other layer.
"""
from pathlib import Path

import cv2
import numpy as np

from app.ai.base_detector import BaseDetector, DetectionCandidate
from app.config import settings

CLASS_NAMES = ["Background", "Ghost Net", "Debris", "Rock", "Wreck", "Other Object"]


class PyTorchDetector(BaseDetector):
    name = "pytorch-detector"
    is_demo = False

    def __init__(self, model_path: str | None = None):
        self.model_path = Path(model_path or settings.PYTORCH_MODEL_PATH)
        self.model = None

    def load(self) -> None:
        import torch  # noqa: raised ImportError handled by inference_service

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model weights not found at {self.model_path}")
        self.model = torch.load(str(self.model_path), map_location="cpu")
        self.model.eval()

    @property
    def version(self) -> str:
        return settings.MODEL_VERSION

    def detect(self, image) -> list:
        import torch

        if self.model is None:
            raise RuntimeError("Model not loaded.")

        tensor = torch.from_numpy(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        ).permute(2, 0, 1).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(tensor)[0]

        candidates = []
        for box, score, cls in zip(
            outputs["boxes"].tolist(),
            outputs["scores"].tolist(),
            outputs["labels"].tolist(),
        ):
            label = CLASS_NAMES[cls] if 0 <= cls < len(CLASS_NAMES) else "Unknown"
            candidates.append(DetectionCandidate(
                bbox=[int(v) for v in box],
                label=label,
                confidence=float(score),
            ))
        return candidates
