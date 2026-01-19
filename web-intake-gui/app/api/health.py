"""Health check endpoints."""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint."""
    # Check database connectivity
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": db_status,
        },
    }


@router.get("/health/ready")
async def readiness_check():
    """Readiness probe for Kubernetes/Docker."""
    return {"ready": True}


@router.get("/health/live")
async def liveness_check():
    """Liveness probe for Kubernetes/Docker."""
    return {"alive": True}
