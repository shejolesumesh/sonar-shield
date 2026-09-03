# 🌊 SONAR-SHIELD

## AI-Powered Underwater Side-Scan Sonar Intelligence & Marine Debris Decision-Support Platform

SONAR-SHIELD is an end-to-end AI-assisted underwater sonar intelligence platform designed to analyze side-scan sonar imagery, identify potential submerged objects, evaluate detection confidence, organize available evidence, estimate prototype risk, prioritize detections, visualize their geographic distribution, and support expert review.

The platform follows a human-in-the-loop approach in which AI assists the analysis process while human experts retain control over final interpretation and decisions.

---

## 🚀 Overview

Side-scan sonar surveys can generate large amounts of underwater imagery. Manually inspecting and organizing these images can be time-consuming, especially when multiple detections need to be reviewed, compared, prioritized, and documented.

SONAR-SHIELD provides a unified workflow that transforms sonar imagery into structured decision-support information.

The complete pipeline is:

Side-Scan Sonar Image
        +
Optional GPS / Depth Metadata
        ↓
Data Ingestion
        ↓
Sonar Preprocessing
        ↓
AI Detection
        ↓
Confidence Analysis
        ↓
Evidence Generation
        ↓
Risk Assessment
        ↓
Recovery Priority
        ↓
Database Storage
        ↓
FastAPI REST API
        ↓
React Dashboard
        ↓
Geospatial Visualization
        ↓
Expert Review
        ↓
Feedback Storage
        ↓
Future Dataset / Model Improvement
````

The key idea behind SONAR-SHIELD is to move beyond simple object detection and provide a complete:

**Detect → Understand → Assess → Prioritize → Review → Report**

workflow.

---

## 🎯 Problem Statement

Underwater environments can contain submerged objects and debris that may be difficult to identify through manual sonar inspection.

Side-scan sonar provides valuable acoustic imagery, but large-scale sonar surveys can produce a significant amount of data that requires careful analysis.

A conventional workflow may look like:

```text
Sonar Survey
     ↓
Large Collection of Images
     ↓
Manual Inspection
     ↓
Manual Detection
     ↓
Manual Interpretation
     ↓
Manual Prioritization
     ↓
Manual Reporting
```

This creates several challenges:

* Large volumes of sonar imagery
* Repetitive manual inspection
* Dependence on expert availability
* Difficulty maintaining consistent analysis
* Difficulty prioritizing multiple detections
* Separation between detection and geographic information
* Difficulty maintaining review history
* Difficulty converting detections into structured reports

A basic AI detector only addresses the detection problem.

A practical decision-support platform should also answer:

* What was detected?
* How confident is the AI?
* Is the confidence sufficient to assign a known class?
* What evidence is actually available?
* What information is unavailable?
* What is the prototype risk score?
* Which detection should be investigated first?
* Where is the detection located?
* Can an expert review the prediction?
* Can the review be stored?
* Can the result be exported?

SONAR-SHIELD is designed around these requirements.

---

## 💡 Proposed Solution

SONAR-SHIELD combines computer vision, AI inference, decision-support logic, geospatial visualization, database persistence, reporting, and human review into a single platform.

```text
┌────────────────────────────────────────────────────┐
│                   SONAR-SHIELD                     │
├────────────────────────────────────────────────────┤
│                                                    │
│  Sonar Image + Metadata                            │
│              ↓                                     │
│  Image Preprocessing                               │
│              ↓                                     │
│  AI Detection                                      │
│              ↓                                     │
│  Confidence / Unknown Analysis                     │
│              ↓                                     │
│  Evidence Engine                                   │
│              ↓                                     │
│  Risk Assessment                                   │
│              ↓                                     │
│  Recovery Priority                                 │
│              ↓                                     │
│  Database                                          │
│              ↓                                     │
│  FastAPI REST API                                  │
│              ↓                                     │
│  React Dashboard                                   │
│              ↓                                     │
│  Map / Heatmap / Analysis / Reports                │
│              ↓                                     │
│  Expert Review                                     │
│              ↓                                     │
│  Feedback                                          │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 🌊 Why SONAR-SHIELD?

Instead of stopping at:

```text
Object Detected
```

SONAR-SHIELD attempts to provide:

```text
Object Detected
      ↓
