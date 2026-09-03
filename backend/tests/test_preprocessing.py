import cv2
import numpy as np

from app.preprocessing.preprocessor import preprocess_sonar_image
from app.preprocessing.validator import validate_image_bytes


def test_validate_accepts_real_image(sample_png_bytes):
    img = validate_image_bytes(sample_png_bytes)
    assert img.shape[0] > 0 and img.shape[1] > 0


def test_validate_rejects_garbage():
    import pytest
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        validate_image_bytes(b"garbage")
    assert exc.value.status_code == 400


def test_preprocess_output_shape_and_range():
    img = np.random.default_rng(0).integers(0, 255, (300, 500), dtype=np.uint8)
    img3 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    out = preprocess_sonar_image(img3)
    assert out.shape == (640, 640, 3)  # letterboxed target size
    assert out.dtype == np.uint8
