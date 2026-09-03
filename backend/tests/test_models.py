import uuid

from app.models.detection import Detection as DetectionModel
from app.models.evidence import Evidence as EvidenceModel
from app.models.feedback import ExpertFeedback as FeedbackModel
from app.models.image import Image as ImageModel
from app.models.model_version import ModelVersion as ModelVersionModel


def test_create_full_chain(db_session):
    img = ImageModel(filename="t.png", storage_path="/tmp/t.png", latitude=1.0, longitude=2.0)
    db_session.add(img)
    db_session.flush()

    det = DetectionModel(image_id=img.id, object_type="Ghost Net", raw_label="Ghost Net",
                         confidence=0.9, risk_score=80, risk_level="CRITICAL", priority=1,
                         bbox=[1, 2, 3, 4], model_version="demo-0.1.0")
    db_session.add(det)
    db_session.flush()

    ev = EvidenceModel(detection_id=det.id, confidence_evidence=["a"], visual_evidence=["b"],
                       shadow_evidence=["c"], explanation="x")
    fb = FeedbackModel(detection_id=det.id, ai_label="Ghost Net", expert_label="Debris",
                       action="RECLASSIFY")
    mv = ModelVersionModel(version=f"v-{uuid.uuid4().hex[:6]}", model_name="m")
    db_session.add_all([ev, fb, mv])
    db_session.commit()

    fetched = db_session.get(DetectionModel, det.id)
    assert fetched.evidence is not None
    assert len(fetched.feedback_items) == 1
    assert fetched.image_id == img.id