Confidence
      ↓
Evidence
      ↓
Risk
      ↓
Recovery Priority
      ↓
Location
      ↓
Expert Review
      ↓
Report
```

This creates a structured decision-support workflow around AI predictions.

The system is not designed to replace domain experts.

It is designed to help experts:

* Find potential detections faster
* Understand available information
* Identify uncertain detections
* Prioritize detections
* Review AI predictions
* Maintain structured records
* Generate reports

---

## 🎯 Objectives

SONAR-SHIELD aims to:

1. Assist with automated side-scan sonar image analysis.
2. Reduce repetitive manual inspection.
3. Provide a structured AI-assisted detection workflow.
4. Preserve uncertainty in AI predictions.
5. Avoid fabricating unavailable evidence.
6. Generate transparent prototype risk scores.
7. Prioritize detections for investigation.
8. Provide geographic visualization when location data is available.
9. Enable expert review of AI predictions.
10. Preserve human feedback.
11. Generate structured reports.
12. Provide a modular architecture for future AI models.
13. Provide a foundation for future validated marine-survey applications.

---

# 🏗️ System Architecture

                         SONAR-SHIELD
                              │
                              ▼
                ┌─────────────────────────┐
                │       SONAR DATA        │
                │                         │
                │ Images                  │
                │ GPS                     │
                │ Depth                   │
                │ Metadata                │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │      DATA INGESTION     │
                │                         │
                │ Validation              │
                │ Upload Handling         │
                │ Storage                 │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │   SONAR PREPROCESSING   │
                │                         │
                │ OpenCV                  │
                │ NumPy                   │
                │ Denoising               │
                │ Normalization           │
                │ CLAHE                   │
                │ Shadow Enhancement      │
                │ Letterboxing            │
                └────────────┬────────────┘
                             │
                             ▼
          ┌────────────────────────────────────┐
          │          AI DETECTION LAYER        │
          │                                    │
          │ ONNX Detector                     │
          │ PyTorch Adapter                   │
          │ Demo Detector                     │
          └────────────────┬───────────────────┘
                           │
                           ▼
                ┌─────────────────────────┐
                │   CONFIDENCE ENGINE     │
                │                         │
                │ Known Class             │
                │ Unknown Anomaly         │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │     EVIDENCE ENGINE     │
                │                         │
                │ Evidence Cards          │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │       RISK ENGINE       │
                │                         │
                │ Prototype Score 0-100   │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │    PRIORITY ENGINE      │
                │                         │
                │ P1 / P2 / P3 / P4       │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │      SQLITE DATABASE    │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │      FASTAPI API        │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │     REACT FRONTEND      │
                │                         │
                │ Dashboard               │
                │ Sonar Analysis          │
                │ Detection Details       │
                │ Recovery Priority       │
                │ Map / Heatmap            │
                │ Expert Review           │
                │ Reports                 │
                │ Model Information       │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │     EXPERT REVIEW       │
                │                         │
                │ Confirm                 │
                │ Reject                  │
                │ Reclassify              │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │    FEEDBACK STORAGE     │
                │                         │
                │ Future Dataset           │
                │ Model Improvement       │
                └─────────────────────────┘
```

---

# 🔄 Complete Workflow

## 1. Sonar Data

The process begins with a side-scan sonar image.

Optional metadata can include:

* Latitude
* Longitude
* Depth
* Survey information

↓

## 2. Data Ingestion

The uploaded data is validated and stored before analysis.

↓

## 3. Preprocessing

The sonar image is processed to improve its suitability for AI inference.

↓

## 4. AI Detection

The processed image is passed to the configured detector.

↓

## 5. Confidence Analysis

The system evaluates the confidence of the prediction.

↓

## 6. Unknown Anomaly Handling

Low-confidence predictions can be represented as:

```text
UNKNOWN ANOMALY
```

rather than being forced into a known class.

