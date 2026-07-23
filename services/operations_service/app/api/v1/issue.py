"""
issue.py

FastAPI routes for Issue operations.
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
from ...schemas.issue import (
    IssueCreate,
    IssuePageResponse,
    IssueResponse,
    IssueUpdate,
)
from ...services.issue_service import IssueService


router = APIRouter(
    prefix="/issues",
    tags=["Issues"],
)

issue_service = IssueService()


@router.get(
    "/",
    response_model=IssuePageResponse,
    summary="Get paginated Issues",
)
def get_issues(
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
    Return a paginated collection of Issues.
    """

    return issue_service.paginate(
        db=db,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/open",
    response_model=list[IssueResponse],
    summary="Get open Issues",
)
def get_open_issues(
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
    Return Issues that have not reached a terminal status.
    """

    return issue_service.get_open_issues(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/overdue",
    response_model=list[IssueResponse],
    summary="Get overdue Issues",
)
def get_overdue_issues(
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
    Return Issues currently marked as overdue.
    """

    return issue_service.get_overdue_issues(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/number/{issue_number}",
    response_model=IssueResponse,
    summary="Get an Issue by issue number",
)
def get_issue_by_number(
    issue_number: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve an Issue using its business issue number.
    """

    issue = issue_service.get_by_issue_number(
        db=db,
        issue_number=issue_number,
    )

    if issue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Issue number '{issue_number}' was not found."
            ),
        )

    return issue


@router.get(
    "/service/{service_id}",
    response_model=list[IssueResponse],
    summary="Get Issues by Service",
)
def get_issues_by_service(
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
    Return Issues associated with a Service.
    """

    return issue_service.get_by_service(
        db=db,
        service_id=service_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/incident/{incident_id}",
    response_model=list[IssueResponse],
    summary="Get Issues by Incident",
)
def get_issues_by_incident(
    incident_id: UUID,
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
    Return Issues associated with an Incident.
    """

    return issue_service.get_by_incident(
        db=db,
        incident_id=incident_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/status/{issue_status}",
    response_model=list[IssueResponse],
    summary="Get Issues by status",
)
def get_issues_by_status(
    issue_status: str,
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
    Return Issues matching a status.
    """

    return issue_service.get_by_status(
        db=db,
        issue_status=issue_status,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/priority/{priority}",
    response_model=list[IssueResponse],
    summary="Get Issues by priority",
)
def get_issues_by_priority(
    priority: str,
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
    Return Issues matching a priority.
    """

    return issue_service.get_by_priority(
        db=db,
        priority=priority,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{issue_id}",
    response_model=IssueResponse,
    summary="Get an Issue by ID",
)
def get_issue(
    issue_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve one Issue by primary key.
    """

    issue = issue_service.get_by_id(
        db=db,
        entity_id=issue_id,
    )

    if issue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Issue with id '{issue_id}' was not found."
            ),
        )

    return issue


@router.post(
    "/",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an Issue",
)
def create_issue(
    issue_in: IssueCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new Issue.
    """

    try:
        return issue_service.create_issue(
            db=db,
            obj_in=issue_in.model_dump(
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
                "The Issue could not be created. Verify that its "
                "Service and optional Incident exist and that all "
                "unique values are valid."
            ),
        ) from exc


@router.patch(
    "/{issue_id}",
    response_model=IssueResponse,
    summary="Update an Issue",
)
def update_issue(
    issue_id: UUID,
    issue_in: IssueUpdate,
    db: Session = Depends(get_db),
):
    """
    Partially update an existing Issue.
    """

    update_data = issue_in.model_dump(
        exclude_unset=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Issue fields were provided for update.",
        )

    try:
        return issue_service.update(
            db=db,
            entity_id=issue_id,
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
                "The Issue could not be updated because the requested "
                "values violate a database constraint."
            ),
        ) from exc


@router.delete(
    "/{issue_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an Issue",
)
def delete_issue(
    issue_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete an Issue by primary key.
    """

    deleted = issue_service.delete(
        db=db,
        entity_id=issue_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Issue with id '{issue_id}' was not found."
            ),
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
