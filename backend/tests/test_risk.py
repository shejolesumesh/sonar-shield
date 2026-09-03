from app.risk.engine import RiskInput, compute_risk, normalize_size, priority_from_risk, risk_level


def test_risk_bounds_and_level_mapping():
    for conf in [0.0, 0.5, 1.0]:
        r = compute_risk(RiskInput(confidence=conf, severity_score=100,
                                   estimated_size_m2=50, location_factor=100))
        assert 0 <= r.risk_score <= 100
        assert r.risk_level in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def test_risk_monotonic_in_confidence():
    low = compute_risk(RiskInput(0.3, 50, None, 50)).risk_score
    high = compute_risk(RiskInput(0.9, 50, None, 50)).risk_score
    assert high > low


def test_risk_levels_thresholds():
    assert risk_level(10) == "LOW"
    assert risk_level(40) == "MEDIUM"
    assert risk_level(60) == "HIGH"
    assert risk_level(90) == "CRITICAL"


def test_normalize_size():
    assert normalize_size(None) == 30.0
    assert normalize_size(0) == 30.0
    assert normalize_size(20) == 100.0
    assert normalize_size(200) == 100.0


def test_priority_ordering():
    p_critical = priority_from_risk(90, "Ghost Net", 0.9, 15.0)
    p_low = priority_from_risk(10, "Rock Outcrop", 0.4, 1.0)
    assert p_critical < p_low
    assert p_critical == 1


def test_unknown_anomaly_never_p1():
    p = priority_from_risk(95, "UNKNOWN ANOMALY", 0.64, 20.0)
    assert p >= 2
