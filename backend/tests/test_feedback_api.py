def _first_detection(client, uploaded_image):
    run = client.post(f"/api/detections/run?image_id={uploaded_image['id']}").json()
    return run[0] if run else None


def test_confirm_feedback(client, uploaded_image):
    det = _first_detection(client, uploaded_image)
    if not det:
        return
    resp = client.post("/api/feedback", json={
        "detection_id": det["id"], "action": "CONFIRM", "comment": "looks right"})
    assert resp.status_code == 201
    detail = client.get(f"/api/detections/{det['id']}").json()
    assert detail["status"] == "CONFIRMED"


def test_reclassify_preserves_ai_label(client, uploaded_image):
    det = _first_detection(client, uploaded_image)
    if not det:
        return
    ai_label = det["object_type"]
    resp = client.post("/api/feedback", json={
        "detection_id": det["id"], "action": "RECLASSIFY", "expert_label": "Other Debris"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["ai_label"] == ai_label          # original preserved
    assert body["expert_label"] == "Other Debris"


def test_reclassify_requires_label(client, uploaded_image):
    det = _first_detection(client, uploaded_image)
    if not det:
        return
    resp = client.post("/api/feedback", json={"detection_id": det["id"], "action": "RECLASSIFY"})
    assert resp.status_code == 422


def test_feedback_invalid_action(client, uploaded_image):
    det = _first_detection(client, uploaded_image)
    if not det:
        return
    resp = client.post("/api/feedback", json={"detection_id": det["id"], "action": "MAYBE"})
    assert resp.status_code == 422


def test_feedback_missing_detection(client):
    resp = client.post("/api/feedback", json={"detection_id": "missing", "action": "CONFIRM"})
    assert resp.status_code == 404


def test_list_feedback(client, uploaded_image):
    resp = client.get("/api/feedback")
    assert resp.status_code == 200
