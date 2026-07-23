"""Database model for engineering issue reports."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class Issue(Base):
    """Represents engineering work identified through incidents or reviews."""

    __tablename__ = "issues"
    __table_args__ = (
        Index(
            "ix_issues_service_created",
            "service_id",
            "created_at",
        ),
        Index(
            "ix_issues_status_priority",
            "status",
            "priority",
        ),
        Index(
            "ix_issues_status_severity",
            "status",
            "severity",
        ),
        Index(
            "ix_issues_incident_id",
            "incident_id",
        ),
        {"schema": "incidents"},
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    issue_number = Column(
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

    incident_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "incidents.incidents.id",
            ondelete="CASCADE",
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

    issue_type = Column(
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

    owner = Column(
        String(150),
        nullable=True,
        index=True,
    )

    remediation_plan = Column(
        Text,
        nullable=True,
    )

    estimated_effort_hours = Column(
        Float,
        nullable=True,
    )

    actual_effort_hours = Column(
        Float,
        nullable=True,
    )

    target_resolution_date = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    actual_resolution_date = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    overdue = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
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

    service = relationship(
        "Service",
        back_populates="issues",
    )

    incident = relationship(
        "Incident",
        back_populates="issues",
    )

    changes = relationship(
        "Change",
        back_populates="issue",
        cascade="all, delete-orphan",
    )

    risk_assessments = relationship(
        "RiskAssessment",
        back_populates="issue",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<Issue("
            f"issue_number='{self.issue_number}', "
            f"severity='{self.severity}', "
            f"priority='{self.priority}', "
            f"status='{self.status}'"
            f")>"
        )

    