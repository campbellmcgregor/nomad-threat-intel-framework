"""Report management service."""

import secrets
from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import ReportDB
from app.models.report import (
    Report,
    ReportCreate,
    ReportContent,
    ReportMetadata,
    ReportType,
    Classification,
)


class ReportService:
    """Service for managing reports."""

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def generate_id() -> str:
        """Generate a unique report ID."""
        return f"rpt_{secrets.token_urlsafe(16)}"

    async def create(self, report_data: ReportCreate) -> Report:
        """Create a new report."""
        report_id = self.generate_id()
        now = datetime.utcnow()

        db_report = ReportDB(
            id=report_id,
            report_type=report_data.report_type.value,
            title=report_data.title,
            organization=report_data.organization,
            classification=report_data.classification.value,
            content_markdown=report_data.content.markdown,
            content_html=report_data.content.html,
            content_raw_data=report_data.content.raw_data,
            metadata_json=report_data.metadata.model_dump() if report_data.metadata else None,
            generated_at=report_data.generated_at or now,
            created_at=now,
        )

        self.db.add(db_report)
        await self.db.commit()
        await self.db.refresh(db_report)

        return self._to_model(db_report)

    async def get(self, report_id: str) -> Report | None:
        """Get a report by ID."""
        result = await self.db.execute(
            select(ReportDB).where(ReportDB.id == report_id)
        )
        db_report = result.scalar_one_or_none()

        if db_report is None:
            return None

        return self._to_model(db_report)

    async def list(
        self,
        report_type: ReportType | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Report]:
        """List reports with optional filtering."""
        query = select(ReportDB).order_by(desc(ReportDB.created_at))

        if report_type:
            query = query.where(ReportDB.report_type == report_type.value)

        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        db_reports = result.scalars().all()

        return [self._to_model(r) for r in db_reports]

    async def delete(self, report_id: str) -> bool:
        """Delete a report."""
        result = await self.db.execute(
            select(ReportDB).where(ReportDB.id == report_id)
        )
        db_report = result.scalar_one_or_none()

        if db_report is None:
            return False

        await self.db.delete(db_report)
        await self.db.commit()
        return True

    async def count(self, report_type: ReportType | None = None) -> int:
        """Count reports."""
        from sqlalchemy import func

        query = select(func.count(ReportDB.id))

        if report_type:
            query = query.where(ReportDB.report_type == report_type.value)

        result = await self.db.execute(query)
        return result.scalar() or 0

    @staticmethod
    def _to_model(db_report: ReportDB) -> Report:
        """Convert database model to Pydantic model."""
        return Report(
            id=db_report.id,
            report_type=ReportType(db_report.report_type),
            title=db_report.title,
            organization=db_report.organization,
            classification=Classification(db_report.classification),
            content=ReportContent(
                markdown=db_report.content_markdown,
                html=db_report.content_html,
                raw_data=db_report.content_raw_data,
            ),
            metadata=ReportMetadata(**db_report.metadata_json) if db_report.metadata_json else None,
            generated_at=db_report.generated_at,
            created_at=db_report.created_at,
        )
