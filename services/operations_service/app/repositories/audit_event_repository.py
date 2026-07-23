"""
audit_event_repository.py

Repository for AuditEvent database operations.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.audit_event import AuditEvent
from .base_repository import BaseRepository


class AuditEventRepository(BaseRepository[AuditEvent]):
    """
    Repository for AuditEvent entity.
    """

    def __init__(self):
        super().__init__(AuditEvent)

    # ------------------------------------------------------------------
    # Audit Event Queries
    # ------------------------------------------------------------------

    def get_by_audit_number(
        self,
        db: Session,
        audit_number: str,
    ) -> Optional[AuditEvent]:
        """
        Retrieve an audit event by audit number.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.audit_number == audit_number)
            .first()
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events for a service.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.service_id == service_id)
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )

    def get_by_incident(
        self,
        db: Session,
        incident_id: UUID,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events for an incident.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.incident_id == incident_id)
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )

    def get_by_change(
        self,
        db: Session,
        change_id: UUID,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events for a change request.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.change_id == change_id)
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )

    def get_by_deployment(
        self,
        db: Session,
        deployment_id: UUID,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events for a deployment.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.deployment_id == deployment_id)
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )

    def get_by_event_type(
        self,
        db: Session,
        event_type: str,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events by event type.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.event_type == event_type)
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )

    def get_by_actor(
        self,
        db: Session,
        actor_name: str,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events performed by an actor.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.actor_name == actor_name)
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )

    def get_by_outcome(
        self,
        db: Session,
        outcome: str,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events by outcome.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.outcome == outcome)
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )

    def get_recent(
        self,
        db: Session,
        limit: int = 10,
    ) -> List[AuditEvent]:
        """
        Retrieve the most recent audit events.
        """

        return (
            db.query(AuditEvent)
            .order_by(AuditEvent.occurred_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_date_range(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events occurring within a date range.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.occurred_at >= start_date)
            .filter(AuditEvent.occurred_at <= end_date)
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )

    def get_failed_events(
        self,
        db: Session,
    ) -> List[AuditEvent]:
        """
        Retrieve audit events with a FAILED outcome.
        """

        return (
            db.query(AuditEvent)
            .filter(AuditEvent.outcome == "FAILED")
            .order_by(AuditEvent.occurred_at.desc())
            .all()
        )