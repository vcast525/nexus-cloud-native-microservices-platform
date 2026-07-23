"""Pydantic schemas for API health-check records."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class APIHealthCreate(BaseModel):
    """Payload used to record an API health check."""

    service_id: UUID
    endpoint: str = Field(min_length=1, max_length=500)
    http_method: str = Field(default="GET", min_length=1, max_length=10)
    status: str = Field(min_length=1, max_length=50)
    status_code: int | None = Field(default=None, ge=100, le=599)
    response_time_ms: float | None = Field(default=None, ge=0.0)
    availability_percent: float = Field(default=100.0, ge=0.0, le=100.0)
    checked_at: datetime | None = None


class APIHealthResponse(BaseModel):
    """API health record returned by the Operations Service."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    service_id: UUID
    endpoint: str
    http_method: str
    status: str
    status_code: int | None
    response_time_ms: float | None
    availability_percent: float
    checked_at: datetime


class APIHealthPage(BaseModel):
    """Paginated collection of API health records."""

    items: list[APIHealthResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class APIHealthSummary(BaseModel):
    """Dashboard-ready API health aggregates."""

    total_checks: int
    healthy_checks: int
    degraded_checks: int
    failed_checks: int

    healthy_percent: float
    degraded_percent: float
    failed_percent: float

    average_response_time_ms: float
    minimum_response_time_ms: float
    maximum_response_time_ms: float
    average_availability_percent: float

    earliest_checked_at: datetime | None
    latest_checked_at: datetime | None
