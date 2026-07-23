from fastapi import FastAPI

from .api.v1 import api_router
from .core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="NEXUS Operations Service API",
)


@app.get(
    "/",
    tags=["Root"],
    summary="Application Health Check",
)
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
)
def health():
    return {
        "status": "healthy",
    }


app.include_router(
    api_router,
    prefix="/api/v1",
)