"""
maintenance_window.py

Pydantic request and response schemas for MaintenanceWindow operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MaintenanceWindowBase(BaseModel):
    """
    Shared MaintenanceWindow fields.
    """

    service_id: UUID

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: Optional[str] = None

    environment: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    maintenance_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    status: str = Field(
        default="SCHEDULED",
        min_length=1,
        max_length=50,
    )

    requested_by: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    approved_by: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    approval_notes: Optional[str] = None

    scheduled_start_at: datetime
    scheduled_end_at: datetime

    actual_start_at: Optional[datetime] = None
    actual_end_at: Optional[datetime] = None

    outage_expected: bool = False

    customer_notification_required: bool = False
    customer_notification_sent: bool = False

    cancellation_reason: Optional[str] = None

    correlation_id: Optional[UUID] = None


class MaintenanceWindowCreate(MaintenanceWindowBase):
    """
    Schema used when creating a Maintenance Window.
    """

    maintenance_number: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )


class MaintenanceWindowUpdate(BaseModel):
    """
    Schema used for partial Maintenance Window updates.
    """

    service_id: Optional[UUID] = None

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: Optional[str] = None

    environment: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    maintenance_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    status: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    requested_by: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    approved_by: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    approval_notes: Optional[str] = None

    scheduled_start_at: Optional[datetime] = None
    scheduled_end_at: Optional[datetime] = None

    actual_start_at: Optional[datetime] = None
    actual_end_at: Optional[datetime] = None

    outage_expected: Optional[bool] = None

    customer_notification_required: Optional[bool] = None
    customer_notification_sent: Optional[bool] = None

    cancellation_reason: Optional[str] = None

    correlation_id: Optional[UUID] = None


class MaintenanceWindowResponse(MaintenanceWindowBase):
    """
    Schema returned by Maintenance Window API endpoints.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    maintenance_number: str

    created_at: datetime
    updated_at: datetime