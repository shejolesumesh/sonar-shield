from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import detections, feedback, health, heatmap, images, model, reports, upload
from app.config import settings
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.ensure_dirs()
    init_db()
    yield


app = FastAPI(
    title="SONAR-SHIELD",
    description=(
        "Underwater side-scan sonar intelligence and marine-debris decision-support system. "
        "Prototype risk scores are NOT scientifically validated. GhostVision ONNX uses demo fallback only if unavailable."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {type(exc).__name__}"},
    )


app.include_router(health.router)
app.include_router(upload.router)
app.include_router(images.router)
app.include_router(detections.router)
app.include_router(heatmap.router)
app.include_router(feedback.router)
app.include_router(model.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "name": "SONAR-SHIELD",
        "docs": "/docs",
        "mode_note": "GhostVision ONNX is active when model assets load; otherwise the DEMO DETECTOR is used with a visible reason.",
    }
