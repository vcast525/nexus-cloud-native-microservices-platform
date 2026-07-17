import os

from sqlalchemy import select

from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models.role import Role
from app.models.user import User


ADMIN_USERNAME = os.getenv("NEXUS_ADMIN_USERNAME", "vincent")
ADMIN_EMAIL = os.getenv("NEXUS_ADMIN_EMAIL", "vincent@nexus.example.com")
ADMIN_PASSWORD = os.getenv("NEXUS_ADMIN_PASSWORD", "NexusAdmin123!")
ADMIN_FIRST_NAME = os.getenv("NEXUS_ADMIN_FIRST_NAME", "Vincent")
ADMIN_LAST_NAME = os.getenv("NEXUS_ADMIN_LAST_NAME", "Castillo")
ADMIN_ROLE_NAME = "Platform Administrator"


def seed_administrator() -> None:
    """Create the initial local NEXUS platform administrator."""

    with SessionLocal() as database_session:
        existing_user = database_session.scalar(
            select(User).where(User.username == ADMIN_USERNAME)
        )

        if existing_user:
            print()
            print("NEXUS administrator already exists.")
            print(f"Username: {existing_user.username}")
            print(f"Email: {existing_user.email}")
            return

        administrator_role = database_session.scalar(
            select(Role).where(Role.name == ADMIN_ROLE_NAME)
        )

        if administrator_role is None:
            raise RuntimeError(
                "Platform Administrator role was not found. "
                "Run python seed_roles.py first."
            )

        administrator = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            first_name=ADMIN_FIRST_NAME,
            last_name=ADMIN_LAST_NAME,
            role_id=administrator_role.id,
            is_active=True,
        )

        database_session.add(administrator)
        database_session.commit()
        database_session.refresh(administrator)

        print()
        print("NEXUS administrator created successfully.")
        print(f"Username: {ADMIN_USERNAME}")
        print(f"Email: {ADMIN_EMAIL}")
        print(f"Temporary local password: {ADMIN_PASSWORD}")
        print(f"Role: {ADMIN_ROLE_NAME}")


if __name__ == "__main__":
    seed_administrator()
