"""
risk_assessment.py

API routes for Risk Assessment operations.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.risk_assessment import (
    RiskAssessmentCreate,
    RiskAssessmentResponse,
    RiskAssessmentUpdate,
)
from ...services.risk_assessment_service import (
    RiskAssessmentService,
)

router = APIRouter(
    prefix="/risk-assessments",
    tags=["Risk Assessments"],
)

service = RiskAssessmentService()


@router.post(
    "/",
    response_model=RiskAssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_risk_assessment(
    risk_assessment: RiskAssessmentCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new Risk Assessment.
    """
    try:
        return service.create_risk_assessment(
            db=db,
            obj_in=risk_assessment.model_dump(),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{risk_assessment_id}",
    response_model=RiskAssessmentResponse,
)
def get_risk_assessment(
    risk_assessment_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve a Risk Assessment by ID.
    """
    assessment = service.get_by_id(
        db=db,
        obj_id=risk_assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk Assessment not found.",
        )

    return assessment


@router.get(
    "/",
    response_model=List[RiskAssessmentResponse],
)
def list_risk_assessments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Retrieve Risk Assessments with pagination.
    """
    return service.paginate(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.put(
    "/{risk_assessment_id}",
    response_model=RiskAssessmentResponse,
)
def update_risk_assessment(
    risk_assessment_id: UUID,
    risk_assessment: RiskAssessmentUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing Risk Assessment.
    """
    updated = service.update(
        db=db,
        obj_id=risk_assessment_id,
        obj_in=risk_assessment.model_dump(exclude_unset=True),
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk Assessment not found.",
        )

    return updated


@router.delete(
    "/{risk_assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_risk_assessment(
    risk_assessment_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a Risk Assessment.
    """
    deleted = service.delete(
        db=db,
        obj_id=risk_assessment_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk Assessment not found.",
        )

    return None
