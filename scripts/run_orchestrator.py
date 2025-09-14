#!/usr/bin/env python3
"""
Direct execution script for Orchestrator Agent
Routes intelligence items based on policy rules
"""

import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import agents
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.base_agent import BaseAgent
from src.config.environment import config

class OrchestratorAgent(BaseAgent):
    """Orchestrator agent for routing intelligence items"""

    def __init__(self):
        super().__init__("orchestrator")

    def run(self, input_file: str = None, input_data: dict = None) -> dict:
        """Run orchestrator on intelligence items

        Args:
            input_file: Path to JSON file containing intelligence items
            input_data: Direct input data (alternative to file)

        Returns:
            Routing decisions for each item
        """
        # Load input data
        if input_file:
            with open(input_file, 'r') as f:
                data = json.load(f)
        elif input_data:
            data = input_data
        else:
            raise ValueError("Either input_file or input_data must be provided")

        # Extract intelligence items
        items = []
        if isinstance(data, list):
            items = data
        elif "intelligence" in data:
            items = data["intelligence"]
        elif "items" in data:
            items = data["items"]
        else:
            raise ValueError("Input data must contain 'intelligence' or 'items' array")

        # Prepare orchestrator input
        orchestrator_input = {
            "received_at_utc": self.get_timestamp(),
            "items": items,
            "context": config.get_context_for_agents()
        }

        # Process with LLM
        result = self.process_with_llm(orchestrator_input)

        return {
            "agent_type": "orchestrator",
            "processed_at_utc": self.get_timestamp(),
            "input_items": len(items),
            "routing_decisions": result,
            "context": orchestrator_input["context"]
        }

def main():
    parser = argparse.ArgumentParser(description="Run NOMAD Orchestrator Agent directly")

    # Input options
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to JSON file with intelligence items (or '-' for stdin)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: auto-generated)"
    )

    # Processing options
    parser.add_argument(
        "--format",
        choices=["json", "table", "summary"],
        default="json",
        help="Output format"
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

    print("🎯 NOMAD Orchestrator Agent - Direct Execution")
    print("=" * 50)

    try:
        # Initialize agent
        agent = OrchestratorAgent()
        print(f"✓ Orchestrator Agent initialized")

        # Validate API access
        if not config.anthropic_api_key:
            print("❌ No ANTHROPIC_API_KEY found")
            print("   Set your API key in .env file for LLM processing")
            return 1

        # Load input data
        if args.input == "-":
            print("📥 Reading input from stdin...")
            input_data = json.loads(sys.stdin.read())
        else:
            input_path = Path(args.input)
            if not input_path.exists():
                print(f"❌ Input file not found: {input_path}")
                return 1

            print(f"📥 Loading input from: {input_path}")
            with open(input_path, 'r') as f:
                input_data = json.load(f)

        # Validate input
        items_count = 0
        if isinstance(input_data, list):
            items_count = len(input_data)
        elif "intelligence" in input_data:
            items_count = len(input_data["intelligence"])
        elif "items" in input_data:
            items_count = len(input_data["items"])

        if items_count == 0:
            print("❌ No intelligence items found in input")
            return 1

        print(f"📊 Processing {items_count} intelligence items")

        if args.dry_run:
            print("   [DRY RUN] Would route these items through orchestrator")
            return 0

        # Run orchestrator
        print("🎯 Running orchestrator routing logic...")
        result = agent.run(input_data=input_data)

        # Output results
        _output_results(result, args.format, args.output)

        print(f"✅ Orchestrator Agent completed successfully")

        return 0

    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running Orchestrator Agent: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def _output_results(result: dict, format_type: str, output_file: str):
    """Output results in requested format"""

    # Generate filename if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/output/orchestrator_result_{timestamp}.json"

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
    """Display routing decisions in table format"""
    try:
        from tabulate import tabulate
    except ImportError:
        print("❌ tabulate package required for table format. Install with: pip install tabulate")
        return

    routing_decisions = result.get("routing_decisions", {})

    # Extract decisions from LLM response
    if "response" in routing_decisions:
        decisions = routing_decisions["response"]
        if isinstance(decisions, dict) and "decisions" in decisions:
            decisions = decisions["decisions"]
        elif isinstance(decisions, dict) and "items" in decisions:
            decisions = decisions["items"]
        elif not isinstance(decisions, list):
            print("📊 No routing decisions found in response")
            return
    else:
        print("📊 No routing decisions to display")
        return

    # Prepare table data
    table_data = []
    for decision in decisions:
        if isinstance(decision, dict):
            table_data.append([
                decision.get("title", "")[:40],
                decision.get("route", ""),
                decision.get("owner_team", ""),
                decision.get("sla_hours", ""),
                decision.get("route_reason", "")[:30],
            ])

    headers = ["Title", "Route", "Owner", "SLA Hours", "Reason"]
    print("\n📊 Routing Decisions:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def _display_summary(result: dict):
    """Display routing summary"""
    routing_decisions = result.get("routing_decisions", {})

    print(f"\n📊 Orchestrator Summary:")
    print(f"   Input items: {result.get('input_items', 0)}")

    # Extract decisions from LLM response
    decisions = []
    if "response" in routing_decisions:
        response = routing_decisions["response"]
        if isinstance(response, dict) and "decisions" in response:
            decisions = response["decisions"]
        elif isinstance(response, dict) and "items" in response:
            decisions = response["items"]

    if decisions:
        # Count by route type
        route_counts = {}
        team_counts = {}

        for decision in decisions:
            if isinstance(decision, dict):
                route = decision.get("route", "Unknown")
                route_counts[route] = route_counts.get(route, 0) + 1

                team = decision.get("owner_team", "Unknown")
                team_counts[team] = team_counts.get(team, 0) + 1

        print("\n   Routing Distribution:")
        for route, count in sorted(route_counts.items()):
            print(f"     {route}: {count} items")

        print("\n   Team Assignment:")
        for team, count in sorted(team_counts.items()):
            print(f"     {team}: {count} items")
    else:
        print("   No routing decisions found")

if __name__ == "__main__":
    exit(main())