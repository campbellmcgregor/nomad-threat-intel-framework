"""PDF generation service."""

import markdown
import bleach
from pathlib import Path

from app.models.report import Report


class PDFService:
    """Service for generating PDF reports."""

    # Allowed HTML tags for sanitization
    ALLOWED_TAGS = [
        "h1", "h2", "h3", "h4", "h5", "h6",
        "p", "br", "hr",
        "ul", "ol", "li",
        "table", "thead", "tbody", "tr", "th", "td",
        "strong", "em", "b", "i", "u", "s",
        "code", "pre",
        "blockquote",
        "a", "img",
        "div", "span",
    ]

    ALLOWED_ATTRIBUTES = {
        "a": ["href", "title"],
        "img": ["src", "alt", "title"],
        "th": ["colspan", "rowspan"],
        "td": ["colspan", "rowspan"],
        "*": ["class", "id"],
    }

    def __init__(self):
        self.md = markdown.Markdown(
            extensions=[
                "tables",
                "fenced_code",
                "codehilite",
                "toc",
                "nl2br",
            ]
        )

    def markdown_to_html(self, md_content: str) -> str:
        """Convert markdown to sanitized HTML."""
        html = self.md.convert(md_content)
        self.md.reset()

        # Sanitize HTML
        clean_html = bleach.clean(
            html,
            tags=self.ALLOWED_TAGS,
            attributes=self.ALLOWED_ATTRIBUTES,
            strip=True,
        )

        return clean_html

    def generate_pdf_html(self, report: Report) -> str:
        """Generate full HTML document for PDF conversion."""
        content_html = report.content.html or self.markdown_to_html(report.content.markdown)

        # Build metadata section
        metadata_html = ""
        if report.metadata:
            meta = report.metadata
            meta_items = []

            if meta.period_start and meta.period_end:
                meta_items.append(f"<strong>Period:</strong> {meta.period_start} to {meta.period_end}")

            if meta.threat_count is not None:
                meta_items.append(f"<strong>Total Threats:</strong> {meta.threat_count}")

            if meta.critical_count is not None:
                meta_items.append(f"<strong>Critical:</strong> {meta.critical_count}")

            if meta.high_count is not None:
                meta_items.append(f"<strong>High:</strong> {meta.high_count}")

            if meta.kev_count is not None:
                meta_items.append(f"<strong>KEV Listed:</strong> {meta.kev_count}")

            if meta.crown_jewels_affected:
                meta_items.append(f"<strong>Affected Systems:</strong> {', '.join(meta.crown_jewels_affected)}")

            if meta.cve_id:
                meta_items.append(f"<strong>CVE:</strong> {meta.cve_id}")

            if meta.cvss_score is not None:
                meta_items.append(f"<strong>CVSS:</strong> {meta.cvss_score}")

            if meta.epss_score is not None:
                meta_items.append(f"<strong>EPSS:</strong> {meta.epss_score:.1%}")

            if meta_items:
                metadata_html = f"""
                <div class="metadata">
                    {' &nbsp;|&nbsp; '.join(meta_items)}
                </div>
                """

        # Report type display names
        type_names = {
            "executive-brief": "Executive Threat Intelligence Brief",
            "technical-alert": "Technical Security Alert",
            "weekly-summary": "Weekly Threat Summary",
            "threats": "Threat Intelligence Report",
            "cve-analysis": "CVE Analysis Report",
            "critical": "Critical Threat Alert",
        }

        report_type_name = type_names.get(report.report_type.value, report.report_type.value)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{report.title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #1a1a1a;
            max-width: 100%;
        }}

        .header {{
            border-bottom: 3px solid #2563eb;
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
        }}

        .header h1 {{
            margin: 0 0 0.5rem 0;
            font-size: 18pt;
            color: #1e40af;
        }}

        .header .subtitle {{
            color: #6b7280;
            font-size: 10pt;
        }}

        .classification {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: #fef3c7;
            color: #92400e;
            font-size: 9pt;
            font-weight: 600;
            border-radius: 4px;
            margin-bottom: 0.5rem;
        }}

        .classification.CONFIDENTIAL {{
            background: #fee2e2;
            color: #991b1b;
        }}

        .classification.PUBLIC {{
            background: #d1fae5;
            color: #065f46;
        }}

        .metadata {{
            background: #f3f4f6;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-size: 9pt;
            color: #4b5563;
            margin-bottom: 1.5rem;
        }}

        h1 {{ font-size: 16pt; color: #1e40af; margin-top: 1.5rem; }}
        h2 {{ font-size: 14pt; color: #1e40af; margin-top: 1.25rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.25rem; }}
        h3 {{ font-size: 12pt; color: #374151; margin-top: 1rem; }}
        h4 {{ font-size: 11pt; color: #374151; margin-top: 0.75rem; }}

        p {{ margin: 0.75rem 0; }}

        ul, ol {{ margin: 0.5rem 0; padding-left: 1.5rem; }}
        li {{ margin: 0.25rem 0; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 10pt;
        }}

        th, td {{
            border: 1px solid #d1d5db;
            padding: 0.5rem;
            text-align: left;
        }}

        th {{
            background: #f3f4f6;
            font-weight: 600;
        }}

        code {{
            background: #f3f4f6;
            padding: 0.125rem 0.375rem;
            border-radius: 3px;
            font-family: "SF Mono", Monaco, "Courier New", monospace;
            font-size: 9pt;
        }}

        pre {{
            background: #1f2937;
            color: #f9fafb;
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 9pt;
        }}

        pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}

        blockquote {{
            border-left: 4px solid #2563eb;
            margin: 1rem 0;
            padding: 0.5rem 1rem;
            background: #eff6ff;
            color: #1e40af;
        }}

        .critical {{ color: #dc2626; font-weight: 600; }}
        .high {{ color: #ea580c; font-weight: 600; }}
        .medium {{ color: #ca8a04; }}
        .low {{ color: #16a34a; }}

        .footer {{
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #e5e7eb;
            font-size: 9pt;
            color: #6b7280;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <span class="classification {report.classification.value}">{report.classification.value}</span>
        <h1>{report_type_name}</h1>
        <div class="subtitle">
            <strong>{report.organization}</strong> &nbsp;|&nbsp;
            Generated: {report.generated_at.strftime("%B %d, %Y at %H:%M UTC")}
        </div>
    </div>

    {metadata_html}

    <div class="content">
        {content_html}
    </div>

    <div class="footer">
        Generated by NOMAD Threat Intelligence Framework
    </div>
</body>
</html>"""

        return html

    async def generate_pdf(self, report: Report) -> bytes:
        """Generate PDF from report."""
        try:
            from weasyprint import HTML
        except ImportError:
            raise RuntimeError("WeasyPrint is not installed. Install with: pip install weasyprint")

        html_content = self.generate_pdf_html(report)
        html = HTML(string=html_content)
        return html.write_pdf()
