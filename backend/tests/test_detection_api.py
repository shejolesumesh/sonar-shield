def test_run_detections_end_to_end(client, uploaded_image):
    image_id = uploaded_image["id"]
    resp = client.post(f"/api/detections/run?image_id={image_id}")
    assert resp.status_code == 201, resp.text
    dets = resp.json()
    assert isinstance(dets, list)
    for d in dets:
        assert 0 <= d["confidence"] <= 1
        assert d["object_type"]
        assert d["model_version"]


def test_run_detections_missing_image(client):
    resp = client.post("/api/detections/run?image_id=nope")
    assert resp.status_code == 404


def test_rerun_replaces_stale_detections(client, uploaded_image, monkeypatch):
    """A valid no-detection result must not keep results from an earlier run."""
    from app.ai.base_detector import DetectionCandidate
    from app.services import detection_service

    class SequenceDetector:
        name = "test-detector"
        version = "test-1"

        def __init__(self):
            self.calls = 0

        def detect(self, _image):
            self.calls += 1
            return [DetectionCandidate([50, 50, 100, 100], "Crab-Pot", 0.95)] if self.calls == 1 else []

    detector = SequenceDetector()
    monkeypatch.setattr(detection_service, "get_detector", lambda: (detector, {"demo": False}))
    image_id = uploaded_image["id"]
    assert len(client.post(f"/api/detections/run?image_id={image_id}").json()) == 1
    assert client.post(f"/api/detections/run?image_id={image_id}").json() == []
    assert [d for d in client.get("/api/detections").json() if d["image_id"] == image_id] == []


def test_list_detections(client, uploaded_image):
    client.post(f"/api/detections/run?image_id={uploaded_image['id']}")
    resp = client.get("/api/detections")
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)


def test_get_detection_detail(client, uploaded_image):
    run = client.post(f"/api/detections/run?image_id={uploaded_image['id']}").json()
    if not run:
        return
    det_id = run[0]["id"]
    resp = client.get(f"/api/detections/{det_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["evidence"] is not None
    assert body["evidence"]["explanation"]
    assert body["latitude"] == uploaded_image["latitude"]


def test_get_detection_invalid_id(client):
    resp = client.get("/api/detections/not-a-uuid")
    assert resp.status_code == 400


def test_priority_queue_sorted(client, uploaded_image):
    client.post(f"/api/detections/run?image_id={uploaded_image['id']}")
    resp = client.get("/api/detections/priority-queue")
    assert resp.status_code == 200
    items = resp.json()
    priorities = [i["priority"] for i in items]
    assert priorities == sorted(priorities)
