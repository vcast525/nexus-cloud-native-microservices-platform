"""Initial operations schema

Revision ID: 7f9700c8c034
Revises:
Create Date: 2026-07-17 12:11:33.713615
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7f9700c8c034"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the Operations Service database tables."""

    op.create_table(
        "services",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("service_name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("owner", sa.String(length=150), nullable=False),
        sa.Column("business_unit", sa.String(length=150), nullable=False),
        sa.Column("environment", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=True),
        sa.Column("repository_url", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="registry",
    )

    op.create_index(
        op.f("ix_registry_services_business_unit"),
        "services",
        ["business_unit"],
        unique=False,
        schema="registry",
    )
    op.create_index(
        op.f("ix_registry_services_environment"),
        "services",
        ["environment"],
        unique=False,
        schema="registry",
    )
    op.create_index(
        op.f("ix_registry_services_service_name"),
        "services",
        ["service_name"],
        unique=True,
        schema="registry",
    )
    op.create_index(
        op.f("ix_registry_services_status"),
        "services",
        ["status"],
        unique=False,
        schema="registry",
    )

    op.create_table(
        "incidents",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("service_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(length=25), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("assigned_team", sa.String(length=150), nullable=True),
        sa.Column("correlation_id", sa.UUID(), nullable=False),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["registry.services.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="incidents",
    )

    op.create_index(
        op.f("ix_incidents_incidents_assigned_team"),
        "incidents",
        ["assigned_team"],
        unique=False,
        schema="incidents",
    )
    op.create_index(
        op.f("ix_incidents_incidents_correlation_id"),
        "incidents",
        ["correlation_id"],
        unique=False,
        schema="incidents",
    )
    op.create_index(
        op.f("ix_incidents_incidents_service_id"),
        "incidents",
        ["service_id"],
        unique=False,
        schema="incidents",
    )
    op.create_index(
        op.f("ix_incidents_incidents_severity"),
        "incidents",
        ["severity"],
        unique=False,
        schema="incidents",
    )
    op.create_index(
        op.f("ix_incidents_incidents_status"),
        "incidents",
        ["status"],
        unique=False,
        schema="incidents",
    )

    op.create_table(
        "api_health",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("service_id", sa.UUID(), nullable=False),
        sa.Column("endpoint", sa.String(length=500), nullable=False),
        sa.Column("http_method", sa.String(length=10), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("response_time_ms", sa.Float(), nullable=True),
        sa.Column("availability_percent", sa.Float(), nullable=False),
        sa.Column("checked_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["registry.services.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="registry",
    )

    op.create_index(
        op.f("ix_registry_api_health_checked_at"),
        "api_health",
        ["checked_at"],
        unique=False,
        schema="registry",
    )
    op.create_index(
        op.f("ix_registry_api_health_service_id"),
        "api_health",
        ["service_id"],
        unique=False,
        schema="registry",
    )
    op.create_index(
        op.f("ix_registry_api_health_status"),
        "api_health",
        ["status"],
        unique=False,
        schema="registry",
    )

    op.create_table(
        "service_metrics",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("service_id", sa.UUID(), nullable=False),
        sa.Column("cpu_usage_percent", sa.Float(), nullable=False),
        sa.Column("memory_usage_percent", sa.Float(), nullable=False),
        sa.Column("request_count", sa.BigInteger(), nullable=False),
        sa.Column("error_count", sa.BigInteger(), nullable=False),
        sa.Column("error_rate_percent", sa.Float(), nullable=False),
        sa.Column("average_response_time_ms", sa.Float(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["registry.services.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="registry",
    )

    op.create_index(
        op.f("ix_registry_service_metrics_recorded_at"),
        "service_metrics",
        ["recorded_at"],
        unique=False,
        schema="registry",
    )
    op.create_index(
        op.f("ix_registry_service_metrics_service_id"),
        "service_metrics",
        ["service_id"],
        unique=False,
        schema="registry",
    )


def downgrade() -> None:
    """Remove only the Operations Service database tables."""

    op.drop_index(
        op.f("ix_registry_service_metrics_service_id"),
        table_name="service_metrics",
        schema="registry",
    )
    op.drop_index(
        op.f("ix_registry_service_metrics_recorded_at"),
        table_name="service_metrics",
        schema="registry",
    )
    op.drop_table("service_metrics", schema="registry")

    op.drop_index(
        op.f("ix_registry_api_health_status"),
        table_name="api_health",
        schema="registry",
    )
    op.drop_index(
        op.f("ix_registry_api_health_service_id"),
        table_name="api_health",
        schema="registry",
    )
    op.drop_index(
        op.f("ix_registry_api_health_checked_at"),
        table_name="api_health",
        schema="registry",
    )
    op.drop_table("api_health", schema="registry")

    op.drop_index(
        op.f("ix_incidents_incidents_status"),
        table_name="incidents",
        schema="incidents",
    )
    op.drop_index(
        op.f("ix_incidents_incidents_severity"),
        table_name="incidents",
        schema="incidents",
    )
    op.drop_index(
        op.f("ix_incidents_incidents_service_id"),
        table_name="incidents",
        schema="incidents",
    )
    op.drop_index(
        op.f("ix_incidents_incidents_correlation_id"),
        table_name="incidents",
        schema="incidents",
    )
    op.drop_index(
        op.f("ix_incidents_incidents_assigned_team"),
        table_name="incidents",
        schema="incidents",
    )
    op.drop_table("incidents", schema="incidents")

    op.drop_index(
        op.f("ix_registry_services_status"),
        table_name="services",
        schema="registry",
    )
    op.drop_index(
        op.f("ix_registry_services_service_name"),
        table_name="services",
        schema="registry",
    )
    op.drop_index(
        op.f("ix_registry_services_environment"),
        table_name="services",
        schema="registry",
    )
    op.drop_index(
        op.f("ix_registry_services_business_unit"),
        table_name="services",
        schema="registry",
    )
    op.drop_table("services", schema="registry")
