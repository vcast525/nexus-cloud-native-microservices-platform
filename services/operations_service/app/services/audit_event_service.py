"""
audit_event_service.py

Business service for AuditEvent operations.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from ..repositories.audit_event_repository import AuditEventRepository
from .base_service import BaseService


class AuditEventService(BaseService):
    """
    Business service for AuditEvent operations.
    """

    def __init__(self):
        super().__init__(AuditEventRepository())

    # ------------------------------------------------------------------
    # Audit Event Business Operations
    # ------------------------------------------------------------------

    def get_by_audit_number(
        self,
        db: Session,
        audit_number: str,
    ):
        """
        Retrieve an audit event by audit number.
        """
        return self.repository.get_by_audit_number(
            db,
            audit_number,
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
    ):
        """
        Retrieve audit events for a service.
        """
        return self.repository.get_by_service(
            db,
            service_id,
        )

    def get_by_incident(
        self,
        db: Session,
        incident_id: UUID,
    ):
        """
        Retrieve audit events for an incident.
        """
        return self.repository.get_by_incident(
            db,
            incident_id,
        )

    def get_by_change(
        self,
        db: Session,
        change_id: UUID,
    ):
        """
        Retrieve audit events for a change request.
        """
        return self.repository.get_by_change(
            db,
            change_id,
        )

    def get_by_deployment(
        self,
        db: Session,
        deployment_id: UUID,
    ):
        """
        Retrieve audit events for a deployment.
        """
        return self.repository.get_by_deployment(
            db,
            deployment_id,
        )

    def get_by_event_type(
        self,
        db: Session,
        event_type: str,
    ):
        """
        Retrieve audit events by event type.
        """
        return self.repository.get_by_event_type(
            db,
            event_type,
        )

    def get_by_actor(
        self,
        db: Session,
        actor_name: str,
    ):
        """
        Retrieve audit events by actor.
        """
        return self.repository.get_by_actor(
            db,
            actor_name,
        )

    def get_by_outcome(
        self,
        db: Session,
        outcome: str,
    ):
        """
        Retrieve audit events by outcome.
        """
        return self.repository.get_by_outcome(
            db,
            outcome,
        )

    def get_recent(
        self,
        db: Session,
        limit: int = 10,
    ):
        """
        Retrieve recent audit events.
        """
        return self.repository.get_recent(
            db,
            limit,
        )

    def get_by_date_range(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime,
    ):
        """
        Retrieve audit events within a date range.
        """
        return self.repository.get_by_date_range(
            db,
            start_date,
            end_date,
        )

    def get_failed_events(
        self,
        db: Session,
    ):
        """
        Retrieve failed audit events.
        """
        return self.repository.get_failed_events(db)