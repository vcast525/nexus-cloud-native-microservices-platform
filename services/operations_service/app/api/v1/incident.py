"""
incident.py

FastAPI routes for Incident operations.
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.incident import (
    IncidentCreate,
    IncidentPageResponse,
    IncidentResponse,
    IncidentUpdate,
)
from ...services.incident_service import IncidentService


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)

incident_service = IncidentService()


@router.get(
    "/",
    response_model=IncidentPageResponse,
    summary="Get paginated Incidents",
)
def get_incidents(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=25,
        ge=1,
        le=500,
    ),
    db: Session = Depends(get_db),
):
    """
    Return a paginated collection of Incidents.
    """

    return incident_service.paginate(
        db=db,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/open",
    response_model=list[IncidentResponse],
    summary="Get open Incidents",
)
def get_open_incidents(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    db: Session = Depends(get_db),
):
    """
    Return Incidents that have not reached a terminal status.
    """

    return incident_service.get_open_incidents(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/number/{incident_number}",
    response_model=IncidentResponse,
    summary="Get an Incident by incident number",
)
def get_incident_by_number(
    incident_number: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve an Incident using its business incident number.
    """

    incident = (
        incident_service.get_by_incident_number(
            db=db,
            incident_number=incident_number,
        )
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Incident number '{incident_number}' was not found."
            ),
        )

    return incident


@router.get(
    "/service/{service_id}",
    response_model=list[IncidentResponse],
    summary="Get Incidents by Service",
)
def get_incidents_by_service(
    service_id: UUID,
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    db: Session = Depends(get_db),
):
    """
    Return Incidents associated with a Service.
    """

    return incident_service.get_by_service(
        db=db,
        service_id=service_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/status/{incident_status}",
    response_model=list[IncidentResponse],
    summary="Get Incidents by status",
)
def get_incidents_by_status(
    incident_status: str,
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    db: Session = Depends(get_db),
):
    """
    Return Incidents matching a status.
    """

    return incident_service.get_by_status(
        db=db,
        incident_status=incident_status,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/severity/{severity}",
    response_model=list[IncidentResponse],
    summary="Get Incidents by severity",
)
def get_incidents_by_severity(
    severity: str,
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    db: Session = Depends(get_db),
):
    """
    Return Incidents matching a severity.
    """

    return incident_service.get_by_severity(
        db=db,
        severity=severity,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
    summary="Get an Incident by ID",
)
def get_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve one Incident by primary key.
    """

    incident = incident_service.get_by_id(
        db=db,
        entity_id=incident_id,
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Incident with id '{incident_id}' was not found."
            ),
        )

    return incident


@router.post(
    "/",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an Incident",
)
def create_incident(
    incident_in: IncidentCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new Incident.
    """

    try:
        return incident_service.create_incident(
            db=db,
            obj_in=incident_in.model_dump(
                exclude_none=True,
            ),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The Incident could not be created. Verify that "
                "the Service exists and all unique values are valid."
            ),
        ) from exc


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
    summary="Update an Incident",
)
def update_incident(
    incident_id: UUID,
    incident_in: IncidentUpdate,
    db: Session = Depends(get_db),
):
    """
    Partially update an existing Incident.
    """

    update_data = incident_in.model_dump(
        exclude_unset=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Incident fields were provided for update.",
        )

    try:
        return incident_service.update(
            db=db,
            entity_id=incident_id,
            obj_in=update_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The Incident could not be updated because the "
                "requested values violate a database constraint."
            ),
        ) from exc


@router.delete(
    "/{incident_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an Incident",
)
def delete_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete an Incident by primary key.
    """

    deleted = incident_service.delete(
        db=db,
        entity_id=incident_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Incident with id '{incident_id}' was not found."
            ),
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
