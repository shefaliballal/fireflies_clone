"""
Health and readiness endpoints for load balancers and monitoring.

These routes do not touch the database by default so they stay fast and reliable
even when downstream services are degraded.
"""

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health", summary="Liveness check")
def health_check() -> dict[str, str]:
    """Return a simple OK payload to confirm the process is running."""
    return {"status": "ok"}


@router.get("/", summary="API root")
def root() -> dict[str, str]:
    """Identify the service name and version at the API root."""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
    }
