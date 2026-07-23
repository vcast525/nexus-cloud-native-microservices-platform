"""
risk_assessment.py

Pydantic request and response schemas for Risk Assessment operations.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RiskAssessmentBase(BaseModel):
    """
    Shared fields used by Risk Assessment creation and response schemas.
    """

    assessment_number: str = Field(
        ...,
        min_length=1,
        max_length=20,
    )

    service_id: UUID
    issue_id: Optional[UUID] = None

    title: str = Field(
        ...,
        min_length=1,
        max_length=250,
    )

    description: Optional[str] = None

    assessment_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    status: str = Field(
        default="Open",
        min_length=1,
        max_length=50,
    )

    methodology: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    risk_owner: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    business_owner: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    assessed_by: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    likelihood_score: int

    impact_score: int

    inherent_risk_score: Decimal = Field(
        ...,
        max_digits=6,
        decimal_places=2,
    )

    control_effectiveness: int

    residual_risk_score: Decimal = Field(
        ...,
        max_digits=6,
        decimal_places=2,
    )

    overall_risk_rating: str = Field(
        ...,
        min_length=1,
        max_length=25,
    )

    risk_statement: Optional[str] = None
    key_controls: Optional[str] = None
    identified_gaps: Optional[str] = None
    mitigation_strategy: Optional[str] = None
    action_plan: Optional[str] = None

    target_completion_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    last_review_date: Optional[datetime] = None

    risk_accepted: bool = False
    executive_approval: bool = False

    correlation_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )


class RiskAssessmentCreate(RiskAssessmentBase):
    """
    Request schema used when creating a Risk Assessment.
    """

    pass


class RiskAssessmentUpdate(BaseModel):
    """
    Request schema used when partially updating a Risk Assessment.

    Every field is optional because a PATCH request may update only
    selected Risk Assessment fields.
    """

    assessment_number: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    service_id: Optional[UUID] = None
    issue_id: Optional[UUID] = None

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=250,
    )

    description: Optional[str] = None

    assessment_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    status: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    methodology: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    risk_owner: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    business_owner: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    assessed_by: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    likelihood_score: Optional[int] = None

    impact_score: Optional[int] = None

    inherent_risk_score: Optional[Decimal] = Field(
        default=None,
        max_digits=6,
        decimal_places=2,
    )

    control_effectiveness: Optional[int] = None

    residual_risk_score: Optional[Decimal] = Field(
        default=None,
        max_digits=6,
        decimal_places=2,
    )

    overall_risk_rating: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=25,
    )

    risk_statement: Optional[str] = None
    key_controls: Optional[str] = None
    identified_gaps: Optional[str] = None
    mitigation_strategy: Optional[str] = None
    action_plan: Optional[str] = None

    target_completion_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    last_review_date: Optional[datetime] = None

    risk_accepted: Optional[bool] = None
    executive_approval: Optional[bool] = None

    correlation_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )


class RiskAssessmentResponse(RiskAssessmentBase):
    """
    Response schema returned by Risk Assessment API endpoints.
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class RiskAssessmentPageResponse(BaseModel):
    """
    Paginated Risk Assessment response.
    """

    items: list[RiskAssessmentResponse]
    page: int
    page_size: int
    total: int
    pages: int
