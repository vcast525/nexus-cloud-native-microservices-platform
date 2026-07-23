"""
incident.py

Pydantic request and response schemas for Incident operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class IncidentBase(BaseModel):
    """
    Shared Incident fields used by create and response schemas.
    """

    incident_number: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    service_id: UUID

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: Optional[str] = None

    incident_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    severity: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    priority: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    status: str = Field(
        default="OPEN",
        min_length=1,
        max_length=50,
    )

    assigned_team: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    detected_by: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    root_cause: Optional[str] = None
    customer_impact: Optional[str] = None
    resolution_summary: Optional[str] = None

    correlation_id: Optional[UUID] = None

    started_at: Optional[datetime] = None
    detected_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    duration_minutes: Optional[int] = Field(
        default=None,
        ge=0,
    )

    sla_breached: bool = False


class IncidentCreate(IncidentBase):
    """
    Request schema used when creating an Incident.
    """

    pass


class IncidentUpdate(BaseModel):
    """
    Request schema used when updating an Incident.

    All fields are optional because updates may modify only
    selected fields.
    """

    incident_number: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    service_id: Optional[UUID] = None

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: Optional[str] = None

    incident_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    severity: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    priority: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    status: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    assigned_team: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    detected_by: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    root_cause: Optional[str] = None
    customer_impact: Optional[str] = None
    resolution_summary: Optional[str] = None

    correlation_id: Optional[UUID] = None

    started_at: Optional[datetime] = None
    detected_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    duration_minutes: Optional[int] = Field(
        default=None,
        ge=0,
    )

    sla_breached: Optional[bool] = None


class IncidentResponse(IncidentBase):
    """
    Response schema returned by Incident API endpoints.
    """

    id: UUID

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class IncidentPageResponse(BaseModel):
    """
    Paginated Incident response.

    This structure supports large datasets without returning every
    Incident record in one request.
    """

    items: list[IncidentResponse]
    page: int
    page_size: int
    total: int
    pages: int
