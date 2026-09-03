from app.ai.base_detector import DetectionCandidate
from app.ai.inference_service import apply_unknown_anomaly_policy
from app.config import settings


def _cand(conf: float) -> DetectionCandidate:
    return DetectionCandidate(bbox=[0, 0, 10, 10], label="Ghost Net", confidence=conf)


def test_high_confidence_keeps_label():
    kept = apply_unknown_anomaly_policy([_cand(0.92)])
    assert len(kept) == 1
    assert kept[0].final_label == "Ghost Net"
    assert kept[0].is_known is True


def test_below_threshold_flagged_but_label_preserved():
    """Low-confidence candidates are flagged for review (is_known False) but the
    detector's actual predicted class is never hidden or replaced."""
    kept = apply_unknown_anomaly_policy([_cand(settings.KNOWN_CLASS_THRESHOLD - 0.06)])
    assert len(kept) == 1
    assert kept[0].final_label == "Ghost Net"
    assert kept[0].is_known is False


def test_at_threshold_is_known():
    kept = apply_unknown_anomaly_policy([_cand(settings.KNOWN_CLASS_THRESHOLD)])
    assert kept[0].is_known is True


def test_subminimum_confidence_dropped():
    kept = apply_unknown_anomaly_policy([_cand(0.05)])
    assert len(kept) == 0
