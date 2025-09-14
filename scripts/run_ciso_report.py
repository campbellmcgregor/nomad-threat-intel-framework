#!/usr/bin/env python3
"""
Direct execution script for CISO Report Generator Agent
Creates executive-level weekly threat intelligence summaries
"""

import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path so we can import agents
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.base_agent import BaseAgent
from src.config.environment import config

class CISOReportAgent(BaseAgent):
    """CISO Report generator agent"""

    def __init__(self):
        super().__init__("ciso-report-generator")

    def run(self, week_start: str = None, week_end: str = None,
            decisions_file: str = None, decisions_data: list = None) -> dict:
        """Generate CISO report

        Args:
            week_start: Start of week in YYYY-MM-DD format
            week_end: End of week in YYYY-MM-DD format
            decisions_file: Path to JSON file with routing decisions
            decisions_data: Direct decision data (alternative to file)

        Returns:
            Executive report data
        """
        # Set default week range
        if not week_start or not week_end:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=7)
            week_start = week_start or start_date.strftime("%Y-%m-%d")
            week_end = week_end or end_date.strftime("%Y-%m-%d")

        # Load decisions data
        decisions = []
        if decisions_file:
            with open(decisions_file, 'r') as f:
                data = json.load(f)
                # Extract decisions from various formats
                if isinstance(data, list):
                    decisions = data
                elif "routing_decisions" in data:
                    routing = data["routing_decisions"]
                    if "response" in routing and isinstance(routing["response"], dict):
                        if "decisions" in routing["response"]:
                            decisions = routing["response"]["decisions"]
                        elif "items" in routing["response"]:
                            decisions = routing["response"]["items"]
                elif "decisions" in data:
                    decisions = data["decisions"]
        elif decisions_data:
            decisions = decisions_data

        # Prepare CISO report input
        report_input = {
            "week_start": week_start,
            "week_end": week_end,
            "org_context": config.get_context_for_agents(),
            "decisions": decisions
        }

        # Process with LLM
        result = self.process_with_llm(report_input)

        return {
            "agent_type": "ciso_report",
            "generated_at_utc": self.get_timestamp(),
            "week_start": week_start,
            "week_end": week_end,
            "input_decisions": len(decisions),
            "report": result,
            "org_context": report_input["org_context"]
        }

def main():
    parser = argparse.ArgumentParser(description="Run NOMAD CISO Report Generator directly")

    # Time range options
    parser.add_argument(
        "--week-start",
        type=str,
        help="Week start date (YYYY-MM-DD format, default: 7 days ago)"
    )
    parser.add_argument(
        "--week-end",
        type=str,
        help="Week end date (YYYY-MM-DD format, default: today)"
    )

    # Input options
    parser.add_argument(
        "--decisions",
        type=str,
        help="Path to JSON file with routing decisions (or '-' for stdin)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: auto-generated)"
    )

    # Processing options
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "executive"],
        default="json",
        help="Output format"
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Generate sample template data for testing"
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

    print("📊 NOMAD CISO Report Generator - Direct Execution")
    print("=" * 50)

    try:
        # Initialize agent
        agent = CISOReportAgent()
        print(f"✓ CISO Report Agent initialized")

        # Handle template generation
        if args.template:
            _generate_template(args.output or "sample_decisions.json")
            return 0

        # Validate API access
        if not config.anthropic_api_key:
            print("❌ No ANTHROPIC_API_KEY found")
            print("   Set your API key in .env file for LLM processing")
            return 1

        # Load decisions data
        decisions_data = None
        if args.decisions:
            if args.decisions == "-":
                print("📥 Reading decisions from stdin...")
                decisions_data = json.loads(sys.stdin.read())
            else:
                decisions_path = Path(args.decisions)
                if not decisions_path.exists():
                    print(f"❌ Decisions file not found: {decisions_path}")
                    return 1

                print(f"📥 Loading decisions from: {decisions_path}")
                with open(decisions_path, 'r') as f:
                    decisions_data = json.load(f)

        # Set date range
        week_start = args.week_start
        week_end = args.week_end

        if not week_start:
            start_date = datetime.utcnow() - timedelta(days=7)
            week_start = start_date.strftime("%Y-%m-%d")
        if not week_end:
            week_end = datetime.utcnow().strftime("%Y-%m-%d")

        print(f"📅 Report period: {week_start} to {week_end}")

        if args.dry_run:
            print("   [DRY RUN] Would generate CISO report for this period")
            if decisions_data:
                decision_count = len(decisions_data) if isinstance(decisions_data, list) else 1
                print(f"   Would process {decision_count} routing decisions")
            return 0

        # Run CISO report generation
        print("📊 Generating executive report...")
        result = agent.run(
            week_start=week_start,
            week_end=week_end,
            decisions_data=decisions_data
        )

        # Output results
        _output_results(result, args.format, args.output)

        print(f"✅ CISO Report Generator completed successfully")

        return 0

    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running CISO Report Generator: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def _generate_template(output_file: str):
    """Generate sample template data for testing"""
    sample_data = [
        {
            "route": "TECHNICAL_ALERT",
            "route_reason": "KEV-listed vulnerability with HIGH asset exposure",
            "dedupe_key": "abc123def456",
            "title": "Microsoft Exchange Server Critical RCE Vulnerability",
            "cves": ["CVE-2025-1234"],
            "owner_team": "SOC",
            "sla_due_utc": "2025-09-15T09:00:00Z",
            "status": "In-Progress",
            "cvss_v3": 9.8,
            "kev_listed": True,
            "asset_exposure": "HIGH"
        },
        {
            "route": "CISO_REPORT",
            "route_reason": "CVSS 9.0+ affecting crown jewel systems",
            "title": "VMware vCenter Authentication Bypass",
            "summary": "Critical authentication bypass in vCenter management platform",
            "metadata": {"cvss_v3": 9.3, "affected_systems": "Virtualization Infrastructure"},
            "status": "Done"
        },
        {
            "route": "WATCHLIST",
            "route_reason": "Medium CVSS, monitoring for exploit development",
            "title": "Linux Kernel Privilege Escalation",
            "cves": ["CVE-2025-5678"],
            "status": "Open"
        }
    ]

    config.ensure_directories()
    output_path = Path(output_file)
    with open(output_path, 'w') as f:
        json.dump(sample_data, f, indent=2)

    print(f"📝 Sample template data generated: {output_path}")
    print("   Use this file with --decisions flag for testing")

