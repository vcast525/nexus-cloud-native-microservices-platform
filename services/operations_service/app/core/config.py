"""Configuration settings for the NEXUS Operations Service."""

import os

class Settings:
    """Application settings loaded from environment variables."""

    APP_NAME = "NEXUS Operations Service"
    APP_VERSION = "1.0.0"

    DATABASE_URL = os.getenv(
        "OPERATIONS_DATABASE_URL",
        os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://nexus_user:nexus_local_password@localhost:5433/nexus",
        ),
    )

settings = Settings()
