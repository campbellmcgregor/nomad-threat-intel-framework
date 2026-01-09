"""API routes for NOMAD Web Intake GUI."""

from app.api.reports import router as reports_router
from app.api.sharing import router as sharing_router
from app.api.health import router as health_router

__all__ = ["reports_router", "sharing_router", "health_router"]
