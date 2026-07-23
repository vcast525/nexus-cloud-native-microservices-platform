"""
incident_service.py

Business service for Incident operations.
"""

from typing import Dict, List
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.incident import Incident
from ..repositories.incident_repository import IncidentRepository
from .base_service import BaseService


class IncidentService(BaseService[IncidentRepository]):
    """
    Business service for Incident operations.

    Common CRUD behavior is inherited from BaseService.
    """

    def __init__(self):
        super().__init__(
            IncidentRepository()
        )

    def create_incident(
        self,
        db: Session,
        obj_in: Dict,
    ) -> Incident:
        """
        Create an Incident after validating its business number.
        """

        incident_number = obj_in.get(
            "incident_number"
        )

        if self.repository.incident_number_exists(
            db=db,
            incident_number=incident_number,
        ):
            raise ValueError(
                f"Incident number '{incident_number}' already exists."
            )

        return self.create(
            db=db,
            obj_in=obj_in,
        )

    def get_by_incident_number(
        self,
        db: Session,
        incident_number: str,
    ):
        """
        Retrieve an Incident by its business incident number.
        """

        return self.repository.get_by_incident_number(
            db=db,
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

        return self.repository.get_by_service(
            db=db,
            service_id=service_id,
            skip=skip,
            limit=limit,
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

        return self.repository.get_by_status(
            db=db,
            incident_status=incident_status,
            skip=skip,
            limit=limit,
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

        return self.repository.get_by_severity(
            db=db,
            severity=severity,
            skip=skip,
            limit=limit,
        )

    def get_open_incidents(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Incident]:
        """
        Retrieve Incidents that are still operationally open.
        """

        return self.repository.get_open_incidents(
            db=db,
            skip=skip,
            limit=limit,
        )
