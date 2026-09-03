"""PROTOTYPE RISK SCORE engine.

risk_score = W_CONF * normalized_confidence
           + W_SEV  * severity
           + W_SIZE * normalized_size
           + W_LOC  * location_factor
All components are 0..100. Result clamped to 0..100.

This is a transparent prototype formula, NOT a scientifically validated
environmental risk model.
"""
from dataclasses import dataclass

from app.config import settings


@dataclass
class RiskInput:
    confidence: float          # 0..1
    severity_score: float      # 0..100
    estimated_size_m2: float | None
    location_factor: float     # 0..100


@dataclass
class RiskResult:
    risk_score: float
    risk_level: str


def normalize_size(size_m2) -> float:
    """Map size to 0..100; saturates at 20 m2. Unknown size -> neutral 30."""
    if size_m2 is None or size_m2 <= 0:
        return 30.0
    return min(100.0, (size_m2 / 20.0) * 100.0)


def compute_risk(ri: RiskInput) -> RiskResult:
    score = (
        settings.RISK_W_CONFIDENCE * (ri.confidence * 100.0)
        + settings.RISK_W_SEVERITY * ri.severity_score
        + settings.RISK_W_SIZE * normalize_size(ri.estimated_size_m2)
        + settings.RISK_W_LOCATION * ri.location_factor
    )
    score = max(0.0, min(100.0, score))
    return RiskResult(risk_score=round(score, 2), risk_level=risk_level(score))


def risk_level(score: float) -> str:
    if score <= 25:
        return "LOW"
    if score <= 50:
        return "MEDIUM"
    if score <= 75:
        return "HIGH"
    return "CRITICAL"


def priority_from_risk(risk_score: float, label: str, confidence: float,
                       estimated_size_m2) -> int:
    """P1 CRITICAL / P2 HIGH / P3 MEDIUM / P4 LOW.
    Considers risk score, object type severity, confidence, and size."""
    from app.evidence.engine import SEVERITY_MAP

    sev = SEVERITY_MAP.get(label.strip().lower(), 40.0)

    p = 4
    if risk_score >= 76 or (risk_score >= 51 and sev >= 80):
        p = 1
    elif risk_score >= 51 or (risk_score >= 26 and sev >= 60):
        p = 2
    elif risk_score >= 26:
        p = 3

    # Size bump for large hazardous items
    if estimated_size_m2 is not None and estimated_size_m2 > 10.0 and p > 1:
        p -= 1
    # Very low confidence can never be P1
    if confidence < settings.KNOWN_CLASS_THRESHOLD:
        p = max(p, 2)
    return p
