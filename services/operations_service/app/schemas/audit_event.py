"""
audit_event.py

Pydantic request and response schemas for AuditEvent operations.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuditEventBase(BaseModel):
    """
    Shared AuditEvent fields.
    """

    service_id: Optional[UUID] = None
    incident_id: Optional[UUID] = None
    change_id: Optional[UUID] = None
    deployment_id: Optional[UUID] = None

    event_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    action: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    entity_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    entity_id: Optional[UUID] = None

    actor_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    actor_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    source_service: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    outcome: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    description: Optional[str] = None

    ip_address: Optional[str] = Field(
        default=None,
        max_length=45,
    )

    correlation_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    event_data: Optional[Dict[str, Any]] = None

    occurred_at: Optional[datetime] = None

class AuditEventCreate(AuditEventBase):
    """
    Schema used when creating an AuditEvent.
    """

    audit_number: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )


class AuditEventUpdate(BaseModel):
    """
    Schema used for partial AuditEvent updates.
    """

    service_id: Optional[UUID] = None
    incident_id: Optional[UUID] = None
    change_id: Optional[UUID] = None
    deployment_id: Optional[UUID] = None

    event_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    action: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    entity_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    entity_id: Optional[UUID] = None

    actor_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    actor_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    source_service: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    outcome: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    description: Optional[str] = None

    ip_address: Optional[str] = Field(
        default=None,
        max_length=45,
    )

    correlation_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    event_data: Optional[Dict[str, Any]] = None

    occurred_at: Optional[datetime] = None


class AuditEventResponse(AuditEventBase):
    """
    Schema returned by AuditEvent API endpoints.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    audit_number: str
    created_at: datetime