"""API routes for service performance metrics."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.service_metric_schema import (
    ServiceMetricCreate,
    ServiceMetricPage,
    ServiceMetricResponse,
    ServiceMetricSummary,
)
from app.services.service_metric_service import (
    ServiceMetricService,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["Service Metrics"],
)


@router.post(
    "/metrics",
    response_model=ServiceMetricResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_metric(
    payload: ServiceMetricCreate,
    db: Session = Depends(get_db),
):
    """Record a new performance observation."""

    return ServiceMetricService(db).create_metric(payload)


@router.get(
    "/metrics",
    response_model=ServiceMetricPage,
)
def get_metrics(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
    service_id: UUID | None = None,
    recorded_from: datetime | None = None,
    recorded_to: datetime | None = None,
    minimum_cpu: float | None = Query(
        default=None,
        ge=0.0,
        le=100.0,
    ),
    minimum_error_rate: float | None = Query(
        default=None,
        ge=0.0,
        le=100.0,
    ),
    db: Session = Depends(get_db),
):
    """Return filtered and paginated metric observations."""

    return ServiceMetricService(db).get_metrics(
        page=page,
        page_size=page_size,
        service_id=service_id,
        recorded_from=recorded_from,
        recorded_to=recorded_to,
        minimum_cpu=minimum_cpu,
        minimum_error_rate=minimum_error_rate,
    )


@router.get(
    "/metrics/summary",
    response_model=ServiceMetricSummary,
)
def get_metric_summary(
    service_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    """Return aggregate metrics for the dashboard."""

    return ServiceMetricService(db).get_summary(service_id)


@router.get(
    "/services/{service_id}/metrics",
    response_model=ServiceMetricPage,
)
def get_service_metrics(
    service_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return metric history for one registered service."""

    return ServiceMetricService(db).get_metrics(
        page=page,
        page_size=page_size,
        service_id=service_id,
        recorded_from=None,
        recorded_to=None,
        minimum_cpu=None,
        minimum_error_rate=None,
    )


@router.get(
    "/metrics/{metric_id}",
    response_model=ServiceMetricResponse,
)
def get_metric(
    metric_id: UUID,
    db: Session = Depends(get_db),
):
    """Return one metric observation."""

    return ServiceMetricService(db).get_metric(metric_id)


@router.delete(
    "/metrics/{metric_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_metric(
    metric_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete one metric observation."""

    ServiceMetricService(db).delete_metric(metric_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
