"""Database migrations and data import utilities."""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from .database import CacheDatabase
from .models import ThreatRecord, CVERecord, VerificationRecord, FeedMetric


def run_migrations(db: CacheDatabase):
    """Run any pending database migrations."""
    # Currently just initializes the schema
    # Future migrations can be added here
    pass


def migrate_json_cache(
    db: CacheDatabase,
    threats_cache_path: str = "data/threats-cache.json",
    verification_cache_path: str = "data/verification-cache.json",
    feed_metrics_path: str = "data/feed-quality-metrics.json"
):
    """Migrate existing JSON cache files to SQLite."""
    
    # Migrate threats cache
    threats_path = Path(threats_cache_path)
    if threats_path.exists():
        try:
            with open(threats_path) as f:
                data = json.load(f)
            
            threats = data.get("threats", [])
            if isinstance(data, list):
                threats = data
            
            migrated = 0
            for threat_data in threats:
                try:
                    threat = ThreatRecord.from_dict(threat_data)
                    db.upsert_threat(threat)
                    migrated += 1
                except Exception as e:
                    print(f"Warning: Failed to migrate threat {threat_data.get('id', 'unknown')}: {e}")
            
            print(f"Migrated {migrated} threats from JSON cache")
        except Exception as e:
            print(f"Warning: Failed to read threats cache: {e}")
    
    # Migrate verification cache
    verification_path = Path(verification_cache_path)
    if verification_path.exists():
        try:
            with open(verification_path) as f:
                data = json.load(f)
            
            verifications = data.get("verifications", {})
            migrated = 0
            for threat_id, verification_data in verifications.items():
                try:
                    # Store in verification_cache table
                    with db._get_connection() as conn:
                        conn.execute("""
                            INSERT OR REPLACE INTO verification_cache (
                                threat_id, verified, confidence_score, verification_method,
                                sources_consulted, nvd_match, cisa_kev_match,
                                vendor_advisory_match, verified_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            threat_id,
                            1 if verification_data.get("verified") else 0,
                            verification_data.get("confidence", 0),
                            verification_data.get("method", "structured"),
                            json.dumps(verification_data.get("sources", [])),
                            1 if verification_data.get("nvd_match") else 0,
                            1 if verification_data.get("cisa_kev_match") else 0,
                            1 if verification_data.get("vendor_advisory_match") else 0,
                            verification_data.get("last_verified", datetime.utcnow().isoformat())
                        ))
                        conn.commit()
                    migrated += 1
                except Exception as e:
                    print(f"Warning: Failed to migrate verification {threat_id}: {e}")
            
            print(f"Migrated {migrated} verifications from JSON cache")
        except Exception as e:
            print(f"Warning: Failed to read verification cache: {e}")
    
    # Migrate feed metrics
    metrics_path = Path(feed_metrics_path)
    if metrics_path.exists():
        try:
            with open(metrics_path) as f:
                data = json.load(f)
            
            feeds = data.get("feeds", data.get("metrics", []))
            if isinstance(feeds, dict):
                feeds = [{"feed_url": k, **v} for k, v in feeds.items()]
            
            migrated = 0
            for feed_data in feeds:
                try:
                    metric = FeedMetric(
                        feed_name=feed_data.get("name", feed_data.get("feed_name", "")),
                        feed_url=feed_data.get("url", feed_data.get("feed_url", "")),
                        last_check=datetime.fromisoformat(feed_data["last_check"]) if feed_data.get("last_check") else datetime.utcnow(),
                        overall_score=feed_data.get("overall_score", feed_data.get("quality_score", 75.0)),
                    )
                    db.update_feed_metrics(metric)
                    migrated += 1
                except Exception as e:
                    print(f"Warning: Failed to migrate feed metric: {e}")
            
            print(f"Migrated {migrated} feed metrics from JSON cache")
        except Exception as e:
            print(f"Warning: Failed to read feed metrics: {e}")


def export_to_json(db: CacheDatabase, output_path: str = "data/threats-export.json"):
    """Export SQLite cache back to JSON format."""
    threats = db.get_threats_by_priority(limit=10000, since_hours=720)  # 30 days
    
    output = {
        "exported_at": datetime.utcnow().isoformat(),
        "threat_count": len(threats),
        "threats": [t.to_dict() for t in threats]
    }
    
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Exported {len(threats)} threats to {output_path}")
