"""Business logic for the Service Registry."""

from sqlalchemy.orm import Session

from app.repositories.service_repository import ServiceRepository


class ServiceService:
    """Implements business logic for registered services."""

    def __init__(self, db: Session):
        self.repository = ServiceRepository(db)

    def get_all_services(self):
        """Return all registered services."""

        return self.repository.get_all_services()