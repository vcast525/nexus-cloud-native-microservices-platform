"""
notification.py

Pydantic request and response schemas for Notification operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NotificationBase(BaseModel):
    """
    Shared Notification fields.
    """

    service_id: Optional[UUID] = None
    incident_id: Optional[UUID] = None
    deployment_id: Optional[UUID] = None
    audit_event_id: Optional[UUID] = None

    notification_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    channel: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    recipient: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    subject: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    message: str = Field(
        ...,
        min_length=1,
    )

    priority: str = Field(
        default="NORMAL",
        min_length=1,
        max_length=50,
    )

    status: str = Field(
        default="PENDING",
        min_length=1,
        max_length=50,
    )

    retry_count: int = Field(
        default=0,
        ge=0,
    )

    max_retries: int = Field(
        default=3,
        ge=0,
    )

    scheduled_at: Optional[datetime] = None
    processing_started_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None

    failure_reason: Optional[str] = None

    correlation_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )

class NotificationCreate(NotificationBase):
    """
    Schema used when creating a Notification.
    """

    notification_number: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )


class NotificationUpdate(BaseModel):
    """
    Schema used for partial Notification updates.
    """

    service_id: Optional[UUID] = None
    incident_id: Optional[UUID] = None
    deployment_id: Optional[UUID] = None
    audit_event_id: Optional[UUID] = None

    notification_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    channel: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    recipient: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    subject: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    message: Optional[str] = Field(
        default=None,
        min_length=1,
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

    retry_count: Optional[int] = Field(
        default=None,
        ge=0,
    )

    max_retries: Optional[int] = Field(
        default=None,
        ge=0,
    )

    scheduled_at: Optional[datetime] = None
    processing_started_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None

    failure_reason: Optional[str] = None

    correlation_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )

class NotificationResponse(NotificationBase):
    """
    Schema returned by Notification API endpoints.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    notification_number: str

    created_at: datetime
    updated_at: datetime