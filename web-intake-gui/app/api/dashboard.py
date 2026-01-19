"""Dashboard API endpoints for threat intelligence visualization."""

from datetime import datetime, timedelta
from pathlib import Path
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text

from app.database import get_db
from app.auth import verify_api_token
from app.models.database import ReportDB

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/stats", dependencies=[Depends(verify_api_token)])
async def get_dashboard_stats(
    hours: int = Query(24, ge=1, le=720, description="Time window in hours"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get summary statistics for the dashboard.
    
    Returns counts of threats by severity, KEV status, and other metrics.
    """
    since = datetime.utcnow() - timedelta(hours=hours)
    
    # Get report counts by type
    report_counts = {}
    result = await db.execute(
        select(ReportDB.report_type, func.count(ReportDB.id))
        .where(ReportDB.created_at >= since)
        .group_by(ReportDB.report_type)
    )
    for row in result:
        report_counts[row[0]] = row[1]
    
    # Total reports
    total_result = await db.execute(
        select(func.count(ReportDB.id)).where(ReportDB.created_at >= since)
    )
    total_reports = total_result.scalar() or 0
    
    # Calculate threat stats from report metadata
    # This will be enhanced when we integrate with the SQLite cache
    stats = {
        "time_window_hours": hours,
        "generated_at": datetime.utcnow().isoformat(),
        "reports": {
            "total": total_reports,
            "by_type": report_counts,
        },
        "threats": {
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "kev_count": 0,
            "high_epss_count": 0,
            "total_count": 0,
        },
        "feeds": {
            "active_count": 0,
            "healthy_count": 0,
            "degraded_count": 0,
        }
    }
    
    # Try to get threat stats from the SQLite cache
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))
        from cache import CacheDatabase
        
        cache_db = CacheDatabase()
        threat_stats = cache_db.get_threat_stats(since_hours=hours)
        stats["threats"] = threat_stats
    except Exception:
        pass  # Cache not available, use defaults
    
    return stats


@router.get("/trends", dependencies=[Depends(verify_api_token)])
async def get_threat_trends(
    days: int = Query(7, ge=1, le=30, description="Number of days for trend data"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get daily threat trends for charting.
    
    Returns daily counts for visualization.
    """
    trends = []
    
    # Try to get trends from SQLite cache
    try:
        from pathlib import Path
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))
        from cache import CacheDatabase
        
        cache_db = CacheDatabase()
        trends = cache_db.get_threat_trends(days=days)
    except Exception:
        # Generate placeholder data from reports
        for i in range(days):
            day = (datetime.utcnow() - timedelta(days=i)).date()
            trends.append({
                "day": day.isoformat(),
                "total": 0,
                "critical": 0,
                "high": 0,
                "kev": 0,
            })
    
    return {
        "days": days,
        "generated_at": datetime.utcnow().isoformat(),
        "trends": trends,
    }


@router.get("/crown-jewels", dependencies=[Depends(verify_api_token)])
async def get_crown_jewel_threats(
    hours: int = Query(24, ge=1, le=720),
    db: AsyncSession = Depends(get_db),
):
    """
    Get threat counts affecting each crown jewel.
    
    Returns heat map data for crown jewel visualization.
    """
    # Load crown jewels from config
    crown_jewels = []
    try:
        from pathlib import Path
        import json
        config_path = Path(__file__).parent.parent.parent.parent.parent / "config" / "user-preferences.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            crown_jewels = config.get("crown_jewels", [])
    except Exception:
        pass
    
    # Get threat counts per crown jewel from cache
    heat_map = []
    try:
        from pathlib import Path
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))
        from cache import CacheDatabase
        
        cache_db = CacheDatabase()
        for cj in crown_jewels:
            threats = cache_db.get_threats_affecting_crown_jewels([cj], limit=100)
            heat_map.append({
                "crown_jewel": cj,
                "threat_count": len(threats),
                "critical_count": sum(1 for t in threats if t.priority_level == "critical"),
                "high_count": sum(1 for t in threats if t.priority_level == "high"),
            })
    except Exception:
        # Return empty heat map if cache not available
        for cj in crown_jewels:
            heat_map.append({
                "crown_jewel": cj,
                "threat_count": 0,
                "critical_count": 0,
                "high_count": 0,
            })
    
    return {
        "time_window_hours": hours,
        "generated_at": datetime.utcnow().isoformat(),
        "crown_jewels": heat_map,
    }


@router.get("/recent-alerts", dependencies=[Depends(verify_api_token)])
async def get_recent_alerts(
    limit: int = Query(10, ge=1, le=50),
    priority: str = Query(None, description="Filter by priority: critical, high, medium, low"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get recent threat alerts for the dashboard feed.
    """
    alerts = []
    
    try:
        from pathlib import Path
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))
        from cache import CacheDatabase
        
        cache_db = CacheDatabase()
        threats = cache_db.get_threats_by_priority(
            priority=priority,
            limit=limit,
            since_hours=168  # Last week
        )
        
        for t in threats:
            alerts.append({
                "id": t.id,
                "title": t.title,
                "priority": t.priority_level,
                "cvss": t.cvss_v3,
                "epss": t.epss_score,
                "kev_listed": t.kev_listed,
                "cves": t.cves,
                "source": t.source_name,
                "published": t.published_utc.isoformat() if t.published_utc else None,
                "affected_crown_jewels": t.affected_crown_jewels,
            })
    except Exception:
        pass
    
    return {
        "generated_at": datetime.utcnow().isoformat(),
        "alerts": alerts,
    }


@router.get("/feed-health", dependencies=[Depends(verify_api_token)])
async def get_feed_health(
    db: AsyncSession = Depends(get_db),
):
    """
    Get health status of all configured threat feeds.
    """
    feeds = []
    
    try:
        from pathlib import Path
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))
        from cache import CacheDatabase
        
        cache_db = CacheDatabase()
        metrics = cache_db.get_all_feed_metrics()
        
        for m in metrics:
            status = "healthy"
            if m.overall_score < 50:
                status = "critical"
            elif m.overall_score < 70:
                status = "degraded"
            
            feeds.append({
                "name": m.feed_name,
                "url": m.feed_url,
                "status": status,
                "overall_score": m.overall_score,
                "last_check": m.last_check.isoformat() if m.last_check else None,
                "response_time_ms": m.response_time_ms,
                "items_24h": m.items_collected_24h,
            })
    except Exception:
        pass
    
    # Count by status
    healthy = sum(1 for f in feeds if f.get("status") == "healthy")
    degraded = sum(1 for f in feeds if f.get("status") == "degraded")
    critical = sum(1 for f in feeds if f.get("status") == "critical")
    
    return {
        "generated_at": datetime.utcnow().isoformat(),
        "summary": {
            "total": len(feeds),
            "healthy": healthy,
            "degraded": degraded,
            "critical": critical,
        },
        "feeds": feeds,
    }
