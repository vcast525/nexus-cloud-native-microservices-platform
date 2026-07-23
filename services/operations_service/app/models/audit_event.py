"""Database model for platform audit events."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class AuditEvent(Base):
    """Records an auditable action or event occurring within NEXUS."""

    __tablename__ = "audit_events"
    __table_args__ = (
        Index(
            "ix_audit_events_event_type_occurred_at",
            "event_type",
            "occurred_at",
        ),
        Index(
            "ix_audit_events_entity",
            "entity_type",
            "entity_id",
        ),
        Index(
            "ix_audit_events_actor_occurred_at",
            "actor_name",
            "occurred_at",
        ),
        Index(
            "ix_audit_events_correlation_id",
            "correlation_id",
        ),
        {"schema": "operations"},
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    audit_number = Column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    service_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "registry.services.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    incident_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "incidents.incidents.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    change_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "incidents.changes.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    deployment_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "operations.deployments.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    event_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    action = Column(
        String(150),
        nullable=False,
        index=True,
    )

    entity_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_id = Column(
        UUID(as_uuid=True),
        nullable=True,
    )

    actor_name = Column(
        String(150),
        nullable=True,
        index=True,
    )

    actor_type = Column(
        String(50),
        nullable=False,
        default="User",
        index=True,
    )

    source_service = Column(
        String(150),
        nullable=True,
        index=True,
    )

    outcome = Column(
        String(50),
        nullable=False,
        default="Success",
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    ip_address = Column(
        String(50),
        nullable=True,
    )

    correlation_id = Column(
        String(100),
        nullable=True,
    )

    event_data = Column(
        JSONB,
        nullable=True,
    )

    occurred_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    service = relationship(
        "Service",
        back_populates="audit_events",
    )

    incident = relationship(
        "Incident",
    )

    change = relationship(
        "Change",
        back_populates="audit_events",
    )

    deployment = relationship(
        "Deployment",
        back_populates="audit_events",
    )

    notifications = relationship(
        "Notification",
        back_populates="audit_event",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self):
        return (
            f"<AuditEvent("
            f"audit_number='{self.audit_number}', "
            f"event_type='{self.event_type}', "
            f"action='{self.action}', "
            f"outcome='{self.outcome}'"
            f")>"
        )