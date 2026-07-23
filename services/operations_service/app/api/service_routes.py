"""API routes for the Service Registry."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.service_schema import ServiceResponse
from app.services.service_service import ServiceService

router = APIRouter(
    prefix="/api/v1/services",
    tags=["Service Registry"],
)


@router.get(
    "/",
    response_model=list[ServiceResponse],
)
def get_services(
    db: Session = Depends(get_db),
):
    """Return all registered services."""

    service = ServiceService(db)

    return service.get_all_services()