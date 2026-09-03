def test_upload_success(client, sample_png_bytes):
    resp = client.post(
        "/api/sonar/upload",
        files={"file": ("scan.png", sample_png_bytes, "image/png")},
        data={"metadata_json": '{"latitude": 10.0, "longitude": 20.0, "depth": 30}'},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["latitude"] == 10.0
    assert body["longitude"] == 20.0
    assert body["storage_path"]


def test_upload_without_metadata(client, sample_png_bytes):
    resp = client.post("/api/sonar/upload", files={"file": ("scan.png", sample_png_bytes, "image/png")})
    assert resp.status_code == 201
    assert resp.json()["latitude"] is None


def test_upload_invalid_extension(client):
    resp = client.post("/api/sonar/upload", files={"file": ("evil.exe", b"not an image", "application/octet-stream")})
    assert resp.status_code == 400


def test_upload_corrupt_image(client):
    resp = client.post("/api/sonar/upload", files={"file": ("fake.png", b"not-a-real-png", "image/png")})
    assert resp.status_code == 400


def test_upload_invalid_metadata_gps(client, sample_png_bytes):
    resp = client.post(
        "/api/sonar/upload",
        files={"file": ("s.png", sample_png_bytes, "image/png")},
        data={"metadata_json": '{"latitude": 999.0}'},
    )
    assert resp.status_code == 422


def test_upload_invalid_metadata_json(client, sample_png_bytes):
    resp = client.post(
        "/api/sonar/upload",
        files={"file": ("s.png", sample_png_bytes, "image/png")},
        data={"metadata_json": "{not json"},
    )
    assert resp.status_code == 400
