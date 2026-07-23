"""
incident_repository.py

Repository for Incident-specific database operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.incident import Incident
from .base_repository import BaseRepository


class IncidentRepository(BaseRepository[Incident]):
    """
    Repository for Incident entities.

    Common CRUD operations are inherited from BaseRepository.
    """

    def __init__(self):
        super().__init__(Incident)

    def get_by_incident_number(
        self,
        db: Session,
        incident_number: str,
    ) -> Optional[Incident]:
        """
        Retrieve an Incident using its business incident number.
        """

        return self.first_by(
            db,
            incident_number=incident_number,
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Incident]:
        """
        Retrieve Incidents associated with a Service.
        """

        return (
            db.query(self.model)
            .filter(self.model.service_id == service_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self,
        db: Session,
        incident_status: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Incident]:
        """
        Retrieve Incidents matching a status.
        """

        return (
            db.query(self.model)
            .filter(self.model.status == incident_status)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_severity(
        self,
        db: Session,
        severity: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Incident]:
        """
        Retrieve Incidents matching a severity.
        """

        return (
            db.query(self.model)
            .filter(self.model.severity == severity)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_open_incidents(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Incident]:
        """
        Retrieve Incidents that have not reached a terminal status.
        """

        closed_statuses = [
            "RESOLVED",
            "CLOSED",
            "CANCELLED",
        ]

        return (
            db.query(self.model)
            .filter(
                self.model.status.notin_(closed_statuses)
            )
            .order_by(
                self.model.severity.asc(),
                self.model.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def incident_number_exists(
        self,
        db: Session,
        incident_number: str,
    ) -> bool:
        """
        Determine whether an Incident number already exists.
        """

        return (
            self.get_by_incident_number(
                db=db,
                incident_number=incident_number,
            )
            is not None
        )
