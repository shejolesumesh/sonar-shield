"""Recovery priority queue builder."""
PRIORITY_LABELS = {1: "P1 CRITICAL", 2: "P2 HIGH", 3: "P3 MEDIUM", 4: "P4 LOW"}


def rationale_text(object_type: str, risk_score: float, confidence: float,
                   priority: int, has_location: bool) -> str:
    parts = [
        f"Risk score {risk_score:.1f} ({PRIORITY_LABELS[priority]}).",
        f"Object type '{object_type}'",
        f"confidence {confidence:.2f}",
    ]
    parts.append("GPS coordinates available for recovery planning"
                 if has_location else "no GPS coordinates - location factor reduced")
    return "; ".join(parts)


def sort_priority_items(items: list) -> list:
    """Sort ascending priority number, then descending risk score, then descending confidence."""
    return sorted(items, key=lambda i: (i.priority, -i.risk_score, -i.confidence))
