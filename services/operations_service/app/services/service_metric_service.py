"""Business logic for service performance metrics."""

import math
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.service import Service
from app.models.service_metric import ServiceMetric
from app.repositories.service_metric_repository import (
    ServiceMetricRepository,
)
from app.schemas.service_metric_schema import (
    ServiceMetricCreate,
    ServiceMetricPage,
    ServiceMetricResponse,
    ServiceMetricSummary,
)


class ServiceMetricService:
    """Coordinates metric validation and database operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ServiceMetricRepository(db)

    def create_metric(
        self,
        payload: ServiceMetricCreate,
    ) -> ServiceMetric:
        """Create a metric after validating its service."""

        registered_service = (
            self.db.query(Service)
            .filter(Service.id == payload.service_id)
            .first()
        )

        if registered_service is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registered service not found.",
            )

        error_rate = (
            payload.error_count / payload.request_count * 100
            if payload.request_count > 0
            else 0.0
        )

        metric = ServiceMetric(
            service_id=payload.service_id,
            cpu_usage_percent=payload.cpu_usage_percent,
            memory_usage_percent=payload.memory_usage_percent,
            request_count=payload.request_count,
            error_count=payload.error_count,
            error_rate_percent=round(error_rate, 4),
            average_response_time_ms=(
                payload.average_response_time_ms
            ),
            recorded_at=(
                payload.recorded_at
                or datetime.now(timezone.utc)
            ),
        )

        return self.repository.create(metric)

    def get_metric(
        self,
        metric_id: UUID,
    ) -> ServiceMetric:
        """Return one metric or raise a not-found response."""

        metric = self.repository.get_by_id(metric_id)

        if metric is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service metric not found.",
            )

        return metric

    def get_metrics(
        self,
        *,
        page: int,
        page_size: int,
        service_id: UUID | None,
        recorded_from: datetime | None,
        recorded_to: datetime | None,
        minimum_cpu: float | None,
        minimum_error_rate: float | None,
    ) -> ServiceMetricPage:
        """Return a safe, paginated metric collection."""

        if (
            recorded_from is not None
            and recorded_to is not None
            and recorded_from > recorded_to
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "recorded_from cannot be later than recorded_to."
                ),
            )

        records, total = self.repository.get_paginated(
            page=page,
            page_size=page_size,
            service_id=service_id,
            recorded_from=recorded_from,
            recorded_to=recorded_to,
            minimum_cpu=minimum_cpu,
            minimum_error_rate=minimum_error_rate,
        )

        return ServiceMetricPage(
            items=[
                ServiceMetricResponse.model_validate(record)
                for record in records
            ],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(
                math.ceil(total / page_size)
                if total > 0
                else 0
            ),
        )

    def get_summary(
        self,
        service_id: UUID | None,
    ) -> ServiceMetricSummary:
        """Return dashboard-ready aggregate statistics."""

        if service_id is not None:
            registered_service = (
                self.db.query(Service)
                .filter(Service.id == service_id)
                .first()
            )

            if registered_service is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registered service not found.",
                )

        summary = self.repository.get_summary(
            service_id=service_id
        )

        for key in (
            "average_cpu_usage_percent",
            "average_memory_usage_percent",
            "average_error_rate_percent",
            "average_response_time_ms",
            "minimum_response_time_ms",
            "maximum_response_time_ms",
        ):
            summary[key] = round(summary[key], 4)

        return ServiceMetricSummary(**summary)

    def delete_metric(
        self,
        metric_id: UUID,
    ) -> None:
        """Delete one metric record."""

        metric = self.get_metric(metric_id)
        self.repository.delete(metric)
