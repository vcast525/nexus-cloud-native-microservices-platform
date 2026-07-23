"""
notification_service.py

Business service for Notification operations.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from ..repositories.notification_repository import NotificationRepository
from .base_service import BaseService


class NotificationService(BaseService):
    """
    Business service for Notification operations.
    """

    def __init__(self):
        super().__init__(NotificationRepository())

    # ------------------------------------------------------------------
    # Notification Business Operations
    # ------------------------------------------------------------------

    def get_by_notification_number(
        self,
        db: Session,
        notification_number: str,
    ):
        """
        Retrieve a notification by notification number.
        """
        return self.repository.get_by_notification_number(
            db,
            notification_number,
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
    ):
        """
        Retrieve notifications for a service.
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
        Retrieve notifications for an incident.
        """
        return self.repository.get_by_incident(
            db,
            incident_id,
        )

    def get_by_deployment(
        self,
        db: Session,
        deployment_id: UUID,
    ):
        """
        Retrieve notifications for a deployment.
        """
        return self.repository.get_by_deployment(
            db,
            deployment_id,
        )

    def get_by_audit_event(
        self,
        db: Session,
        audit_event_id: UUID,
    ):
        """
        Retrieve notifications for an audit event.
        """
        return self.repository.get_by_audit_event(
            db,
            audit_event_id,
        )

    def get_by_status(
        self,
        db: Session,
        status: str,
    ):
        """
        Retrieve notifications by status.
        """
        return self.repository.get_by_status(
            db,
            status,
        )

    def get_by_channel(
        self,
        db: Session,
        channel: str,
    ):
        """
        Retrieve notifications by delivery channel.
        """
        return self.repository.get_by_channel(
            db,
            channel,
        )

    def get_by_priority(
        self,
        db: Session,
        priority: str,
    ):
        """
        Retrieve notifications by priority.
        """
        return self.repository.get_by_priority(
            db,
            priority,
        )

    def get_by_recipient(
        self,
        db: Session,
        recipient: str,
    ):
        """
        Retrieve notifications for a recipient.
        """
        return self.repository.get_by_recipient(
            db,
            recipient,
        )

    def get_pending(
        self,
        db: Session,
    ):
        """
        Retrieve pending notifications.
        """
        return self.repository.get_pending(db)

    def get_failed(
        self,
        db: Session,
    ):
        """
        Retrieve failed notifications.
        """
        return self.repository.get_failed(db)

    def get_scheduled_before(
        self,
        db: Session,
        scheduled_at: datetime,
    ):
        """
        Retrieve notifications scheduled before a specified datetime.
        """
        return self.repository.get_scheduled_before(
            db,
            scheduled_at,
        )

    def get_recent(
        self,
        db: Session,
        limit: int = 10,
    ):
        """
        Retrieve recent notifications.
        """
        return self.repository.get_recent(
            db,
            limit,
        )

    def update_status(
        self,
        db: Session,
        notification_id: UUID,
        status: str,
    ):
        """
        Update notification status.
        """

        notification = self.get_by_id(
            db,
            notification_id,
        )

        if notification is None:
            raise ValueError(
                f"Notification '{notification_id}' not found."
            )

        return self.repository.update_status(
            db,
            notification,
            status,
        )