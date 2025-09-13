#!/usr/bin/env python3
"""
Claude Code Workflow Runner for NOMAD Framework
This script helps Claude Code orchestrate multiple agents in workflows
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta

class NomadWorkflow:
    """Workflow runner for Claude Code agent orchestration"""

    def __init__(self):
        self.config = self._load_config()
        self.results = {}

    def _load_config(self):
        """Load Claude Code agent configuration"""
        config_path = Path("config/claude_agent_config.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def list_workflows(self):
        """List available workflows"""
        print("\n" + "="*60)
        print("AVAILABLE NOMAD WORKFLOWS FOR CLAUDE CODE")
        print("="*60)

        workflows = self.config.get("workflows", {})
        for wf_id, wf_config in workflows.items():
            print(f"\n{wf_id}:")
            print(f"  Name: {wf_config.get('name')}")
            print(f"  Description: {wf_config.get('description')}")
            print(f"  Steps: {len(wf_config.get('steps', []))}")

        print("\n" + "="*60)
        print("\nUsage: python claude_workflow.py run <workflow_name>")
        print("Example: python claude_workflow.py run morning_check")

    def prepare_workflow(self, workflow_name):
        """Prepare a workflow for Claude Code execution"""
        workflows = self.config.get("workflows", {})

        if workflow_name not in workflows:
            print(f"Unknown workflow: {workflow_name}")
            print("Available workflows:", list(workflows.keys()))
            return None

        workflow = workflows[workflow_name]
        print(f"\n{'='*60}")
        print(f"WORKFLOW: {workflow.get('name')}")
        print(f"{'='*60}")
        print(f"Description: {workflow.get('description')}")
        print(f"\nSteps to execute:")

        steps_info = []
        for i, step in enumerate(workflow.get('steps', []), 1):
            if isinstance(step, dict):
                if 'agent' in step:
                    agent_name = step['agent']
                    agent_config = self.config.get('agents', {}).get(agent_name, {})
                    prompt_file = agent_config.get('prompt_file')
                    subagent_type = agent_config.get('subagent_type', 'general-purpose')

                    print(f"\n{i}. {agent_config.get('name', agent_name)}")
                    print(f"   Prompt: {prompt_file}")
                    print(f"   Agent Type: {subagent_type}")

                    steps_info.append({
                        "step": i,
                        "agent": agent_name,
                        "prompt_file": prompt_file,
                        "subagent_type": subagent_type,
                        "config": step.get('config', {})
                    })

                elif 'conditional' in step:
                    print(f"\n{i}. Conditional execution:")
                    for condition in step['conditional']:
                        print(f"   If {condition.get('condition')}: Run {condition.get('agent')}")

                elif 'parallel' in step:
                    print(f"\n{i}. Parallel execution:")
                    for parallel_agent in step['parallel']:
                        print(f"   - {parallel_agent.get('agent')}")

        return steps_info

    def generate_agent_instructions(self, workflow_name):
        """Generate instructions for Claude Code to execute the workflow"""
        steps = self.prepare_workflow(workflow_name)

        if not steps:
            return

        print(f"\n{'='*60}")
        print("CLAUDE CODE EXECUTION INSTRUCTIONS")
        print("="*60)

        print("\nTo execute this workflow, Claude Code should:")
        print("\n1. Run each agent in sequence using the Task tool")
        print("2. Pass the output of each agent as input to the next")
        print("3. Save intermediate results for debugging")

        print("\n" + "="*60)
        print("STEP-BY-STEP COMMANDS FOR CLAUDE CODE:")
        print("="*60)

        for step_info in steps:
            print(f"\n# Step {step_info['step']}: {step_info['agent']}")
            print(f"Task(")
            print(f'    description="{step_info["agent"]} agent",')
            print(f'    prompt=open("{step_info["prompt_file"]}").read(),')
            print(f'    subagent_type="{step_info["subagent_type"]}",')
            print(f'    # Add input_data from previous step')
            print(f")")

        # Save workflow plan
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_file = Path(f"data/output/workflow_plan_{workflow_name}_{timestamp}.json")
        plan_file.parent.mkdir(parents=True, exist_ok=True)

        with open(plan_file, 'w') as f:
            json.dump({
                "workflow": workflow_name,
                "timestamp": timestamp,
                "steps": steps
            }, f, indent=2)

        print(f"\n{'='*60}")
        print(f"Workflow plan saved to: {plan_file}")
        print("\nClaude Code can now execute these agents in sequence!")

    def run_morning_check(self):
        """Example: Morning security check workflow"""
        print("\n" + "="*60)
        print("MORNING SECURITY CHECK WORKFLOW")
        print("="*60)

        # Step 1: Prepare RSS Agent input
        since = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
        until = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        print("\nStep 1: RSS Feed Collection")
        print(f"  Time range: {since} to {until}")
        print("  Priority: high")
        print("  Claude Code should run RSS agent with these parameters")

        # Step 2: Enrichment
        print("\nStep 2: Enrichment")
        print("  Input: RSS agent output")
        print("  Claude Code should run Enrichment agent")

        # Step 3: Orchestrator
        print("\nStep 3: Orchestration")
        print("  Input: Enriched items")
        print("  Claude Code should run Orchestrator agent")

        # Step 4: Generate outputs
        print("\nStep 4: Output Generation")
        print("  Based on routing decisions:")
        print("  - If TECHNICAL_ALERT: Run Technical Alert agent")
        print("  - If CISO_REPORT: Run CISO Report agent")
        print("  - If WATCHLIST: Run Watchlist Digest agent")

        print("\n" + "="*60)
        print("Claude Code can now orchestrate these agents!")

def main():
    """Main entry point"""
    workflow = NomadWorkflow()

    if len(sys.argv) < 2:
        print("\nNOMAD Workflow Runner for Claude Code")
        print("=" * 40)
        print("\nUsage:")
        print("  python claude_workflow.py list")
        print("  python claude_workflow.py run <workflow_name>")
        print("  python claude_workflow.py morning_check")
        print("\nExamples:")
        print("  python claude_workflow.py list")
        print("  python claude_workflow.py run morning_check")
        print("  python claude_workflow.py run weekly_report")
        return

    command = sys.argv[1].lower()

    if command == "list":
        workflow.list_workflows()
    elif command == "run" and len(sys.argv) > 2:
        workflow_name = sys.argv[2]
        workflow.generate_agent_instructions(workflow_name)
    elif command == "morning_check":
        workflow.run_morning_check()
    else:
        print(f"Unknown command: {command}")
        print("Use 'list' to see available workflows or 'run <workflow>' to execute")

if __name__ == "__main__":
    main()