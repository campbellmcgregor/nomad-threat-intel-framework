"""API Key management models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ApiKeyScope(str, Enum):
    """API key permission scopes."""
    READ_ONLY = "read_only"
    REPORTS = "reports"
    ADMIN = "admin"


class ApiKeyCreate(BaseModel):
    """Schema for creating an API key."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Friendly name for the key")
    scope: ApiKeyScope = Field(ApiKeyScope.READ_ONLY, description="Permission scope")
    expires_days: Optional[int] = Field(None, ge=1, le=365, description="Days until expiration (null=never)")


class ApiKey(BaseModel):
    """API key model (without the actual key value)."""
    
    id: str
    name: str
    scope: ApiKeyScope
    key_prefix: str = Field(..., description="First 8 chars of key for identification")
    
    created_at: datetime
    expires_at: Optional[datetime]
    last_used: Optional[datetime]
    
    # Usage tracking
    request_count: int = 0
    is_active: bool = True
    
    class Config:
        from_attributes = True


class ApiKeyCreateResponse(BaseModel):
    """Response when creating an API key - includes the full key (shown only once)."""
    
    id: str
    name: str
    key: str = Field(..., description="Full API key - save this, it won't be shown again!")
    scope: ApiKeyScope
    expires_at: Optional[datetime]


class ApiKeyUsage(BaseModel):
    """API key usage statistics."""
    
    key_id: str
    date: datetime
    request_count: int
    endpoints: dict[str, int] = Field(default_factory=dict, description="Requests per endpoint")
