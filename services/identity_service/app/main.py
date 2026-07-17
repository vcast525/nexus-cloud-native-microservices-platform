from fastapi import FastAPI

from app.api.auth import router as authentication_router


application = FastAPI(
    title="NEXUS Identity Service",
    description=(
        "Authentication, authorization, user identity, and role management "
        "for the NEXUS cloud-native platform."
    ),
    version="1.0.0",
)

application.include_router(authentication_router)


@application.get(
    "/health",
    tags=["System"],
    summary="Check Identity Service health",
)
def health_check() -> dict[str, str]:
    """Return a basic service health response."""

    return {
        "service": "NEXUS Identity Service",
        "status": "healthy",
    }


app = application
