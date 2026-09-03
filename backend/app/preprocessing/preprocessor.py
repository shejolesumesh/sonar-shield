"""Sonar image preprocessing pipeline.

Raw -> grayscale -> denoise (median + bilateral) -> normalize -> CLAHE contrast
-> shadow enhancement -> resize. Originals are never modified; processed images
are written to PROCESSED_DIR.
"""
from pathlib import Path

import cv2
import numpy as np

TARGET_SIZE = (640, 640)


def letterbox_transform(source_shape: tuple[int, int] | tuple[int, int, int], target=TARGET_SIZE) -> dict:
    """Return the exact scale and padding used by _letterbox_resize."""
    h, w = source_shape[:2]
    th, tw = target
    scale = min(tw / w, th / h)
    nh, nw = max(1, int(h * scale)), max(1, int(w * scale))
    return {"scale": scale, "pad_left": (tw - nw) // 2, "pad_top": (th - nh) // 2,
            "source_width": w, "source_height": h}


def unletterbox_bbox(bbox: list[float], transform: dict) -> list[int]:
    """Map a model-input xyxy box back to the original image pixel coordinate system."""
    scale = transform["scale"]
    left, top = transform["pad_left"], transform["pad_top"]
    w, h = transform["source_width"], transform["source_height"]
    x1, y1, x2, y2 = bbox
    x1, x2 = (x1 - left) / scale, (x2 - left) / scale
    y1, y2 = (y1 - top) / scale, (y2 - top) / scale
    return [int(round(max(0, min(w, x1)))), int(round(max(0, min(h, y1)))),
            int(round(max(0, min(w, x2)))), int(round(max(0, min(h, y2))))]


def preprocess_sonar_image(image_bgr: np.ndarray) -> np.ndarray:
    """Full preprocessing pipeline. Input/output are BGR uint8 arrays."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Denoising: median filter for speckle, bilateral for edge preservation
    denoised = cv2.medianBlur(gray, 5)
    denoised = cv2.bilateralFilter(denoised, d=9, sigmaColor=75, sigmaSpace=75)

    # Normalization to full dynamic range
    normalized = cv2.normalize(denoised, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    # Contrast enhancement via CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(normalized)

    # Shadow enhancement: emphasize dark low-contrast regions where acoustic shadows live
    blurred = cv2.GaussianBlur(enhanced, (0, 0), 3)
    shadow_detail = cv2.addWeighted(enhanced, 1.4, blurred, -0.4, 0)
    result = cv2.normalize(shadow_detail, None, 0, 255, cv2.NORM_MINMAX)

    bgr_out = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    # Resize preserving aspect ratio with letterbox padding
    bgr_out = _letterbox_resize(bgr_out, TARGET_SIZE)
    return bgr_out


def _letterbox_resize(img: np.ndarray, target) -> np.ndarray:
    th, tw = target
    h, w = img.shape[:2]
    transform = letterbox_transform(img.shape, target)
    nh, nw = int(h * transform["scale"]), int(w * transform["scale"])
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)
    canvas = np.zeros((th, tw, 3), dtype=np.uint8)
    top, left = transform["pad_top"], transform["pad_left"]
    canvas[top:top + nh, left:left + nw] = resized
    return canvas


def save_processed_image(image_bgr: np.ndarray, processed_dir: Path, stored_filename: str) -> Path:
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_path = processed_dir / f"processed_{Path(stored_filename).stem}.png"
    ok, buf = cv2.imencode(".png", image_bgr)
    if not ok:
        raise RuntimeError("Failed to encode processed image.")
    out_path.write_bytes(buf.tobytes())
    return out_path
