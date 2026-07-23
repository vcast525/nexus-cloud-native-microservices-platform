"""
maintenance_window_service.py

Business service for MaintenanceWindow operations.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from ..repositories.maintenance_window_repository import (
    MaintenanceWindowRepository,
)
from .base_service import BaseService


class MaintenanceWindowService(BaseService):
    """
    Business service for Maintenance Window operations.
    """

    def __init__(self):
        super().__init__(MaintenanceWindowRepository())

    # ------------------------------------------------------------------
    # Maintenance Window Business Operations
    # ------------------------------------------------------------------

    def get_by_maintenance_number(
        self,
        db: Session,
        maintenance_number: str,
    ):
        """
        Retrieve a maintenance window by maintenance number.
        """
        return self.repository.get_by_maintenance_number(
            db,
            maintenance_number,
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
    ):
        """
        Retrieve maintenance windows for a service.
        """
        return self.repository.get_by_service(
            db,
            service_id,
        )

    def get_by_status(
        self,
        db: Session,
        status: str,
    ):
        """
        Retrieve maintenance windows by status.
        """
        return self.repository.get_by_status(
            db,
            status,
        )

    def get_upcoming(
        self,
        db: Session,
    ):
        """
        Retrieve upcoming maintenance windows.
        """
        return self.repository.get_upcoming(db)

    def get_active(
        self,
        db: Session,
    ):
        """
        Retrieve active maintenance windows.
        """
        return self.repository.get_active(db)

    def get_completed(
        self,
        db: Session,
    ):
        """
        Retrieve completed maintenance windows.
        """
        return self.repository.get_completed(db)

    def get_by_date_range(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime,
    ):
        """
        Retrieve maintenance windows within a date range.
        """
        return self.repository.get_by_date_range(
            db,
            start_date,
            end_date,
        )

    def get_recent(
        self,
        db: Session,
        limit: int = 10,
    ):
        """
        Retrieve recent maintenance windows.
        """
        return self.repository.get_recent(
            db,
            limit,
        )

    def update_status(
        self,
        db: Session,
        maintenance_window_id: UUID,
        status: str,
    ):
        """
        Update maintenance window status.
        """

        maintenance_window = self.get_by_id(
            db,
            maintenance_window_id,
        )

        if maintenance_window is None:
            raise ValueError(
                f"Maintenance window '{maintenance_window_id}' not found."
            )

        return self.repository.update_status(
            db,
            maintenance_window,
            status,
        )