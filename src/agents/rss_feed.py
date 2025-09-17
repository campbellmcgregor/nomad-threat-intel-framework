"""
RSS Feed Agent for NOMAD framework
Collects and normalizes threat intelligence from RSS/Atom feeds
"""

import re
import hashlib
import feedparser
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class RSSFeedAgent(BaseAgent):
    """Agent for processing RSS/Atom feeds"""

    def __init__(self):
        super().__init__("rss-agent")
        self.cve_pattern = re.compile(r'CVE-\d{4}-\d{4,7}')

    def run(self, since: Optional[str] = None, until: Optional[str] = None,
            priority: Optional[str] = None, source_type: Optional[str] = None) -> Dict[str, Any]:
        """Run RSS feed collection

        Args:
            since: Start date in YYYY-MM-DD format (default: 7 days ago)
            until: End date in YYYY-MM-DD format (default: now)
            priority: Filter feeds by priority (high, medium, low)
            source_type: Filter feeds by type (cert, vendor, research, news, database)

        Returns:
            Normalized intelligence items
        """
        # Set default time range
        if not since:
            since_date = datetime.now(timezone.utc) - timedelta(days=7)
            since = since_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            since = f"{since}T00:00:00Z"

        if not until:
            until = self.get_timestamp()
        else:
            until = f"{until}T23:59:59Z"

        self.logger.info(f"Collecting feeds from {since} to {until}")

        # Get feeds from configuration
        feeds = self._get_feeds(priority, source_type)

        # Collect intelligence from all feeds
        all_items = []
        for feed_config in feeds:
            if feed_config.get('enabled', True):
                items = self._process_feed(feed_config, since, until)
                all_items.extend(items)

        # Deduplicate items
        unique_items = self._deduplicate_items(all_items)

        # Format output
        output = {
            "agent_type": "rss",
            "collected_at_utc": self.get_timestamp(),
            "intelligence": unique_items
        }

        self.logger.info(f"Collected {len(unique_items)} unique items from {len(feeds)} feeds")

        return output

    def _get_feeds(self, priority: Optional[str] = None,
                   source_type: Optional[str] = None) -> List[Dict]:
        """Get feeds from configuration with optional filters"""
        if 'feeds' not in self.config or 'feeds' not in self.config['feeds']:
            self.logger.warning("No feeds found in configuration")
            return []

        feeds = self.config['feeds']['feeds']

        # Apply filters
        if priority:
            feeds = [f for f in feeds if f.get('priority') == priority]

        if source_type:
            feeds = [f for f in feeds if f.get('source_type') == source_type]

        return feeds

    def _process_feed(self, feed_config: Dict, since: str, until: str) -> List[Dict]:
        """Process a single RSS feed

        Args:
            feed_config: Feed configuration
            since: Start date
            until: End date

        Returns:
            List of normalized items from feed
        """
        items = []
        feed_name = feed_config.get('name', 'Unknown')
        feed_url = feed_config.get('url')

        if not feed_url:
            return items

        try:
            self.logger.info(f"Processing feed: {feed_name}")

            # Parse feed
            feed = feedparser.parse(feed_url)

            if feed.bozo:
                self.logger.warning(f"Feed parsing issue for {feed_name}: {feed.bozo_exception}")

            # Process entries
            total_entries = len(feed.entries)
            filtered_entries = 0
            for entry in feed.entries:
                item = self._normalize_entry(entry, feed_config, since, until)
                if item:
                    items.append(item)
                else:
                    filtered_entries += 1

            if total_entries > 0:
                self.logger.info(f"Feed {feed_name}: {len(items)}/{total_entries} entries passed date filter (filtered: {filtered_entries})")

        except Exception as e:
            self.logger.error(f"Error processing feed {feed_name}: {e}")

        return items

    def _normalize_entry(self, entry: Any, feed_config: Dict,
                        since: str, until: str) -> Optional[Dict]:
        """Normalize a feed entry to standard format

        Args:
            entry: Feed entry from feedparser
            feed_config: Feed configuration
            since: Start date filter
            until: End date filter

        Returns:
            Normalized item or None if filtered out
        """
        # Extract basic fields
        title = entry.get('title', '')
        link = entry.get('link', '')
        summary = entry.get('summary', '')[:300] if entry.get('summary') else ''

        # Get published date
        published = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

        # Apply date filter
        if published:
            published_str = published.strftime("%Y-%m-%dT%H:%M:%SZ")
            # Parse since and until for proper comparison
            since_dt = datetime.strptime(since, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            until_dt = datetime.strptime(until, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

            if published < since_dt or published > until_dt:
                return None
        else:
            # No date found, include by default with current timestamp
            published_str = self.get_timestamp()

        # Extract CVEs from title, summary, and raw content
        text = f"{title} {summary}"

        # Also check content field and other text fields
        if hasattr(entry, 'content') and entry.content:
            for content_item in entry.content:
                if hasattr(content_item, 'value'):
                    text += f" {content_item.value}"

        # Check description field
        if entry.get('description'):
            text += f" {entry.get('description')}"

        cves = list(set(self.cve_pattern.findall(text)))

        # Generate dedupe key
        dedupe_key = self._generate_dedupe_key(title, link)

        # Determine Admiralty ratings based on source type and URL
        source_type = feed_config.get('source_type', 'unknown')

        # For manual feeds, try to detect source from URL
        if feed_config.get('name') == 'Manual Feed':
            if 'cisa.gov' in link or 'cisa.gov' in feed_config.get('url', ''):
                source_type = 'cert'
                feed_config['name'] = 'CISA Cybersecurity Advisories'
            elif 'nvd.nist.gov' in link or 'nvd.nist.gov' in feed_config.get('url', ''):
                source_type = 'database'
                feed_config['name'] = 'NVD Vulnerability Database'
            elif 'bleepingcomputer.com' in link or 'bleepingcomputer.com' in feed_config.get('url', ''):
                source_type = 'news'
                feed_config['name'] = 'BleepingComputer'

        source_reliability, info_credibility, admiralty_reason = self._get_admiralty_ratings(
            source_type, feed_config.get('name', '')
        )

        # Extract affected products (basic extraction)
        affected_products = self._extract_products(text)

        # Build normalized item
        item = {
            "source_type": "rss",
            "source_name": feed_config.get('name', 'Unknown'),
            "source_url": link,
            "title": title,
            "summary": summary,
            "published_utc": published_str,
            "cves": cves,
            "cvss_v3": None,
            "cvss_v4": None,
            "epss": None,
            "kev_listed": None,
            "kev_date_added": None,
            "exploit_status": None,
            "affected_products": affected_products,
            "evidence_excerpt": summary[:150] if summary else "",
            "admiralty_source_reliability": source_reliability,
            "admiralty_info_credibility": info_credibility,
            "admiralty_reason": admiralty_reason,
            "dedupe_key": dedupe_key
        }

        return item

    def _generate_dedupe_key(self, title: str, url: str) -> str:
        """Generate stable dedupe key"""
        content = f"{title.lower()}|{url.lower()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _get_admiralty_ratings(self, source_type: str, source_name: str) -> tuple:
        """Determine Admiralty ratings based on source

        Returns:
            Tuple of (source_reliability, info_credibility, reason)
        """
        ratings_map = {
            'cert': ('A', 2, "Official CERT/CSIRT advisory"),
            'vendor': ('A', 2, "Official vendor security advisory"),
            'research': ('B', 3, "Security research organization"),
            'database': ('B', 3, "Vulnerability database entry"),
            'news': ('C', 4, "Security news media")
        }

        default = ('D', 4, "Unverified source")
        reliability, credibility, base_reason = ratings_map.get(source_type, default)

        # Adjust for specific high-trust sources
        high_trust = ['CISA', 'Microsoft Security', 'NCSC', 'US-CERT']
        if any(trust in source_name for trust in high_trust):
            reliability = 'A'
            credibility = 2
            base_reason = f"High-trust source: {source_name}"

        return reliability, credibility, base_reason

    def _extract_products(self, text: str) -> List[Dict]:
        """Basic product extraction from text

        Args:
            text: Text to extract products from

        Returns:
            List of affected products
        """
        products = []

        # Common vendor/product patterns
        patterns = [
            (r'Microsoft\s+(Exchange|Windows|Office|Azure|Teams)', 'Microsoft'),
            (r'Cisco\s+(ASA|IOS|AnyConnect|Webex)', 'Cisco'),
            (r'VMware\s+(vSphere|ESXi|vCenter|Horizon)', 'VMware'),
            (r'Oracle\s+(WebLogic|Database|Java)', 'Oracle'),
            (r'Apache\s+(Struts|Tomcat|HTTP Server|Log4j)', 'Apache'),
            (r'Fortinet\s+(FortiGate|FortiOS|FortiManager)', 'Fortinet'),
            (r'Ivanti\s+(Connect Secure|Policy Secure|Endpoint Manager)', 'Ivanti'),
        ]

        for pattern, vendor in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                product_name = match.group(1)
                products.append({
                    "vendor": vendor,
                    "product": product_name,
                    "versions": []  # Would need more sophisticated parsing
                })

        return products

    def _deduplicate_items(self, items: List[Dict]) -> List[Dict]:
        """Remove duplicate items based on dedupe_key and similarity

        Args:
            items: List of items to deduplicate

        Returns:
            List of unique items
        """
        seen_keys = set()
        seen_urls = set()
        unique_items = []

        for item in items:
            dedupe_key = item.get('dedupe_key')
            source_url = item.get('source_url')

            # Skip if we've seen this exact key or URL
            if dedupe_key in seen_keys or source_url in seen_urls:
                continue

            seen_keys.add(dedupe_key)
            seen_urls.add(source_url)
            unique_items.append(item)

        return unique_items

    def process_single_feed(self, feed_url: str) -> Dict[str, Any]:
        """Process a single feed URL (useful for testing)

        Args:
            feed_url: URL of feed to process

        Returns:
            Normalized intelligence items from feed
        """
        # Try to determine feed details from URL
        feed_name = 'Manual Feed'
        source_type = 'unknown'

        if 'cisa.gov' in feed_url:
            feed_name = 'CISA Cybersecurity Advisories'
            source_type = 'cert'
        elif 'nvd.nist.gov' in feed_url:
            feed_name = 'NVD Vulnerability Database'
            source_type = 'database'
        elif 'bleepingcomputer.com' in feed_url:
            feed_name = 'BleepingComputer'
            source_type = 'news'

        feed_config = {
            'name': feed_name,
            'url': feed_url,
            'source_type': source_type,
            'priority': 'medium'
        }

        since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        until = self.get_timestamp()

        items = self._process_feed(feed_config, since, until)

        return {
            "agent_type": "rss",
            "collected_at_utc": self.get_timestamp(),
            "intelligence": items
        }