"""
deployment_service.py

Business service for Deployment operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..repositories.deployment_repository import DeploymentRepository
from .base_service import BaseService


from sqlalchemy.orm import Session

from ..repositories.deployment_repository import DeploymentRepository
from .base_service import BaseService


class DeploymentService(BaseService):
    """
    Business service for Deployment operations.
    """

    def __init__(self):
        super().__init__(DeploymentRepository())

    # ------------------------------------------------------------------
    # Deployment Business Operations
    # ------------------------------------------------------------------

    def get_by_deployment_number(
        self,
        db: Session,
        deployment_number: str,
    ):
        """
        Retrieve a deployment by deployment number.
        """
        return self.repository.get_by_deployment_number(
            db,
            deployment_number,
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
    ):
        """
        Retrieve all deployments for a service.
        """
        return self.repository.get_by_service(
            db,
            service_id,
        )

    def get_by_change(
        self,
        db: Session,
        change_id: UUID,
    ):
        """
        Retrieve all deployments for a change request.
        """
        return self.repository.get_by_change(
            db,
            change_id,
        )

    def get_by_maintenance_window(
        self,
        db: Session,
        maintenance_window_id: UUID,
    ):
        """
        Retrieve deployments for a maintenance window.
        """
        return self.repository.get_by_maintenance_window(
            db,
            maintenance_window_id,
        )

    def get_by_status(
        self,
        db: Session,
        status: str,
    ):
        """
        Retrieve deployments by status.
        """
        return self.repository.get_by_status(
            db,
            status,
        )

    def get_by_environment(
        self,
        db: Session,
        environment: str,
    ):
        """
        Retrieve deployments by environment.
        """
        return self.repository.get_by_environment(
            db,
            environment,
        )

    def get_recent(
        self,
        db: Session,
        limit: int = 10,
    ):
        """
        Retrieve recent deployments.
        """
        return self.repository.get_recent(
            db,
            limit,
        )

    def get_completed(
        self,
        db: Session,
    ):
        """
        Retrieve completed deployments.
        """
        return self.repository.get_completed(db)

    def get_rollbacks_required(
        self,
        db: Session,
    ):
        """
        Retrieve deployments requiring rollback.
        """
        return self.repository.get_rollbacks_required(db)

    def get_rollbacks_completed(
        self,
        db: Session,
    ):
        """
        Retrieve completed rollbacks.
        """
        return self.repository.get_rollbacks_completed(db)

    def update_status(
        self,
        db: Session,
        deployment_id: UUID,
        status: str,
    ):
        """
        Update deployment status.
        """

        deployment = self.get_by_id(
            db,
            deployment_id,
        )

        if deployment is None:
            raise ValueError(
                f"Deployment '{deployment_id}' not found."
            )

        return self.repository.update_status(
            db,
            deployment,
            status,
        )