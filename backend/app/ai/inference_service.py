"""Inference service: selects detector, applies UNKNOWN ANOMALY thresholding,
drops sub-minimum-confidence noise, returns final detection records."""
from app.ai.base_detector import BaseDetector
from app.ai.demo_detector import DemoDetector
from app.ai.onnx_detector import ONNXDetector
from app.ai.pytorch_detector import PyTorchDetector
from app.config import settings


def get_detector():
    """Return an active detector plus its descriptor. Falls back to demo."""
    info = {"requested": settings.DETECTOR_TYPE}
    if settings.DETECTOR_TYPE == "onnx":
        try:
            det: BaseDetector = ONNXDetector()
            det.load()
            info.update(det.info)
            info["mode"] = "REAL AI MODEL"
            info["demo"] = False
            return det, info
        except Exception as exc:
            info["fallback_reason"] = f"ONNX model failed to load: {type(exc).__name__}: {exc}"
    elif settings.DETECTOR_TYPE == "pytorch":
        try:
            det: BaseDetector = PyTorchDetector()
            det.load()
            info["mode"] = "REAL AI MODEL"
            info["demo"] = False
            return det, info
        except Exception as exc:  # torch missing, weights missing, corrupt weights...
            info["fallback_reason"] = f"{type(exc).__name__}: {exc}"
    det = DemoDetector()
    det.load()
    info["mode"] = "DEMO DETECTOR"
    info["demo"] = True
    return det, info


def apply_unknown_anomaly_policy(candidates):
    """Threshold policy:
      confidence >= MIN_DETECTION_CONFIDENCE : keep
      confidence >= KNOWN_CLASS_THRESHOLD    : known class, shown normally
      else                                   : keep the detector's actual raw
                                                label but flag it (is_known=False)
                                                for expert review instead of
                                                hiding the predicted class.
    We never invent or force a *different* class label onto a low-confidence
    candidate. But we also never discard the class the model actually
    predicted - c.label always reflects what the model output, so
    final_label is left at its default (== c.label) in both branches."""
    kept = []
    for c in candidates:
        if c.confidence < settings.MIN_DETECTION_CONFIDENCE:
            continue
        c.is_known = c.confidence >= settings.KNOWN_CLASS_THRESHOLD
        c.final_label = c.label
        kept.append(c)
    return kept
