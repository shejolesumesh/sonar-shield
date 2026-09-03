import os
import sys
from pathlib import Path

# Ensure backend package is importable when running pytest from backend/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

TEST_DIR = Path(__file__).resolve().parent
DATA_DIR = TEST_DIR / "_test_data"

os.environ["DATABASE_URL"] = f"sqlite:///{DATA_DIR / 'test_sonar_shield.db'}"
os.environ["UPLOAD_DIR"] = str(DATA_DIR / "uploads")
os.environ["PROCESSED_DIR"] = str(DATA_DIR / "processed")
DATA_DIR.mkdir(parents=True, exist_ok=True)

import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    from app import models  # noqa: F401
    from app.models import image, detection, evidence, feedback, model_version  # noqa: F401
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def sample_png_bytes():
    """Deterministic synthetic sonar-like image with a bright blob and dark shadow."""
    import cv2

    img = np.full((480, 640), 60, dtype=np.uint8)
    noise = np.random.default_rng(42).integers(-10, 10, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.circle(img, (320, 240), 60, 220, -1)   # bright object return
    cv2.ellipse(img, (320, 330), (70, 25), 0, 0, 360, 15, -1)  # shadow region
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


@pytest.fixture()
def uploaded_image(client, sample_png_bytes):
    resp = client.post(
        "/api/sonar/upload",
        files={"file": ("test_sonar.png", sample_png_bytes, "image/png")},
        data={"metadata_json": '{"latitude": 12.9716, "longitude": 77.5946, "depth": 42.5}'},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()
