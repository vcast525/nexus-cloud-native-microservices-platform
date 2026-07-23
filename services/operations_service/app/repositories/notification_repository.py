"""
notification_repository.py

Repository for Notification database operations.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.notification import Notification
from .base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """
    Repository for Notification entity.
    """

    def __init__(self):
        super().__init__(Notification)

    # ------------------------------------------------------------------
    # Notification Queries
    # ------------------------------------------------------------------

    def get_by_notification_number(
        self,
        db: Session,
        notification_number: str,
    ) -> Optional[Notification]:
        """
        Retrieve a notification by notification number.
        """

        return (
            db.query(Notification)
            .filter(
                Notification.notification_number == notification_number
            )
            .first()
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
    ) -> List[Notification]:
        """
        Retrieve notifications for a service.
        """

        return (
            db.query(Notification)
            .filter(Notification.service_id == service_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_by_incident(
        self,
        db: Session,
        incident_id: UUID,
    ) -> List[Notification]:
        """
        Retrieve notifications for an incident.
        """

        return (
            db.query(Notification)
            .filter(Notification.incident_id == incident_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_by_deployment(
        self,
        db: Session,
        deployment_id: UUID,
    ) -> List[Notification]:
        """
        Retrieve notifications for a deployment.
        """

        return (
            db.query(Notification)
            .filter(Notification.deployment_id == deployment_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_by_audit_event(
        self,
        db: Session,
        audit_event_id: UUID,
    ) -> List[Notification]:
        """
        Retrieve notifications for an audit event.
        """

        return (
            db.query(Notification)
            .filter(Notification.audit_event_id == audit_event_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_by_status(
        self,
        db: Session,
        status: str,
    ) -> List[Notification]:
        """
        Retrieve notifications by status.
        """

        return (
            db.query(Notification)
            .filter(Notification.status == status)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_by_channel(
        self,
        db: Session,
        channel: str,
    ) -> List[Notification]:
        """
        Retrieve notifications by delivery channel.
        """

        return (
            db.query(Notification)
            .filter(Notification.channel == channel)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_by_priority(
        self,
        db: Session,
        priority: str,
    ) -> List[Notification]:
        """
        Retrieve notifications by priority.
        """

        return (
            db.query(Notification)
            .filter(Notification.priority == priority)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_by_recipient(
        self,
        db: Session,
        recipient: str,
    ) -> List[Notification]:
        """
        Retrieve notifications for a recipient.
        """

        return (
            db.query(Notification)
            .filter(Notification.recipient == recipient)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_pending(
        self,
        db: Session,
    ) -> List[Notification]:
        """
        Retrieve pending notifications.
        """

        return (
            db.query(Notification)
            .filter(Notification.status == "PENDING")
            .order_by(Notification.scheduled_at.asc())
            .all()
        )

    def get_failed(
        self,
        db: Session,
    ) -> List[Notification]:
        """
        Retrieve failed notifications.
        """

        return (
            db.query(Notification)
            .filter(Notification.status == "FAILED")
            .order_by(Notification.failed_at.desc())
            .all()
        )

    def get_scheduled_before(
        self,
        db: Session,
        scheduled_at: datetime,
    ) -> List[Notification]:
        """
        Retrieve notifications scheduled before a specified datetime.
        """

        return (
            db.query(Notification)
            .filter(Notification.scheduled_at <= scheduled_at)
            .order_by(Notification.scheduled_at.asc())
            .all()
        )

    def get_recent(
        self,
        db: Session,
        limit: int = 10,
    ) -> List[Notification]:
        """
        Retrieve the most recently created notifications.
        """

        return (
            db.query(Notification)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .all()
        )

    def update_status(
        self,
        db: Session,
        notification: Notification,
        status: str,
    ) -> Notification:
        """
        Update notification status.
        """

        notification.status = status

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification