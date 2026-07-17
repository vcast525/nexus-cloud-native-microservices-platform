from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.authentication_event import AuthenticationEvent
from app.models.user import User
from app.repositories.user_repository import get_user_by_username


def record_authentication_event(
    database_session: Session,
    event_type: str,
    result: str,
    user: User | None = None,
    ip_address: str | None = None,
    correlation_id: str | None = None,
) -> AuthenticationEvent:
    """Record an authentication event for security auditing."""

    authentication_event = AuthenticationEvent(
        user_id=user.id if user else None,
        event_type=event_type,
        result=result,
        ip_address=ip_address,
        correlation_id=correlation_id,
    )

    database_session.add(authentication_event)

    return authentication_event


def authenticate_user(
    database_session: Session,
    username: str,
    password: str,
    ip_address: str | None = None,
) -> User | None:
    """Authenticate an active user and record the result."""

    user = get_user_by_username(database_session, username)

    if user is None:
        record_authentication_event(
            database_session=database_session,
            event_type="LOGIN",
            result="FAILURE",
            ip_address=ip_address,
        )
        database_session.commit()
        return None

    if not user.is_active or not verify_password(password, user.password_hash):
        record_authentication_event(
            database_session=database_session,
            event_type="LOGIN",
            result="FAILURE",
            user=user,
            ip_address=ip_address,
        )
        database_session.commit()
        return None

    user.last_login_at = datetime.now(timezone.utc)

    record_authentication_event(
        database_session=database_session,
        event_type="LOGIN",
        result="SUCCESS",
        user=user,
        ip_address=ip_address,
    )

    database_session.commit()
    database_session.refresh(user)

    return user
