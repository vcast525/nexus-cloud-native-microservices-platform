from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.deployment import (
    DeploymentCreate,
    DeploymentResponse,
    DeploymentUpdate,
)
from ...services.deployment_service import DeploymentService


router = APIRouter(
    prefix="/deployments",
    tags=["Deployments"],
)


@router.get(
    "/",
    response_model=list[DeploymentResponse],
    summary="Get all deployments",
)
def get_deployments(
    db: Session = Depends(get_db),
):
    service = DeploymentService()

    return service.get_all(
        db=db,
    )


@router.get(
    "/{deployment_id}",
    response_model=DeploymentResponse,
    summary="Get deployment by ID",
)
def get_deployment(
    deployment_id: UUID,
    db: Session = Depends(get_db),
):
    service = DeploymentService()

    deployment = service.get_by_id(
        db=db,
        entity_id=deployment_id,
    )

    if deployment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found",
        )

    return deployment


@router.post(
    "/",
    response_model=DeploymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create deployment",
)
def create_deployment(
    deployment: DeploymentCreate,
    db: Session = Depends(get_db),
):
    service = DeploymentService()

    return service.create(
        db=db,
        obj_in=deployment.model_dump(),
    )


@router.put(
    "/{deployment_id}",
    response_model=DeploymentResponse,
    summary="Update deployment",
)
def update_deployment(
    deployment_id: UUID,
    deployment: DeploymentUpdate,
    db: Session = Depends(get_db),
):
    service = DeploymentService()

    try:
        return service.update(
            db=db,
            entity_id=deployment_id,
            obj_in=deployment.model_dump(
                exclude_unset=True,
            ),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{deployment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete deployment",
)
def delete_deployment(
    deployment_id: UUID,
    db: Session = Depends(get_db),
):
    service = DeploymentService()

    deleted = service.delete(
        db=db,
        entity_id=deployment_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found",
        )

    return None