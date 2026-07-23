"""Pydantic schemas for service performance metrics."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ServiceMetricCreate(BaseModel):
    """Payload used to record a service metric observation."""

    service_id: UUID

    cpu_usage_percent: float = Field(
        ge=0.0,
        le=100.0,
        examples=[52.4],
    )

    memory_usage_percent: float = Field(
        ge=0.0,
        le=100.0,
        examples=[68.1],
    )

    request_count: int = Field(
        ge=0,
        examples=[12500],
    )

    error_count: int = Field(
        ge=0,
        examples=[42],
    )

    average_response_time_ms: float = Field(
        ge=0.0,
        examples=[184.7],
    )

    recorded_at: datetime | None = None

    @model_validator(mode="after")
    def validate_error_count(self):
        """Ensure errors cannot exceed the total request count."""

        if self.error_count > self.request_count:
            raise ValueError(
                "error_count cannot be greater than request_count"
            )

        return self


class ServiceMetricResponse(BaseModel):
    """Metric record returned by the Operations Service API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    service_id: UUID
    cpu_usage_percent: float
    memory_usage_percent: float
    request_count: int
    error_count: int
    error_rate_percent: float
    average_response_time_ms: float
    recorded_at: datetime


class ServiceMetricPage(BaseModel):
    """Paginated collection of service metric records."""

    items: list[ServiceMetricResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ServiceMetricSummary(BaseModel):
    """Aggregated metric summary used by dashboards."""

    total_records: int
    total_requests: int
    total_errors: int

    average_cpu_usage_percent: float
    average_memory_usage_percent: float
    average_error_rate_percent: float
    average_response_time_ms: float

    minimum_response_time_ms: float
    maximum_response_time_ms: float

    earliest_recorded_at: datetime | None
    latest_recorded_at: datetime | None
