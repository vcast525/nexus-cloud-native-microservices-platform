"""Database model for software deployment records."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class Deployment(Base):
    """Represents a software release deployed to a managed service."""

    __tablename__ = "deployments"
    __table_args__ = (
        Index(
            "ix_deployments_service_started_at",
            "service_id",
            "started_at",
        ),
        Index(
            "ix_deployments_status_environment",
            "status",
            "environment",
        ),
        Index(
            "ix_deployments_change_id",
            "change_id",
        ),
        Index(
            "ix_deployments_maintenance_window_id",
            "maintenance_window_id",
        ),
        {"schema": "operations"},
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    deployment_number = Column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    service_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "registry.services.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    change_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "incidents.changes.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    maintenance_window_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "operations.maintenance_windows.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    version = Column(
        String(50),
        nullable=False,
        index=True,
    )

    previous_version = Column(
        String(50),
        nullable=True,
    )

    environment = Column(
        String(50),
        nullable=False,
        index=True,
    )

    deployment_type = Column(
        String(50),
        nullable=False,
        default="Automated",
        index=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="Pending",
        index=True,
    )

    initiated_by = Column(
        String(150),
        nullable=False,
        index=True,
    )

    source_branch = Column(
        String(150),
        nullable=True,
    )

    commit_sha = Column(
        String(100),
        nullable=True,
        index=True,
    )

    artifact_uri = Column(
        String(500),
        nullable=True,
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    duration_seconds = Column(
        Integer,
        nullable=True,
    )

    deployment_notes = Column(
        Text,
        nullable=True,
    )

    rollback_required = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    rollback_completed = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    rollback_reason = Column(
        Text,
        nullable=True,
    )

    correlation_id = Column(
        String(100),
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    service = relationship(
        "Service",
        back_populates="deployments",
    )

    change = relationship(
        "Change",
        back_populates="deployments",
    )

    maintenance_window = relationship(
        "MaintenanceWindow",
        back_populates="deployments",
    )

    audit_events = relationship(
        "AuditEvent",
        back_populates="deployment",
    )

    notifications = relationship(
        "Notification",
        back_populates="deployment",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self):
        return (
            f"<Deployment("
            f"deployment_number='{self.deployment_number}', "
            f"version='{self.version}', "
            f"environment='{self.environment}', "
            f"status='{self.status}'"
            f")>"
        )