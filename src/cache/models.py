"""SQLite cache data models for NOMAD threat intelligence."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json


@dataclass
class ThreatRecord:
    """Threat intelligence record stored in SQLite cache."""
    
    id: str
    source_type: str  # rss, vendor, cert
    source_name: str
    source_url: str
    title: str
    summary: str
    published_utc: datetime
    collected_utc: datetime
    
    # CVE data
    cves: list[str] = field(default_factory=list)
    
    # Enrichment data
    cvss_v3: Optional[float] = None
    epss_score: Optional[float] = None
    epss_percentile: Optional[float] = None
    kev_listed: bool = False
    exploit_status: Optional[str] = None  # ITW, PoC, None
    
    # Admiralty ratings
    admiralty_source_reliability: str = "C"  # A-F
    admiralty_info_credibility: int = 3  # 1-6
    
    # Processing metadata
    priority_level: str = "medium"  # critical, high, medium, low, watchlist
    risk_score: float = 0.0
    
    # Verification
    verification_confidence: Optional[float] = None
    verification_method: Optional[str] = None
    verification_timestamp: Optional[datetime] = None
    
    # Crown jewel correlation
    affected_crown_jewels: list[str] = field(default_factory=list)
    asset_exposure_match: list[str] = field(default_factory=list)
    
    # Deduplication
    dedupe_key: str = ""
    
    # Full-text search content
    search_content: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "source_type": self.source_type,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "title": self.title,
            "summary": self.summary,
            "published_utc": self.published_utc.isoformat() if self.published_utc else None,
            "collected_utc": self.collected_utc.isoformat() if self.collected_utc else None,
            "cves": self.cves,
            "cvss_v3": self.cvss_v3,
            "epss_score": self.epss_score,
            "epss_percentile": self.epss_percentile,
            "kev_listed": self.kev_listed,
            "exploit_status": self.exploit_status,
            "admiralty_source_reliability": self.admiralty_source_reliability,
            "admiralty_info_credibility": self.admiralty_info_credibility,
            "priority_level": self.priority_level,
            "risk_score": self.risk_score,
            "verification_confidence": self.verification_confidence,
            "verification_method": self.verification_method,
            "verification_timestamp": self.verification_timestamp.isoformat() if self.verification_timestamp else None,
            "affected_crown_jewels": self.affected_crown_jewels,
            "asset_exposure_match": self.asset_exposure_match,
            "dedupe_key": self.dedupe_key,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ThreatRecord":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            source_type=data.get("source_type", "rss"),
            source_name=data.get("source_name", ""),
            source_url=data.get("source_url", ""),
            title=data.get("title", ""),
            summary=data.get("summary", ""),
            published_utc=datetime.fromisoformat(data["published_utc"]) if data.get("published_utc") else datetime.utcnow(),
            collected_utc=datetime.fromisoformat(data["collected_utc"]) if data.get("collected_utc") else datetime.utcnow(),
            cves=data.get("cves", []),
            cvss_v3=data.get("cvss_v3"),
            epss_score=data.get("epss_score"),
            epss_percentile=data.get("epss_percentile"),
            kev_listed=data.get("kev_listed", False),
            exploit_status=data.get("exploit_status"),
            admiralty_source_reliability=data.get("admiralty_source_reliability", "C"),
            admiralty_info_credibility=data.get("admiralty_info_credibility", 3),
            priority_level=data.get("priority_level", "medium"),
            risk_score=data.get("risk_score", 0.0),
            verification_confidence=data.get("verification_confidence"),
            verification_method=data.get("verification_method"),
            verification_timestamp=datetime.fromisoformat(data["verification_timestamp"]) if data.get("verification_timestamp") else None,
            affected_crown_jewels=data.get("affected_crown_jewels", []),
            asset_exposure_match=data.get("asset_exposure_match", []),
            dedupe_key=data.get("dedupe_key", ""),
            search_content=f"{data.get('title', '')} {data.get('summary', '')} {' '.join(data.get('cves', []))}",
        )


@dataclass
class CVERecord:
    """CVE enrichment cache record."""
    
    cve_id: str
    cvss_v3_score: Optional[float] = None
    cvss_v3_vector: Optional[str] = None
    cvss_v4_score: Optional[float] = None
    epss_score: Optional[float] = None
    epss_percentile: Optional[float] = None
    kev_listed: bool = False
    kev_date_added: Optional[datetime] = None
    kev_due_date: Optional[datetime] = None
    description: str = ""
    affected_products: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    published_date: Optional[datetime] = None
    last_modified: Optional[datetime] = None
    cached_at: datetime = field(default_factory=datetime.utcnow)
    cache_expires: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "cve_id": self.cve_id,
            "cvss_v3_score": self.cvss_v3_score,
            "cvss_v3_vector": self.cvss_v3_vector,
            "cvss_v4_score": self.cvss_v4_score,
            "epss_score": self.epss_score,
            "epss_percentile": self.epss_percentile,
            "kev_listed": self.kev_listed,
            "kev_date_added": self.kev_date_added.isoformat() if self.kev_date_added else None,
            "kev_due_date": self.kev_due_date.isoformat() if self.kev_due_date else None,
            "description": self.description,
            "affected_products": self.affected_products,
            "references": self.references,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "cached_at": self.cached_at.isoformat(),
        }


@dataclass
class VerificationRecord:
    """Threat verification cache record."""
    
    threat_id: str
    verified: bool = False
    confidence_score: float = 0.0
    verification_method: str = "structured"  # structured, jina, hybrid
    sources_consulted: list[str] = field(default_factory=list)
    nvd_match: bool = False
    cisa_kev_match: bool = False
    vendor_advisory_match: bool = False
    web_sources_count: int = 0
    verified_at: datetime = field(default_factory=datetime.utcnow)
    cache_expires: Optional[datetime] = None
    cost_usd: float = 0.0
    
    def to_dict(self) -> dict:
        return {
            "threat_id": self.threat_id,
            "verified": self.verified,
            "confidence_score": self.confidence_score,
            "verification_method": self.verification_method,
            "sources_consulted": self.sources_consulted,
            "nvd_match": self.nvd_match,
            "cisa_kev_match": self.cisa_kev_match,
            "vendor_advisory_match": self.vendor_advisory_match,
            "web_sources_count": self.web_sources_count,
            "verified_at": self.verified_at.isoformat(),
            "cost_usd": self.cost_usd,
        }


@dataclass
class FeedMetric:
    """Feed quality metrics record."""
    
    feed_name: str
    feed_url: str
    
    # Accessibility metrics
    last_check: datetime = field(default_factory=datetime.utcnow)
    last_success: Optional[datetime] = None
    response_time_ms: int = 0
    http_status: int = 0
    error_count_24h: int = 0
    
    # Content metrics
    items_collected_24h: int = 0
    items_collected_7d: int = 0
    security_relevance_score: float = 0.0
    duplicate_rate: float = 0.0
    avg_cves_per_item: float = 0.0
    
    # Quality scores
    accessibility_score: float = 100.0
    relevance_score: float = 50.0
    timeliness_score: float = 50.0
    uniqueness_score: float = 100.0
    overall_score: float = 75.0
    
    def to_dict(self) -> dict:
        return {
            "feed_name": self.feed_name,
            "feed_url": self.feed_url,
            "last_check": self.last_check.isoformat(),
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "response_time_ms": self.response_time_ms,
            "http_status": self.http_status,
            "error_count_24h": self.error_count_24h,
            "items_collected_24h": self.items_collected_24h,
            "items_collected_7d": self.items_collected_7d,
            "security_relevance_score": self.security_relevance_score,
            "duplicate_rate": self.duplicate_rate,
            "avg_cves_per_item": self.avg_cves_per_item,
            "accessibility_score": self.accessibility_score,
            "relevance_score": self.relevance_score,
            "timeliness_score": self.timeliness_score,
            "uniqueness_score": self.uniqueness_score,
            "overall_score": self.overall_score,
        }
