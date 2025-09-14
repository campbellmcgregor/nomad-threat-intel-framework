# Using NOMAD with Claude Code's Agent System

This guide explains how to use Claude Code as the full orchestrator for the NOMAD threat intelligence framework, leveraging Claude Code's built-in Task tool and agent capabilities.

## Quick Start

### 1. Setup (One-time)
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pyyaml feedparser python-dateutil requests
```

### 2. Basic Agent Execution

Claude Code can run NOMAD agents in three ways:

#### Method 1: Direct Natural Language
Tell Claude Code:
- "Run the RSS Feed Agent to collect today's threats"
- "Use the Orchestrator Agent to route these intelligence items"
- "Execute the morning security check workflow"

#### Method 2: Using Helper Scripts
```bash
# Prepare agent for Claude Code
source venv/bin/activate
python run_agent.py rss --since 2024-01-13

# This shows Claude Code exactly what to run with the Task tool
```

#### Method 3: Workflow Execution
```bash
# List available workflows
python claude_workflow.py list

# Run a workflow
python claude_workflow.py run morning_check
```

## How Claude Code Uses Its Agent System

### Agent Execution Flow

1. **Claude Code receives request** (e.g., "Check for critical threats")
2. **Claude Code uses Task tool** to spawn specialized agents:
   ```python
   Task(
       description="RSS Feed Collection",
       prompt=<contents of rss-agent-prompt.md>,
       subagent_type="general-purpose"
   )
   ```
3. **Agent processes according to prompt** and returns JSON
4. **Claude Code chains agents** passing output to next agent
5. **Results are saved** to `data/output/`

### Available Claude Code Agent Types

- **`general-purpose`**: Best for most NOMAD agents (RSS, Orchestrator, Alerts)
- **`backend-architect`**: Good for API integrations (Enrichment agent)
- **`python-expert`**: For custom data processing
- **`qa-evaluator`**: For validating outputs

## Workflows

### Morning Security Check
```bash
python claude_workflow.py run morning_check
```

Claude Code will:
1. Run RSS Feed Agent (last 24 hours, high priority)
2. Run Enrichment Agent (add CVSS/EPSS data)
3. Run Dedup Agent (remove duplicates)
4. Run Orchestrator Agent (route items)
5. Generate alerts based on routing

### Weekly CISO Report
```bash
python claude_workflow.py run weekly_report
```

Claude Code will:
1. Collect week's intelligence
2. Enrich with context
3. Route through orchestrator
4. Generate executive summary

### Vendor Advisory Check
```bash
python claude_workflow.py run vendor_check
```

Claude Code will:
1. Collect vendor feeds only
2. Parse vendor-specific formats
3. Enrich and route
4. Generate appropriate outputs

## Natural Language Commands

You can ask Claude Code directly:

### Collection Commands
- "Collect all high-priority threats from today"
- "Get Microsoft security advisories from this week"
- "Check CISA feeds for new CVEs"
- "Find any VMware security bulletins"

### Processing Commands
- "Enrich these CVEs with CVSS scores"
- "Remove duplicate intelligence items"
- "Route these items according to policy"

### Output Commands
- "Generate technical alerts for critical items"
- "Create a CISO report for this week"
- "Summarize watchlist items"

### Workflow Commands
- "Run the morning security check"
- "Execute the full NOMAD pipeline"
- "Process today's vendor advisories"

## Example: Complete Pipeline Execution

### Step 1: Tell Claude Code
"Run the full NOMAD pipeline for today's threats"

### Step 2: Claude Code Executes
```python
# 1. RSS Collection
Task(
    description="Collect RSS feeds",
    prompt=open("rss-agent-prompt.md").read(),
    subagent_type="general-purpose",
    input_data={
        "since_utc": "2024-01-13T00:00:00Z",
        "until_utc": "2024-01-13T23:59:59Z",
        "feeds": [...] # From config
    }
)

# 2. Enrichment
Task(
    description="Enrich intelligence",
    prompt=open("enrichment-agent-prompt.md").read(),
    subagent_type="backend-architect",
    input_data=<output from RSS agent>
)

# 3. Orchestration
Task(
    description="Route intelligence",
    prompt=open("orchestrator-system-prompt.md").read(),
    subagent_type="general-purpose",
    input_data=<output from enrichment>
)

# 4. Generate Outputs
# Based on routing decisions...
```

### Step 3: Review Results
- Check `data/output/` for JSON results
- Review routing decisions
- Act on technical alerts

## Configuration Files

### `config/rss_feeds.yaml`
Contains 40+ security RSS feeds categorized by:
- CERT/CSIRT feeds
- Vendor advisories
- Research organizations
- Vulnerability databases

### `config/claude_agent_config.yaml`
Maps NOMAD agents to Claude Code agent types:
- Agent descriptions
- Required inputs
- Workflow definitions

## Helper Scripts

### `run_agent.py`
Prepares individual agents for Claude Code:
```bash
python run_agent.py <agent> [options]

# Examples:
python run_agent.py rss --since 2024-01-13
python run_agent.py orchestrator --input intel.json
python run_agent.py enrichment --input items.json
```

### `claude_workflow.py`
Manages multi-agent workflows:
```bash
python claude_workflow.py list                    # List workflows
python claude_workflow.py run <workflow>          # Run workflow
python claude_workflow.py run morning_check       # Morning check
```

### `nomad.py`
Direct Python implementation (can run without Claude Code):
```bash
python nomad.py rss --priority high              # Collect RSS
python nomad.py list-feeds                       # List feeds
python nomad.py test-feed <URL>                  # Test feed
```

## Output Files

All outputs are saved with timestamps to:
- `data/output/intel_rss_*.json` - RSS collection results
- `data/output/routing_decisions_*.json` - Orchestrator outputs
- `data/output/technical_alerts_*.json` - Generated alerts
- `data/output/workflow_plan_*.json` - Workflow execution plans

## Advanced Usage

### Custom Workflows
Create new workflows in `config/claude_agent_config.yaml`:
```yaml
workflows:
  custom_check:
    name: "Custom Security Check"
    steps:
      - agent: rss_feed
        config:
          source_type: vendor
      - agent: orchestrator
      - agent: technical_alert
```

### Agent Chaining
Claude Code can chain agents dynamically:
```
"Chain RSS → Enrichment → Orchestrator for Microsoft advisories"
```

### Conditional Execution
Claude Code can make decisions:
```
"If any critical CVEs are found, generate technical alerts and notify the team"
```

## Troubleshooting

### Common Issues

1. **Virtual environment not activated**
   ```bash
   source venv/bin/activate
   ```

2. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Feed parsing errors**
   - Some feeds may have format issues
   - Use `python nomad.py test-feed <URL>` to debug

4. **Agent execution errors**
   - Check prompt files exist in root directory
   - Verify input JSON format matches schema

## Best Practices

1. **Always use virtual environment** to avoid system Python conflicts
2. **Start with high-priority feeds** for faster testing
3. **Review routing decisions** before generating alerts
4. **Save intermediate outputs** for debugging
5. **Use workflows** for repeated tasks

## Next Steps

1. Test basic RSS collection
2. Try the morning security check workflow
3. Experiment with natural language commands
4. Customize workflows for your needs
5. Add organization-specific asset exposure mappings

Claude Code's agent system makes NOMAD a fully AI-powered threat intelligence platform!