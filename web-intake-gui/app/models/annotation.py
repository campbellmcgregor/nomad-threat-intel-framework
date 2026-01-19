"""Threat annotation and status tracking models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ThreatStatus(str, Enum):
    """Threat handling status."""
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    MITIGATING = "mitigating"
    MITIGATED = "mitigated"
    FALSE_POSITIVE = "false_positive"
    ACCEPTED_RISK = "accepted_risk"


class AnnotationCreate(BaseModel):
    """Schema for creating an annotation."""
    
    threat_id: str = Field(..., description="ID of the threat being annotated")
    content: str = Field(..., min_length=1, max_length=5000, description="Annotation text (markdown supported)")
    is_internal: bool = Field(True, description="Internal note vs shared comment")


class Annotation(BaseModel):
    """Threat annotation model."""
    
    id: str
    threat_id: str
    content: str
    is_internal: bool
    
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ThreatStatusUpdate(BaseModel):
    """Schema for updating threat status."""
    
    threat_id: str
    status: ThreatStatus
    note: Optional[str] = Field(None, max_length=1000, description="Optional note about status change")
    assigned_to: Optional[str] = Field(None, description="Assignee email/name")
    due_date: Optional[datetime] = Field(None, description="Due date for remediation")


class ThreatStatusHistory(BaseModel):
    """Threat status history entry."""
    
    id: str
    threat_id: str
    old_status: Optional[ThreatStatus]
    new_status: ThreatStatus
    note: Optional[str]
    changed_by: Optional[str]
    changed_at: datetime


class RemediationChecklist(BaseModel):
    """Remediation checklist for a threat."""
    
    threat_id: str
    items: list["ChecklistItem"]
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    @property
    def completion_percentage(self) -> float:
        if not self.items:
            return 0.0
        completed = sum(1 for item in self.items if item.completed)
        return (completed / len(self.items)) * 100


class ChecklistItem(BaseModel):
    """Single checklist item."""
    
    id: str
    description: str
    completed: bool = False
    completed_by: Optional[str] = None
    completed_at: Optional[datetime] = None
    order: int = 0
