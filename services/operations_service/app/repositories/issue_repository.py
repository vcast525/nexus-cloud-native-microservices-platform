"""
issue_repository.py

Repository for Issue-specific database operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.issue import Issue
from .base_repository import BaseRepository


class IssueRepository(BaseRepository[Issue]):
    """
    Repository for Issue entities.

    Common CRUD and pagination operations are inherited from
    BaseRepository.
    """

    def __init__(self):
        super().__init__(Issue)

    def get_by_issue_number(
        self,
        db: Session,
        issue_number: str,
    ) -> Optional[Issue]:
        """
        Retrieve an Issue using its business issue number.
        """

        return self.first_by(
            db,
            issue_number=issue_number,
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Issue]:
        """
        Retrieve Issues associated with a Service.
        """

        return (
            db.query(self.model)
            .filter(self.model.service_id == service_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_incident(
        self,
        db: Session,
        incident_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Issue]:
        """
        Retrieve Issues associated with an Incident.
        """

        return (
            db.query(self.model)
            .filter(self.model.incident_id == incident_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self,
        db: Session,
        issue_status: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Issue]:
        """
        Retrieve Issues matching a status.
        """

        return (
            db.query(self.model)
            .filter(self.model.status == issue_status)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_priority(
        self,
        db: Session,
        priority: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Issue]:
        """
        Retrieve Issues matching a priority.
        """

        return (
            db.query(self.model)
            .filter(self.model.priority == priority)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_overdue_issues(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Issue]:
        """
        Retrieve Issues currently marked as overdue.
        """

        return (
            db.query(self.model)
            .filter(self.model.overdue.is_(True))
            .order_by(
                self.model.target_resolution_date.asc(),
                self.model.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_open_issues(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Issue]:
        """
        Retrieve Issues that have not reached a terminal status.
        """

        closed_statuses = [
            "Resolved",
            "Closed",
            "Cancelled",
        ]

        return (
            db.query(self.model)
            .filter(
                self.model.status.notin_(closed_statuses)
            )
            .order_by(
                self.model.priority.asc(),
                self.model.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def issue_number_exists(
        self,
        db: Session,
        issue_number: str,
    ) -> bool:
        """
        Determine whether an Issue number already exists.
        """

        return (
            self.get_by_issue_number(
                db=db,
                issue_number=issue_number,
            )
            is not None
        )
