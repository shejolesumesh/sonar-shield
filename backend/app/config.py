"""Central configuration. All tunables live here - never duplicate thresholds elsewhere."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root (sonar-shield/)


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _float(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)))


class Settings:
    # Storage
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'sonar_shield.db'}")
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "data" / "uploads"))
    PROCESSED_DIR: Path = Path(os.getenv("PROCESSED_DIR", BASE_DIR / "data" / "processed"))
    MAX_UPLOAD_SIZE_MB: int = _int("MAX_UPLOAD_SIZE_MB", 25)

    # Detection
    DETECTOR_TYPE: str = os.getenv("DETECTOR_TYPE", "onnx")
    ONNX_MODEL_PATH: str = os.getenv("ONNX_MODEL_PATH", str(BASE_DIR / "models" / "weights.onnx"))
    CLASS_NAMES_PATH: str = os.getenv("CLASS_NAMES_PATH", str(BASE_DIR / "models" / "class_names.txt"))
    PYTORCH_MODEL_PATH: str = os.getenv("PYTORCH_MODEL_PATH", str(BASE_DIR / "models" / "sonar_detector.pt"))
    MODEL_VERSION: str = os.getenv("MODEL_VERSION", "GhostVision-ONNX-2026-01-27")
    KNOWN_CLASS_THRESHOLD: float = _float("KNOWN_CLASS_THRESHOLD", 0.70)
    MIN_DETECTION_CONFIDENCE: float = 0.30  # below this, candidate boxes are dropped entirely

    # Risk engine weights (sum should be 1.0; clamped anyway)
    RISK_W_CONFIDENCE: float = _float("RISK_W_CONFIDENCE", 0.35)
    RISK_W_SEVERITY: float = _float("RISK_W_SEVERITY", 0.25)
    RISK_W_SIZE: float = _float("RISK_W_SIZE", 0.20)
    RISK_W_LOCATION: float = _float("RISK_W_LOCATION", 0.20)

    # CORS
    CORS_ORIGINS: list = [
        o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()
    ]

    ALLOWED_IMAGE_EXTENSIONS: set = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

    def ensure_dirs(self) -> None:
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        Path(self.DATABASE_URL.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True) \
            if self.DATABASE_URL.startswith("sqlite:///") else None


settings = Settings()
