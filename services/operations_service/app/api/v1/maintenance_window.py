from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.maintenance_window import (
    MaintenanceWindowCreate,
    MaintenanceWindowResponse,
    MaintenanceWindowUpdate,
)
from ...services.maintenance_window_service import (
    MaintenanceWindowService,
)


router = APIRouter(
    prefix="/maintenance-windows",
    tags=["Maintenance Windows"],
)


@router.get(
    "/",
    response_model=list[MaintenanceWindowResponse],
    summary="Get all maintenance windows",
)
def get_maintenance_windows(
    db: Session = Depends(get_db),
):
    service = MaintenanceWindowService()

    return service.get_all(
        db=db,
    )


@router.get(
    "/{maintenance_window_id}",
    response_model=MaintenanceWindowResponse,
    summary="Get maintenance window by ID",
)
def get_maintenance_window(
    maintenance_window_id: UUID,
    db: Session = Depends(get_db),
):
    service = MaintenanceWindowService()

    maintenance_window = service.get_by_id(
        db=db,
        entity_id=maintenance_window_id,
    )

    if maintenance_window is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance window not found",
        )

    return maintenance_window


@router.post(
    "/",
    response_model=MaintenanceWindowResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create maintenance window",
)
def create_maintenance_window(
    maintenance_window: MaintenanceWindowCreate,
    db: Session = Depends(get_db),
):
    service = MaintenanceWindowService()

    return service.create(
        db=db,
        obj_in=maintenance_window.model_dump(),
    )


@router.put(
    "/{maintenance_window_id}",
    response_model=MaintenanceWindowResponse,
    summary="Update maintenance window",
)
def update_maintenance_window(
    maintenance_window_id: UUID,
    maintenance_window: MaintenanceWindowUpdate,
    db: Session = Depends(get_db),
):
    service = MaintenanceWindowService()

    try:
        return service.update(
            db=db,
            entity_id=maintenance_window_id,
            obj_in=maintenance_window.model_dump(
                exclude_unset=True,
            ),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{maintenance_window_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete maintenance window",
)
def delete_maintenance_window(
    maintenance_window_id: UUID,
    db: Session = Depends(get_db),
):
    service = MaintenanceWindowService()

    deleted = service.delete(
        db=db,
        entity_id=maintenance_window_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance window not found",
        )

    return None