from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.audit_event import (
    AuditEventCreate,
    AuditEventResponse,
    AuditEventUpdate,
)
from ...services.audit_event_service import AuditEventService


router = APIRouter(
    prefix="/audit-events",
    tags=["Audit Events"],
)


@router.get(
    "/",
    response_model=list[AuditEventResponse],
    summary="Get all audit events",
)
def get_audit_events(
    db: Session = Depends(get_db),
):
    service = AuditEventService()
    return service.get_all(
        db=db,
    )

@router.get(
    "/{audit_event_id}",
    response_model=AuditEventResponse,
    summary="Get audit event by ID",
)
def get_audit_event(
    audit_event_id: UUID,
    db: Session = Depends(get_db),
):
    service = AuditEventService()

    audit_event = service.get_by_id(
        db=db,
        entity_id=audit_event_id,
    )

    if not audit_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit event not found",
        )

    return audit_event


@router.post(
    "/",
    response_model=AuditEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create audit event",
)
def create_audit_event(
    audit_event: AuditEventCreate,
    db: Session = Depends(get_db),
):
    service = AuditEventService()
    return service.create(
        db=db,
        obj_in=audit_event.model_dump(),
    )


@router.put(
    "/{audit_event_id}",
    response_model=AuditEventResponse,
    summary="Update audit event",
)
def update_audit_event(
    audit_event_id: UUID,
    audit_event: AuditEventUpdate,
    db: Session = Depends(get_db),
):
    service = AuditEventService()

    updated_audit_event = service.update(
        db=db,
        entity_id=audit_event_id,
        obj_in=audit_event.model_dump(
            exclude_unset=True,
        ),
    )

    if not updated_audit_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit event not found",
        )

    return updated_audit_event


@router.delete(
    "/{audit_event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete audit event",
)
def delete_audit_event(
    audit_event_id: UUID,
    db: Session = Depends(get_db),
):
    service = AuditEventService()

    deleted = service.delete(
        db=db,
        entity_id=audit_event_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit event not found",
        )

    return None