"""Authentication utilities."""

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import get_settings

security = HTTPBearer()


async def verify_api_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> str:
    """
    Verify API token from Authorization header.

    Returns the token if valid, raises HTTPException if not.
    """
    settings = get_settings()

    if not settings.api_token:
        # No token configured - reject all requests
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API token not configured on server",
        )

    if credentials.credentials != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials
