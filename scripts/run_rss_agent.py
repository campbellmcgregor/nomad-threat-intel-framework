#!/usr/bin/env python3
"""
Direct execution script for RSS Feed Agent
Allows running the RSS agent standalone without Claude Code orchestration
"""

import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path so we can import agents
sys.path.append(str(Path(__file__).parent.parent))

from agents.rss_feed import RSSFeedAgent
from config.environment import config

def main():
    parser = argparse.ArgumentParser(description="Run NOMAD RSS Feed Agent directly")

    # Time range arguments
    parser.add_argument(
        "--since",
        type=str,
        help="Start date (YYYY-MM-DD format, default: 7 days ago)"
    )
    parser.add_argument(
        "--until",
        type=str,
        help="End date (YYYY-MM-DD format, default: now)"
    )

    # Filtering arguments
    parser.add_argument(
        "--priority",
        choices=["high", "medium", "low"],
        help="Filter feeds by priority level"
    )
    parser.add_argument(
        "--source-type",
        choices=["cert", "vendor", "research", "news", "database"],
        help="Filter feeds by source type"
    )

    # Processing options
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use LLM processing for enhanced analysis (requires API key)"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="Save output to specific file (default: auto-generated)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "table", "summary"],
        default="json",
        help="Output format"
    )

    # Testing options
    parser.add_argument(
        "--single-feed",
        type=str,
        help="Process a single RSS feed URL for testing"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without making API calls"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    import logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("🔍 NOMAD RSS Feed Agent - Direct Execution")
    print("=" * 50)

    # Initialize agent
    try:
        agent = RSSFeedAgent()
        print(f"✓ RSS Feed Agent initialized")

        # Validate configuration
        if args.use_llm and not config.anthropic_api_key:
            print("❌ LLM processing requested but no ANTHROPIC_API_KEY found")
            print("   Set your API key in .env file or disable --use-llm")
            return 1

        # Handle single feed processing
        if args.single_feed:
            print(f"📡 Processing single feed: {args.single_feed}")

            if args.dry_run:
                print("   [DRY RUN] Would process this feed")
                return 0

            result = agent.process_single_feed(args.single_feed)

            if args.use_llm and result.get("intelligence"):
                print("🧠 Enhancing with LLM processing...")
                for item in result["intelligence"]:
                    enhanced = agent.process_with_llm(item)
                    item["llm_analysis"] = enhanced

            _output_results(result, args.format, args.output_file, "single_feed")
            return 0

        # Regular multi-feed processing
        print("📡 Processing RSS feeds...")

        # Show processing parameters
        since = args.since
        until = args.until
        if not since:
            since_date = datetime.utcnow() - timedelta(days=7)
            since = since_date.strftime("%Y-%m-%d")
        if not until:
            until = datetime.utcnow().strftime("%Y-%m-%d")

        print(f"   Time range: {since} to {until}")
        if args.priority:
            print(f"   Priority filter: {args.priority}")
        if args.source_type:
            print(f"   Source type filter: {args.source_type}")

        if args.dry_run:
            print("   [DRY RUN] Would process feeds with these parameters")
            return 0

        # Run the agent
        result = agent.run(
            since=since,
            until=until,
            priority=args.priority,
            source_type=args.source_type
        )

        # Enhance with LLM if requested
        if args.use_llm and result.get("intelligence"):
            print(f"🧠 Enhancing {len(result['intelligence'])} items with LLM processing...")

            enhanced_items = []
            for i, item in enumerate(result["intelligence"]):
                print(f"   Processing item {i+1}/{len(result['intelligence'])}")
                enhanced = agent.process_with_llm(item)
                item["llm_analysis"] = enhanced
                enhanced_items.append(item)

            result["intelligence"] = enhanced_items
            result["llm_enhanced"] = True

        # Output results
        _output_results(result, args.format, args.output_file, "rss_feed")

        print(f"✅ RSS Feed Agent completed successfully")
        print(f"   Processed {len(result.get('intelligence', []))} intelligence items")

        return 0

    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running RSS Feed Agent: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def _output_results(result: dict, format_type: str, output_file: str, prefix: str):
    """Output results in requested format"""

    # Generate filename if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/output/{prefix}_result_{timestamp}.json"

    # Ensure output directory exists
    config.ensure_directories()

    if format_type == "json":
        # Save as JSON
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"💾 Results saved to: {output_path}")

    elif format_type == "table":
        # Display as table
        _display_table(result)
        # Still save JSON
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"💾 Full results saved to: {output_path}")

    elif format_type == "summary":
        # Display summary
        _display_summary(result)
        # Still save JSON
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"💾 Full results saved to: {output_path}")

def _display_table(result: dict):
    """Display results in table format"""
    try:
        from tabulate import tabulate
    except ImportError:
        print("❌ tabulate package required for table format. Install with: pip install tabulate")
        return

    intelligence = result.get("intelligence", [])
    if not intelligence:
        print("📊 No intelligence items to display")
        return

    # Prepare table data
    table_data = []
    for item in intelligence:
        table_data.append([
            item.get("source_name", "")[:20],
            item.get("title", "")[:40],
            len(item.get("cves", [])),
            item.get("admiralty_source_reliability", ""),
            item.get("published_utc", "")[:10],
        ])

    headers = ["Source", "Title", "CVEs", "Reliability", "Published"]
    print("\n📊 Intelligence Items Summary:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def _display_summary(result: dict):
    """Display results summary"""
    intelligence = result.get("intelligence", [])
    total_items = len(intelligence)

    print(f"\n📊 RSS Feed Agent Summary:")
    print(f"   Total items collected: {total_items}")

    if total_items > 0:
        # Count by source type
        sources = {}
        cve_count = 0
        reliability_count = {}

        for item in intelligence:
            source = item.get("source_name", "Unknown")
            sources[source] = sources.get(source, 0) + 1

            cve_count += len(item.get("cves", []))

            reliability = item.get("admiralty_source_reliability", "Unknown")
            reliability_count[reliability] = reliability_count.get(reliability, 0) + 1

        print(f"   Total CVEs found: {cve_count}")

        print("\n   Sources:")
        for source, count in sorted(sources.items()):
            print(f"     {source}: {count} items")

        print("\n   Source Reliability:")
        for reliability, count in sorted(reliability_count.items()):
            print(f"     {reliability}: {count} items")

if __name__ == "__main__":
    exit(main())