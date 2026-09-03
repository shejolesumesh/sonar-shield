import numpy as np
import pytest

from app.ai.onnx_detector import ONNXDetector
from app.config import settings


def test_real_onnx_model_loads_and_runs():
    detector = ONNXDetector()
    detector.load()
    assert detector.class_names == ["Crab-Pot"]
    assert detector.detect(np.zeros((640, 640, 3), dtype=np.uint8)) == []


def test_missing_model_fails_loudly(tmp_path):
    with pytest.raises(FileNotFoundError):
        ONNXDetector(tmp_path / "missing.onnx", settings.CLASS_NAMES_PATH).load()


def test_invalid_model_fails_loudly(tmp_path):
    invalid = tmp_path / "invalid.onnx"
    invalid.write_bytes(b"not an onnx model")
    with pytest.raises(Exception):
        ONNXDetector(invalid, settings.CLASS_NAMES_PATH).load()