↓

## 7. Evidence Generation

The system organizes the available information into an Evidence Card.

↓

## 8. Risk Assessment

A transparent prototype risk score is calculated.

↓

## 9. Recovery Priority

The detection is assigned a priority level.

↓

## 10. Database

Analysis results and review information are stored.

↓

## 11. Dashboard

The React frontend presents the information to the user.

↓

## 12. Expert Review

An expert can:

```text
CONFIRM
REJECT
RECLASSIFY
```

↓

## 13. Reporting

Results can be exported in structured formats.

↓

## 14. Future Improvement

Human feedback can provide a foundation for future dataset creation and model improvement.

---

# 🖼️ Sonar Preprocessing

Raw sonar imagery may contain noise, inconsistent intensity, low contrast, and other characteristics that can affect downstream analysis.

SONAR-SHIELD contains a dedicated preprocessing pipeline.

```text
Input Sonar Image
        ↓
Grayscale Processing
        ↓
Median Filtering
        ↓
Bilateral Filtering
        ↓
Normalization
        ↓
CLAHE
        ↓
Shadow Enhancement
        ↓
Letterboxing
        ↓
AI Model Input
```

### Denoising

Median and bilateral filtering are used to reduce unwanted image noise while preserving relevant structures.

### Normalization

Image intensity values are normalized to create a more consistent representation.

### CLAHE

Contrast Limited Adaptive Histogram Equalization is used to improve local image contrast.

### Shadow Enhancement

Sonar shadows can provide useful contextual information around submerged objects.

### Letterboxing

The image is prepared for the expected model input dimensions while maintaining spatial proportions.

The current inference pipeline uses:

```text
640 × 640
```

model input dimensions.

---

# 🤖 AI Detection Engine

SONAR-SHIELD uses a modular detector architecture.

```text
                    BaseDetector
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    ONNX Detector   PyTorch Adapter   Demo Detector
```

This separation allows the underlying detection implementation to be replaced or extended without redesigning the entire platform.

### ONNX Detector

Used to integrate the supplied ONNX model through ONNX Runtime.

### PyTorch Adapter

Provides an architecture for integrating PyTorch-based detection models.

### Demo Detector

Provides deterministic detection behavior for development and UI testing.

---

# 🧠 Current AI Model

The current integrated real model is:

```text
GhostVision ONNX
```

The supplied class mapping currently contains:

```text
Crab-Pot
```

Therefore, the currently integrated real detector is a:

**Single-class Crab-Pot detector.**

The application architecture is designed to support additional validated side-scan sonar classes and models in future versions.

The project does not claim unsupported accuracy or performance metrics for the current model.

---

# ⚙️ Model Inference

The model inference pipeline is:

```text
Input Image
     ↓
Sonar Preprocessing
     ↓
640 × 640 Model Input
     ↓
ONNX Runtime
     ↓
Raw Model Output
     ↓
Post Processing
     ↓
Non-Maximum Suppression
     ↓
Confidence Processing
     ↓
Coordinate Mapping
     ↓
Detection Result
```

The current ONNX model uses an input representation corresponding to:

```text
[1, 3, 640, 640]
```

The detector validates model assets and processes the model output before returning detection results.

Post-processing includes non-maximum suppression and mapping detected coordinates back to the original image space.

---

# ❓ Confidence & Unknown Anomaly Handling

SONAR-SHIELD does not assume that every AI prediction is reliable.

The system uses a configurable confidence threshold.

Default:

```text
KNOWN_CLASS_THRESHOLD = 0.70
```

The workflow is:

```text
                 AI Prediction
                       ↓
                  Confidence
                       ↓
             ┌─────────┴─────────┐
             │                   │
          ≥ 0.70              < 0.70
             │                   │
             ▼                   ▼
       Known Class        UNKNOWN ANOMALY
```

This approach prevents low-confidence predictions from automatically being presented as confidently identified objects.

Unknown Anomaly handling also creates a path for future discovery of objects that are not represented in the current model's known classes.

---

# 🔎 Evidence Engine

