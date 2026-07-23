"""
deployment.py

Pydantic request and response schemas for Deployment operations.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DeploymentBase(BaseModel):
    """
    Shared Deployment fields.
    """

    service_id: UUID
    change_id: Optional[UUID] = None
    maintenance_window_id: Optional[UUID] = None

    version: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    previous_version: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    environment: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    deployment_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    status: str = Field(
        default="PENDING",
        min_length=1,
        max_length=50,
    )

    initiated_by: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    source_branch: Optional[str] = Field(
        default=None,
        max_length=255,
    )
    commit_sha: Optional[str] = Field(
        default=None,
        max_length=255,
    )
    artifact_uri: Optional[str] = None

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = Field(
        default=None,
        ge=0,
    )

    deployment_notes: Optional[str] = None

    rollback_required: bool = False
    rollback_completed: bool = False
    rollback_reason: Optional[str] = None

    correlation_id: Optional[UUID] = None


class DeploymentCreate(DeploymentBase):
    """
    Schema used when creating a Deployment.

    deployment_number may be provided by the caller or generated
    by the service layer.
    """

    deployment_number: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )


class DeploymentUpdate(BaseModel):
    """
    Schema used for partial Deployment updates.

    Every field is optional so callers may update only the fields
    that need to change.
    """

    service_id: Optional[UUID] = None
    change_id: Optional[UUID] = None
    maintenance_window_id: Optional[UUID] = None

    version: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    previous_version: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    environment: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    deployment_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    status: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    initiated_by: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    source_branch: Optional[str] = Field(
        default=None,
        max_length=255,
    )
    commit_sha: Optional[str] = Field(
        default=None,
        max_length=255,
    )
    artifact_uri: Optional[str] = None

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = Field(
        default=None,
        ge=0,
    )

    deployment_notes: Optional[str] = None

    rollback_required: Optional[bool] = None
    rollback_completed: Optional[bool] = None
    rollback_reason: Optional[str] = None

    correlation_id: Optional[UUID] = None


class DeploymentResponse(DeploymentBase):
    """
    Schema returned by Deployment API endpoints.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    deployment_number: str

    created_at: datetime
    updated_at: datetime