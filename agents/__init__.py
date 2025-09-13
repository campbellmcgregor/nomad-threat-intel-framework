"""
NOMAD Threat Intelligence Framework - Agent Module
"""

from .base_agent import BaseAgent
from .rss_feed import RSSFeedAgent

# Future agents (not yet implemented)
# from .orchestrator import OrchestratorAgent
# from .enrichment import EnrichmentAgent
# from .dedup import DedupAgent
# from .vendor_parser import VendorParserAgent
# from .technical_alert import TechnicalAlertAgent
# from .ciso_report import CISOReportAgent
# from .watchlist_digest import WatchlistDigestAgent
# from .evidence_vault import EvidenceVaultAgent

__all__ = [
    'BaseAgent',
    'RSSFeedAgent',
]