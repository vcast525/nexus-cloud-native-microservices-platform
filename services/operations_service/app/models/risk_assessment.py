"""Database model for enterprise operational risk assessments."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class RiskAssessment(Base):
    """Represents a formal operational risk assessment."""

    __tablename__ = "risk_assessments"

    __table_args__ = (
        Index(
            "ix_risk_assessments_service_status",
            "service_id",
            "status",
        ),
        Index(
            "ix_risk_assessments_rating",
            "overall_risk_rating",
        ),
        Index(
            "ix_risk_assessments_owner",
            "risk_owner",
        ),
        Index(
            "ix_risk_assessments_review",
            "next_review_date",
        ),
        Index(
            "ix_risk_assessments_issue",
            "issue_id",
        ),
        {"schema": "incidents"},
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    assessment_number = Column(
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

    assessment_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="Open",
        index=True,
    )

    methodology = Column(
        String(100),
        nullable=True,
    )

    risk_owner = Column(
        String(150),
        nullable=False,
        index=True,
    )

    business_owner = Column(
        String(150),
        nullable=True,
    )

    assessed_by = Column(
        String(150),
        nullable=False,
    )

    likelihood_score = Column(
        Integer,
        nullable=False,
    )

    impact_score = Column(
        Integer,
        nullable=False,
    )

    inherent_risk_score = Column(
        Numeric(6, 2),
        nullable=False,
    )

    control_effectiveness = Column(
        Integer,
        nullable=False,
    )

    residual_risk_score = Column(
        Numeric(6, 2),
        nullable=False,
    )

    overall_risk_rating = Column(
        String(25),
        nullable=False,
        index=True,
    )

    risk_statement = Column(
        Text,
        nullable=True,
    )

    key_controls = Column(
        Text,
        nullable=True,
    )

    identified_gaps = Column(
        Text,
        nullable=True,
    )

    mitigation_strategy = Column(
        Text,
        nullable=True,
    )

    action_plan = Column(
        Text,
        nullable=True,
    )

    target_completion_date = Column(
        DateTime,
        nullable=True,
    )

    next_review_date = Column(
        DateTime,
        nullable=True,
        index=True,
    )

    last_review_date = Column(
        DateTime,
        nullable=True,
    )

    risk_accepted = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    executive_approval = Column(
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
        back_populates="risk_assessments",
    )

    issue = relationship(
        "Issue",
        back_populates="risk_assessments",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self):
        return (
            f"<RiskAssessment("
            f"assessment_number='{self.assessment_number}', "
            f"overall_risk_rating='{self.overall_risk_rating}', "
            f"status='{self.status}'"
            f")>"
        )