"""Image validation - verifies the upload is a decodable image."""
import cv2
import numpy as np
from fastapi import HTTPException


def validate_image_bytes(data: bytes) -> np.ndarray:
    """Decode uploaded bytes to an OpenCV BGR image. Raise 400 if invalid."""
    if not data:
        raise HTTPException(status_code=400, detail="Empty file.")
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="File is not a decodable image.")
    h, w = img.shape[:2]
    if w < 16 or h < 16:
        raise HTTPException(status_code=400, detail="Image too small (minimum 16x16 pixels).")
    return img
