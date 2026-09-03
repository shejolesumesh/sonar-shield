def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] in {"ok", "degraded"}
    assert "detector_mode" in body


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["name"] == "SONAR-SHIELD"
