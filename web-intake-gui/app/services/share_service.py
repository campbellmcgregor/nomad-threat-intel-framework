"""Share link management service."""

import secrets
from datetime import datetime, timedelta

from passlib.hash import bcrypt
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import ShareLinkDB, ReportDB
from app.models.share import ShareLink, ShareLinkCreate
from app.config import get_settings


class ShareService:
    """Service for managing share links."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()

    def generate_token(self) -> str:
        """Generate a unique share token."""
        return f"sh_{secrets.token_urlsafe(self.settings.share_token_length)}"

    @staticmethod
    def generate_id() -> str:
        """Generate a unique share link ID."""
        return f"shl_{secrets.token_urlsafe(16)}"

    async def create(
        self, report_id: str, share_data: ShareLinkCreate, base_url: str
    ) -> tuple[ShareLink, str] | None:
        """Create a new share link. Returns (ShareLink, share_url) or None if report not found."""
        # Verify report exists
        result = await self.db.execute(
            select(ReportDB).where(ReportDB.id == report_id)
        )
        if result.scalar_one_or_none() is None:
            return None

        share_id = self.generate_id()
        token = self.generate_token()
        now = datetime.utcnow()

        # Calculate expiry
        expires_at = None
        if share_data.expires_hours is not None:
            expires_at = now + timedelta(hours=share_data.expires_hours)

        # Hash password if provided
        password_hash = None
        if share_data.password:
            password_hash = bcrypt.hash(share_data.password)

        db_share = ShareLinkDB(
            id=share_id,
            report_id=report_id,
            token=token,
            password_hash=password_hash,
            allow_download=share_data.allow_download,
            expires_at=expires_at,
            created_at=now,
        )

        self.db.add(db_share)
        await self.db.commit()
        await self.db.refresh(db_share)

        share_link = self._to_model(db_share)
        share_url = f"{base_url.rstrip('/')}/s/{token}"

        return share_link, share_url

    async def get_by_token(self, token: str) -> ShareLink | None:
        """Get a share link by token."""
        result = await self.db.execute(
            select(ShareLinkDB).where(ShareLinkDB.token == token)
        )
        db_share = result.scalar_one_or_none()

        if db_share is None:
            return None

        return self._to_model(db_share)

    async def validate_and_get_report(
        self, token: str, password: str | None = None
    ) -> tuple[str, bool] | tuple[None, str]:
        """
        Validate share link and return report ID if valid.
        Returns (report_id, allow_download) on success, (None, error_message) on failure.
        """
        result = await self.db.execute(
            select(ShareLinkDB).where(ShareLinkDB.token == token)
        )
        db_share = result.scalar_one_or_none()

        if db_share is None:
            return None, "Share link not found"

        # Check expiry
        if db_share.expires_at and datetime.utcnow() > db_share.expires_at:
            return None, "Share link has expired"

        # Check password
        if db_share.password_hash:
            if not password:
                return None, "Password required"
            if not bcrypt.verify(password, db_share.password_hash):
                return None, "Invalid password"

        # Increment view count
        await self.db.execute(
            update(ShareLinkDB)
            .where(ShareLinkDB.id == db_share.id)
            .values(view_count=ShareLinkDB.view_count + 1)
        )
        await self.db.commit()

        return db_share.report_id, db_share.allow_download

    async def list_for_report(self, report_id: str) -> list[ShareLink]:
        """List all share links for a report."""
        result = await self.db.execute(
            select(ShareLinkDB).where(ShareLinkDB.report_id == report_id)
        )
        db_shares = result.scalars().all()
        return [self._to_model(s) for s in db_shares]

    async def delete(self, share_id: str) -> bool:
        """Delete a share link."""
        result = await self.db.execute(
            select(ShareLinkDB).where(ShareLinkDB.id == share_id)
        )
        db_share = result.scalar_one_or_none()

        if db_share is None:
            return False

        await self.db.delete(db_share)
        await self.db.commit()
        return True

    @staticmethod
    def _to_model(db_share: ShareLinkDB) -> ShareLink:
        """Convert database model to Pydantic model."""
        return ShareLink(
            id=db_share.id,
            report_id=db_share.report_id,
            token=db_share.token,
            password_hash=db_share.password_hash,
            allow_download=db_share.allow_download,
            expires_at=db_share.expires_at,
            created_at=db_share.created_at,
            view_count=db_share.view_count,
        )