The Evidence Engine organizes information associated with each detection.

The system follows an important principle:

> **Do not fabricate evidence.**

If a property cannot be reliably determined from the available analysis, the system can represent it as:

```text
Not available from current analysis
```

This creates a clear distinction between:

```text
Available Evidence
```

and:

```text
Unavailable Information
```

The Evidence Engine is therefore designed to improve transparency and prevent unsupported information from being presented as measured fact.

---

# ⚠️ Risk Assessment Engine

SONAR-SHIELD includes a transparent prototype risk-assessment engine.

The current output is:

```text
Prototype Risk Score
0 - 100
```

The score is intended for decision support and prioritization.

It is **not a scientifically validated environmental-risk measurement.**

### Current Risk Weights

| Factor     | Weight |
| ---------- | -----: |
| Confidence |   0.35 |
| Severity   |   0.25 |
| Size       |   0.20 |
| Location   |   0.20 |

Conceptually:

```text
                  Confidence
                       │
                       ▼
                 ┌──────────┐
                 │          │
Severity ───────►│   RISK   │◄────── Size
                 │          │
                 └────┬─────┘
                      ▲
                      │
                   Location
```

The resulting score is constrained between:

```text
0 and 100
```

The risk engine is intentionally transparent and configurable rather than being presented as a scientifically validated black-box risk model.

---

# 🚨 Recovery Priority Engine

The Recovery Priority Engine uses the decision-support information to organize detections.

Current priority levels:

```text
P1
P2
P3
P4
```

Conceptually:

```text
Detection
    ↓
Risk Score
    ↓
Priority Engine
    ↓
┌────┬────┬────┬────┐
│ P1 │ P2 │ P3 │ P4 │
└────┴────┴────┴────┘
```

The priority system helps organize detections for investigation and potential recovery planning.

These priority levels are part of the current prototype and should not be interpreted as scientifically validated recovery classifications.

---

# 🗺️ Geospatial Intelligence

SONAR-SHIELD supports geographic visualization when valid GPS metadata is available.

### Interactive Map

The frontend uses Leaflet for interactive geographic visualization.

### Heatmap

The platform can visualize the spatial concentration of detections through heatmap functionality.

### Missing GPS Data

If GPS information is unavailable, the system does not fabricate coordinates.

This avoids presenting false geographic precision.

---

# 👨‍🔬 Expert Review

SONAR-SHIELD follows a human-in-the-loop architecture.

AI predictions can be reviewed by an expert.

The expert can:

```text
CONFIRM
REJECT
RECLASSIFY
```

The workflow is:

```text
                 AI Prediction
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
      Original Result       Expert Review
                                 │
                      ┌──────────┼──────────┐
                      │          │          │
                      ▼          ▼          ▼
                   Confirm     Reject    Reclassify
```

The system preserves the distinction between the original AI output and the human review decision.

This makes the workflow auditable and suitable for future feedback-driven development.

---

# 🔁 Human Feedback Loop

Expert feedback can form the foundation of a future model-improvement pipeline.

```text
AI Detection
     ↓
Expert Review
     ↓
Confirm / Reject / Reclassify
     ↓
Validated Data
     ↓
Future Dataset
     ↓
Model Training
     ↓
Model Evaluation
     ↓
Improved Model
     ↓
Deployment
```

The current implementation does **not automatically retrain the AI model**.

Instead, expert feedback provides structured information that can be used in future dataset development and model validation.

---

# 📊 Reporting

SONAR-SHIELD provides structured reporting functionality.

Supported output formats include:

```text
CSV
JSON
```

Reports can be used for:

* Analysis
* Research
* Documentation
* Expert review
* Dataset preparation
* Future model evaluation

---

# 🖥️ Frontend

The frontend is built using React and provides the primary user interface.

The application includes interfaces for:

* Dashboard
* Sonar Analysis
* Detection Details
* Recovery Priority
* Map
* Heatmap
* Expert Review
* Reports
* Model Information

The frontend communicates with the backend through REST APIs.

API communication is centralized through the frontend service layer.

---

# ⚙️ Backend

