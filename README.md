# SONAR-SHIELD

End-to-end underwater side-scan sonar intelligence and marine-debris decision-support system.

## Overview

SONAR-SHIELD ingests side-scan sonar imagery (+ optional GPS/depth metadata), preprocesses it,
runs AI object detection through a pluggable detector layer, produces Evidence Cards, computes a
transparent **PROTOTYPE RISK SCORE**, assigns recovery priority (P1-P4), and presents everything in
a professional web dashboard with interactive map, heatmap, expert review workflow, and reporting.

> This is a decision-support prototype. The supplied GhostVision ONNX model is used as **REAL AI MODEL**
> when its supplied assets load; otherwise the clearly labeled **DEMO DETECTOR** is used. Demo outputs
> are not scientifically validated. Real-world deployment requires validated
> side-scan sonar datasets, domain-expert annotation, real hardware integration, geolocation
> calibration, field testing, and benchmarking.

## Architecture

Side-scan sonar image + metadata -> Ingestion -> Preprocessing -> AI Detection Engine
-> Confidence & Evidence Engine -> Risk Engine -> Priority Engine -> SQLite Database
-> FastAPI REST API -> React Dashboard (Map / Heatmap / Expert Review / Reports)
-> Human Feedback Loop -> Validated dataset for future retraining.

See `models/README.md` for the supplied GhostVision ONNX integration and optional PyTorch adapter.

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env    # edit if desired
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Dashboard: http://localhost:5173

### Docker
```bash
docker compose up --build
```

## Environment Variables

Copy `.env.example` to `.env`. Never commit `.env`.

| Variable | Default | Description |
|---|---|---|
| DATABASE_URL | sqlite:///./data/sonar_shield.db | SQLAlchemy URL (PostgreSQL-compatible) |
| UPLOAD_DIR | ./data/uploads | Original image storage |
| PROCESSED_DIR | ./data/processed | Processed image storage |
| MAX_UPLOAD_SIZE_MB | 25 | Upload size limit |
| KNOWN_CLASS_THRESHOLD | 0.70 | Below this confidence -> UNKNOWN ANOMALY |
| DETECTOR_TYPE | onnx | onnx, demo, or pytorch |
| ONNX_MODEL_PATH | ./models/weights.onnx | Supplied GhostVision ONNX weights |
| CLASS_NAMES_PATH | ./models/class_names.txt | Supplied real class mapping |
| MODEL_VERSION | GhostVision-ONNX-2026-01-27 | Active model version label |
| RISK_W_CONFIDENCE | 0.35 | Risk formula weight |
| RISK_W_SEVERITY | 0.25 | Risk formula weight |
| RISK_W_SIZE | 0.20 | Risk formula weight |
| RISK_W_LOCATION | 0.20 | Risk formula weight |
| CORS_ORIGINS | http://localhost:5173 | Comma-separated allowed origins |

## Key Features

- Sonar preprocessing (denoise, normalize, CLAHE contrast, shadow enhancement)
- UNKNOWN ANOMALY handling - low-confidence detections are never forced into known classes
- Per-detection Evidence Card with honest "Not available" fields
- Transparent PROTOTYPE RISK SCORE (configurable weights, clamped 0-100)
- Recovery priority queue P1-P4
- Leaflet map + detection-density heatmap (empty state when no GPS)
- Expert CONFIRM / REJECT / RECLASSIFY workflow preserving original AI predictions
- CSV & JSON report export
- Full test suite

## Limitations

- Demo detector produces deterministic heuristic pseudo-detections for development only.
- No accuracy/precision/recall/F1 is claimed anywhere without evaluated data.
- No automatic retraining; feedback is stored for future training pipelines.
- No vehicle control; no satellite-based underwater debris claims.
