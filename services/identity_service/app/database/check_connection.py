from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import engine


def check_database_connection() -> None:
    """Verify PostgreSQL connectivity and display available NEXUS schemas."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        inspector = inspect(engine)
        schemas = inspector.get_schema_names()

        nexus_schemas = [
            schema
            for schema in schemas
            if schema
            in {
                "identity",
                "registry",
                "incidents",
                "notifications",
                "audit",
            }
        ]

        print("Database connection successful.")
        print("Available NEXUS schemas:")

        for schema in sorted(nexus_schemas):
            print(f"- {schema}")

    except SQLAlchemyError as error:
        print("Database connection failed.")
        print(f"Reason: {error}")
        raise


if __name__ == "__main__":
    check_database_connection()