The backend is built using Python and FastAPI.

It is responsible for:

* API endpoints
* Upload handling
* Data validation
* Image preprocessing
* AI inference
* Detection processing
* Confidence analysis
* Evidence generation
* Risk calculation
* Priority calculation
* Database operations
* Expert feedback
* Report generation

The backend follows a modular architecture to keep responsibilities separated.

---

# 🗄️ Database

The current prototype uses:

```text
SQLite
```

with:

```text
SQLAlchemy
```

SQLite is suitable for the current prototype because it is:

* Lightweight
* File-based
* Easy to configure
* Easy to run locally
* Suitable for development
* Suitable for testing

The architecture can be extended to a production database such as PostgreSQL in future deployments.

---

# 🌐 API Architecture

The communication flow is:

```text
React Frontend
       ↓
HTTP / REST
       ↓
FastAPI
       ↓
Application Services
       ↓
AI / Evidence / Risk / Priority
       ↓
SQLite Database
```

FastAPI also provides interactive API documentation.

When running locally:

```text
http://localhost:8000/docs
```

The API includes functionality related to areas such as:

* Health
* Upload
* Detection
* Model information
* Feedback
* Heatmap
* Reports
* Risk
* Expert review

---

# 🧰 Technology Stack

## Frontend

| Technology   | Purpose                       |
| ------------ | ----------------------------- |
| React        | User interface                |
| Vite         | Development and build tooling |
| Tailwind CSS | Styling                       |
| React Router | Frontend routing              |
| Axios        | API communication             |
| Leaflet      | Interactive maps              |
| Recharts     | Data visualization            |

## Backend

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Backend programming language |
| FastAPI    | REST API framework           |
| SQLAlchemy | Database ORM                 |
| Pydantic   | Data validation              |
| SQLite     | Local database               |

## AI & Computer Vision

| Technology   | Purpose                        |
| ------------ | ------------------------------ |
| ONNX Runtime | ONNX model inference           |
| OpenCV       | Image processing               |
| NumPy        | Numerical and image operations |
| PyTorch      | Optional detector adapter      |

## Infrastructure

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| Docker         | Containerization              |
| Docker Compose | Multi-container orchestration |
| Git            | Version control               |
| GitHub         | Source-code hosting           |

## Testing

| Technology         | Purpose                     |
| ------------------ | --------------------------- |
| Pytest             | Backend testing             |
| FastAPI TestClient | API testing                 |
| Vite Build         | Frontend build verification |

---

# 📁 Project Structure

```text
sonar-shield/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── api/
│   │   ├── evidence/
│   │   ├── models/
│   │   ├── preprocessing/
│   │   ├── priority/
│   │   ├── quality/
│   │   ├── risk/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── models/
│   ├── weights.onnx
│   ├── class_names.txt
│   └── README.md
│
├── data/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# ✨ Application Features

## AI

* AI-assisted sonar object detection
* ONNX model inference
* PyTorch detector adapter
* Deterministic demo detector
* Confidence thresholding
* Unknown anomaly handling

## Image Processing

* Grayscale processing
* Median filtering
* Bilateral filtering
* Normalization
* CLAHE
* Shadow enhancement
* Letterboxing
* Image-quality analysis

## Decision Support

* Evidence Cards
* Prototype Risk Score
* Configurable risk weights
* Recovery Priority
* P1-P4 prioritization

## Visualization

* Interactive dashboard
* Detection details
* Interactive map
* Heatmap
* GPS-aware visualization
* Charts

## Human-in-the-Loop

* Confirm detection
* Reject detection
* Reclassify detection
* Preserve original AI result
* Store review feedback

## Reporting

* CSV export
* JSON export

## Engineering

* FastAPI REST API
* React frontend
* SQLite persistence
* Docker Compose
* Automated backend testing

---

# 📦 Installation

## Requirements

Recommended environment:

```text
Python 3.x
Node.js
npm
Git
Docker (optional)
```

---

# ▶️ Running Locally

## Backend

From the project root:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```powershell
.\venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

## Frontend

Open another terminal.

