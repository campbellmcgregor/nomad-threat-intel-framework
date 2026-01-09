"""Share link API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import verify_api_token
from app.models.share import ShareLinkCreate, ShareLinkResponse
from app.services.share_service import ShareService
from app.services.report_service import ReportService
from app.services.pdf_service import PDFService

router = APIRouter(tags=["sharing"])


@router.post(
    "/api/v1/reports/{report_id}/share",
    response_model=ShareLinkResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_token)],
)
async def create_share_link(
    report_id: str,
    share_data: ShareLinkCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a share link for a report.

    Requires API token authentication.
    """
    service = ShareService(db)

    # Build base URL from request
    base_url = str(request.base_url).rstrip("/")

    result = await service.create(report_id, share_data, base_url)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    share_link, share_url = result

    return ShareLinkResponse(
        share_token=share_link.token,
        share_url=share_url,
        expires_at=share_link.expires_at,
    )


@router.get(
    "/api/v1/reports/{report_id}/shares",
    dependencies=[Depends(verify_api_token)],
)
async def list_share_links(
    report_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    List all share links for a report.

    Requires API token authentication.
    """
    service = ShareService(db)
    shares = await service.list_for_report(report_id)

    return [
        {
            "id": s.id,
            "token": s.token,
            "has_password": s.password_hash is not None,
            "allow_download": s.allow_download,
            "expires_at": s.expires_at,
            "created_at": s.created_at,
            "view_count": s.view_count,
        }
        for s in shares
    ]


@router.delete(
    "/api/v1/shares/{share_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_token)],
)
async def delete_share_link(
    share_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a share link.

    Requires API token authentication.
    """
    service = ShareService(db)
    deleted = await service.delete(share_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found",
        )


# Public endpoints (no auth required)


@router.get("/s/{token}", response_class=HTMLResponse)
async def view_shared_report(
    token: str,
    password: str | None = Query(None, description="Password for protected shares"),
    db: AsyncSession = Depends(get_db),
):
    """
    View a shared report. No authentication required.
    """
    share_service = ShareService(db)
    result = await share_service.validate_and_get_report(token, password)

    if result[0] is None:
        error_message = result[1]

        # If password required, show password form
        if error_message == "Password required":
            return _password_form_html(token)

        # Otherwise show error
        return _error_html(error_message)

    report_id, allow_download = result

    # Get the report
    report_service = ReportService(db)
    report = await report_service.get(report_id)

    if report is None:
        return _error_html("Report not found")

    # Render the report
    return _render_report_html(report, token, allow_download)


@router.get("/s/{token}/pdf")
async def download_shared_report_pdf(
    token: str,
    password: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Download shared report as PDF. No authentication required.
    """
    share_service = ShareService(db)
    result = await share_service.validate_and_get_report(token, password)

    if result[0] is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result[1],
        )

    report_id, allow_download = result

    if not allow_download:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="PDF download not allowed for this share link",
        )

    # Get the report
    report_service = ReportService(db)
    report = await report_service.get(report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    # Generate PDF
    pdf_service = PDFService()
    try:
        pdf_bytes = await pdf_service.generate_pdf(report)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    # Create filename
    safe_title = "".join(c for c in report.title if c.isalnum() or c in " -_")[:50]
    filename = f"{safe_title}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


def _password_form_html(token: str) -> str:
    """Generate password form HTML."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Required - NOMAD</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <div class="text-center mb-6">
            <div class="text-4xl mb-2">🔒</div>
            <h1 class="text-xl font-semibold text-gray-800">Password Required</h1>
            <p class="text-gray-600 mt-2">This report is protected. Enter the password to view.</p>
        </div>
        <form method="GET" action="/s/{token}">
            <input
                type="password"
                name="password"
                placeholder="Enter password"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                autofocus
            >
            <button
                type="submit"
                class="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
                View Report
            </button>
        </form>
    </div>
</body>
</html>"""


def _error_html(message: str) -> str:
    """Generate error page HTML."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - NOMAD</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full text-center">
        <div class="text-4xl mb-4">⚠️</div>
        <h1 class="text-xl font-semibold text-gray-800 mb-2">Unable to View Report</h1>
        <p class="text-gray-600">{message}</p>
    </div>
</body>
</html>"""


def _render_report_html(report, token: str, allow_download: bool) -> str:
    """Render report as HTML page."""
    from app.services.pdf_service import PDFService

    pdf_service = PDFService()
    content_html = report.content.html or pdf_service.markdown_to_html(report.content.markdown)

    # Build metadata display
    metadata_html = ""
    if report.metadata:
        meta = report.metadata
        meta_items = []

        if meta.period_start and meta.period_end:
            meta_items.append(f"<span><strong>Period:</strong> {meta.period_start} to {meta.period_end}</span>")

        if meta.threat_count is not None:
            meta_items.append(f"<span><strong>Threats:</strong> {meta.threat_count}</span>")

        if meta.critical_count is not None:
            meta_items.append(f"<span class='text-red-600'><strong>Critical:</strong> {meta.critical_count}</span>")

        if meta.high_count is not None:
            meta_items.append(f"<span class='text-orange-600'><strong>High:</strong> {meta.high_count}</span>")

        if meta.kev_count is not None:
            meta_items.append(f"<span class='text-red-700'><strong>KEV:</strong> {meta.kev_count}</span>")

        if meta.crown_jewels_affected:
            meta_items.append(f"<span><strong>Affected:</strong> {', '.join(meta.crown_jewels_affected)}</span>")

        if meta.cve_id:
            meta_items.append(f"<span><strong>CVE:</strong> {meta.cve_id}</span>")

        if meta.cvss_score is not None:
            cvss_class = "text-red-600" if meta.cvss_score >= 9.0 else "text-orange-600" if meta.cvss_score >= 7.0 else ""
            meta_items.append(f"<span class='{cvss_class}'><strong>CVSS:</strong> {meta.cvss_score}</span>")

        if meta.epss_score is not None:
            meta_items.append(f"<span><strong>EPSS:</strong> {meta.epss_score:.1%}</span>")

        if meta_items:
            metadata_html = f"""
            <div class="flex flex-wrap gap-4 text-sm text-gray-600 mb-6 p-4 bg-gray-50 rounded-lg">
                {' '.join(meta_items)}
            </div>
            """

    # Report type icons and names
    type_config = {
        "executive-brief": ("📈", "Executive Brief"),
        "technical-alert": ("🚨", "Technical Alert"),
        "weekly-summary": ("📅", "Weekly Summary"),
        "threats": ("🛡️", "Threat Report"),
        "cve-analysis": ("🔍", "CVE Analysis"),
        "critical": ("🔴", "Critical Alert"),
    }

    icon, type_name = type_config.get(report.report_type.value, ("📄", "Report"))

    # Classification colors
    class_colors = {
        "PUBLIC": "bg-green-100 text-green-800",
        "INTERNAL": "bg-yellow-100 text-yellow-800",
        "CONFIDENTIAL": "bg-red-100 text-red-800",
    }
    class_color = class_colors.get(report.classification.value, "bg-gray-100 text-gray-800")

    # Download button
    download_btn = ""
    if allow_download:
        download_btn = f"""
        <a href="/s/{token}/pdf" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Download PDF
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report.title} - NOMAD</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .prose h1 {{ font-size: 1.5rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #1e40af; }}
        .prose h2 {{ font-size: 1.25rem; font-weight: 600; margin-top: 1.25rem; margin-bottom: 0.5rem; color: #1e40af; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.25rem; }}
        .prose h3 {{ font-size: 1.1rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem; color: #374151; }}
        .prose p {{ margin: 0.75rem 0; line-height: 1.625; }}
        .prose ul, .prose ol {{ margin: 0.5rem 0; padding-left: 1.5rem; }}
        .prose li {{ margin: 0.25rem 0; }}
        .prose table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
        .prose th, .prose td {{ border: 1px solid #d1d5db; padding: 0.5rem; text-align: left; }}
        .prose th {{ background: #f3f4f6; font-weight: 600; }}
        .prose code {{ background: #f3f4f6; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.875rem; }}
        .prose pre {{ background: #1f2937; color: #f9fafb; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; }}
        .prose pre code {{ background: none; padding: 0; color: inherit; }}
        .prose blockquote {{ border-left: 4px solid #2563eb; margin: 1rem 0; padding: 0.5rem 1rem; background: #eff6ff; }}
    </style>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="max-w-4xl mx-auto py-8 px-4">
        <!-- Header -->
        <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
            <div class="flex items-start justify-between">
                <div class="flex items-center space-x-3">
                    <span class="text-3xl">{icon}</span>
                    <div>
                        <span class="inline-block px-2 py-1 text-xs font-semibold rounded {class_color} mb-1">
                            {report.classification.value}
                        </span>
                        <h1 class="text-xl font-bold text-gray-900">{report.title}</h1>
                        <p class="text-sm text-gray-500">
                            {type_name} &bull; {report.organization} &bull; {report.generated_at.strftime("%B %d, %Y")}
                        </p>
                    </div>
                </div>
                {download_btn}
            </div>
        </div>

        <!-- Metadata -->
        {metadata_html}

        <!-- Content -->
        <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="prose max-w-none">
                {content_html}
            </div>
        </div>

        <!-- Footer -->
        <div class="text-center text-sm text-gray-500 mt-6">
            Powered by NOMAD Threat Intelligence Framework
        </div>
    </div>
</body>
</html>"""
