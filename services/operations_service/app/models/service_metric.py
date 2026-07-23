"""Database model for service performance metrics."""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class ServiceMetric(Base):
    """Stores time-series operational metrics for a registered service."""

    __tablename__ = "service_metrics"
    __table_args__ = (
        Index(
            "ix_service_metrics_service_recorded_at",
            "service_id",
            "recorded_at",
        ),
        {"schema": "registry"},
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    service_id = Column(
        UUID(as_uuid=True),
        ForeignKey("registry.services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cpu_usage_percent = Column(
        Float,
        nullable=False,
    )

    memory_usage_percent = Column(
        Float,
        nullable=False,
    )

    request_count = Column(
        BigInteger,
        nullable=False,
        default=0,
    )

    error_count = Column(
        BigInteger,
        nullable=False,
        default=0,
    )

    error_rate_percent = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    average_response_time_ms = Column(
        Float,
        nullable=False,
    )

    recorded_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    service = relationship(
        "Service",
        back_populates="metrics",
    )
