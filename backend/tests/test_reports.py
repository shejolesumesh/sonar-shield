def test_csv_export(client, uploaded_image):
    client.post(f"/api/detections/run?image_id={uploaded_image['id']}")
    resp = client.get("/api/reports/export/csv")
    assert resp.status_code == 200
    text = resp.text
    assert "detection_id" in text
    assert "PROTOTYPE" in text.upper() or "#" in text


def test_json_export(client, uploaded_image):
    client.post(f"/api/detections/run?image_id={uploaded_image['id']}")
    resp = client.get("/api/reports/export/json")
    assert resp.status_code == 200
    body = resp.json()
    assert "meta" in body and "rows" in body
    assert body["meta"]["disclaimer"]


def test_summary(client, uploaded_image):
    client.post(f"/api/detections/run?image_id={uploaded_image['id']}")
    resp = client.get("/api/reports/summary")
    assert resp.status_code == 200
    body = resp.json()
    assert "by_risk_level" in body and "by_priority" in body
