# NOMAD Basic Usage Examples

This guide provides practical examples of using NOMAD for common threat intelligence tasks.

## Table of Contents
- [Processing RSS Feeds](#processing-rss-feeds)
- [Running the Orchestrator](#running-the-orchestrator)
- [Generating Reports](#generating-reports)
- [Simple Workflow Execution](#simple-workflow-execution)

## Processing RSS Feeds

### Example 1: Process High-Priority Feeds

```bash
# Process only high-priority RSS feeds with LLM enhancement
python scripts/run_rss_agent.py --priority high --use-llm --format json

# Process with verbose output for debugging
python scripts/run_rss_agent.py --priority high --use-llm --verbose
```

### Example 2: Process Specific Feed

```bash
# Process a single feed URL
python scripts/run_rss_agent.py \
  --single-feed https://www.cisa.gov/uscert/ncas/current-activity.xml \
  --use-llm \
  --format summary
```

### Example 3: Process Feeds from Last 24 Hours

```bash
# Process feeds with time filtering
python scripts/run_rss_agent.py \
  --since "2025-09-13T00:00:00Z" \
  --until "2025-09-14T00:00:00Z" \
  --output data/output/daily-feed-$(date +%Y%m%d).json
```

## Running the Orchestrator

### Example 4: Route Intelligence Items

```bash
# Process intelligence items through routing logic
python scripts/run_orchestrator.py \
  --input data/output/rss-feed-output.json \
  --output data/output/orchestrator-decisions.json \
  --use-llm
```

### Example 5: Dry Run Mode

```bash
# Test routing logic without LLM calls
python scripts/run_orchestrator.py \
  --input data/output/rss-feed-output.json \
  --dry-run \
  --verbose
```

## Generating Reports

### Example 6: Weekly CISO Report

```bash
# Generate executive report for the week
python scripts/run_ciso_report.py \
  --week-start 2025-09-07 \
  --week-end 2025-09-13 \
  --output weekly-report.json \
  --use-llm
```

### Example 7: Custom Report Period

```bash
# Generate report for custom date range
python scripts/run_ciso_report.py \
  --start-date 2025-09-01 \
  --end-date 2025-09-14 \
  --format markdown \
  --output monthly-report.md
```

## Simple Workflow Execution

### Example 8: Morning Security Check

```bash
# Run the morning check workflow
python nomad_workflow_enhanced.py execute morning_check --mode=direct

# Run with verbose output
python nomad_workflow_enhanced.py execute morning_check --mode=direct --verbose
```

### Example 9: Weekly Report Workflow

```bash
# Generate weekly executive report
python nomad_workflow_enhanced.py execute weekly_report --mode=direct

# Preview what will be executed
python nomad_workflow_enhanced.py plan weekly_report --mode=direct
```

### Example 10: Incident Response Workflow

```bash
# Run incident response for high-priority threats
python nomad_workflow_enhanced.py execute incident_response --mode=direct
```

## Working with Output

### JSON Output Processing

```python
import json

# Load orchestrator decisions
with open('data/output/orchestrator-decisions.json', 'r') as f:
    decisions = json.load(f)

# Filter for technical alerts
tech_alerts = [d for d in decisions['items']
               if d['routing_decision'] == 'TECHNICAL_ALERT']

print(f"Found {len(tech_alerts)} technical alerts")
```

### CSV Export

```python
import pandas as pd
import json

# Convert JSON to CSV for analysis
with open('data/output/rss-feed-output.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data['items'])
df.to_csv('threat-intelligence.csv', index=False)
```

## Environment Configuration

### Basic Setup

```bash
# Set required environment variables
export ANTHROPIC_API_KEY="your-api-key-here"
export ORG_NAME="Your Organization"
export CROWN_JEWELS="Exchange,Active Directory,Database"

# Run with configuration
python scripts/run_rss_agent.py --use-llm
```

### Using .env File

```bash
# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your-api-key-here
ORG_NAME=Your Organization
CROWN_JEWELS=Exchange,Active Directory
BUSINESS_SECTORS=Financial Services,Healthcare
ALERT_CVSS_THRESHOLD=7.0
ALERT_EPSS_THRESHOLD=0.5
EOF

# Run with .env configuration
python scripts/run_rss_agent.py --use-llm
```

## Debugging and Troubleshooting

### Enable Debug Logging

```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG
python scripts/run_rss_agent.py --verbose
```

### Check Configuration

```python
# Verify environment configuration
from src.config.environment import config

# Check API access
config.validate_api_access()

# Display current settings
print(f"Organization: {config.ORG_NAME}")
print(f"Crown Jewels: {config.CROWN_JEWELS}")
print(f"CVSS Threshold: {config.ALERT_CVSS_THRESHOLD}")
```

### Test Single Agent

```bash
# Test RSS agent with minimal input
echo '{"feed_url": "https://example.com/feed.xml"}' | \
  python scripts/run_rss_agent.py --stdin --dry-run
```

## Common Patterns

### Chain Agents Together

```bash
# Step 1: Collect RSS feeds
python scripts/run_rss_agent.py \
  --priority high \
  --use-llm \
  --output /tmp/rss-output.json

# Step 2: Route through orchestrator
python scripts/run_orchestrator.py \
  --input /tmp/rss-output.json \
  --output /tmp/routing-decisions.json \
  --use-llm

# Step 3: Generate alerts
python scripts/run_technical_alert.py \
  --input /tmp/routing-decisions.json \
  --filter "routing_decision=TECHNICAL_ALERT" \
  --output alerts.json
```

### Scheduled Execution

```bash
# Add to crontab for daily execution
0 9 * * * cd /path/to/nomad && python nomad_workflow_enhanced.py execute morning_check --mode=direct

# Weekly report every Monday
0 8 * * 1 cd /path/to/nomad && python nomad_workflow_enhanced.py execute weekly_report --mode=direct
```

## Next Steps

- Review [Advanced Workflows](advanced-workflows.md) for complex scenarios
- Learn about [Custom Agent Development](custom-agents.md)
- See the [User Manual](../user-guide/user-manual.md) for complete feature documentation