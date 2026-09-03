from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.detection import Detection as DetectionModel
from app.models.image import Image as ImageModel
from app.schemas.detection import HeatmapResponse, MapPoint
from app.utils.gps import is_valid_gps

router = APIRouter(tags=["map"])


def _points_for_statuses(db: Session, exclude_rejected: bool = True):
    rows = (
        db.query(DetectionModel, ImageModel)
        .join(ImageModel, DetectionModel.image_id == ImageModel.id)
        .all()
    )
    points = []
    for det, img in rows:
        if exclude_rejected and det.status == "REJECTED":
            continue
        if not is_valid_gps(img.latitude, img.longitude):
            continue
        points.append(MapPoint(
            detection_id=det.id,
            latitude=img.latitude,
            longitude=img.longitude,
            object_type=det.object_type,
            confidence=det.confidence,
            risk_level=det.risk_level,
            priority=det.priority,
            status=det.status,
        ))
    return points


@router.get("/api/heatmap", response_model=HeatmapResponse)
def heatmap(db: Session = Depends(get_db)):
    points = _points_for_statuses(db)
    if not points:
        return HeatmapResponse(
            has_data=False,
            points=[],
            message=("No geolocated detections available. Upload sonar images with valid "
                     "latitude/longitude metadata to build the debris-density heatmap. "
                     "Coordinates are never invented."),
        )
    return HeatmapResponse(has_data=True, points=points)


@router.get("/api/map-points", response_model=HeatmapResponse)
def map_points(db: Session = Depends(get_db)):
    """All geolocated detections (including rejected) for the map view."""
    points = _points_for_statuses(db, exclude_rejected=False)
    if not points:
        return HeatmapResponse(has_data=False, points=[],
                               message="No detections with GPS coordinates yet.")
    return HeatmapResponse(has_data=True, points=points)
