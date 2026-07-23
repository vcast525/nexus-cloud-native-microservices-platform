"""
issue.py

Pydantic request and response schemas for Issue operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class IssueBase(BaseModel):
    """
    Shared fields used by Issue creation and response schemas.
    """

    issue_number: str = Field(
        ...,
        min_length=1,
        max_length=20,
    )

    service_id: UUID

    incident_id: Optional[UUID] = None

    title: str = Field(
        ...,
        min_length=1,
        max_length=250,
    )

    description: Optional[str] = None

    issue_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    severity: str = Field(
        ...,
        min_length=1,
        max_length=25,
    )

    priority: str = Field(
        ...,
        min_length=1,
        max_length=10,
    )

    status: str = Field(
        default="Open",
        min_length=1,
        max_length=50,
    )

    assigned_team: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    owner: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    remediation_plan: Optional[str] = None

    estimated_effort_hours: Optional[float] = Field(
        default=None,
        ge=0,
    )

    actual_effort_hours: Optional[float] = Field(
        default=None,
        ge=0,
    )

    target_resolution_date: Optional[datetime] = None
    actual_resolution_date: Optional[datetime] = None

    overdue: bool = False

    correlation_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )


class IssueCreate(IssueBase):
    """
    Request schema used when creating an Issue.
    """

    pass


class IssueUpdate(BaseModel):
    """
    Request schema used when partially updating an Issue.

    Every field is optional because a PATCH request may update only
    selected Issue fields.
    """

    issue_number: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    service_id: Optional[UUID] = None
    incident_id: Optional[UUID] = None

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=250,
    )

    description: Optional[str] = None

    issue_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    severity: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=25,
    )

    priority: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=10,
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

    owner: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    remediation_plan: Optional[str] = None

    estimated_effort_hours: Optional[float] = Field(
        default=None,
        ge=0,
    )

    actual_effort_hours: Optional[float] = Field(
        default=None,
        ge=0,
    )

    target_resolution_date: Optional[datetime] = None
    actual_resolution_date: Optional[datetime] = None

    overdue: Optional[bool] = None

    correlation_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )


class IssueResponse(IssueBase):
    """
    Response schema returned by Issue API endpoints.
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class IssuePageResponse(BaseModel):
    """
    Paginated Issue response.
    """

    items: list[IssueResponse]
    page: int
    page_size: int
    total: int
    pages: int
