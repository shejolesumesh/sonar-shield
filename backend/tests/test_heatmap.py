def test_heatmap_with_geolocated_detection(client, uploaded_image):
    client.post(f"/api/detections/run?image_id={uploaded_image['id']}")
    resp = client.get("/api/heatmap")
    assert resp.status_code == 200
    body = resp.json()
    if body["has_data"]:
        assert all("latitude" in p for p in body["points"])
    else:
        assert body["message"]


def test_map_points_endpoint(client):
    resp = client.get("/api/map-points")
    assert resp.status_code == 200
