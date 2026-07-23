"""
maintenance_window_repository.py

Repository for MaintenanceWindow database operations.

Contains maintenance window-specific queries in addition to the
generic CRUD operations inherited from BaseRepository.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.maintenance_window import MaintenanceWindow
from .base_repository import BaseRepository


class MaintenanceWindowRepository(BaseRepository[MaintenanceWindow]):
    """
    Repository for MaintenanceWindow entity.
    """

    def __init__(self):
        super().__init__(MaintenanceWindow)

    # ------------------------------------------------------------------
    # Maintenance Window Queries
    # ------------------------------------------------------------------

    def get_by_name(
        self,
        db: Session,
        name: str,
    ) -> Optional[MaintenanceWindow]:
        """
        Retrieve a maintenance window by name.
        """

        return (
            db.query(MaintenanceWindow)
            .filter(MaintenanceWindow.name == name)
            .first()
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
    ) -> List[MaintenanceWindow]:
        """
        Retrieve all maintenance windows for a service.
        """

        return (
            db.query(MaintenanceWindow)
            .filter(MaintenanceWindow.service_id == service_id)
            .order_by(MaintenanceWindow.start_time.desc())
            .all()
        )

    def get_by_status(
        self,
        db: Session,
        status: str,
    ) -> List[MaintenanceWindow]:
        """
        Retrieve maintenance windows by status.
        """

        return (
            db.query(MaintenanceWindow)
            .filter(MaintenanceWindow.status == status)
            .order_by(MaintenanceWindow.start_time.desc())
            .all()
        )

    def get_upcoming(
        self,
        db: Session,
    ) -> List[MaintenanceWindow]:
        """
        Retrieve upcoming maintenance windows.
        """

        return (
            db.query(MaintenanceWindow)
            .filter(MaintenanceWindow.start_time > datetime.utcnow())
            .order_by(MaintenanceWindow.start_time.asc())
            .all()
        )

    def get_active(
        self,
        db: Session,
    ) -> List[MaintenanceWindow]:
        """
        Retrieve maintenance windows currently in progress.
        """

        now = datetime.utcnow()

        return (
            db.query(MaintenanceWindow)
            .filter(MaintenanceWindow.start_time <= now)
            .filter(MaintenanceWindow.end_time >= now)
            .order_by(MaintenanceWindow.start_time.asc())
            .all()
        )

    def get_completed(
        self,
        db: Session,
    ) -> List[MaintenanceWindow]:
        """
        Retrieve completed maintenance windows.
        """

        return (
            db.query(MaintenanceWindow)
            .filter(MaintenanceWindow.end_time < datetime.utcnow())
            .order_by(MaintenanceWindow.end_time.desc())
            .all()
        )

    def get_by_date_range(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime,
    ) -> List[MaintenanceWindow]:
        """
        Retrieve maintenance windows occurring within a date range.
        """

        return (
            db.query(MaintenanceWindow)
            .filter(MaintenanceWindow.start_time >= start_date)
            .filter(MaintenanceWindow.end_time <= end_date)
            .order_by(MaintenanceWindow.start_time.asc())
            .all()
        )

    def search(
        self,
        db: Session,
        search_term: str,
    ) -> List[MaintenanceWindow]:
        """
        Search maintenance windows by name.
        """

        return (
            db.query(MaintenanceWindow)
            .filter(
                MaintenanceWindow.name.ilike(f"%{search_term}%")
            )
            .order_by(MaintenanceWindow.start_time.desc())
            .all()
        )

    def update_status(
        self,
        db: Session,
        maintenance_window: MaintenanceWindow,
        status: str,
    ) -> MaintenanceWindow:
        """
        Update maintenance window status.
        """

        maintenance_window.status = status

        db.add(maintenance_window)
        db.commit()
        db.refresh(maintenance_window)

        return maintenance_window

    def get_recent(
        self,
        db: Session,
        limit: int = 10,
    ) -> List[MaintenanceWindow]:
        """
        Retrieve the most recently created maintenance windows.
        """

        return (
            db.query(MaintenanceWindow)
            .order_by(MaintenanceWindow.created_at.desc())
            .limit(limit)
            .all()
        )