def _output_results(result: dict, format_type: str, output_file: str):
    """Output results in requested format"""

    # Generate filename if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/output/ciso_report_{timestamp}.json"

    # Ensure output directory exists
    config.ensure_directories()

    if format_type == "json":
        # Save as JSON
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"💾 Results saved to: {output_path}")

    elif format_type == "markdown":
        # Generate markdown report
        _generate_markdown(result, output_file)

    elif format_type == "executive":
        # Display executive summary
        _display_executive(result)
        # Still save JSON
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"💾 Full results saved to: {output_path}")

def _generate_markdown(result: dict, output_file: str):
    """Generate markdown formatted report"""
    report = result.get("report", {})
    response = report.get("response", {})

    # Handle different response formats
    if isinstance(response, dict) and "text_response" in response:
        content = response["text_response"]
    elif isinstance(response, dict):
        # Try to extract structured data
        content = f"# Weekly Threat Intelligence Report\n\n"
        content += f"**Period:** {result.get('week_start')} to {result.get('week_end')}\n\n"

        for key, value in response.items():
            if key != "text_response":
                content += f"**{key.replace('_', ' ').title()}:** {value}\n\n"
    else:
        content = str(response)

    # Save as markdown
    md_file = output_file.replace('.json', '.md')
    output_path = Path(md_file)
    with open(output_path, 'w') as f:
        f.write(content)

    print(f"📄 Markdown report saved to: {output_path}")

    # Also save JSON
    json_path = Path(output_file)
    with open(json_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"💾 Full results saved to: {json_path}")

def _display_executive(result: dict):
    """Display executive summary"""
    print(f"\n📊 CISO Report Summary:")
    print(f"   Period: {result.get('week_start')} to {result.get('week_end')}")
    print(f"   Input decisions: {result.get('input_decisions', 0)}")
    print(f"   Generated at: {result.get('generated_at_utc', '')}")

    report = result.get("report", {})
    if report.get("status") == "success":
        response = report.get("response", {})
        if isinstance(response, dict):
            # Try to extract key metrics
            if "headline" in response:
                print(f"\n   Headline: {response['headline']}")

            if "metrics" in response:
                metrics = response["metrics"]
                print("\n   Key Metrics:")
                for key, value in metrics.items():
                    print(f"     {key.replace('_', ' ').title()}: {value}")
        else:
            print(f"\n   Report generated successfully")
    else:
        print(f"\n   Status: {report.get('status', 'Unknown')}")

if __name__ == "__main__":
    exit(main())