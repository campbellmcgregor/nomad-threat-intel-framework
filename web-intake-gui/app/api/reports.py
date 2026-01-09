"""Report API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import verify_api_token
from app.models.report import (
    Report,
    ReportCreate,
    ReportResponse,
    ReportType,
)
from app.services.report_service import ReportService

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.post(
    "",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_token)],
)
async def create_report(
    report_data: ReportCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new threat intelligence report.

    Requires API token authentication.
    """
    service = ReportService(db)
    report = await service.create(report_data)

    return ReportResponse(
        id=report.id,
        created_at=report.created_at,
    )


@router.get(
    "",
    response_model=list[Report],
    dependencies=[Depends(verify_api_token)],
)
async def list_reports(
    report_type: ReportType | None = Query(None, description="Filter by report type"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of reports"),
    offset: int = Query(0, ge=0, description="Number of reports to skip"),
    db: AsyncSession = Depends(get_db),
):
    """
    List all reports with optional filtering.

    Requires API token authentication.
    """
    service = ReportService(db)
    return await service.list(report_type=report_type, limit=limit, offset=offset)


@router.get(
    "/{report_id}",
    response_model=Report,
    dependencies=[Depends(verify_api_token)],
)
async def get_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific report by ID.

    Requires API token authentication.
    """
    service = ReportService(db)
    report = await service.get(report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    return report


@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_token)],
)
async def delete_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a report and all its share links.

    Requires API token authentication.
    """
    service = ReportService(db)
    deleted = await service.delete(report_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )


@router.get(
    "/{report_id}/stats",
    dependencies=[Depends(verify_api_token)],
)
async def get_report_stats(
    report_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get statistics for a report including share link views.

    Requires API token authentication.
    """
    from app.services.share_service import ShareService

    report_service = ReportService(db)
    report = await report_service.get(report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    share_service = ShareService(db)
    share_links = await share_service.list_for_report(report_id)

    total_views = sum(link.view_count for link in share_links)
    active_links = sum(
        1 for link in share_links
        if link.expires_at is None or link.expires_at > report.created_at
    )

    return {
        "report_id": report_id,
        "total_share_links": len(share_links),
        "active_share_links": active_links,
        "total_views": total_views,
    }
