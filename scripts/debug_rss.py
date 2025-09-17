#!/usr/bin/env python3
"""
Debug script for RSS feed parsing
"""

import feedparser
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def debug_feed(feed_url):
    print(f"\n🔍 Debugging RSS feed: {feed_url}")
    print("=" * 60)

    # Parse the feed
    feed = feedparser.parse(feed_url)

    # Check for errors
    if feed.bozo:
        print(f"⚠️  Feed parsing error: {feed.bozo_exception}")

    # Basic feed info
    print(f"Feed title: {feed.feed.get('title', 'No title')}")
    print(f"Feed link: {feed.feed.get('link', 'No link')}")
    print(f"Feed description: {feed.feed.get('description', 'No description')[:100]}")

    # Check entries
    print(f"\n📊 Total entries found: {len(feed.entries)}")

    if len(feed.entries) == 0:
        print("❌ No entries found in feed!")
        print("\nFeed structure:")
        print(f"  Feed keys: {list(feed.keys())}")
        print(f"  Feed.feed keys: {list(feed.feed.keys()) if hasattr(feed, 'feed') else 'No feed attribute'}")
        return

    # Analyze first few entries
    print("\n🔍 Analyzing first 3 entries:")
    for i, entry in enumerate(feed.entries[:3]):
        print(f"\n  Entry {i+1}:")
        print(f"    Title: {entry.get('title', 'No title')[:60]}")
        print(f"    Link: {entry.get('link', 'No link')}")

        # Check date fields
        if hasattr(entry, 'published_parsed'):
            pub_date = datetime(*entry.published_parsed[:6])
            print(f"    Published: {pub_date.strftime('%Y-%m-%d %H:%M:%S')}")
        elif hasattr(entry, 'updated_parsed'):
            upd_date = datetime(*entry.updated_parsed[:6])
            print(f"    Updated: {upd_date.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"    Date: No date found")
            print(f"    Available fields: {list(entry.keys())}")

        # Check for CVEs in content
        content = f"{entry.get('title', '')} {entry.get('summary', '')}"
        import re
        cve_pattern = re.compile(r'CVE-\d{4}-\d{4,7}')
        cves = cve_pattern.findall(content)
        if cves:
            print(f"    CVEs found: {', '.join(cves[:5])}")

    # Date range analysis
    print("\n📅 Date range analysis:")
    dates = []
    for entry in feed.entries:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            dates.append(datetime(*entry.published_parsed[:6]))
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            dates.append(datetime(*entry.updated_parsed[:6]))

    if dates:
        dates.sort()
        print(f"  Oldest entry: {dates[0].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Newest entry: {dates[-1].strftime('%Y-%m-%d %H:%M:%S')}")

        # Check how many would pass different date filters
        now = datetime.utcnow()
        ranges = [1, 7, 30, 365]
        for days in ranges:
            since = now - timedelta(days=days)
            count = sum(1 for d in dates if d >= since)
            print(f"  Entries from last {days} days: {count}")
    else:
        print("  ❌ No valid dates found in entries")

# Test multiple feeds
test_feeds = [
    "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml",
    "https://www.cisa.gov/cybersecurity-advisories/all.xml",
    "https://www.bleepingcomputer.com/feed/"
]

if __name__ == "__main__":
    for feed_url in test_feeds:
        try:
            debug_feed(feed_url)
        except Exception as e:
            print(f"\n❌ Error processing {feed_url}: {e}")
            import traceback
            traceback.print_exc()