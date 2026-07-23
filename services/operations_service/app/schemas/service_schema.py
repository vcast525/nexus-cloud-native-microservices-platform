"""Pydantic schemas for the Service Registry."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ServiceResponse(BaseModel):
    """Returned when reading a registered service."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    service_name: str
    description: str | None
    owner: str
    business_unit: str
    environment: str
    status: str
    version: str | None
    repository_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime