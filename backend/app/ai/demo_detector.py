"""DEMO DETECTOR - clearly labeled development model.

Produces deterministic pseudo-detections from image structure (edge/contour
analysis). Outputs are NOT scientifically validated predictions. Used when no
trained model is available so the entire workflow remains exercisable
end-to-end.
"""
import hashlib

import cv2

from app.ai.base_detector import BaseDetector, DetectionCandidate
from app.config import settings

# Deterministic per-image pseudo-label assignment pool.
_LABELS = ["DEMO CANDIDATE"]


class DemoDetector(BaseDetector):
    name = "demo-detector"
    is_demo = True

    def __init__(self):
        self._loaded = False

    def load(self) -> None:
        self._loaded = True

    @property
    def version(self) -> str:
        return settings.MODEL_VERSION

    def detect(self, image) -> list:
        if image.ndim == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        h, w = gray.shape

        # Image fingerprint -> deterministic behavior per unique image
        digest = hashlib.sha256(gray.tobytes()).hexdigest()

        # NOTE: cv2.findContours treats every non-zero pixel as foreground, so
        # running it directly on a continuous grayscale frame (a real photo or
        # sonar tile almost never contains true-zero pixels) produces a single
        # contour spanning ~100% of the frame, which the size filter below then
        # discards - i.e. zero detections, always, on real imagery. We first
        # extract edges (Canny) and dilate them into closed blobs so contours
        # correspond to actual object boundaries instead of "the whole image".
        edges = cv2.Canny(gray, 40, 120)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closed = cv2.dilate(edges, kernel, iterations=2)

        contours, _ = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        area_total = float(h * w)
        ranked = sorted(contours, key=cv2.contourArea, reverse=True)

        candidates = []
        accepted_boxes = []  # for de-duplicating nested/concentric edge contours
        idx = 0
        for cnt in ranked:
            if len(candidates) >= 6:
                break
            area = cv2.contourArea(cnt)
            if area < area_total * 0.005 or area > area_total * 0.35:
                continue
            x, y, bw, bh = cv2.boundingRect(cnt)
            # Pad box slightly
            pad_x, pad_y = int(bw * 0.05), int(bh * 0.05)
            x1, y1 = max(0, x - pad_x), max(0, y - pad_y)
            x2, y2 = min(w, x + bw + pad_x), min(h, y + bh + pad_y)

            # Skip boxes whose center already falls inside an accepted box -
            # Canny commonly yields both an inner and outer edge contour for
            # the same object, which would otherwise double-count it.
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            if any(bx1 <= cx <= bx2 and by1 <= cy <= by2 for bx1, by1, bx2, by2 in accepted_boxes):
                continue

            roi = gray[y1:y2, x1:x2]
            local_mean = float(gray[max(0, y1 - 20):min(h, y2 + 20), max(0, x1 - 20):min(w, x2 + 20)].mean()) or 1.0
            contrast_ratio = (float(roi.mean()) / local_mean) if roi.size else 1.0

            # Deterministic pseudo-confidence derived from contour shape + image hash
            hull_area = cv2.convexHull(cnt)
            solidity = float(area / max(cv2.contourArea(hull_area), 1.0))
            seed_hex = digest[(idx * 8) % 56:(idx * 8) % 56 + 8] or digest[:8]
            seed = int(seed_hex, 16) / 0xFFFFFFFF
            confidence = round(min(0.97, 0.40 + 0.45 * solidity + 0.15 * seed), 3)
            label = _LABELS[int(seed * len(_LABELS)) % len(_LABELS)]

            est_size = None
            shadow = None
            if contrast_ratio < 0.85:  # darker than surroundings -> plausible shadow signature
                shadow = round(min(1.0, (0.85 - contrast_ratio) / 0.85), 3)

            candidates.append(DetectionCandidate(
                bbox=[int(x1), int(y1), int(x2), int(y2)],
                label=label,
                confidence=confidence,
                estimated_size_m2=est_size,
                shadow_strength=shadow,
                extras={"contrast_ratio": round(contrast_ratio, 3), "solidity": round(solidity, 3)},
            ))
            accepted_boxes.append((x1, y1, x2, y2))
            idx += 1
        return candidates
