#!/usr/bin/env python3
"""
Enhanced NOMAD Workflow Runner
Supports both Claude Code orchestration and direct agent execution
"""

import sys
import json
import yaml
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta
from config.environment import config

class NomadWorkflow:
    """Enhanced workflow runner for both Claude Code and direct agent execution"""

    def __init__(self):
        self.config = self._load_config()
        self.results = {}
        self.execution_mode = "claude_code"

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
        print("AVAILABLE NOMAD WORKFLOWS")
        print("="*60)

        workflows = self.config.get("workflows", {})
        for wf_id, wf_config in workflows.items():
            print(f"\n{wf_id}:")
            print(f"  Name: {wf_config.get('name')}")
            print(f"  Description: {wf_config.get('description')}")
            print(f"  Steps: {len(wf_config.get('steps', []))}")

        print("\n" + "="*60)
        print("\\nExecution modes:")
        print("  Claude Code: python nomad_workflow_enhanced.py plan <workflow> --mode=claude_code")
        print("  Direct:      python nomad_workflow_enhanced.py execute <workflow>")

    def prepare_workflow(self, workflow_name, execution_mode="claude_code"):
        """Prepare a workflow for execution

        Args:
            workflow_name: Name of workflow to prepare
            execution_mode: 'claude_code' or 'direct'
        """
        workflows = self.config.get("workflows", {})

        if workflow_name not in workflows:
            print(f"❌ Unknown workflow: {workflow_name}")
            print("Available workflows:", list(workflows.keys()))
            return None

        self.execution_mode = execution_mode
        workflow = workflows[workflow_name]
        print(f"\n{'='*60}")
        print(f"WORKFLOW: {workflow.get('name')} [{execution_mode.upper()} MODE]")
        print(f"{'='*60}")
        print(f"Description: {workflow.get('description')}")
        print(f"\\nSteps to execute:")

        steps_info = []
        for i, step in enumerate(workflow.get('steps', []), 1):
            if isinstance(step, dict):
                if 'agent' in step:
                    agent_name = step['agent']
                    agent_config = self.config.get('agents', {}).get(agent_name, {})
                    prompt_file = agent_config.get('prompt_file')
                    subagent_type = agent_config.get('subagent_type', 'general-purpose')

                    print(f"\n{i}. {agent_config.get('name', agent_name)}")
                    if execution_mode == "claude_code":
                        print(f"   Prompt: {prompt_file}")
                        print(f"   Agent Type: {subagent_type}")
                    else:
                        script_path = f"scripts/run_{agent_name}.py"
                        print(f"   Script: {script_path}")
                        print(f"   Direct execution mode")

                    steps_info.append({
                        "step": i,
                        "agent": agent_name,
                        "prompt_file": prompt_file,
                        "subagent_type": subagent_type,
                        "config": step.get('config', {}),
                        "script_path": f"scripts/run_{agent_name}.py"
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

    def generate_execution_plan(self, workflow_name, execution_mode="claude_code"):
        """Generate execution plan for workflow

        Args:
            workflow_name: Name of workflow to execute
            execution_mode: 'claude_code' or 'direct'
        """
        steps = self.prepare_workflow(workflow_name, execution_mode)

        if not steps:
            return

        if execution_mode == "claude_code":
            self._generate_claude_instructions(workflow_name, steps)
        else:
            self._generate_direct_instructions(workflow_name, steps)

    def _generate_claude_instructions(self, workflow_name, steps):
        """Generate Claude Code execution instructions"""
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

        self._save_workflow_plan(workflow_name, steps, "claude_code")

    def _generate_direct_instructions(self, workflow_name, steps):
        """Generate direct execution instructions"""
        print(f"\n{'='*60}")
        print("DIRECT EXECUTION INSTRUCTIONS")
        print("="*60)

        print("\nTo execute this workflow directly:")
        print("\n1. Ensure ANTHROPIC_API_KEY is set in .env file")
        print("2. Run each script in sequence")
        print("3. Pass output files between agents")

        print("\n" + "="*60)
        print("STEP-BY-STEP BASH COMMANDS:")
        print("="*60)

        for step_info in steps:
            agent_name = step_info['agent']
            script_path = step_info['script_path']

            print(f"\n# Step {step_info['step']}: {step_info['agent']}")

            if agent_name == "rss_feed":
                config_params = step_info.get('config', {})
                cmd = f"python {script_path}"
                if 'priority' in config_params:
                    cmd += f" --priority {config_params['priority']}"
                if 'source_type' in config_params:
                    cmd += f" --source-type {config_params['source_type']}"
                if 'since' in config_params:
                    cmd += f" --since {config_params['since']}"
                cmd += " --use-llm --format summary"
                print(cmd)

            elif agent_name == "orchestrator":
                print(f"python {script_path} --input data/output/rss_feed_result_*.json --format summary")

            elif agent_name == "ciso_report":
                print(f"python {script_path} --decisions data/output/orchestrator_result_*.json --format executive")

            else:
                print(f"python {script_path} --help  # Check available options")

        self._save_workflow_plan(workflow_name, steps, "direct")

    def _save_workflow_plan(self, workflow_name, steps, execution_mode):
        """Save workflow execution plan to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_file = Path(f"data/output/workflow_plan_{workflow_name}_{execution_mode}_{timestamp}.json")
        plan_file.parent.mkdir(parents=True, exist_ok=True)

        with open(plan_file, 'w') as f:
            json.dump({
                "workflow": workflow_name,
                "execution_mode": execution_mode,
                "timestamp": timestamp,
                "steps": steps
            }, f, indent=2)

        print(f"\n{'='*60}")
        print(f"📋 Workflow plan saved to: {plan_file}")
        if execution_mode == "claude_code":
            print("\n🤖 Claude Code can now execute these agents in sequence!")
        else:
            print("\n🚀 You can now run these commands to execute the workflow!")

    def execute_workflow(self, workflow_name):
        """Execute a workflow in direct mode with error handling

        Args:
            workflow_name: Name of workflow to execute

        Returns:
            True if successful, False otherwise
        """
        # Validate API key
        if not config.anthropic_api_key:
            print("❌ ANTHROPIC_API_KEY not found")
            print("   Please set your API key in .env file")
            return False

        steps = self.prepare_workflow(workflow_name, "direct")
        if not steps:
            return False

        print(f"\n🚀 EXECUTING WORKFLOW: {workflow_name}")
        print("="*60)

        results = {}
        previous_output = None

        for step_info in steps:
            agent_name = step_info['agent']
            step_num = step_info['step']

            print(f"\n📍 Step {step_num}: {agent_name.upper()} Agent")
            print("-" * 40)

            try:
                result = self._execute_agent_step(agent_name, step_info, previous_output)

                if result and result.get('success'):
                    print(f"✅ {agent_name} completed successfully")
                    if result.get('summary'):
                        print(f"   {result['summary']}")
                    results[agent_name] = result
                    previous_output = result.get('output_file')
                else:
                    print(f"❌ {agent_name} failed")
                    if result and result.get('error'):
                        print(f"   Error: {result['error']}")
                    return False

                # Brief pause between steps
                time.sleep(1)

            except KeyboardInterrupt:
                print(f"\n❌ Workflow interrupted by user")
                return False
            except Exception as e:
                print(f"❌ Unexpected error in {agent_name}: {e}")
                return False

        print(f"\n🎉 WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"📁 Results:")
        for agent_name, result in results.items():
            if result.get('output_file'):
                print(f"  {agent_name}: {result['output_file']}")

        return True

    def _execute_agent_step(self, agent_name, step_info, input_file):
        """Execute a single agent step

        Args:
            agent_name: Name of agent to execute
            step_info: Step configuration
            input_file: Previous step's output file

        Returns:
            Result dict with success status and output file
        """
        script_path = Path(step_info['script_path'])
        if not script_path.exists():
            return {'success': False, 'error': f'Script not found: {script_path}'}

        # Build command
        cmd = ['python', str(script_path)]

        # Add agent-specific arguments
        if agent_name == 'rss_feed':
            config_params = step_info.get('config', {})
            if 'priority' in config_params:
                cmd.extend(['--priority', config_params['priority']])
            if 'source_type' in config_params:
                cmd.extend(['--source-type', config_params['source_type']])
            if 'since' in config_params:
                if config_params['since'] == "24 hours ago":
                    since_date = datetime.utcnow() - timedelta(hours=24)
                    cmd.extend(['--since', since_date.strftime("%Y-%m-%d")])
                elif config_params['since'] == "7 days ago":
                    since_date = datetime.utcnow() - timedelta(days=7)
                    cmd.extend(['--since', since_date.strftime("%Y-%m-%d")])
            cmd.extend(['--use-llm', '--format', 'json'])

        elif agent_name == 'orchestrator':
            if input_file:
                cmd.extend(['--input', input_file])
            else:
                return {'success': False, 'error': 'No input file for orchestrator'}
            cmd.extend(['--format', 'json'])

        elif agent_name == 'ciso_report':
            if input_file:
                cmd.extend(['--decisions', input_file])
            cmd.extend(['--format', 'json'])

        # Execute command
        try:
            print(f"   Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                # Find output file from stdout
                output_file = self._extract_output_file(result.stdout)
                summary = self._extract_summary(result.stdout, agent_name)
                return {
                    'success': True,
                    'output_file': output_file,
                    'summary': summary,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr or 'Command failed',
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }

        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Command timeout (5 minutes)'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _extract_output_file(self, stdout):
        """Extract output file path from command output"""
        lines = stdout.split('\n')
        for line in lines:
            if 'Results saved to:' in line or 'saved to:' in line:
                # Extract file path
                parts = line.split(': ', 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return None

    def _extract_summary(self, stdout, agent_name):
        """Extract summary information from command output"""
        lines = stdout.split('\n')
        for line in lines:
            if 'completed successfully' in line.lower():
                return line.strip('✅ ')
            elif 'items collected' in line or 'items processed' in line:
                return line.strip()
        return f"{agent_name} executed successfully"

def main():
    """Main entry point"""
    workflow = NomadWorkflow()

    if len(sys.argv) < 2:
        print("\n🔥 NOMAD Enhanced Workflow Runner")
        print("=" * 50)
        print("\nUsage:")
        print("  python nomad_workflow_enhanced.py list")
        print("  python nomad_workflow_enhanced.py plan <workflow> [--mode=claude_code|direct]")
        print("  python nomad_workflow_enhanced.py execute <workflow>")
        print("\nExecution Modes:")
        print("  plan    - Generate execution instructions")
        print("  execute - Run workflow directly with error handling")
        print("\nExamples:")
        print("  python nomad_workflow_enhanced.py list")
        print("  python nomad_workflow_enhanced.py plan morning_check")
        print("  python nomad_workflow_enhanced.py plan morning_check --mode=direct")
        print("  python nomad_workflow_enhanced.py execute morning_check")
        return

    command = sys.argv[1].lower()

    # Parse mode flag
    execution_mode = "claude_code"
    if "--mode=direct" in sys.argv:
        execution_mode = "direct"
        sys.argv.remove("--mode=direct")
    elif "--mode=claude_code" in sys.argv:
        execution_mode = "claude_code"
        sys.argv.remove("--mode=claude_code")

    try:
        if command == "list":
            workflow.list_workflows()

        elif command == "plan" and len(sys.argv) > 2:
            workflow_name = sys.argv[2]
            workflow.generate_execution_plan(workflow_name, execution_mode)

        elif command == "execute" and len(sys.argv) > 2:
            workflow_name = sys.argv[2]
            print(f"🎯 Executing workflow: {workflow_name}")
            success = workflow.execute_workflow(workflow_name)
            if not success:
                print("❌ Workflow execution failed")
                sys.exit(1)
            else:
                print("🎉 Workflow execution completed successfully")

        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'list', 'plan <workflow>', or 'execute <workflow>'")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()