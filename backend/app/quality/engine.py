"""Conservative, image-derived quality and low-information region assessment."""
import cv2
import numpy as np


def assess_sonar_quality(image_bgr: np.ndarray) -> dict:
    """Return calculated image indicators; none are claimed as calibrated sonar measures."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY) if image_bgr.ndim == 3 else image_bgr
    gray = gray.astype(np.uint8)
    noise = float(np.median(np.abs(cv2.Laplacian(gray, cv2.CV_32F))))
    contrast = float(gray.std())
    shadow_fraction = float((gray < np.percentile(gray, 15)).mean())
    dropout = detect_dropout(gray)
    # A transparent, bounded usability indicator; it is intentionally not a sonar calibration.
    resolution_score = min(1.0, (gray.shape[0] * gray.shape[1]) / (640 * 640))
    contrast_score = min(1.0, contrast / 50.0)
    noise_score = max(0.0, 1.0 - max(0.0, noise - 12.0) / 50.0)
    quality_score = round(100 * (0.35 * contrast_score + 0.25 * noise_score + 0.20 * resolution_score + 0.20 * (1 - dropout["affected_percentage"] / 100)), 1)
    return {
        "kind": "image-derived indicators; not calibrated sonar measurements",
        "noise_indicator": round(noise, 2),
        "contrast_stddev": round(contrast, 2),
        "resolution_px": {"width": int(gray.shape[1]), "height": int(gray.shape[0])},
        "acoustic_shadow_visibility_fraction": round(shadow_fraction, 4),
        "dropout": dropout,
        "overall_quality_score": quality_score,
    }


def detect_dropout(gray: np.ndarray) -> dict:
    """Flag substantial, unusually uniform regions; percentage is measured from the image."""
    local_std = cv2.blur(gray.astype(np.float32) ** 2, (31, 31)) - cv2.blur(gray.astype(np.float32), (31, 31)) ** 2
    uniform = (local_std < 4.0) & ((gray < 8) | (gray > 247))
    count, labels, stats, _ = cv2.connectedComponentsWithStats(uniform.astype(np.uint8), connectivity=8)
    total = gray.shape[0] * gray.shape[1]
    regions, covered = [], 0
    for index in range(1, count):
        x, y, width, height, area = stats[index]
        if area < max(64, total * 0.002):
            continue
        covered += int(area)
        regions.append({"bbox": [int(x), int(y), int(x + width), int(y + height)], "pixel_count": int(area)})
    percentage = 100 * covered / total
    return {"detected": percentage >= 2.0, "affected_percentage": round(percentage, 3), "regions": regions}
