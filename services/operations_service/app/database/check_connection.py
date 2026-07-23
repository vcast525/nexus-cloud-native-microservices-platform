"""Verify connectivity to the Operations Service PostgreSQL database."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import engine


def check_database_connection() -> None:
    """Connect to PostgreSQL and print the active database details."""

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT
                        current_database() AS database_name,
                        current_user AS database_user,
                        version() AS database_version
                    """
                )
            ).mappings().one()

            print("Operations Service database connection successful.")
            print(f"Database: {result['database_name']}")
            print(f"User: {result['database_user']}")
            print(f"Version: {result['database_version']}")

    except SQLAlchemyError as error:
        print("Operations Service database connection failed.")
        print(error)
        raise


if __name__ == "__main__":
    check_database_connection()
