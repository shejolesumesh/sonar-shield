import csv
import io
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.detection import Detection as DetectionModel
from app.models.image import Image as ImageModel
from app.schemas.report import ReportMeta, ReportRow

DISCLAIMER = ("PROTOTYPE RISK SCORES from a decision-support prototype. Demo detector "
              "outputs are not scientifically validated.")

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _rows(db: Session) -> list:
    out = []
    for det, img in (
        db.query(DetectionModel, ImageModel)
        .join(ImageModel, DetectionModel.image_id == ImageModel.id)
        .all()
    ):
        expert_status = det.status
        latest_fb = max(det.feedback_items, key=lambda f: f.created_at, default=None)
        if latest_fb:
            expert_status = f"{det.status} ({latest_fb.action})"
        out.append(ReportRow(
            detection_id=det.id,
            object_type=det.object_type,
            confidence=det.confidence,
            risk_level=det.risk_level,
            risk_score=det.risk_score,
            priority=det.priority,
            latitude=img.latitude,
            longitude=img.longitude,
            timestamp=img.timestamp or str(img.created_at),
            model_version=det.model_version,
            expert_status=expert_status,
        ))
    return out


def _meta(fmt: str, total: int) -> dict:
    return ReportMeta(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        disclaimer=DISCLAIMER,
        total_rows=total,
        format=fmt,
    ).model_dump()


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    rows = _rows(db)
    meta = _meta("csv", len(rows))
    buf = io.StringIO()
    buf.write(f"# {meta['disclaimer']}\n")
    buf.write(f"# generated_at_utc={meta['generated_at_utc']}\n")
    writer = csv.writer(buf)
    writer.writerow(list(ReportRow.model_fields.keys()))
    for r in rows:
        writer.writerow([getattr(r, k) for k in ReportRow.model_fields.keys()])
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sonar_shield_report.csv"},
    )


@router.get("/export/json")
def export_json(db: Session = Depends(get_db)):
    rows = _rows(db)
    payload = {"meta": _meta("json", len(rows)), "rows": [r.model_dump() for r in rows]}
    return StreamingResponse(
        iter([json.dumps(payload, indent=2)]),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=sonar_shield_report.json"},
    )


@router.get("/summary")
def report_summary(db: Session = Depends(get_db)):
    rows = _rows(db)
    by_level = {}
    by_priority = {}
    unknown_count = 0
    reviewed = 0
    for r in rows:
        by_level[r.risk_level] = by_level.get(r.risk_level, 0) + 1
        by_priority[r.priority] = by_priority.get(r.priority, 0) + 1
        if "ANOMALY" in r.object_type.upper():
            unknown_count += 1
        if r.expert_status != "PENDING":
            reviewed += 1
    return {
        **_meta("summary", len(rows)),
        "by_risk_level": by_level,
        "by_priority": {f"P{k}": v for k, v in sorted(by_priority.items())},
        "unknown_anomalies": unknown_count,
        "reviewed": reviewed,
    }
