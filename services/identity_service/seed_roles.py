"""Seed the identity.roles table with the default NEXUS roles."""

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import SessionLocal
from app.models.role import Role


DEFAULT_ROLES = [
    {
        "name": "Platform Administrator",
        "description": "Full access to users, services, incidents, analytics, and platform settings.",
    },
    {
        "name": "Service Owner",
        "description": "Manages assigned services and reviews their operational health and incidents.",
    },
    {
        "name": "Operations Analyst",
        "description": "Monitors enterprise operations, investigates incidents, and reviews analytics.",
    },
    {
        "name": "Viewer",
        "description": "Has read-only access to approved dashboards and operational information.",
    },
]


def seed_roles() -> None:
    """Insert default roles without creating duplicates."""

    with SessionLocal() as session:
        try:
            created_count = 0

            for role_data in DEFAULT_ROLES:
                existing_role = session.scalar(
                    select(Role).where(Role.name == role_data["name"])
                )

                if existing_role:
                    print(f"Already exists: {role_data['name']}")
                    continue

                session.add(Role(**role_data))
                created_count += 1

            session.commit()

            print()
            print("NEXUS role seeding complete.")
            print(f"New roles created: {created_count}")

        except SQLAlchemyError as error:
            session.rollback()
            print(f"Role seeding failed: {error}")
            raise


if __name__ == "__main__":
    seed_roles()