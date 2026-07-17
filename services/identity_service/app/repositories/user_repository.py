import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.user import User


def get_user_by_username(
    database_session: Session,
    username: str,
) -> User | None:
    """Retrieve a user and their role by username."""

    statement = (
        select(User)
        .options(joinedload(User.role))
        .where(User.username == username)
    )

    return database_session.scalar(statement)


def get_user_by_id(
    database_session: Session,
    user_id: uuid.UUID,
) -> User | None:
    """Retrieve a user and their role by ID."""

    statement = (
        select(User)
        .options(joinedload(User.role))
        .where(User.id == user_id)
    )

    return database_session.scalar(statement)
