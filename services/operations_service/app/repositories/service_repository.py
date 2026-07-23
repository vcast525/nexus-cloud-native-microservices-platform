"""Repository layer for Service Registry database operations."""

from sqlalchemy.orm import Session

from app.models.service import Service


class ServiceRepository:
    """Handles all database operations for registered services."""

    def __init__(self, db: Session):
        self.db = db

    def get_all_services(self) -> list[Service]:
        """Return all registered services ordered by name."""

        return (
            self.db.query(Service)
            .order_by(Service.service_name)
            .all()
        )