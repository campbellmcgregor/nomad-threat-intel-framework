"""Report data models."""

from datetime import datetime, date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator
import bleach


class ReportType(str, Enum):
    """Types of threat intelligence reports."""

    EXECUTIVE_BRIEF = "executive-brief"
    TECHNICAL_ALERT = "technical-alert"
    WEEKLY_SUMMARY = "weekly-summary"
    THREATS = "threats"
    CVE_ANALYSIS = "cve-analysis"
    CRITICAL = "critical"


class Classification(str, Enum):
    """Report classification levels."""

    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"


class ReportContent(BaseModel):
    """Report content container."""

    markdown: str = Field(..., description="Markdown formatted report content")
    html: str | None = Field(None, description="Pre-rendered HTML content")
    raw_data: dict[str, Any] | None = Field(None, description="Structured threat data")

    @model_validator(mode='after')
    def sanitize_content(self):
        """Sanitize markdown content to prevent XSS."""
        if self.markdown:
            self.markdown = bleach.clean(
                self.markdown,
                tags=bleach.sanitizer.ALLOWED_TAGS + [
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                    'p', 'br', 'hr', 
                    'ul', 'ol', 'li', 
                    'table', 'thead', 'tbody', 'tr', 'th', 'td',
                    'strong', 'b', 'em', 'i', 'u', 's', 'strike',
                    'code', 'pre', 'blockquote', 
                    'a', 'img'
                ],
                attributes={
                    'a': ['href', 'title', 'target'],
                    'img': ['src', 'alt', 'title', 'width', 'height'],
                    '*': ['class', 'id']
                },
                protocols=['http', 'https', 'mailto'],
                strip=True
            )
        return self


class ReportMetadata(BaseModel):
    """Report metadata."""

    period_start: date | None = None
    period_end: date | None = None
    threat_count: int | None = None
    critical_count: int | None = None
    high_count: int | None = None
    kev_count: int | None = None
    crown_jewels_affected: list[str] | None = None
    data_sources: list[str] | None = None
    cve_id: str | None = Field(None, description="CVE ID for CVE analysis reports")
    cvss_score: float | None = None
    epss_score: float | None = None


class ReportCreate(BaseModel):
    """Schema for creating a new report."""

    report_type: ReportType
    title: str = Field(..., min_length=1, max_length=500)
    organization: str = Field(..., min_length=1, max_length=200)
    content: ReportContent
    metadata: ReportMetadata | None = None
    classification: Classification = Classification.INTERNAL
    generated_at: datetime | None = None


class Report(BaseModel):
    """Full report model."""

    id: str
    report_type: ReportType
    title: str
    organization: str
    content: ReportContent
    metadata: ReportMetadata | None
    classification: Classification
    generated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    """Response after creating a report."""

    id: str
    created_at: datetime
