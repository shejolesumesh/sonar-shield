import numpy as np

from app.quality.engine import assess_sonar_quality, detect_dropout


def test_quality_metrics_are_image_derived():
    image = np.full((128, 256, 3), 80, dtype=np.uint8)
    result = assess_sonar_quality(image)
    assert result["resolution_px"] == {"width": 256, "height": 128}
    assert 0 <= result["overall_quality_score"] <= 100


def test_dropout_percentage_is_measured():
    gray = np.full((200, 200), 100, dtype=np.uint8)
    gray[:, :100] = 0
    result = detect_dropout(gray)
    assert result["detected"] is True
    assert result["affected_percentage"] > 40
