from fastapi import APIRouter
from sqlalchemy import text

from app.ai.inference_service import get_detector
from app.database import engine

router = APIRouter(tags=["health"])


@router.get("/api/health")
def health():
    db_ok = True
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    _, detector_info = get_detector()
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "unavailable",
        "detector_mode": detector_info.get("mode"),
        "demo_model": detector_info.get("demo", True),
        "fallback_reason": detector_info.get("fallback_reason"),
    }
