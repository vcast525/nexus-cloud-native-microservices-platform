"""API routes for API health-check records."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.api_health_schema import (
    APIHealthCreate,
    APIHealthPage,
    APIHealthResponse,
    APIHealthSummary,
)
from app.services.api_health_service import APIHealthService

router = APIRouter(
    prefix="/api/v1",
    tags=["API Health"],
)


@router.post(
    "/api-health",
    response_model=APIHealthResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_api_health_check(
    payload: APIHealthCreate,
    db: Session = Depends(get_db),
):
    """Record a new API health-check observation."""

    return APIHealthService(db).create_health_check(payload)


@router.get(
    "/api-health",
    response_model=APIHealthPage,
)
def get_api_health_checks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
    service_id: UUID | None = None,
    status_filter: str | None = Query(
        default=None,
        alias="status",
    ),
    status_code: int | None = Query(
        default=None,
        ge=100,
        le=599,
    ),
    endpoint: str | None = None,
    checked_from: datetime | None = None,
    checked_to: datetime | None = None,
    minimum_response_time_ms: float | None = Query(
        default=None,
        ge=0.0,
    ),
    db: Session = Depends(get_db),
):
    """Return filtered, paginated API health records."""

    return APIHealthService(db).get_health_checks(
        page=page,
        page_size=page_size,
        service_id=service_id,
        status_filter=status_filter,
        status_code=status_code,
        endpoint=endpoint,
        checked_from=checked_from,
        checked_to=checked_to,
        minimum_response_time_ms=minimum_response_time_ms,
    )


@router.get(
    "/api-health/summary",
    response_model=APIHealthSummary,
)
def get_api_health_summary(
    service_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    """Return API health aggregates for the dashboard."""

    return APIHealthService(db).get_summary(service_id)


@router.get(
    "/services/{service_id}/api-health",
    response_model=APIHealthPage,
)
def get_service_api_health(
    service_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return API health history for one service."""

    return APIHealthService(db).get_health_checks(
        page=page,
        page_size=page_size,
        service_id=service_id,
        status_filter=None,
        status_code=None,
        endpoint=None,
        checked_from=None,
        checked_to=None,
        minimum_response_time_ms=None,
    )


@router.get(
    "/api-health/{health_check_id}",
    response_model=APIHealthResponse,
)
def get_api_health_check(
    health_check_id: UUID,
    db: Session = Depends(get_db),
):
    """Return one API health-check record."""

    return APIHealthService(db).get_health_check(health_check_id)


@router.delete(
    "/api-health/{health_check_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_api_health_check(
    health_check_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete one API health-check record."""

    APIHealthService(db).delete_health_check(health_check_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
