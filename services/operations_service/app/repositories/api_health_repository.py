"""Repository layer for API health-check database operations."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.api_health import APIHealth


class APIHealthRepository:
    """Performs database operations for API health records."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, health_check: APIHealth) -> APIHealth:
        """Persist and return a new API health record."""

        self.db.add(health_check)
        self.db.commit()
        self.db.refresh(health_check)

        return health_check

    def get_by_id(self, health_check_id: UUID) -> APIHealth | None:
        """Return one health-check record."""

        return (
            self.db.query(APIHealth)
            .filter(APIHealth.id == health_check_id)
            .first()
        )

    def get_paginated(
        self,
        *,
        page: int,
        page_size: int,
        service_id: UUID | None = None,
        status: str | None = None,
        status_code: int | None = None,
        endpoint: str | None = None,
        checked_from: datetime | None = None,
        checked_to: datetime | None = None,
        minimum_response_time_ms: float | None = None,
    ) -> tuple[list[APIHealth], int]:
        """Return filtered API health records and total count."""

        query = self.db.query(APIHealth)

        if service_id is not None:
            query = query.filter(APIHealth.service_id == service_id)

        if status is not None:
            query = query.filter(
                func.lower(APIHealth.status) == status.lower()
            )

        if status_code is not None:
            query = query.filter(APIHealth.status_code == status_code)

        if endpoint is not None:
            query = query.filter(APIHealth.endpoint.ilike(f"%{endpoint}%"))

        if checked_from is not None:
            query = query.filter(APIHealth.checked_at >= checked_from)

        if checked_to is not None:
            query = query.filter(APIHealth.checked_at <= checked_to)

        if minimum_response_time_ms is not None:
            query = query.filter(
                APIHealth.response_time_ms >= minimum_response_time_ms
            )

        total = query.count()
        offset = (page - 1) * page_size

        records = (
            query.order_by(APIHealth.checked_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return records, total

    def get_summary(
        self,
        *,
        service_id: UUID | None = None,
    ) -> dict:
        """Return API-health aggregate statistics."""

        query = self.db.query(
            func.count(APIHealth.id),
            func.coalesce(
                func.sum(
                    case(
                        (func.lower(APIHealth.status) == "healthy", 1),
                        else_=0,
                    )
                ),
                0,
            ),
            func.coalesce(
                func.sum(
                    case(
                        (func.lower(APIHealth.status) == "degraded", 1),
                        else_=0,
                    )
                ),
                0,
            ),
            func.coalesce(
                func.sum(
                    case(
                        (func.lower(APIHealth.status) == "failed", 1),
                        else_=0,
                    )
                ),
                0,
            ),
            func.coalesce(func.avg(APIHealth.response_time_ms), 0.0),
            func.coalesce(func.min(APIHealth.response_time_ms), 0.0),
            func.coalesce(func.max(APIHealth.response_time_ms), 0.0),
            func.coalesce(
                func.avg(APIHealth.availability_percent),
                0.0,
            ),
            func.min(APIHealth.checked_at),
            func.max(APIHealth.checked_at),
        )

        if service_id is not None:
            query = query.filter(APIHealth.service_id == service_id)

        result = query.one()

        total_checks = int(result[0] or 0)
        healthy_checks = int(result[1] or 0)
        degraded_checks = int(result[2] or 0)
        failed_checks = int(result[3] or 0)

        def percentage(value: int) -> float:
            return (
                value / total_checks * 100
                if total_checks > 0
                else 0.0
            )

        return {
            "total_checks": total_checks,
            "healthy_checks": healthy_checks,
            "degraded_checks": degraded_checks,
            "failed_checks": failed_checks,
            "healthy_percent": percentage(healthy_checks),
            "degraded_percent": percentage(degraded_checks),
            "failed_percent": percentage(failed_checks),
            "average_response_time_ms": float(result[4] or 0.0),
            "minimum_response_time_ms": float(result[5] or 0.0),
            "maximum_response_time_ms": float(result[6] or 0.0),
            "average_availability_percent": float(result[7] or 0.0),
            "earliest_checked_at": result[8],
            "latest_checked_at": result[9],
        }

    def delete(self, health_check: APIHealth) -> None:
        """Delete one API health record."""

        self.db.delete(health_check)
        self.db.commit()
