"""
risk_assessment_service.py

Business service for Risk Assessment operations.
"""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.risk_assessment import RiskAssessment
from ..repositories.risk_assessment_repository import (
    RiskAssessmentRepository,
)
from .base_service import BaseService


class RiskAssessmentService(
    BaseService[RiskAssessmentRepository]
):
    """
    Business service for Risk Assessment operations.

    Common CRUD and pagination behavior is inherited from BaseService.
    """

    def __init__(self):
        super().__init__(
            RiskAssessmentRepository()
        )

    def create_risk_assessment(
        self,
        db: Session,
        obj_in: Dict,
    ) -> RiskAssessment:
        """
        Create a Risk Assessment after validating its assessment number.
        """

        assessment_number = obj_in.get(
            "assessment_number"
        )

        if self.repository.assessment_number_exists(
            db=db,
            assessment_number=assessment_number,
        ):
            raise ValueError(
                f"Assessment number '{assessment_number}' already exists."
            )

        return self.create(
            db=db,
            obj_in=obj_in,
        )

    def get_by_assessment_number(
        self,
        db: Session,
        assessment_number: str,
    ) -> Optional[RiskAssessment]:
        """
        Retrieve a Risk Assessment by its business assessment number.
        """

        return self.repository.get_by_assessment_number(
            db=db,
            assessment_number=assessment_number,
        )

    def get_by_service(
        self,
        db: Session,
        service_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments associated with a Service.
        """

        return self.repository.get_by_service(
            db=db,
            service_id=service_id,
            skip=skip,
            limit=limit,
        )

    def get_by_issue(
        self,
        db: Session,
        issue_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments associated with an Issue.
        """

        return self.repository.get_by_issue(
            db=db,
            issue_id=issue_id,
            skip=skip,
            limit=limit,
        )

    def get_by_status(
        self,
        db: Session,
        assessment_status: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments matching a status.
        """

        return self.repository.get_by_status(
            db=db,
            assessment_status=assessment_status,
            skip=skip,
            limit=limit,
        )

    def get_by_rating(
        self,
        db: Session,
        overall_risk_rating: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments matching an overall risk rating.
        """

        return self.repository.get_by_rating(
            db=db,
            overall_risk_rating=overall_risk_rating,
            skip=skip,
            limit=limit,
        )

    def get_by_risk_owner(
        self,
        db: Session,
        risk_owner: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments assigned to a risk owner.
        """

        return self.repository.get_by_risk_owner(
            db=db,
            risk_owner=risk_owner,
            skip=skip,
            limit=limit,
        )

    def get_due_for_review(
        self,
        db: Session,
        review_before: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments due for review by a supplied date.
        """

        return self.repository.get_due_for_review(
            db=db,
            review_before=review_before,
            skip=skip,
            limit=limit,
        )

    def get_unaccepted_risks(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments that have not been formally accepted.
        """

        return self.repository.get_unaccepted_risks(
            db=db,
            skip=skip,
            limit=limit,
        )

    def get_pending_executive_approval(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments awaiting executive approval.
        """

        return self.repository.get_pending_executive_approval(
            db=db,
            skip=skip,
            limit=limit,
        )
