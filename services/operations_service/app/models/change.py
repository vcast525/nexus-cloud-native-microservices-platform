"""Database model for production change-management records."""

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


class Change(Base):
    """Represents a controlled modification to a production service."""

    __tablename__ = "changes"
    __table_args__ = (
        Index(
            "ix_changes_service_planned_start",
            "service_id",
            "planned_start_at",
        ),
        Index(
            "ix_changes_status_risk_level",
            "status",
            "risk_level",
        ),
        Index(
            "ix_changes_approval_status",
            "approval_status",
            "status",
        ),
        Index(
            "ix_changes_issue_id",
            "issue_id",
        ),
        {"schema": "incidents"},
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    change_number = Column(
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

    issue_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "incidents.issues.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    title = Column(
        String(250),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    change_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    change_category = Column(
        String(100),
        nullable=False,
        index=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="Draft",
        index=True,
    )

    approval_status = Column(
        String(50),
        nullable=False,
        default="Pending",
        index=True,
    )

    risk_level = Column(
        String(25),
        nullable=False,
        default="Medium",
        index=True,
    )

    business_justification = Column(
        Text,
        nullable=True,
    )

    implementation_plan = Column(
        Text,
        nullable=True,
    )

    validation_plan = Column(
        Text,
        nullable=True,
    )

    rollback_plan = Column(
        Text,
        nullable=True,
    )

    implementation_team = Column(
        String(150),
        nullable=True,
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

    planned_start_at = Column(
        DateTime,
        nullable=True,
        index=True,
    )

    planned_end_at = Column(
        DateTime,
        nullable=True,
    )

    actual_start_at = Column(
        DateTime,
        nullable=True,
    )

    actual_end_at = Column(
        DateTime,
        nullable=True,
    )

    outage_required = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    outage_duration_minutes = Column(
        String(10),
        nullable=True,
    )

    implementation_successful = Column(
        Boolean,
        nullable=False,
        default=False,
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

    post_implementation_review = Column(
        Text,
        nullable=True,
    )

    customer_notification_sent = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    emergency_change = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    correlation_id = Column(
        String(100),
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    service = relationship(
        "Service",
        back_populates="changes",
    )

    issue = relationship(
        "Issue",
        back_populates="changes",
    )

    deployments = relationship(
        "Deployment",
        back_populates="change",
    )

    audit_events = relationship(
        "AuditEvent",
        back_populates="change",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self):
        return (
            f"<Change("
            f"change_number='{self.change_number}', "
            f"status='{self.status}', "
            f"risk_level='{self.risk_level}'"
            f")>"
        )