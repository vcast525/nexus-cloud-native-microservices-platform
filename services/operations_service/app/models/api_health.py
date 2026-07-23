"""Database model for API health-check results."""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class APIHealth(Base):
    """Stores the result of an API endpoint health check."""

    __tablename__ = "api_health"
    __table_args__ = (
        Index(
            "ix_api_health_service_checked_at",
            "service_id",
            "checked_at",
        ),
        Index(
            "ix_api_health_status_checked_at",
            "status",
            "checked_at",
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

    endpoint = Column(
        String(500),
        nullable=False,
    )

    http_method = Column(
        String(10),
        nullable=False,
        default="GET",
    )

    status = Column(
        String(50),
        nullable=False,
        index=True,
    )

    status_code = Column(
        Integer,
        nullable=True,
    )

    response_time_ms = Column(
        Float,
        nullable=True,
    )

    availability_percent = Column(
        Float,
        nullable=False,
        default=100.0,
    )

    checked_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    service = relationship(
        "Service",
        back_populates="api_health_records",
    )
