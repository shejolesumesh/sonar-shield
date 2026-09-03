# SONAR-SHIELD

> End-to-end underwater side-scan sonar intelligence and marine-debris decision-support system.

## Overview

SONAR-SHIELD ingests side-scan sonar imagery with optional GPS/depth metadata, preprocesses the imagery, runs AI object detection through a pluggable detector layer, produces Evidence Cards, computes a transparent **PROTOTYPE RISK SCORE**, assigns recovery priority (P1-P4), and presents the results through a professional web dashboard with interactive mapping, heatmaps, expert review, and reporting.

> **Prototype Notice:** SONAR-SHIELD is a decision-support prototype. The currently integrated GhostVision ONNX model is a **single-class Crab-Pot detector** when its supplied model assets are available. A clearly labeled **DEMO DETECTOR** is also available for development and UI testing when the real model is unavailable or explicitly configured.
>
> Demo outputs and prototype risk scores are not scientifically validated. Real-world deployment would require validated side-scan sonar datasets, domain-expert annotation, real hardware integration, geolocation calibration, field testing, and formal benchmarking.

## Architecture

```text
Side-scan sonar image + metadata
                ↓
           Ingestion
                ↓
         Preprocessing
                ↓
       AI Detection Engine
                ↓
   Confidence & Evidence Engine
                ↓
           Risk Engine
                ↓
        Priority Engine
                ↓
         SQLite Database
                ↓
        FastAPI REST API
                ↓
        React Dashboard
       ↙       ↓       ↘
    Map    Heatmap    Reports
                ↓
        Expert Review
                ↓
        Human Feedback
                ↓
    Future Dataset / Retraining