"""
deployment_repository.py

Repository for Deployment database operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.deployment import Deployment
from .base_repository import BaseRepository


class DeploymentRepository(BaseRepository[Deployment]):
    """
    Repository for Deployment entity.
    """

    def __init__(self):
        super().__init__(Deployment)

    # ------------------------------------------------------------------
    # Deployment Queries
    # ------------------------------------------------------------------

    def get_by_deployment_number(
        self,
        db: Session,
        deployment_number: str,
    ) -> Optional[Deployment]:
        """
        Retrieve a deployment by deployment number.
        """

        return (
            db.query(Deployment)
            .filter(
                Deployment.deployment_number == deployment_number
            )
            .first()
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
    ) -> List[Deployment]:
        """
        Retrieve all deployments for a service.
        """

        return (
            db.query(Deployment)
            .filter(Deployment.service_id == service_id)
            .order_by(Deployment.created_at.desc())
            .all()
        )

    def get_by_change(
        self,
        db: Session,
        change_id: UUID,
    ) -> List[Deployment]:
        """
        Retrieve deployments associated with a change.
        """

        return (
            db.query(Deployment)
            .filter(Deployment.change_id == change_id)
            .order_by(Deployment.created_at.desc())
            .all()
        )

    def get_by_maintenance_window(
        self,
        db: Session,
        maintenance_window_id: UUID,
    ) -> List[Deployment]:
        """
        Retrieve deployments for a maintenance window.
        """

        return (
            db.query(Deployment)
            .filter(
                Deployment.maintenance_window_id == maintenance_window_id
            )
            .order_by(Deployment.created_at.desc())
            .all()
        )

    def get_by_status(
        self,
        db: Session,
        status: str,
    ) -> List[Deployment]:
        """
        Retrieve deployments by status.
        """

        return (
            db.query(Deployment)
            .filter(Deployment.status == status)
            .order_by(Deployment.created_at.desc())
            .all()
        )

    def get_by_environment(
        self,
        db: Session,
        environment: str,
    ) -> List[Deployment]:
        """
        Retrieve deployments by environment.
        """

        return (
            db.query(Deployment)
            .filter(Deployment.environment == environment)
            .order_by(Deployment.created_at.desc())
            .all()
        )

    def get_recent(
        self,
        db: Session,
        limit: int = 10,
    ) -> List[Deployment]:
        """
        Retrieve the most recent deployments.
        """

        return (
            db.query(Deployment)
            .order_by(Deployment.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_started_after(
        self,
        db: Session,
        started_at,
    ) -> List[Deployment]:
        """
        Retrieve deployments started after the specified datetime.
        """

        return (
            db.query(Deployment)
            .filter(Deployment.started_at >= started_at)
            .order_by(Deployment.started_at.desc())
            .all()
        )

    def get_completed(
        self,
        db: Session,
    ) -> List[Deployment]:
        """
        Retrieve completed deployments.
        """

        return (
            db.query(Deployment)
            .filter(Deployment.completed_at.isnot(None))
            .order_by(Deployment.completed_at.desc())
            .all()
        )

    def get_rollbacks_required(
        self,
        db: Session,
    ) -> List[Deployment]:
        """
        Retrieve deployments requiring rollback.
        """

        return (
            db.query(Deployment)
            .filter(Deployment.rollback_required.is_(True))
            .order_by(Deployment.created_at.desc())
            .all()
        )

    def get_rollbacks_completed(
        self,
        db: Session,
    ) -> List[Deployment]:
        """
        Retrieve deployments where rollback has completed.
        """

        return (
            db.query(Deployment)
            .filter(Deployment.rollback_completed.is_(True))
            .order_by(Deployment.created_at.desc())
            .all()
        )

    def update_status(
        self,
        db: Session,
        deployment: Deployment,
        status: str,
    ) -> Deployment:
        """
        Update deployment status.
        """

        deployment.status = status

        db.add(deployment)
        db.commit()
        db.refresh(deployment)

        return deployment