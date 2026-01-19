"""SQLite cache database for NOMAD threat intelligence."""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from .models import ThreatRecord, CVERecord, VerificationRecord, FeedMetric


class CacheDatabase:
    """High-performance SQLite cache for threat intelligence data."""
    
    def __init__(self, db_path: str = "data/nomad.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    @contextmanager
    def _get_connection(self):
        """Get a database connection with proper settings."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        conn.execute("PRAGMA temp_store=MEMORY")
        try:
            yield conn
        finally:
            conn.close()
    
    def _init_db(self):
        """Initialize database schema with FTS5 for full-text search."""
        with self._get_connection() as conn:
            # Threats table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS threats (
                    id TEXT PRIMARY KEY,
                    source_type TEXT NOT NULL,
                    source_name TEXT NOT NULL,
                    source_url TEXT,
                    title TEXT NOT NULL,
                    summary TEXT,
                    published_utc TEXT NOT NULL,
                    collected_utc TEXT NOT NULL,
                    cves TEXT,  -- JSON array
                    cvss_v3 REAL,
                    epss_score REAL,
                    epss_percentile REAL,
                    kev_listed INTEGER DEFAULT 0,
                    exploit_status TEXT,
                    admiralty_source_reliability TEXT DEFAULT 'C',
                    admiralty_info_credibility INTEGER DEFAULT 3,
                    priority_level TEXT DEFAULT 'medium',
                    risk_score REAL DEFAULT 0.0,
                    verification_confidence REAL,
                    verification_method TEXT,
                    verification_timestamp TEXT,
                    affected_crown_jewels TEXT,  -- JSON array
                    asset_exposure_match TEXT,  -- JSON array
                    dedupe_key TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # FTS5 virtual table for full-text search
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS threats_fts USING fts5(
                    id,
                    title,
                    summary,
                    cves,
                    source_name,
                    content='threats',
                    content_rowid='rowid'
                )
            """)
            
            # Triggers to keep FTS in sync
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS threats_ai AFTER INSERT ON threats BEGIN
                    INSERT INTO threats_fts(rowid, id, title, summary, cves, source_name)
                    VALUES (NEW.rowid, NEW.id, NEW.title, NEW.summary, NEW.cves, NEW.source_name);
                END
            """)
            
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS threats_ad AFTER DELETE ON threats BEGIN
                    INSERT INTO threats_fts(threats_fts, rowid, id, title, summary, cves, source_name)
                    VALUES ('delete', OLD.rowid, OLD.id, OLD.title, OLD.summary, OLD.cves, OLD.source_name);
                END
            """)
            
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS threats_au AFTER UPDATE ON threats BEGIN
                    INSERT INTO threats_fts(threats_fts, rowid, id, title, summary, cves, source_name)
                    VALUES ('delete', OLD.rowid, OLD.id, OLD.title, OLD.summary, OLD.cves, OLD.source_name);
                    INSERT INTO threats_fts(rowid, id, title, summary, cves, source_name)
                    VALUES (NEW.rowid, NEW.id, NEW.title, NEW.summary, NEW.cves, NEW.source_name);
                END
            """)
            
            # CVE cache table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cve_cache (
                    cve_id TEXT PRIMARY KEY,
                    cvss_v3_score REAL,
                    cvss_v3_vector TEXT,
                    cvss_v4_score REAL,
                    epss_score REAL,
                    epss_percentile REAL,
                    kev_listed INTEGER DEFAULT 0,
                    kev_date_added TEXT,
                    kev_due_date TEXT,
                    description TEXT,
                    affected_products TEXT,  -- JSON array
                    references_json TEXT,  -- JSON array
                    published_date TEXT,
                    last_modified TEXT,
                    cached_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    cache_expires TEXT
                )
            """)
            
            # Verification cache table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS verification_cache (
                    threat_id TEXT PRIMARY KEY,
                    verified INTEGER DEFAULT 0,
                    confidence_score REAL DEFAULT 0.0,
                    verification_method TEXT,
                    sources_consulted TEXT,  -- JSON array
                    nvd_match INTEGER DEFAULT 0,
                    cisa_kev_match INTEGER DEFAULT 0,
                    vendor_advisory_match INTEGER DEFAULT 0,
                    web_sources_count INTEGER DEFAULT 0,
                    verified_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    cache_expires TEXT,
                    cost_usd REAL DEFAULT 0.0
                )
            """)
            
            # Feed metrics table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feed_metrics (
                    feed_url TEXT PRIMARY KEY,
                    feed_name TEXT NOT NULL,
                    last_check TEXT,
                    last_success TEXT,
                    response_time_ms INTEGER DEFAULT 0,
                    http_status INTEGER DEFAULT 0,
                    error_count_24h INTEGER DEFAULT 0,
                    items_collected_24h INTEGER DEFAULT 0,
                    items_collected_7d INTEGER DEFAULT 0,
                    security_relevance_score REAL DEFAULT 0.0,
                    duplicate_rate REAL DEFAULT 0.0,
                    avg_cves_per_item REAL DEFAULT 0.0,
                    accessibility_score REAL DEFAULT 100.0,
                    relevance_score REAL DEFAULT 50.0,
                    timeliness_score REAL DEFAULT 50.0,
                    uniqueness_score REAL DEFAULT 100.0,
                    overall_score REAL DEFAULT 75.0
                )
            """)
            
            # Indexes for fast lookups
            conn.execute("CREATE INDEX IF NOT EXISTS idx_threats_priority ON threats(priority_level)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_threats_published ON threats(published_utc DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_threats_kev ON threats(kev_listed)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_threats_cvss ON threats(cvss_v3 DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_threats_dedupe ON threats(dedupe_key)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cve_cache_expires ON cve_cache(cache_expires)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_verification_expires ON verification_cache(cache_expires)")
            
            conn.commit()
    
    # ==================== THREAT OPERATIONS ====================
    
    def upsert_threat(self, threat: ThreatRecord) -> bool:
        """Insert or update a threat record."""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO threats (
                    id, source_type, source_name, source_url, title, summary,
                    published_utc, collected_utc, cves, cvss_v3, epss_score,
                    epss_percentile, kev_listed, exploit_status,
                    admiralty_source_reliability, admiralty_info_credibility,
                    priority_level, risk_score, verification_confidence,
                    verification_method, verification_timestamp,
                    affected_crown_jewels, asset_exposure_match, dedupe_key,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET
                    source_type = excluded.source_type,
                    source_name = excluded.source_name,
                    source_url = excluded.source_url,
                    title = excluded.title,
                    summary = excluded.summary,
                    cves = excluded.cves,
                    cvss_v3 = excluded.cvss_v3,
                    epss_score = excluded.epss_score,
                    epss_percentile = excluded.epss_percentile,
                    kev_listed = excluded.kev_listed,
                    exploit_status = excluded.exploit_status,
                    priority_level = excluded.priority_level,
                    risk_score = excluded.risk_score,
                    verification_confidence = excluded.verification_confidence,
                    verification_method = excluded.verification_method,
                    verification_timestamp = excluded.verification_timestamp,
                    affected_crown_jewels = excluded.affected_crown_jewels,
                    asset_exposure_match = excluded.asset_exposure_match,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                threat.id, threat.source_type, threat.source_name, threat.source_url,
                threat.title, threat.summary,
                threat.published_utc.isoformat() if threat.published_utc else None,
                threat.collected_utc.isoformat() if threat.collected_utc else None,
                json.dumps(threat.cves),
                threat.cvss_v3, threat.epss_score, threat.epss_percentile,
                1 if threat.kev_listed else 0, threat.exploit_status,
                threat.admiralty_source_reliability, threat.admiralty_info_credibility,
                threat.priority_level, threat.risk_score,
                threat.verification_confidence, threat.verification_method,
                threat.verification_timestamp.isoformat() if threat.verification_timestamp else None,
                json.dumps(threat.affected_crown_jewels),
                json.dumps(threat.asset_exposure_match),
                threat.dedupe_key
            ))
            conn.commit()
            return True
    
    def get_threat(self, threat_id: str) -> Optional[ThreatRecord]:
        """Get a single threat by ID."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM threats WHERE id = ?", (threat_id,)
            ).fetchone()
            if row:
                return self._row_to_threat(row)
            return None
    
    def search_threats(self, query: str, limit: int = 50) -> list[ThreatRecord]:
        """Full-text search across threats."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT t.* FROM threats t
                JOIN threats_fts fts ON t.id = fts.id
                WHERE threats_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit)).fetchall()
            return [self._row_to_threat(row) for row in rows]
    
    def get_threats_by_priority(
        self, 
        priority: str = None,
        limit: int = 100,
        since_hours: int = 24
    ) -> list[ThreatRecord]:
        """Get threats filtered by priority level."""
        since = (datetime.utcnow() - timedelta(hours=since_hours)).isoformat()
        with self._get_connection() as conn:
            if priority:
                rows = conn.execute("""
                    SELECT * FROM threats 
                    WHERE priority_level = ? AND published_utc >= ?
                    ORDER BY risk_score DESC, published_utc DESC
                    LIMIT ?
                """, (priority, since, limit)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT * FROM threats 
                    WHERE published_utc >= ?
                    ORDER BY risk_score DESC, published_utc DESC
                    LIMIT ?
                """, (since, limit)).fetchall()
            return [self._row_to_threat(row) for row in rows]
    
    def get_kev_threats(self, limit: int = 50) -> list[ThreatRecord]:
        """Get all KEV-listed threats."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM threats 
                WHERE kev_listed = 1
                ORDER BY published_utc DESC
                LIMIT ?
            """, (limit,)).fetchall()
            return [self._row_to_threat(row) for row in rows]
    
    def get_threats_affecting_crown_jewels(
        self, 
        crown_jewels: list[str],
        limit: int = 50
    ) -> list[ThreatRecord]:
        """Get threats affecting specific crown jewels."""
        with self._get_connection() as conn:
            # Build query for JSON array contains
            placeholders = " OR ".join(
                [f"affected_crown_jewels LIKE ?" for _ in crown_jewels]
            )
            params = [f'%"{cj}"%' for cj in crown_jewels]
            params.append(limit)
            
            rows = conn.execute(f"""
                SELECT * FROM threats 
                WHERE {placeholders}
                ORDER BY risk_score DESC, published_utc DESC
                LIMIT ?
            """, params).fetchall()
            return [self._row_to_threat(row) for row in rows]
    
    def get_threat_stats(self, since_hours: int = 24) -> dict:
        """Get threat statistics for dashboard."""
        since = (datetime.utcnow() - timedelta(hours=since_hours)).isoformat()
        with self._get_connection() as conn:
            stats = {}
            
            # Count by priority
            for priority in ["critical", "high", "medium", "low", "watchlist"]:
                count = conn.execute("""
                    SELECT COUNT(*) FROM threats 
                    WHERE priority_level = ? AND published_utc >= ?
                """, (priority, since)).fetchone()[0]
                stats[f"{priority}_count"] = count
            
            # KEV count
            stats["kev_count"] = conn.execute("""
                SELECT COUNT(*) FROM threats 
                WHERE kev_listed = 1 AND published_utc >= ?
            """, (since,)).fetchone()[0]
            
            # High EPSS count
            stats["high_epss_count"] = conn.execute("""
                SELECT COUNT(*) FROM threats 
                WHERE epss_score >= 0.7 AND published_utc >= ?
            """, (since,)).fetchone()[0]
            
            # Total count
            stats["total_count"] = conn.execute("""
                SELECT COUNT(*) FROM threats WHERE published_utc >= ?
            """, (since,)).fetchone()[0]
            
            return stats
    
    def get_threat_trends(self, days: int = 7) -> list[dict]:
        """Get daily threat counts for trending."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT 
                    date(published_utc) as day,
                    COUNT(*) as total,
                    SUM(CASE WHEN priority_level = 'critical' THEN 1 ELSE 0 END) as critical,
                    SUM(CASE WHEN priority_level = 'high' THEN 1 ELSE 0 END) as high,
                    SUM(CASE WHEN kev_listed = 1 THEN 1 ELSE 0 END) as kev
                FROM threats
                WHERE published_utc >= date('now', ?)
                GROUP BY date(published_utc)
                ORDER BY day DESC
            """, (f"-{days} days",)).fetchall()
            return [dict(row) for row in rows]
    
    def _row_to_threat(self, row: sqlite3.Row) -> ThreatRecord:
        """Convert database row to ThreatRecord."""
        return ThreatRecord(
            id=row["id"],
            source_type=row["source_type"],
            source_name=row["source_name"],
            source_url=row["source_url"] or "",
            title=row["title"],
            summary=row["summary"] or "",
            published_utc=datetime.fromisoformat(row["published_utc"]) if row["published_utc"] else datetime.utcnow(),
            collected_utc=datetime.fromisoformat(row["collected_utc"]) if row["collected_utc"] else datetime.utcnow(),
            cves=json.loads(row["cves"]) if row["cves"] else [],
            cvss_v3=row["cvss_v3"],
            epss_score=row["epss_score"],
            epss_percentile=row["epss_percentile"],
            kev_listed=bool(row["kev_listed"]),
            exploit_status=row["exploit_status"],
            admiralty_source_reliability=row["admiralty_source_reliability"] or "C",
            admiralty_info_credibility=row["admiralty_info_credibility"] or 3,
            priority_level=row["priority_level"] or "medium",
            risk_score=row["risk_score"] or 0.0,
            verification_confidence=row["verification_confidence"],
            verification_method=row["verification_method"],
            verification_timestamp=datetime.fromisoformat(row["verification_timestamp"]) if row["verification_timestamp"] else None,
            affected_crown_jewels=json.loads(row["affected_crown_jewels"]) if row["affected_crown_jewels"] else [],
            asset_exposure_match=json.loads(row["asset_exposure_match"]) if row["asset_exposure_match"] else [],
            dedupe_key=row["dedupe_key"] or "",
        )
    
    # ==================== CVE CACHE OPERATIONS ====================
    
    def get_cve(self, cve_id: str) -> Optional[CVERecord]:
        """Get cached CVE data."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM cve_cache WHERE cve_id = ?", (cve_id,)
            ).fetchone()
            if row and (not row["cache_expires"] or datetime.fromisoformat(row["cache_expires"]) > datetime.utcnow()):
                return CVERecord(
                    cve_id=row["cve_id"],
                    cvss_v3_score=row["cvss_v3_score"],
                    cvss_v3_vector=row["cvss_v3_vector"],
                    cvss_v4_score=row["cvss_v4_score"],
                    epss_score=row["epss_score"],
                    epss_percentile=row["epss_percentile"],
                    kev_listed=bool(row["kev_listed"]),
                    description=row["description"] or "",
                    affected_products=json.loads(row["affected_products"]) if row["affected_products"] else [],
                    references=json.loads(row["references_json"]) if row["references_json"] else [],
                )
            return None
    
    def cache_cve(self, cve: CVERecord, ttl_hours: int = 24):
        """Cache CVE enrichment data."""
        expires = (datetime.utcnow() + timedelta(hours=ttl_hours)).isoformat()
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO cve_cache (
                    cve_id, cvss_v3_score, cvss_v3_vector, cvss_v4_score,
                    epss_score, epss_percentile, kev_listed, kev_date_added,
                    kev_due_date, description, affected_products, references_json,
                    published_date, last_modified, cache_expires
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(cve_id) DO UPDATE SET
                    cvss_v3_score = excluded.cvss_v3_score,
                    cvss_v3_vector = excluded.cvss_v3_vector,
                    cvss_v4_score = excluded.cvss_v4_score,
                    epss_score = excluded.epss_score,
                    epss_percentile = excluded.epss_percentile,
                    kev_listed = excluded.kev_listed,
                    description = excluded.description,
                    affected_products = excluded.affected_products,
                    references_json = excluded.references_json,
                    cached_at = CURRENT_TIMESTAMP,
                    cache_expires = excluded.cache_expires
            """, (
                cve.cve_id, cve.cvss_v3_score, cve.cvss_v3_vector, cve.cvss_v4_score,
                cve.epss_score, cve.epss_percentile, 1 if cve.kev_listed else 0,
                cve.kev_date_added.isoformat() if cve.kev_date_added else None,
                cve.kev_due_date.isoformat() if cve.kev_due_date else None,
                cve.description, json.dumps(cve.affected_products),
                json.dumps(cve.references),
                cve.published_date.isoformat() if cve.published_date else None,
                cve.last_modified.isoformat() if cve.last_modified else None,
                expires
            ))
            conn.commit()
    
    # ==================== FEED METRICS OPERATIONS ====================
    
    def update_feed_metrics(self, metrics: FeedMetric):
        """Update feed quality metrics."""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO feed_metrics (
                    feed_url, feed_name, last_check, last_success, response_time_ms,
                    http_status, error_count_24h, items_collected_24h, items_collected_7d,
                    security_relevance_score, duplicate_rate, avg_cves_per_item,
                    accessibility_score, relevance_score, timeliness_score,
                    uniqueness_score, overall_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(feed_url) DO UPDATE SET
                    feed_name = excluded.feed_name,
                    last_check = excluded.last_check,
                    last_success = excluded.last_success,
                    response_time_ms = excluded.response_time_ms,
                    http_status = excluded.http_status,
                    error_count_24h = excluded.error_count_24h,
                    items_collected_24h = excluded.items_collected_24h,
                    items_collected_7d = excluded.items_collected_7d,
                    security_relevance_score = excluded.security_relevance_score,
                    duplicate_rate = excluded.duplicate_rate,
                    avg_cves_per_item = excluded.avg_cves_per_item,
                    accessibility_score = excluded.accessibility_score,
                    relevance_score = excluded.relevance_score,
                    timeliness_score = excluded.timeliness_score,
                    uniqueness_score = excluded.uniqueness_score,
                    overall_score = excluded.overall_score
            """, (
                metrics.feed_url, metrics.feed_name,
                metrics.last_check.isoformat(), 
                metrics.last_success.isoformat() if metrics.last_success else None,
                metrics.response_time_ms, metrics.http_status,
                metrics.error_count_24h, metrics.items_collected_24h,
                metrics.items_collected_7d, metrics.security_relevance_score,
                metrics.duplicate_rate, metrics.avg_cves_per_item,
                metrics.accessibility_score, metrics.relevance_score,
                metrics.timeliness_score, metrics.uniqueness_score,
                metrics.overall_score
            ))
            conn.commit()
    
    def get_all_feed_metrics(self) -> list[FeedMetric]:
        """Get all feed metrics."""
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM feed_metrics ORDER BY overall_score DESC"
            ).fetchall()
            return [
                FeedMetric(
                    feed_name=row["feed_name"],
                    feed_url=row["feed_url"],
                    last_check=datetime.fromisoformat(row["last_check"]) if row["last_check"] else datetime.utcnow(),
                    last_success=datetime.fromisoformat(row["last_success"]) if row["last_success"] else None,
                    response_time_ms=row["response_time_ms"] or 0,
                    http_status=row["http_status"] or 0,
                    error_count_24h=row["error_count_24h"] or 0,
                    items_collected_24h=row["items_collected_24h"] or 0,
                    items_collected_7d=row["items_collected_7d"] or 0,
                    security_relevance_score=row["security_relevance_score"] or 0.0,
                    duplicate_rate=row["duplicate_rate"] or 0.0,
                    avg_cves_per_item=row["avg_cves_per_item"] or 0.0,
                    accessibility_score=row["accessibility_score"] or 100.0,
                    relevance_score=row["relevance_score"] or 50.0,
                    timeliness_score=row["timeliness_score"] or 50.0,
                    uniqueness_score=row["uniqueness_score"] or 100.0,
                    overall_score=row["overall_score"] or 75.0,
                )
                for row in rows
            ]
    
    # ==================== MAINTENANCE ====================
    
    def cleanup_expired(self):
        """Remove expired cache entries."""
        now = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            conn.execute("DELETE FROM cve_cache WHERE cache_expires < ?", (now,))
            conn.execute("DELETE FROM verification_cache WHERE cache_expires < ?", (now,))
            conn.commit()
    
    def vacuum(self):
        """Optimize database size."""
        with self._get_connection() as conn:
            conn.execute("VACUUM")
