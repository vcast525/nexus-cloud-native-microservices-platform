from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """Create a secure bcrypt hash for a plaintext password."""

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode("utf-8")


def verify_password(plaintext_password: str, password_hash: str) -> bool:
    """Compare a plaintext password with a stored bcrypt hash."""

    return bcrypt.checkpw(
        plaintext_password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


def create_access_token(
    subject: str,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed JWT access token."""

    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    token_payload: dict[str, Any] = {
        "sub": subject,
        "exp": expiration_time,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    if additional_claims:
        token_payload.update(additional_claims)

    return jwt.encode(
        token_payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token."""

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as error:
        raise ValueError("Invalid or expired access token.") from error

    if payload.get("type") != "access":
        raise ValueError("Invalid token type.")

    if not payload.get("sub"):
        raise ValueError("Token subject is missing.")

    return payload
