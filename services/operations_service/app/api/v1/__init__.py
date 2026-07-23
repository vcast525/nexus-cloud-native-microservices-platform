from fastapi import APIRouter

from .audit_event import router as audit_event_router
from .deployment import router as deployment_router
from .incident import router as incident_router
from .issue import router as issue_router
from .maintenance_window import router as maintenance_window_router
from .notification import router as notification_router
from .risk_assessment import router as risk_assessment_router


api_router = APIRouter()

api_router.include_router(audit_event_router)
api_router.include_router(deployment_router)
api_router.include_router(incident_router)
api_router.include_router(issue_router)
api_router.include_router(maintenance_window_router)
api_router.include_router(notification_router)
api_router.include_router(risk_assessment_router)