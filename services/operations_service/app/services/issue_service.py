"""
issue_service.py

Business service for Issue operations.
"""

from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.issue import Issue
from ..repositories.issue_repository import IssueRepository
from .base_service import BaseService


class IssueService(BaseService[IssueRepository]):
    """
    Business service for Issue operations.

    Common CRUD and pagination behavior is inherited from BaseService.
    """

    def __init__(self):
        super().__init__(
            IssueRepository()
        )

    def create_issue(
        self,
        db: Session,
        obj_in: Dict,
    ) -> Issue:
        """
        Create an Issue after validating its business issue number.
        """

        issue_number = obj_in.get(
            "issue_number"
        )

        if self.repository.issue_number_exists(
            db=db,
            issue_number=issue_number,
        ):
            raise ValueError(
                f"Issue number '{issue_number}' already exists."
            )

        return self.create(
            db=db,
            obj_in=obj_in,
        )

    def get_by_issue_number(
        self,
        db: Session,
        issue_number: str,
    ) -> Optional[Issue]:
        """
        Retrieve an Issue by its business issue number.
        """

        return self.repository.get_by_issue_number(
            db=db,
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

        return self.repository.get_by_service(
            db=db,
            service_id=service_id,
            skip=skip,
            limit=limit,
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

        return self.repository.get_by_incident(
            db=db,
            incident_id=incident_id,
            skip=skip,
            limit=limit,
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

        return self.repository.get_by_status(
            db=db,
            issue_status=issue_status,
            skip=skip,
            limit=limit,
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

        return self.repository.get_by_priority(
            db=db,
            priority=priority,
            skip=skip,
            limit=limit,
        )

    def get_overdue_issues(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Issue]:
        """
        Retrieve Issues marked as overdue.
        """

        return self.repository.get_overdue_issues(
            db=db,
            skip=skip,
            limit=limit,
        )

    def get_open_issues(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Issue]:
        """
        Retrieve Issues that are still operationally open.
        """

        return self.repository.get_open_issues(
            db=db,
            skip=skip,
            limit=limit,
        )
