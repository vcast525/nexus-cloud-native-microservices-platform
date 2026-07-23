"""Alembic migration environment for the Operations Service."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.database.base import Base

import app.models  # noqa: F401


config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("%", "%%"),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

OPERATIONS_SCHEMAS = {
    "registry",
    "incidents",
    "operations",
}

def include_name(name, type_, parent_names):
    """
    Restrict Alembic autogeneration to schemas owned by the
    Operations Service.
    """

    if type_ == "schema":
        return name in OPERATIONS_SCHEMAS

    if type_ == "table":
        schema_name = parent_names.get("schema_name")
        return schema_name in OPERATIONS_SCHEMAS

    return True


def run_migrations_offline() -> None:
    """Run migrations without creating a live database connection."""

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a live SQLAlchemy database connection."""

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {},
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()