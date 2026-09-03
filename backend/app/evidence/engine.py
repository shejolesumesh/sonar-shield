"""Evidence engine: builds honest Evidence Card content per detection.

Never fabricates evidence. If a metric cannot be computed, the UI-facing
placeholder 'Not available from current analysis' is used.
"""
from app.config import settings

NOT_AVAILABLE = "Not available from current analysis"

# Prototype severity map by object type (0..100). Transparent and configurable.
SEVERITY_MAP = {
    "ghost net": 90.0,
    "debris": 60.0,
    "other debris": 55.0,
    "wreck": 70.0,
    "wreck fragment": 65.0,
    "rock": 15.0,
    "rock outcrop": 15.0,
    "unknown anomaly": 50.0,
}


def severity_for(label: str) -> float:
    return SEVERITY_MAP.get(label.strip().lower(), 40.0)


def location_factor(lat, lon) -> float:
    """Prototype location factor: known coordinates imply actionable recovery (75),
    unknown coordinates reduce actionability (25). Never fabricates coordinates."""
    return 75.0 if lat is not None and lon is not None else 25.0


def build_evidence(candidate, image_shape) -> dict:
    """Return evidence lists for a detection candidate."""
    confidence_ev = []
    visual_ev = []
    shadow_ev = []

    x1, y1, x2, y2 = candidate.bbox
    h, w = image_shape[:2]

    confidence_ev.append(f"Detector confidence {candidate.confidence:.2f} "
                         f"(known-class threshold {settings.KNOWN_CLASS_THRESHOLD:.2f})")
    if candidate.confidence < settings.KNOWN_CLASS_THRESHOLD:
        confidence_ev.append("Confidence below classification threshold - flagged for expert review "
                             "(predicted class shown as-is, not hidden)")
    else:
        confidence_ev.append("Confidence meets or exceeds classification threshold")

    visual_ev.append(f"Detectable object boundary at pixel region [{x1}, {y1}, {x2}, {y2}]")

    contrast = candidate.extras.get("contrast_ratio")
    if contrast is not None:
        direction = "brighter" if contrast >= 1.0 else "darker"
        visual_ev.append(f"Region is {direction} than local sonar background "
                         f"(contrast ratio {contrast:.2f})")
    else:
        visual_ev.append(NOT_AVAILABLE)

    solidity = candidate.extras.get("solidity")
    if solidity is not None:
        visual_ev.append(f"Contour solidity {solidity:.2f} (shape compactness indicator)")
    else:
        visual_ev.append(NOT_AVAILABLE)

    shadow = candidate.shadow_strength
    if shadow is not None:
        shadow_ev.append(f"Acoustic-shadow-like dark region adjacent to object "
                         f"(shadow strength {shadow:.2f})")
    else:
        shadow_ev.append(NOT_AVAILABLE)

    size_note = (f"Estimated footprint {candidate.estimated_size_m2:.1f} m2"
                 if candidate.estimated_size_m2 is not None else NOT_AVAILABLE)
    visual_ev.append(f"Estimated size: {size_note}")

    final_label = getattr(candidate, "final_label", candidate.label)
    is_known = getattr(candidate, "is_known", True)

    explanation = (
        f"Candidate region detected at [{x1}, {y1}, {x2}, {y2}] in a {w}x{h} preprocessed frame. "
        + (f"Detector predicted '{final_label}' but confidence fell below the "
           f"{settings.KNOWN_CLASS_THRESHOLD:.2f} known-class threshold, so this candidate is "
           "flagged LOW CONFIDENCE - EXPERT REVIEW REQUIRED rather than hidden or forced into a class."
           if not is_known
           else f"Labeled '{final_label}' with sufficient confidence.")
        + " All metrics above are computed from this prototype analysis only."
    )

    return {
        "confidence_evidence": confidence_ev,
        "visual_evidence": visual_ev,
        "shadow_evidence": shadow_ev,
        "explanation": explanation,
        "severity_score": severity_for(final_label),
        "location_factor": 0.0,  # filled by detection_service when metadata known
    }
