"""Adapter for the supplied GhostVision YOLOv12 ONNX detector.

The checked model accepts float32 NCHW 640x640 input and emits [1, 5, 8400]:
xywh plus one class confidence for each proposal. It does not contain NMS.
"""
import logging
from pathlib import Path

import cv2
import numpy as np

from app.ai.base_detector import BaseDetector, DetectionCandidate
from app.config import settings

logger = logging.getLogger("sonar_shield.onnx_detector")


class ONNXDetector(BaseDetector):
    name = "GhostVision YOLOv12s ONNX"
    is_demo = False

    def __init__(self, model_path: str | None = None, class_names_path: str | None = None):
        self.model_path = Path(model_path or settings.ONNX_MODEL_PATH)
        self.class_names_path = Path(class_names_path or settings.CLASS_NAMES_PATH)
        self.session = None
        self.input_name = ""
        self.class_names: list[str] = []
        self._metadata: dict[str, str] = {}

    def load(self) -> None:
        import onnxruntime as ort

        if not self.model_path.is_file():
            raise FileNotFoundError(f"Model weights not found at {self.model_path}")
        if not self.class_names_path.is_file():
            raise FileNotFoundError(f"Class names not found at {self.class_names_path}")
        self.class_names = [line.strip() for line in self.class_names_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not self.class_names:
            raise ValueError("Class names file is empty")
        self.session = ort.InferenceSession(str(self.model_path), providers=["CPUExecutionProvider"])
        inputs, outputs = self.session.get_inputs(), self.session.get_outputs()
        if len(inputs) != 1 or inputs[0].shape != [1, 3, 640, 640] or inputs[0].type != "tensor(float)":
            raise ValueError(f"Unsupported ONNX input: {[(x.name, x.shape, x.type) for x in inputs]}")
        expected_output = [1, 4 + len(self.class_names), 8400]
        if len(outputs) != 1 or outputs[0].shape != expected_output or outputs[0].type != "tensor(float)":
            raise ValueError(
                f"Unsupported ONNX output: {[(x.name, x.shape, x.type) for x in outputs]}; "
                f"expected one float32 tensor shaped {expected_output} (xywh + class scores)."
            )
        self.input_name = inputs[0].name
        self._metadata = dict(self.session.get_modelmeta().custom_metadata_map)

    @property
    def version(self) -> str:
        return settings.MODEL_VERSION

    @property
    def info(self) -> dict:
        return {"model_name": self.name, "model_format": "ONNX", "supported_classes": self.class_names,
                "model_path": str(self.model_path), "input_shape": [1, 3, 640, 640],
                "output_shape": [1, 4 + len(self.class_names), 8400], "nms_in_model": False,
                "embedded_class_metadata": self._metadata.get("names")}

    def detect(self, image) -> list:
        if self.session is None:
            raise RuntimeError("Model not loaded.")
        if image.shape[:2] != (640, 640):
            raise ValueError(f"Expected 640x640 preprocessed image, got {image.shape[:2]}")
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.ndim == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        tensor = np.ascontiguousarray(rgb.transpose(2, 0, 1)[None].astype(np.float32) / 255.0)
        output = self.session.run(None, {self.input_name: tensor})[0]
        rows = output[0].T  # [8400, 5] for this one-class export
        raw_max_score = float(rows[:, 4:].max()) if rows.size else 0.0
        boxes, scores, labels = [], [], []
        for row in rows:
            cls = int(np.argmax(row[4:]))
            score = float(row[4 + cls])
            if score < settings.MIN_DETECTION_CONFIDENCE:
                continue
            cx, cy, w, h = map(float, row[:4])
            if w <= 0 or h <= 0:
                continue
            boxes.append([max(0.0, cx - w / 2), max(0.0, cy - h / 2),
                          min(640.0, cx + w / 2), min(640.0, cy + h / 2)])
            scores.append(score)
            labels.append(cls)
        after_conf_filter = len(scores)
        kept = self._nms(boxes, scores, labels, iou_threshold=0.45)
        logger.debug(
            "raw_candidates=%d max_raw_score=%.4f after_conf_filter=%d after_nms=%d "
            "min_conf_threshold=%.2f known_class_threshold=%.2f",
            rows.shape[0], raw_max_score, after_conf_filter, len(kept),
            settings.MIN_DETECTION_CONFIDENCE, settings.KNOWN_CLASS_THRESHOLD,
        )
        return [DetectionCandidate(bbox=[int(round(v)) for v in boxes[i]], label=self.class_names[labels[i]],
                                   confidence=scores[i], extras={"model_output": "xywh/class-confidence"}) for i in kept]

    @staticmethod
    def _nms(boxes, scores, labels, iou_threshold: float) -> list[int]:
        kept = []
        for label in sorted(set(labels)):
            ids = [i for i, value in enumerate(labels) if value == label]
            ids.sort(key=lambda i: scores[i], reverse=True)
            while ids:
                current = ids.pop(0)
                kept.append(current)
                x1, y1, x2, y2 = boxes[current]
                survivors = []
                for other in ids:
                    ox1, oy1, ox2, oy2 = boxes[other]
                    intersection = max(0.0, min(x2, ox2) - max(x1, ox1)) * max(0.0, min(y2, oy2) - max(y1, oy1))
                    union = (x2 - x1) * (y2 - y1) + (ox2 - ox1) * (oy2 - oy1) - intersection
                    if union <= 0 or intersection / union <= iou_threshold:
                        survivors.append(other)
                ids = survivors
        return kept
