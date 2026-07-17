import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class TokenResponse(BaseModel):
    """Response returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class RoleResponse(BaseModel):
    """Public representation of a NEXUS role."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None


class UserResponse(BaseModel):
    """Safe public representation of a NEXUS user."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime
    role: RoleResponse


class AuthenticationStatusResponse(BaseModel):
    """Simple authentication status response."""

    authenticated: bool
    user: UserResponse