From the project root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🐳 Docker Deployment

From the project root:

```bash
docker compose build
```

Start the application:

```bash
docker compose up
```

Or build and start together:

```bash
docker compose up --build
```

The configured services are:

```text
Backend
Frontend
```

Expected local endpoints:

```text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000

API Documentation:
http://localhost:8000/docs
```

---

# 🔐 Environment Variables

The application provides sensible defaults for local development.

If custom configuration is required, create a `.env` file in the project root.

**Never commit `.env` files or secrets to GitHub.**

| Variable                | Default                            | Description               |
| ----------------------- | ---------------------------------- | ------------------------- |
| `DATABASE_URL`          | `sqlite:///./data/sonar_shield.db` | Database connection       |
| `UPLOAD_DIR`            | `./data/uploads`                   | Uploaded image directory  |
| `PROCESSED_DIR`         | `./data/processed`                 | Processed image directory |
| `MAX_UPLOAD_SIZE_MB`    | `25`                               | Maximum upload size       |
| `KNOWN_CLASS_THRESHOLD` | `0.70`                             | Confidence threshold      |
| `DETECTOR_TYPE`         | `onnx`                             | Detector implementation   |
| `ONNX_MODEL_PATH`       | `./models/weights.onnx`            | ONNX model path           |
| `CLASS_NAMES_PATH`      | `./models/class_names.txt`         | Class mapping             |
| `MODEL_VERSION`         | `GhostVision-ONNX-2026-01-27`      | Model version             |
| `RISK_W_CONFIDENCE`     | `0.35`                             | Confidence weight         |
| `RISK_W_SEVERITY`       | `0.25`                             | Severity weight           |
| `RISK_W_SIZE`           | `0.20`                             | Size weight               |
| `RISK_W_LOCATION`       | `0.20`                             | Location weight           |
| `CORS_ORIGINS`          | `http://localhost:5173`            | Allowed frontend origin   |

---

# 🧪 Testing

SONAR-SHIELD includes an automated backend test suite.

Run:

```bash
cd backend
pytest
```

The test suite covers areas including:

* Detection
* Feedback
* Health
* Heatmap
* Model APIs
* Model loading
* ONNX detector
* Preprocessing
* Image quality
* Risk assessment
* Reporting
* Upload handling
* Unknown anomaly handling

For Windows environments where temporary-directory permissions cause pytest issues, a project-local temporary directory can be used:

```bash
pytest --basetemp .pytest_temp
```

---

# ✅ Current Validation

The current development environment successfully passed:

```text
46 / 46 backend tests
```

The test suite completed successfully with:

```text
46 passed
2 warnings
```

The warnings were dependency deprecation warnings and did not cause test failures.

The application has also been run successfully in the local development environment with:

```text
Backend API        → Working
Frontend           → Working
Frontend ↔ Backend → Working
```

These results demonstrate software-level functionality in the current development environment.

They do not represent scientific validation of the AI model.

---

# 🧠 Design Principles

## Transparency

SONAR-SHIELD separates:

```text
AI Prediction
Prototype Risk Score
Human Review
```

These represent different stages of the decision-support process.

---

## Uncertainty Preservation

Low-confidence predictions can become:

```text
UNKNOWN ANOMALY
```

instead of being incorrectly forced into a known class.

---

## Evidence Integrity

The system avoids intentionally fabricating evidence.

Unavailable information can be represented as:

```text
Not available from current analysis
```

---

## Human Oversight

AI predictions can be reviewed and corrected by human experts.

---

## Original Result Preservation

Human review does not erase the original AI prediction.

This allows the system to preserve the history of:

```text
AI Decision
      +
Human Decision
```

---

## Modular Architecture

Major components are separated into:

```text
AI
Preprocessing
Evidence
Risk
Priority
API
Frontend
Database
```

This makes future upgrades easier.

---

## No Unsupported Accuracy Claims

The project does not claim precision, recall, F1, mAP, or other model-performance metrics without an appropriately evaluated dataset.

---

# 🔒 Security Considerations

