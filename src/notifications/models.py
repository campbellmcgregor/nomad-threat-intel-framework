"""Notification data models."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class AlertPriority(Enum):
    """Alert priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class DeliveryStatus(Enum):
    """Delivery status codes."""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"
    QUEUED = "queued"


@dataclass
class Alert:
    """Threat alert for notification dispatch."""
    
    id: str
    title: str
    summary: str
    priority: AlertPriority
    
    # Threat details
    cves: list[str] = field(default_factory=list)
    cvss_score: Optional[float] = None
    epss_score: Optional[float] = None
    kev_listed: bool = False
    exploit_status: Optional[str] = None
    
    # Context
    affected_crown_jewels: list[str] = field(default_factory=list)
    source_name: str = ""
    source_url: str = ""
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    threat_id: Optional[str] = None
    report_url: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "priority": self.priority.value,
            "cves": self.cves,
            "cvss_score": self.cvss_score,
            "epss_score": self.epss_score,
            "kev_listed": self.kev_listed,
            "exploit_status": self.exploit_status,
            "affected_crown_jewels": self.affected_crown_jewels,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "created_at": self.created_at.isoformat(),
            "threat_id": self.threat_id,
            "report_url": self.report_url,
        }
    
    def get_severity_emoji(self) -> str:
        """Get emoji for alert severity."""
        return {
            AlertPriority.CRITICAL: "🔴",
            AlertPriority.HIGH: "🟠",
            AlertPriority.MEDIUM: "🟡",
            AlertPriority.LOW: "🟢",
            AlertPriority.INFO: "🔵",
        }.get(self.priority, "⚪")
    
    def get_severity_color(self) -> str:
        """Get hex color for alert severity."""
        return {
            AlertPriority.CRITICAL: "#dc2626",
            AlertPriority.HIGH: "#ea580c",
            AlertPriority.MEDIUM: "#ca8a04",
            AlertPriority.LOW: "#16a34a",
            AlertPriority.INFO: "#2563eb",
        }.get(self.priority, "#6b7280")


@dataclass
class DeliveryResult:
    """Result of alert delivery attempt."""
    
    alert_id: str
    channel: str
    status: DeliveryStatus
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    # Response details
    response_code: Optional[int] = None
    response_message: str = ""
    
    # Retry info
    retry_count: int = 0
    next_retry: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "alert_id": self.alert_id,
            "channel": self.channel,
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "response_code": self.response_code,
            "response_message": self.response_message,
            "retry_count": self.retry_count,
            "next_retry": self.next_retry.isoformat() if self.next_retry else None,
        }


@dataclass
class NotificationRule:
    """Rule for routing alerts to channels."""
    
    name: str
    condition: str  # Expression like "kev_listed == true"
    channels: list[str]
    priority: AlertPriority
    enabled: bool = True
    
    def matches(self, alert: Alert) -> bool:
        """Check if alert matches this rule's condition."""
        # Simple condition evaluation
        condition = self.condition.lower().strip()
        
        if "kev_listed" in condition and "true" in condition:
            return alert.kev_listed
        
        if "cvss" in condition:
            if ">=" in condition:
                threshold = float(condition.split(">=")[1].strip())
                return (alert.cvss_score or 0) >= threshold
            elif ">" in condition:
                threshold = float(condition.split(">")[1].strip())
                return (alert.cvss_score or 0) > threshold
        
        if "epss" in condition:
            if ">=" in condition:
                threshold = float(condition.split(">=")[1].strip())
                return (alert.epss_score or 0) >= threshold
        
        if "crown_jewels" in condition or "affected_crown_jewels" in condition:
            return len(alert.affected_crown_jewels) > 0
        
        return False


@dataclass
class RateLimitConfig:
    """Rate limit configuration for a priority level."""
    
    priority: AlertPriority
    max_per_hour: int = -1  # -1 = unlimited
    max_per_day: int = -1
    current_hour_count: int = 0
    current_day_count: int = 0
    hour_reset: Optional[datetime] = None
    day_reset: Optional[datetime] = None
    
    def is_allowed(self) -> bool:
        """Check if sending is allowed under rate limits."""
        now = datetime.utcnow()
        
        # Reset counters if needed
        if self.hour_reset and now >= self.hour_reset:
            self.current_hour_count = 0
            self.hour_reset = None
        
        if self.day_reset and now >= self.day_reset:
            self.current_day_count = 0
            self.day_reset = None
        
        # Check limits
        if self.max_per_hour > 0 and self.current_hour_count >= self.max_per_hour:
            return False
        
        if self.max_per_day > 0 and self.current_day_count >= self.max_per_day:
            return False
        
        return True
    
    def record_send(self):
        """Record that an alert was sent."""
        from datetime import timedelta
        
        now = datetime.utcnow()
        self.current_hour_count += 1
        self.current_day_count += 1
        
        if not self.hour_reset:
            self.hour_reset = now + timedelta(hours=1)
        
        if not self.day_reset:
            self.day_reset = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
