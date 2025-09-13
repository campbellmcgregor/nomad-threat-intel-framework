#!/usr/bin/env python3
"""
Minimal helper for Claude Code to run NOMAD agents using the Task tool
This script prepares the inputs for Claude Code's agent system
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta

def load_feeds_config():
    """Load RSS feeds configuration"""
    config_path = Path("config/rss_feeds.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            return [
                {"name": feed["name"], "url": feed["url"], "priority": feed.get("priority", "medium")}
                for feed in config.get("feeds", [])
                if feed.get("enabled", True)
            ]
    return []

def load_context_config():
    """Load orchestrator context configuration"""
    return {
        "asset_exposure": {
            "Microsoft Exchange Server": "HIGH",
            "Microsoft Office": "HIGH",
            "Microsoft Windows": "HIGH",
            "VMware vSphere": "MEDIUM",
            "VMware ESXi": "MEDIUM",
            "Ivanti Connect Secure": "MEDIUM",
            "Cisco ASA": "LOW",
            "Apache Log4j": "HIGH",
            "Apache Struts": "MEDIUM"
        },
        "policy": {
            "alert_epss_threshold": 0.70,
            "alert_cvss_threshold": 9.0,
            "sla_hours_critical": 48,
            "legal_sector_keywords": ["DMS", "M365", "e-billing", "videoconf", "law firm", "professional services"]
        }
    }

def prepare_rss_agent_input(args):
    """Prepare input for RSS Feed Agent"""
    since = args.get("since", (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"))
    until = args.get("until", datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))

    # Filter feeds if requested
    feeds = load_feeds_config()
    if args.get("priority"):
        feeds = [f for f in feeds if f.get("priority") == args["priority"]]

    return {
        "crawl_started_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "feeds": feeds[:10],  # Limit to 10 feeds for testing
        "since_utc": since,
        "until_utc": until
    }

def prepare_orchestrator_input(items_file=None):
    """Prepare input for Orchestrator Agent"""
    items = []

    if items_file and Path(items_file).exists():
        with open(items_file, 'r') as f:
            data = json.load(f)
            items = data.get("intelligence", [])

    return {
        "received_at_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": items,
        "context": load_context_config()
    }

def prepare_enrichment_input(items_file=None):
    """Prepare input for Enrichment Agent"""
    items = []

    if items_file and Path(items_file).exists():
        with open(items_file, 'r') as f:
            data = json.load(f)
            items = data.get("intelligence", [])

    # Simplify for enrichment
    simplified = [
        {
            "dedupe_key": item.get("dedupe_key", ""),
            "cves": item.get("cves", []),
            "source_url": item.get("source_url", ""),
            "title": item.get("title", ""),
            "summary": item.get("summary", "")
        }
        for item in items
    ]

    return {
        "queried_at_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": simplified
    }

def main():
    """Main entry point for Claude Code agent runner"""

    if len(sys.argv) < 2:
        print("NOMAD Agent Runner for Claude Code")
        print("=" * 40)
        print("\nUsage: python run_agent.py <agent> [options]")
        print("\nAvailable agents:")
        print("  rss         - RSS Feed Agent")
        print("  orchestrator - Orchestrator Agent")
        print("  enrichment  - Enrichment Agent")
        print("  dedup       - Deduplication Agent")
        print("  alert       - Technical Alert Agent")
        print("  ciso        - CISO Report Agent")
        print("\nExamples:")
        print("  python run_agent.py rss --since 2024-01-13")
        print("  python run_agent.py orchestrator --input intel.json")
        print("  python run_agent.py enrichment --input intel.json")
        return

    agent = sys.argv[1].lower()

    # Map agent names to prompt files
    agent_prompts = {
        "rss": "rss-agent-prompt.md",
        "orchestrator": "orchestrator-system-prompt.md",
        "enrichment": "enrichment-agent-prompt.md",
        "dedup": "dedup-agent-prompt.md",
        "alert": "technical-alert-prompt.md",
        "ciso": "ciso-report-generator-prompt.md",
        "watchlist": "watchlist-digest-agent-prompt.md",
        "evidence": "evidence-vault-writer-prompt.md"
    }

    if agent not in agent_prompts:
        print(f"Unknown agent: {agent}")
        return

    prompt_file = Path(agent_prompts[agent])

    if not prompt_file.exists():
        print(f"Prompt file not found: {prompt_file}")
        return

    # Read the prompt
    with open(prompt_file, 'r') as f:
        prompt = f.read()

    # Prepare input based on agent type
    args = {}
    for i in range(2, len(sys.argv)):
        if sys.argv[i].startswith("--"):
            key = sys.argv[i][2:]
            value = sys.argv[i+1] if i+1 < len(sys.argv) else None
            args[key] = value

    # Generate appropriate input
    if agent == "rss":
        input_data = prepare_rss_agent_input(args)
    elif agent == "orchestrator":
        input_data = prepare_orchestrator_input(args.get("input"))
    elif agent == "enrichment":
        input_data = prepare_enrichment_input(args.get("input"))
    else:
        input_data = {}

    # Output instructions for Claude Code
    print(f"\n{'='*60}")
    print(f"READY TO RUN: {agent.upper()} AGENT")
    print(f"{'='*60}")
    print(f"\nPrompt File: {prompt_file}")
    print(f"\nAgent Type: general-purpose")
    print(f"\nInput Data (for Claude Code Task tool):")
    print(json.dumps(input_data, indent=2))
    print(f"\n{'='*60}")
    print("\nClaude Code Instructions:")
    print("1. Use the Task tool with subagent_type='general-purpose'")
    print(f"2. Load the prompt from: {prompt_file}")
    print("3. Pass the input data shown above")
    print("4. The agent will return structured JSON output")
    print(f"\n{'='*60}")

    # Save input to file for easy access
    input_file = Path(f"data/input/agent_input_{agent}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    input_file.parent.mkdir(parents=True, exist_ok=True)
    with open(input_file, 'w') as f:
        json.dump(input_data, f, indent=2)

    print(f"\nInput saved to: {input_file}")
    print("\nClaude Code can now use the Task tool to run this agent!")

if __name__ == "__main__":
    main()