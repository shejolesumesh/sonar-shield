def test_model_info(client):
    resp = client.get("/api/model")
    assert resp.status_code == 200
    body = resp.json()
    assert body["active_mode"] in {"DEMO DETECTOR", "REAL AI MODEL"}
    if body["active_mode"] == "REAL AI MODEL":
        assert body["supported_classes"] == ["Crab-Pot"]
    assert body["known_class_threshold"] > 0
    assert "weights" in body["risk_formula"]
    assert "retraining_note" in body
