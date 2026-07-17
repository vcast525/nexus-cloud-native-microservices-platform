import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, decode_access_token
from app.database.session import get_database_session
from app.models.user import User
from app.repositories.user_repository import get_user_by_id
from app.schemas.auth import (
    AuthenticationStatusResponse,
    TokenResponse,
    UserResponse,
)
from app.services.authentication_service import authenticate_user


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    database_session: Annotated[Session, Depends(get_database_session)],
) -> User:
    """Resolve and validate the user represented by a JWT token."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication credentials are invalid or expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_payload = decode_access_token(token)
        user_id = uuid.UUID(token_payload["sub"])
    except (ValueError, KeyError):
        raise credentials_exception

    user = get_user_by_id(database_session, user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate a NEXUS user",
)
def login(
    request: Request,
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    database_session: Annotated[Session, Depends(get_database_session)],
) -> TokenResponse:
    """Validate credentials and return a JWT access token."""

    ip_address = request.client.host if request.client else None

    user = authenticate_user(
        database_session=database_session,
        username=login_form.username,
        password=login_form.password,
        ip_address=ip_address,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=str(user.id),
        additional_claims={
            "username": user.username,
            "role": user.role.name,
        },
    )

    return TokenResponse(
        access_token=access_token,
        expires_in_minutes=settings.access_token_expire_minutes,
    )


@router.get(
    "/me",
    response_model=AuthenticationStatusResponse,
    summary="Return the authenticated user",
)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> AuthenticationStatusResponse:
    """Return the user represented by the supplied JWT token."""

    return AuthenticationStatusResponse(
        authenticated=True,
        user=UserResponse.model_validate(current_user),
    )
