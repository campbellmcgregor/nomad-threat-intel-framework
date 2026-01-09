"""Share link data models."""

from datetime import datetime

from pydantic import BaseModel, Field


class ShareLinkCreate(BaseModel):
    """Schema for creating a share link."""

    expires_hours: int | None = Field(
        72, description="Hours until link expires. Null for permanent."
    )
    password: str | None = Field(None, description="Optional password protection")
    allow_download: bool = Field(True, description="Allow PDF download")


class ShareLinkResponse(BaseModel):
    """Response after creating a share link."""

    share_token: str
    share_url: str
    expires_at: datetime | None


class ShareLink(BaseModel):
    """Full share link model."""

    id: str
    report_id: str
    token: str
    password_hash: str | None
    allow_download: bool
    expires_at: datetime | None
    created_at: datetime
    view_count: int = 0

    class Config:
        from_attributes = True
