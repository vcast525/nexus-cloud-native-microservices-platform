from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)
from ...services.notification_service import NotificationService


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "/",
    response_model=list[NotificationResponse],
    summary="Get all notifications",
)
def get_notifications(
    db: Session = Depends(get_db),
):
    service = NotificationService()
    return service.get_all(db=db)

@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Get notification by ID",
)
def get_notification(
    notification_id: UUID,
    db: Session = Depends(get_db),
):
    service = NotificationService()

    notification = service.get_by_id(
        db=db,
        entity_id=notification_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return notification


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create notification",
)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):
    service = NotificationService()
    return service.create(
        db=db,
        obj_in=notification.model_dump(),
    )


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Update notification",
)
def update_notification(
    notification_id: UUID,
    notification: NotificationUpdate,
    db: Session = Depends(get_db),
):
    service = NotificationService()

    updated_notification = service.update(
        db=db,
        entity_id=notification_id,
        obj_in=notification.model_dump(
            exclude_unset=True,
        ),
    )

    if not updated_notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return updated_notification


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete notification",
)
def delete_notification(
    notification_id: UUID,
    db: Session = Depends(get_db),
):
    service = NotificationService()

    deleted = service.delete(
        db=db,
        entity_id=notification_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return None