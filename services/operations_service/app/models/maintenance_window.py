"""Database model for planned service maintenance windows."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class MaintenanceWindow(Base):
    """Represents an approved period for planned service maintenance."""

    __tablename__ = "maintenance_windows"
    __table_args__ = (
        Index(
            "ix_maintenance_windows_service_schedule",
            "service_id",
            "scheduled_start_at",
        ),
        Index(
            "ix_maintenance_windows_status_schedule",
            "status",
            "scheduled_start_at",
        ),
        Index(
            "ix_maintenance_windows_environment_status",
            "environment",
            "status",
        ),
        {"schema": "operations"},
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    maintenance_number = Column(
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

    title = Column(
        String(250),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    environment = Column(
        String(50),
        nullable=False,
        index=True,
    )

    maintenance_type = Column(
        String(100),
        nullable=False,
        default="Planned",
        index=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="Scheduled",
        index=True,
    )

    requested_by = Column(
        String(150),
        nullable=True,
        index=True,
    )

    approved_by = Column(
        String(150),
        nullable=True,
        index=True,
    )

    approval_notes = Column(
        Text,
        nullable=True,
    )

    scheduled_start_at = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    scheduled_end_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    actual_start_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    actual_end_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    outage_expected = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    customer_notification_required = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    customer_notification_sent = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    cancellation_reason = Column(
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
        back_populates="maintenance_windows",
    )

    deployments = relationship(
        "Deployment",
        back_populates="maintenance_window",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self):
        return (
            f"<MaintenanceWindow("
            f"maintenance_number='{self.maintenance_number}', "
            f"status='{self.status}', "
            f"environment='{self.environment}'"
            f")>"
        )