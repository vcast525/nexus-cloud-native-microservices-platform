"""Database model for registered NEXUS services."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class Service(Base):
    """Represents an application or microservice monitored by NEXUS."""

    __tablename__ = "services"
    __table_args__ = {"schema": "registry"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    service_name = Column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    owner = Column(
        String(150),
        nullable=False,
    )

    business_unit = Column(
        String(150),
        nullable=False,
        index=True,
    )

    environment = Column(
        String(50),
        nullable=False,
        index=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="healthy",
        index=True,
    )

    version = Column(
        String(50),
        nullable=True,
    )

    repository_url = Column(
        String(500),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
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

    incidents = relationship(
        "Incident",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    issues = relationship(
        "Issue",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    changes = relationship(
        "Change",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    risk_assessments = relationship(
        "RiskAssessment",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    api_health_records = relationship(
        "APIHealth",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    metrics = relationship(
        "ServiceMetric",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    deployments = relationship(
        "Deployment",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    maintenance_windows = relationship(
        "MaintenanceWindow",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    audit_events = relationship(
        "AuditEvent",
        back_populates="service",
    )

    notifications = relationship(
        "Notification",
        back_populates="service",
    )