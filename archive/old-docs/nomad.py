#!/usr/bin/env python3
"""
NOMAD Threat Intelligence Framework CLI
Designed for execution by Claude Code

Usage:
    python nomad.py rss [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--priority high|medium|low] [--output FILE]
    python nomad.py orchestrate --input FILE [--output FILE]
    python nomad.py enrich --input FILE [--output FILE]
    python nomad.py dedup --input FILE [--output FILE]
    python nomad.py alert --input FILE [--output FILE]
    python nomad.py ciso-report --week YYYY-WNN [--output FILE]
    python nomad.py pipeline [--since YYYY-MM-DD]
    python nomad.py list-feeds [--priority high|medium|low] [--source-type TYPE]
    python nomad.py test-feed URL

Examples:
    python nomad.py rss --since 2024-01-01 --priority high
    python nomad.py orchestrate --input data/output/intel.json
    python nomad.py pipeline --since 2024-01-01
    python nomad.py list-feeds --priority high
    python nomad.py test-feed "https://www.cisa.gov/cybersecurity-advisories/all.xml"
"""

import argparse
import json
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.rss_feed import RSSFeedAgent
# Future imports:
# from agents.orchestrator import OrchestratorAgent
# from agents.enrichment import EnrichmentAgent
# from agents.dedup import DedupAgent
# from agents.technical_alert import TechnicalAlertAgent
# from agents.ciso_report import CISOReportAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('nomad')

