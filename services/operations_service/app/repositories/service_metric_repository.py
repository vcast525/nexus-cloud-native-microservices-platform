"""Repository layer for service metric database operations."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.service_metric import ServiceMetric


class ServiceMetricRepository:
    """Performs database operations for service metric records."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        metric: ServiceMetric,
    ) -> ServiceMetric:
        """Persist and return a new metric record."""

        self.db.add(metric)
        self.db.commit()
        self.db.refresh(metric)

        return metric

    def get_by_id(
        self,
        metric_id: UUID,
    ) -> ServiceMetric | None:
        """Return one metric record by identifier."""

        return (
            self.db.query(ServiceMetric)
            .filter(ServiceMetric.id == metric_id)
            .first()
        )

    def get_paginated(
        self,
        *,
        page: int,
        page_size: int,
        service_id: UUID | None = None,
        recorded_from: datetime | None = None,
        recorded_to: datetime | None = None,
        minimum_cpu: float | None = None,
        minimum_error_rate: float | None = None,
    ) -> tuple[list[ServiceMetric], int]:
        """Return filtered metrics and the total matching count."""

        query = self.db.query(ServiceMetric)

        if service_id is not None:
            query = query.filter(
                ServiceMetric.service_id == service_id
            )

        if recorded_from is not None:
            query = query.filter(
                ServiceMetric.recorded_at >= recorded_from
            )

        if recorded_to is not None:
            query = query.filter(
                ServiceMetric.recorded_at <= recorded_to
            )

        if minimum_cpu is not None:
            query = query.filter(
                ServiceMetric.cpu_usage_percent >= minimum_cpu
            )

        if minimum_error_rate is not None:
            query = query.filter(
                ServiceMetric.error_rate_percent
                >= minimum_error_rate
            )

        total = query.count()
        offset = (page - 1) * page_size

        records = (
            query.order_by(ServiceMetric.recorded_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return records, total

    def get_service_metrics(
        self,
        *,
        service_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[ServiceMetric], int]:
        """Return paginated metric history for one service."""

        return self.get_paginated(
            page=page,
            page_size=page_size,
            service_id=service_id,
        )

    def get_summary(
        self,
        *,
        service_id: UUID | None = None,
    ) -> dict:
        """Return aggregate statistics for all or one service."""

        query = self.db.query(
            func.count(ServiceMetric.id),
            func.coalesce(func.sum(ServiceMetric.request_count), 0),
            func.coalesce(func.sum(ServiceMetric.error_count), 0),
            func.coalesce(
                func.avg(ServiceMetric.cpu_usage_percent),
                0.0,
            ),
            func.coalesce(
                func.avg(ServiceMetric.memory_usage_percent),
                0.0,
            ),
            func.coalesce(
                func.avg(ServiceMetric.error_rate_percent),
                0.0,
            ),
            func.coalesce(
                func.avg(ServiceMetric.average_response_time_ms),
                0.0,
            ),
            func.coalesce(
                func.min(ServiceMetric.average_response_time_ms),
                0.0,
            ),
            func.coalesce(
                func.max(ServiceMetric.average_response_time_ms),
                0.0,
            ),
            func.min(ServiceMetric.recorded_at),
            func.max(ServiceMetric.recorded_at),
        )

        if service_id is not None:
            query = query.filter(
                ServiceMetric.service_id == service_id
            )

        result = query.one()

        return {
            "total_records": int(result[0] or 0),
            "total_requests": int(result[1] or 0),
            "total_errors": int(result[2] or 0),
            "average_cpu_usage_percent": float(result[3] or 0.0),
            "average_memory_usage_percent": float(result[4] or 0.0),
            "average_error_rate_percent": float(result[5] or 0.0),
            "average_response_time_ms": float(result[6] or 0.0),
            "minimum_response_time_ms": float(result[7] or 0.0),
            "maximum_response_time_ms": float(result[8] or 0.0),
            "earliest_recorded_at": result[9],
            "latest_recorded_at": result[10],
        }

    def delete(
        self,
        metric: ServiceMetric,
    ) -> None:
        """Delete a metric record."""

        self.db.delete(metric)
        self.db.commit()
