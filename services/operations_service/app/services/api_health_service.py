"""Business logic for API health-check records."""

import math
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.api_health import APIHealth
from app.models.service import Service
from app.repositories.api_health_repository import APIHealthRepository
from app.schemas.api_health_schema import (
    APIHealthCreate,
    APIHealthPage,
    APIHealthResponse,
    APIHealthSummary,
)


class APIHealthService:
    """Coordinates API health validation and persistence."""

    VALID_STATUSES = {"healthy", "degraded", "failed"}

    def __init__(self, db: Session):
        self.db = db
        self.repository = APIHealthRepository(db)

    def _require_service(self, service_id: UUID) -> Service:
        """Return a registered service or raise 404."""

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

        return registered_service

    def create_health_check(
        self,
        payload: APIHealthCreate,
    ) -> APIHealth:
        """Create a validated API health-check record."""

        self._require_service(payload.service_id)

        normalized_status = payload.status.lower()

        if normalized_status not in self.VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "status must be healthy, degraded, or failed."
                ),
            )

        health_check = APIHealth(
            service_id=payload.service_id,
            endpoint=payload.endpoint,
            http_method=payload.http_method.upper(),
            status=normalized_status,
            status_code=payload.status_code,
            response_time_ms=payload.response_time_ms,
            availability_percent=payload.availability_percent,
            checked_at=payload.checked_at or datetime.now(timezone.utc),
        )

        return self.repository.create(health_check)

    def get_health_check(self, health_check_id: UUID) -> APIHealth:
        """Return one health-check record or raise 404."""

        health_check = self.repository.get_by_id(health_check_id)

        if health_check is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API health-check record not found.",
            )

        return health_check

    def get_health_checks(
        self,
        *,
        page: int,
        page_size: int,
        service_id: UUID | None,
        status_filter: str | None,
        status_code: int | None,
        endpoint: str | None,
        checked_from: datetime | None,
        checked_to: datetime | None,
        minimum_response_time_ms: float | None,
    ) -> APIHealthPage:
        """Return filtered and paginated API health records."""

        if (
            checked_from is not None
            and checked_to is not None
            and checked_from > checked_to
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="checked_from cannot be later than checked_to.",
            )

        if (
            status_filter is not None
            and status_filter.lower() not in self.VALID_STATUSES
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "status must be healthy, degraded, or failed."
                ),
            )

        records, total = self.repository.get_paginated(
            page=page,
            page_size=page_size,
            service_id=service_id,
            status=status_filter,
            status_code=status_code,
            endpoint=endpoint,
            checked_from=checked_from,
            checked_to=checked_to,
            minimum_response_time_ms=minimum_response_time_ms,
        )

        return APIHealthPage(
            items=[
                APIHealthResponse.model_validate(record)
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
    ) -> APIHealthSummary:
        """Return dashboard-ready API health aggregates."""

        if service_id is not None:
            self._require_service(service_id)

        summary = self.repository.get_summary(
            service_id=service_id
        )

        for key in (
            "healthy_percent",
            "degraded_percent",
            "failed_percent",
            "average_response_time_ms",
            "minimum_response_time_ms",
            "maximum_response_time_ms",
            "average_availability_percent",
        ):
            summary[key] = round(summary[key], 4)

        return APIHealthSummary(**summary)

    def delete_health_check(self, health_check_id: UUID) -> None:
        """Delete one API health-check record."""

        health_check = self.get_health_check(health_check_id)
        self.repository.delete(health_check)