class NomadCLI:
    """Main CLI interface for NOMAD framework"""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            description='NOMAD Threat Intelligence Framework',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__doc__
        )

        subparsers = parser.add_subparsers(dest='command', help='Commands')

        # RSS command
        rss_parser = subparsers.add_parser('rss', help='Collect RSS feeds')
        rss_parser.add_argument('--since', help='Start date (YYYY-MM-DD)')
        rss_parser.add_argument('--until', help='End date (YYYY-MM-DD)')
        rss_parser.add_argument('--priority', choices=['high', 'medium', 'low'],
                               help='Filter by priority')
        rss_parser.add_argument('--source-type',
                               choices=['cert', 'vendor', 'research', 'news', 'database'],
                               help='Filter by source type')
        rss_parser.add_argument('--output', help='Output file (default: auto-generated)')

        # Orchestrate command
        orch_parser = subparsers.add_parser('orchestrate', help='Route intelligence items')
        orch_parser.add_argument('--input', required=True, help='Input file with intelligence')
        orch_parser.add_argument('--output', help='Output file (default: auto-generated)')

        # Enrich command
        enrich_parser = subparsers.add_parser('enrich', help='Enrich intelligence items')
        enrich_parser.add_argument('--input', required=True, help='Input file')
        enrich_parser.add_argument('--output', help='Output file')

        # Dedup command
        dedup_parser = subparsers.add_parser('dedup', help='Deduplicate items')
        dedup_parser.add_argument('--input', required=True, help='Input file')
        dedup_parser.add_argument('--output', help='Output file')

        # Alert command
        alert_parser = subparsers.add_parser('alert', help='Generate technical alert')
        alert_parser.add_argument('--input', required=True, help='Input file')
        alert_parser.add_argument('--output', help='Output file')

        # CISO report command
        ciso_parser = subparsers.add_parser('ciso-report', help='Generate CISO report')
        ciso_parser.add_argument('--week', help='Week (YYYY-WNN)')
        ciso_parser.add_argument('--output', help='Output file')

        # Pipeline command
        pipeline_parser = subparsers.add_parser('pipeline', help='Run full pipeline')
        pipeline_parser.add_argument('--since', help='Start date (YYYY-MM-DD)')
        pipeline_parser.add_argument('--config', help='Config file')

        # List feeds command
        list_parser = subparsers.add_parser('list-feeds', help='List configured feeds')
        list_parser.add_argument('--priority', choices=['high', 'medium', 'low'],
                                help='Filter by priority')
        list_parser.add_argument('--source-type',
                                choices=['cert', 'vendor', 'research', 'news', 'database'],
                                help='Filter by source type')
        list_parser.add_argument('--enabled-only', action='store_true',
                                help='Show only enabled feeds')

        # Test feed command
        test_parser = subparsers.add_parser('test-feed', help='Test a single feed')
        test_parser.add_argument('url', help='Feed URL to test')

        return parser

    def run(self, args=None):
        """Run the CLI"""
        args = self.parser.parse_args(args)

        if not args.command:
            self.parser.print_help()
            return 1

        # Route to appropriate handler
        handlers = {
            'rss': self.handle_rss,
            'orchestrate': self.handle_orchestrate,
            'enrich': self.handle_enrich,
            'dedup': self.handle_dedup,
            'alert': self.handle_alert,
            'ciso-report': self.handle_ciso_report,
            'pipeline': self.handle_pipeline,
            'list-feeds': self.handle_list_feeds,
            'test-feed': self.handle_test_feed
        }

        handler = handlers.get(args.command)
        if handler:
            return handler(args)
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1

    def handle_rss(self, args) -> int:
        """Handle RSS feed collection"""
        try:
            logger.info("Starting RSS feed collection...")

            agent = RSSFeedAgent()
            result = agent.run(
                since=args.since,
                until=args.until,
                priority=args.priority,
                source_type=args.source_type
            )

            # Determine output file
            if args.output:
                output_file = args.output
            else:
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                output_file = f"intel_rss_{timestamp}.json"

            # Save output
            output_path = agent.save_output(result, output_file)

            # Print summary
            print(f"\n✓ RSS Collection Complete")
            print(f"  Items collected: {len(result.get('intelligence', []))}")
            print(f"  Output saved to: {output_path}")

            # Show sample items
            items = result.get('intelligence', [])
            if items:
                print("\n  Sample items:")
                for item in items[:3]:
                    print(f"    - {item.get('title', 'No title')[:80]}")
                    if item.get('cves'):
                        print(f"      CVEs: {', '.join(item['cves'][:3])}")

            return 0

        except Exception as e:
            logger.error(f"RSS collection failed: {e}")
            return 1

    def handle_orchestrate(self, args) -> int:
        """Handle orchestration"""
        logger.info("Orchestrator not yet implemented")
        print("⚠ Orchestrator agent is pending implementation")
        return 0

    def handle_enrich(self, args) -> int:
        """Handle enrichment"""
        logger.info("Enrichment not yet implemented")
        print("⚠ Enrichment agent is pending implementation")
        return 0

    def handle_dedup(self, args) -> int:
        """Handle deduplication"""
        logger.info("Deduplication not yet implemented")
        print("⚠ Deduplication agent is pending implementation")
        return 0

    def handle_alert(self, args) -> int:
        """Handle alert generation"""
        logger.info("Alert generation not yet implemented")
        print("⚠ Technical alert agent is pending implementation")
        return 0

    def handle_ciso_report(self, args) -> int:
        """Handle CISO report generation"""
        logger.info("CISO report not yet implemented")
        print("⚠ CISO report agent is pending implementation")
        return 0

    def handle_pipeline(self, args) -> int:
        """Handle full pipeline execution"""
        try:
            logger.info("Starting full pipeline...")
            print("\n🚀 NOMAD Pipeline Starting\n")

            # Step 1: Collect RSS feeds
            print("Step 1: Collecting RSS feeds...")
            rss_agent = RSSFeedAgent()
            intel = rss_agent.run(since=args.since)

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            intel_file = f"pipeline_intel_{timestamp}.json"
            rss_agent.save_output(intel, intel_file)
            print(f"  ✓ Collected {len(intel.get('intelligence', []))} items")

            # Step 2: Deduplication (pending)
            print("\nStep 2: Deduplication...")
            print("  ⚠ Pending implementation")

            # Step 3: Enrichment (pending)
            print("\nStep 3: Enrichment...")
            print("  ⚠ Pending implementation")

            # Step 4: Orchestration (pending)
            print("\nStep 4: Orchestration/Routing...")
            print("  ⚠ Pending implementation")

            # Step 5: Output generation (pending)
            print("\nStep 5: Output Generation...")
            print("  ⚠ Pending implementation")

            print("\n✓ Pipeline complete (partial)")
            return 0

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return 1

    def handle_list_feeds(self, args) -> int:
        """List configured feeds"""
        try:
            import yaml
            config_path = Path(__file__).parent / "config" / "rss_feeds.yaml"

            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            feeds = config.get('feeds', [])

            # Apply filters
            if args.priority:
                feeds = [f for f in feeds if f.get('priority') == args.priority]

            if args.source_type:
                feeds = [f for f in feeds if f.get('source_type') == args.source_type]

            if args.enabled_only:
                feeds = [f for f in feeds if f.get('enabled', True)]

            # Group by source type
            by_type = {}
            for feed in feeds:
                source_type = feed.get('source_type', 'unknown')
                if source_type not in by_type:
                    by_type[source_type] = []
                by_type[source_type].append(feed)

            # Display feeds
            print(f"\n📡 Configured RSS Feeds ({len(feeds)} total)\n")

            for source_type in sorted(by_type.keys()):
                type_feeds = by_type[source_type]
                print(f"{source_type.upper()} ({len(type_feeds)} feeds):")
                print("-" * 50)

                for feed in type_feeds:
                    status = "✓" if feed.get('enabled', True) else "✗"
                    priority = feed.get('priority', 'unknown')
                    name = feed.get('name', 'Unknown')
                    freq = feed.get('check_frequency', 'unknown')

                    print(f"  {status} [{priority:6}] {name}")
                    print(f"     Frequency: {freq}")
                    if feed.get('description'):
                        print(f"     {feed['description']}")
                    print()

            return 0

        except Exception as e:
            logger.error(f"Failed to list feeds: {e}")
            return 1

    def handle_test_feed(self, args) -> int:
        """Test a single feed"""
        try:
            logger.info(f"Testing feed: {args.url}")
            print(f"\n🔍 Testing feed: {args.url}\n")

            agent = RSSFeedAgent()
            result = agent.process_single_feed(args.url)

            items = result.get('intelligence', [])
            print(f"✓ Feed processed successfully")
            print(f"  Items found: {len(items)}")

            if items:
                print("\n  Recent items:")
                for i, item in enumerate(items[:5], 1):
                    print(f"\n  {i}. {item.get('title', 'No title')}")
                    print(f"     Published: {item.get('published_utc', 'Unknown')}")
                    if item.get('cves'):
                        print(f"     CVEs: {', '.join(item['cves'])}")
                    print(f"     Admiralty: {item.get('admiralty_source_reliability')}/{item.get('admiralty_info_credibility')}")

            # Save test output
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_feed_{timestamp}.json"
            agent.save_output(result, output_file)
            print(f"\n  Full output saved to: data/output/{output_file}")

            return 0

        except Exception as e:
            logger.error(f"Feed test failed: {e}")
            print(f"\n✗ Feed test failed: {e}")
            return 1

def main():
    """Main entry point"""
    cli = NomadCLI()
    sys.exit(cli.run())

if __name__ == '__main__':
    main()