The current system is primarily intended for prototype and local-development usage.

A production deployment should additionally implement:

* Authentication
* Authorization
* Role-based access control
* Secure secret management
* HTTPS
* Rate limiting
* Stronger file validation
* Secure file storage
* Audit logging
* Production database security
* Model access controls
* Monitoring and logging

---

# ⚠️ Limitations

## Current AI Model

The supplied GhostVision ONNX model currently contains a single class:

```text
Crab-Pot
```

Therefore, the current real detector should not be described as a fully validated multi-class marine-debris detector.

---

## Dataset

A production-grade system would require a significantly larger and domain-specific dataset containing:

* Diverse sonar environments
* Different depths
* Different sonar devices
* Different image resolutions
* Different environmental conditions
* Expert annotations
* Multiple object categories

---

## Model Validation

A properly validated production model would require evaluation using metrics such as:

* Precision
* Recall
* F1 Score
* mAP
* Confusion Matrix
* Per-class performance
* False-positive rate
* False-negative rate

These metrics should be calculated using an appropriately designed evaluation dataset.

---

## Risk Score

The current risk score is a prototype decision-support heuristic.

It is not a scientifically validated environmental-risk measurement.

---

## GPS

Geospatial visualization depends on valid location metadata.

The system does not fabricate GPS coordinates when location information is unavailable.

---

## Automatic Retraining

The current system does not automatically retrain the AI model.

Expert feedback is stored as a foundation for potential future dataset creation and model improvement.

---

## Hardware Integration

The current application does not directly control underwater vehicles or sonar acquisition hardware.

---

# 🔮 Future Scope

## Multi-Class Marine Object Detection

Future validated models could support additional underwater-object categories.

Examples may include:

```text
Fishing Nets
Fishing Gear
Cables
Containers
Wreck Fragments
Other Validated Sonar Objects
```

These categories should only be introduced after appropriate dataset creation and model validation.

---

## Large-Scale Sonar Dataset

A future dataset could contain:

```text
Sonar Image
     +
Object Class
     +
Bounding Box
     +
GPS
     +
Depth
     +
Expert Annotation
     +
Review Result
```

This could enable domain-specific model training and evaluation.

---

## Model Benchmarking

Future versions can provide:

```text
Precision
Recall
F1 Score
mAP
Confusion Matrix
Per-Class Metrics
False-Positive Rate
False-Negative Rate
```

using properly separated training, validation, and test datasets.

---

## Advanced Geospatial Intelligence

Potential improvements include:

* Survey-track visualization
* Spatial clustering
* Depth-aware visualization
* Detection-density analysis
* Geographic priority analysis
* Survey coverage analysis

---

## Human-in-the-Loop Learning

The feedback system could eventually become a complete model-improvement pipeline:

```text
AI Prediction
      ↓
Expert Review
      ↓
Validated Data
      ↓
Dataset
      ↓
Training
      ↓
Evaluation
      ↓
Model Selection
      ↓
Deployment
```

---

## Production Database

SQLite can eventually be replaced with a production database such as PostgreSQL.

---

## Authentication & Authorization

Future versions could support:

* User accounts
* Expert accounts
* Administrator accounts
* Role-based permissions
* Audit trails

---

## Cloud Deployment

Potential future infrastructure could include:

* Cloud object storage
* Cloud databases
* Background inference workers
* Scalable model serving
* Centralized monitoring
* Centralized logging

---

## Real Sonar Hardware Integration

After appropriate validation, SONAR-SHIELD could be integrated with real sonar acquisition systems and underwater survey workflows.

---

# 🤝 Responsible AI

SONAR-SHIELD follows several principles intended to make AI-assisted decision support transparent.

### AI predictions are not treated as absolute truth.

Model predictions can be uncertain.

### Uncertainty is preserved.

Low-confidence results can be represented as:

```text
UNKNOWN ANOMALY
```

### Evidence is not fabricated.

Unavailable information is clearly represented as unavailable.

### Human experts remain involved.

AI results can be confirmed, rejected, or reclassified.

### Original predictions are preserved.

