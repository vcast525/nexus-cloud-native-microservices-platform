"""
risk_assessment_repository.py

Repository for Risk Assessment-specific database operations.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.risk_assessment import RiskAssessment
from .base_repository import BaseRepository


class RiskAssessmentRepository(BaseRepository[RiskAssessment]):
    """
    Repository for Risk Assessment entities.

    Common CRUD and pagination operations are inherited from
    BaseRepository.
    """

    def __init__(self):
        super().__init__(RiskAssessment)

    def get_by_assessment_number(
        self,
        db: Session,
        assessment_number: str,
    ) -> Optional[RiskAssessment]:
        """
        Retrieve a Risk Assessment using its business assessment number.
        """

        return self.first_by(
            db,
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

        return (
            db.query(self.model)
            .filter(self.model.service_id == service_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
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

        return (
            db.query(self.model)
            .filter(self.model.issue_id == issue_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
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

        return (
            db.query(self.model)
            .filter(self.model.status == assessment_status)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
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

        return (
            db.query(self.model)
            .filter(
                self.model.overall_risk_rating
                == overall_risk_rating
            )
            .order_by(
                self.model.residual_risk_score.desc(),
                self.model.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
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

        return (
            db.query(self.model)
            .filter(self.model.risk_owner == risk_owner)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_due_for_review(
        self,
        db: Session,
        review_before: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RiskAssessment]:
        """
        Retrieve Risk Assessments whose next review date is due
        on or before the supplied date.
        """

        return (
            db.query(self.model)
            .filter(
                self.model.next_review_date.is_not(None),
                self.model.next_review_date <= review_before,
            )
            .order_by(
                self.model.next_review_date.asc(),
                self.model.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
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

        return (
            db.query(self.model)
            .filter(self.model.risk_accepted.is_(False))
            .order_by(
                self.model.residual_risk_score.desc(),
                self.model.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
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

        return (
            db.query(self.model)
            .filter(
                self.model.executive_approval.is_(False)
            )
            .order_by(
                self.model.residual_risk_score.desc(),
                self.model.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def assessment_number_exists(
        self,
        db: Session,
        assessment_number: str,
    ) -> bool:
        """
        Determine whether a Risk Assessment number already exists.
        """

        return (
            self.get_by_assessment_number(
                db=db,
                assessment_number=assessment_number,
            )
            is not None
        )
