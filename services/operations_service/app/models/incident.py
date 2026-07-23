"""Database model for operational incidents."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class Incident(Base):
    """Represents an operational incident affecting a registered service."""

    __tablename__ = "incidents"
    __table_args__ = (
        Index(
            "ix_incidents_service_started",
            "service_id",
            "started_at",
        ),
        Index(
            "ix_incidents_status_severity",
            "status",
            "severity",
        ),
        Index(
            "ix_incidents_priority_status",
            "priority",
            "status",
        ),
        {"schema": "incidents"},
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    incident_number = Column(
        String(20),
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

    incident_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    severity = Column(
        String(25),
        nullable=False,
        index=True,
    )

    priority = Column(
        String(10),
        nullable=False,
        index=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="Open",
        index=True,
    )

    assigned_team = Column(
        String(150),
        nullable=True,
        index=True,
    )

    detected_by = Column(
        String(150),
        nullable=True,
    )

    root_cause = Column(
        Text,
        nullable=True,
    )

    customer_impact = Column(
        Text,
        nullable=True,
    )

    resolution_summary = Column(
        Text,
        nullable=True,
    )

    correlation_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        index=True,
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    detected_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    acknowledged_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    duration_minutes = Column(
        Integer,
        nullable=True,
    )

    sla_breached = Column(
        Boolean,
        nullable=False,
        default=False,
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

    service = relationship(
        "Service",
        back_populates="incidents",
    )

    issues = relationship(
        "Issue",
        back_populates="incident",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<Incident("
            f"incident_number='{self.incident_number}', "
            f"severity='{self.severity}', "
            f"priority='{self.priority}', "
            f"status='{self.status}'"
            f")>"
        )