Human review does not silently replace the original AI output.

### Prototype risk scores are clearly identified.

The current risk engine is a decision-support heuristic and not a scientifically validated environmental-risk model.

---

# 📌 Project Status

### Implemented

```text
🟢 Backend
🟢 React Frontend
🟢 AI Detection Architecture
🟢 ONNX Model Integration
🟢 Demo Detector
🟢 Sonar Preprocessing
🟢 Confidence Handling
🟢 Unknown Anomaly Handling
🟢 Evidence Engine
🟢 Risk Engine
🟢 Priority Engine
🟢 Geospatial Visualization
🟢 Expert Review
🟢 Feedback Storage
🟢 Reporting
🟢 SQLite Persistence
🟢 REST API
🟢 Automated Tests
🟢 Docker Configuration
```

### Future / Requires Further Validation

```text
🟡 Large-Scale Validated Sonar Dataset
🟡 Scientific AI Model Evaluation
🟡 Multi-Class Production Detector
🟡 Production Authentication
🟡 Production Database
🟡 Automatic Model Retraining
🟡 Real Sonar Hardware Integration
🟡 Field Validation
```

---

# 📸 Screenshots

Add project screenshots here when available.

Recommended screenshots:

```text
Dashboard
Sonar Analysis
Detection Details
Recovery Priority
Interactive Map
Heatmap
Expert Review
Reports
Model Information
```

Example structure:

```markdown
![SONAR-SHIELD Dashboard](screenshots/dashboard.png)

![Sonar Analysis](screenshots/sonar-analysis.png)

![Detection Details](screenshots/detection-details.png)

![Recovery Priority](screenshots/recovery-priority.png)

![Map and Heatmap](screenshots/map.png)

![Expert Review](screenshots/expert-review.png)
```

---

# 📚 Documentation

The complete technical explanation of SONAR-SHIELD is maintained in this README.

The README covers:

```text
Problem
Solution
Architecture
Workflow
AI Pipeline
Preprocessing
Model
Confidence
Unknown Anomalies
Evidence
Risk
Priority
Geospatial Intelligence
Expert Review
Feedback
Reporting
Technology Stack
Frontend
Backend
Database
API
Project Structure
Installation
Docker
Testing
Validation
Security
Limitations
Future Scope
Responsible AI
```

---

# 🏁 Conclusion

SONAR-SHIELD demonstrates how AI, computer vision, sonar-image processing, decision-support logic, geospatial visualization, database systems, and human review can be combined into a single underwater sonar intelligence platform.

The system goes beyond simple object detection.

Instead of only answering:

```text
"Was something detected?"
```

SONAR-SHIELD organizes a broader workflow:

```text
What was detected?
        ↓
How confident is the prediction?
        ↓
What evidence is available?
        ↓
What information is unavailable?
        ↓
What is the prototype risk?
        ↓
What is the recovery priority?
        ↓
Where is the detection?
        ↓
Can an expert review it?
        ↓
Can the result be reported?
```

The complete concept can therefore be summarized as:

```text
             ┌───────────┐
             │  DETECT   │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │ UNDERSTAND│
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │  ASSESS   │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │ PRIORITIZE│
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │   REVIEW  │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │  REPORT   │
             └───────────┘
```

SONAR-SHIELD provides the software foundation for this workflow while clearly separating what is currently implemented from what requires future scientific validation and production deployment.

---

# ⚠️ Disclaimer

SONAR-SHIELD is a research, demonstration, and decision-support prototype.

The current system and its prototype risk scoring should not be used as the sole basis for real-world marine recovery, environmental, navigation, or safety decisions.

Real-world deployment would require:

* Validated side-scan sonar datasets
* Domain-expert annotation
* Formal AI model evaluation
* Geolocation validation
* Real sonar hardware integration
* Field testing
* Safety validation
* Appropriate human oversight

---

## 🌊 SONAR-SHIELD

### Detect. Understand. Assess. Prioritize. Review. Report.

**AI-assisted underwater sonar intelligence for a structured, transparent, and human-reviewed decision-support workflow.**

```
```
