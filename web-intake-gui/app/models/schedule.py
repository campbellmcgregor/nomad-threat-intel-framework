"""Scheduled report models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ScheduleFrequency(str, Enum):
    """Schedule frequency options."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ScheduledReportCreate(BaseModel):
    """Schema for creating a scheduled report."""
    
    name: str = Field(..., min_length=1, max_length=200)
    report_type: str = Field(..., description="Type of report to generate")
    frequency: ScheduleFrequency
    
    # Schedule timing
    hour: int = Field(9, ge=0, le=23, description="Hour to run (UTC)")
    minute: int = Field(0, ge=0, le=59, description="Minute to run")
    day_of_week: Optional[int] = Field(None, ge=0, le=6, description="Day of week (0=Monday) for weekly")
    day_of_month: Optional[int] = Field(None, ge=1, le=28, description="Day of month for monthly")
    
    # Delivery
    recipients: list[str] = Field(default_factory=list, description="Email recipients")
    publish_to_gui: bool = Field(True, description="Also publish to Web GUI")
    
    # Report options
    time_window_hours: int = Field(168, description="Hours of data to include")
    include_pdf: bool = Field(True)
    
    enabled: bool = True


class ScheduledReport(BaseModel):
    """Full scheduled report model."""
    
    id: str
    name: str
    report_type: str
    frequency: ScheduleFrequency
    hour: int
    minute: int
    day_of_week: Optional[int]
    day_of_month: Optional[int]
    recipients: list[str]
    publish_to_gui: bool
    time_window_hours: int
    include_pdf: bool
    enabled: bool
    
    # Tracking
    created_at: datetime
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    run_count: int = 0
    last_status: Optional[str] = None
    
    class Config:
        from_attributes = True


class ScheduledReportResponse(BaseModel):
    """Response after creating a scheduled report."""
    
    id: str
    next_run: Optional[datetime]
