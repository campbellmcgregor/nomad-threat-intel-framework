# NOMAD User Manual

Complete guide to using the NOMAD Threat Intelligence Framework for security professionals.

## Table of Contents

- [Overview](#overview)
- [Core Concepts](#core-concepts)
- [Agents and Workflows](#agents-and-workflows)
- [Execution Modes](#execution-modes)
- [Output Formats](#output-formats)
- [Advanced Features](#advanced-features)
- [Use Cases](#use-cases)
- [Best Practices](#best-practices)

## Overview

NOMAD (Notable Object Monitoring And Analysis Director) is a comprehensive AI-powered threat intelligence framework designed to automate the collection, analysis, and distribution of security threats.

### Key Capabilities

- **Automated Collection**: Ingests threat data from 100+ RSS feeds, vendor advisories, and security bulletins
- **AI-Powered Analysis**: Uses Claude AI to analyze, prioritize, and contextualize threats
- **Intelligent Routing**: Automatically routes threats to appropriate teams (SOC, Vuln Management, IT Ops)
- **Executive Reporting**: Generates business-focused summaries for leadership
- **Flexible Execution**: Supports both interactive (Claude Code) and automated (CLI) workflows

### Architecture Overview

```
RSS Feeds → RSS Agent → Orchestrator → Routing Decision
                ↓             ↓              ↓
         Vendor Parser → Enrichment → Deduplication
                              ↓              ↓
                     Evidence Vault    Watchlist Digest
                              ↓              ↓
                     Technical Alert   CISO Report
```

## Core Concepts

### Intelligence Items

Every piece of threat intelligence in NOMAD is represented as a standardized **Intelligence Item** with these key fields:

```json
{
  "source_type": "rss",
  "source_name": "CISA Alerts",
  "source_url": "https://example.com/alert",
  "title": "Critical VMware vCenter Vulnerability",
  "summary": "Authentication bypass vulnerability...",
  "published_utc": "2025-09-13T10:00:00Z",
  "cves": ["CVE-2025-1234"],
  "cvss_v3": 9.8,
  "kev_listed": true,
  "admiralty_source_reliability": "A",
  "admiralty_info_credibility": 2
}
```

### Admiralty Grading System

NOMAD uses the NATO Admiralty Code to rate source reliability and information credibility:

**Source Reliability (A-F):**
- **A**: Official vendor advisory, CERT/NCSC/CISA
- **B**: Major security organization (MSRC, Talos, Unit42)
- **C**: Reputable media/researcher blog
- **D**: Community forum/unverified blog
- **E-F**: Unreliable sources (auto-dropped)

**Information Credibility (1-6):**
- **1**: Primary evidence with vendor confirmation
- **2**: Advisory/CERT with cited evidence
- **3**: Newsroom/researcher report
- **4**: Social/unverified content
- **5-6**: Unreliable (auto-dropped)

### Routing Logic

The Orchestrator applies strict routing rules in priority order:

1. **DROP**: Source reliability E/F OR info credibility ≥5
2. **TECHNICAL_ALERT**: KEV-listed OR EPSS ≥0.70 OR exploit_status=ITW with HIGH/MEDIUM asset exposure
3. **CISO_REPORT**: CVSS ≥9.0 OR significant business impact
4. **WATCHLIST**: Credible but not immediately actionable

## Agents and Workflows

### Core Agents

#### RSS Feed Agent
**Purpose**: Collects and normalizes threat intelligence from RSS/Atom feeds

**Key Features**:
- Supports 100+ feed formats
- CVE extraction via regex patterns
- Automatic deduplication
- Time-range filtering
- Source reliability assessment

**Usage Examples**:
```bash
# Basic collection (last 7 days)
python scripts/run_rss_agent.py --use-llm

# High-priority feeds only
python scripts/run_rss_agent.py --priority high --use-llm

# Specific date range
python scripts/run_rss_agent.py --since 2025-09-01 --until 2025-09-07 --use-llm

# Single feed testing
python scripts/run_rss_agent.py --single-feed https://feeds.feedburner.com/eset/blog --use-llm

# Vendor advisories only
python scripts/run_rss_agent.py --source-type vendor --use-llm
```

#### Orchestrator Agent
**Purpose**: Routes intelligence items based on organizational policy and threat severity

**Key Features**:
- Policy-based routing rules
- Asset exposure assessment
- SLA assignment
- Owner team allocation

**Usage Examples**:
```bash
# Route RSS output
python scripts/run_orchestrator.py --input data/output/rss_feed_result_*.json

# Custom input file
python scripts/run_orchestrator.py --input custom_intel.json --format table

# From stdin
cat threat_data.json | python scripts/run_orchestrator.py --input - --verbose
```

#### CISO Report Agent
**Purpose**: Generates executive-level weekly threat summaries

**Key Features**:
- Business impact focus
- Metrics and KPIs
- Decision tracking
- Risk trend analysis

**Usage Examples**:
```bash
# Weekly report from routing decisions
python scripts/run_ciso_report.py --decisions data/output/orchestrator_result_*.json

# Custom date range
python scripts/run_ciso_report.py --week-start 2025-09-01 --week-end 2025-09-07

# Markdown output
python scripts/run_ciso_report.py --decisions decisions.json --format markdown

# Generate sample template
python scripts/run_ciso_report.py --template
```

### Pre-built Workflows

#### Morning Security Check
**Purpose**: Daily high-priority threat assessment

**Steps**:
1. Collect high-priority RSS feeds (last 24 hours)
2. Route intelligence items
3. Generate alerts and reports

```bash
python nomad_workflow_enhanced.py execute morning_check
```

#### Weekly CISO Report
**Purpose**: Executive summary for leadership

**Steps**:
1. Collect all feeds (last 7 days)
2. Route and prioritize
3. Generate executive report

```bash
python nomad_workflow_enhanced.py execute weekly_report
```

#### Vendor Advisory Check
**Purpose**: Process vendor security bulletins

**Steps**:
1. Collect vendor feeds only
2. Parse vendor-specific formats
3. Enrich with external data
4. Route based on asset exposure

```bash
python nomad_workflow_enhanced.py execute vendor_check
```

## Execution Modes

### Interactive Mode (Claude Code)
Use NOMAD agents within Claude Code for interactive analysis:

```python
# Generate execution plan
python nomad_workflow_enhanced.py plan morning_check --mode=claude_code

# Then use Task tool in Claude Code:
Task(
    description="RSS Feed Agent",
    prompt=open("rss-agent-prompt.md").read(),
    subagent_type="general-purpose"
)
```

### Automated Mode (Direct Execution)
Run complete workflows with error recovery:

```bash
# Full workflow with monitoring
python nomad_workflow_enhanced.py execute morning_check

# Generate execution plan first
python nomad_workflow_enhanced.py plan morning_check --mode=direct
```

### Individual Agent Mode
Run single agents for testing or custom workflows:

```bash
# Each agent independently
python scripts/run_rss_agent.py --use-llm
python scripts/run_orchestrator.py --input output.json
python scripts/run_ciso_report.py --decisions routing.json
```

## Output Formats

### JSON Format (Default)
Structured data suitable for further processing:

```json
{
  "agent_type": "rss",
  "collected_at_utc": "2025-09-13T14:30:22Z",
  "intelligence": [
    {
      "title": "Critical Exchange Server Vulnerability",
      "cves": ["CVE-2025-1234"],
      "cvss_v3": 9.8,
      "admiralty_source_reliability": "A"
    }
  ]
}
```

### Table Format
Human-readable tabular output:

```
┌─────────────────────┬──────────────────────────────┬──────┬──────────────┬─────────────┐
│ Source              │ Title                        │ CVEs │ Reliability  │ Published   │
├─────────────────────┼──────────────────────────────┼──────┼──────────────┼─────────────┤
│ CISA Alerts         │ Critical VMware vCenter...   │ 1    │ A            │ 2025-09-13  │
│ Microsoft Security  │ Windows Kernel Exploit...    │ 2    │ A            │ 2025-09-12  │
└─────────────────────┴──────────────────────────────┴──────┴──────────────┴─────────────┘
```

### Summary Format
High-level overview with key metrics:

```
📊 RSS Feed Agent Summary:
   Total items collected: 15
   Total CVEs found: 8

   Sources:
     CISA Alerts: 5 items
     Microsoft Security: 3 items

   Source Reliability:
     A: 10 items
     B: 3 items
     C: 2 items
```

### Executive Format (CISO Reports)
Business-focused presentation:

```
📊 CISO Report Summary:
   Period: 2025-09-07 to 2025-09-13

   Headline: 3 critical vulnerabilities patched, 2 ITW campaigns contained

   Key Metrics:
     Alerts Created: 12
     Alerts Closed: 9
     Median Time To Patch Hours: 26
     SLA Compliance Rate: 92%
```

### Markdown Format
Documentation-ready output:

```markdown
# Weekly Threat Intelligence Report

**Period:** 2025-09-07 to 2025-09-13

## Executive Summary
This week demonstrated strong incident response capability...

## Top Risks
1. **Microsoft Exchange Server** - CVE-2025-1234
   - Impact: Internet-facing email infrastructure
   - Status: Patched
```

## Advanced Features

### Filtering and Time Ranges

**Date Range Filtering**:
```bash
# Specific date range
--since 2025-09-01 --until 2025-09-07

# Relative times (RSS agent only)
--since "7 days ago"
--since "24 hours ago"
```

**Priority Filtering**:
```bash
# High priority feeds only
--priority high

# Medium and low priority
--priority medium
```

**Source Type Filtering**:
```bash
# Vendor advisories only
--source-type vendor

# CERT/government sources
--source-type cert

# Research organizations
--source-type research
```

### Dry Run Mode
Test execution without making API calls:

```bash
# See what would be processed
python scripts/run_rss_agent.py --priority high --dry-run

# Validate workflow plan
python nomad_workflow_enhanced.py plan morning_check --mode=direct
```

### Verbose Logging
Enable detailed logging for troubleshooting:

```bash
# Detailed execution logs
python scripts/run_rss_agent.py --verbose --use-llm

# Debug level logging
LOG_LEVEL=DEBUG python scripts/run_orchestrator.py --input data.json
```

### Custom Output Files
Specify output locations:

```bash
# Custom output file
python scripts/run_rss_agent.py --output-file custom_results.json

# Multiple formats
python scripts/run_ciso_report.py --format markdown --output weekly_report.md
```

### Checkpointing and Recovery
Automatic workflow state preservation:

```bash
# Workflow automatically creates checkpoints
python nomad_workflow_enhanced.py execute morning_check

# Checkpoints saved to data/checkpoints/
# Recovery logs in data/logs/
```

## Use Cases

### Daily Security Operations

**Morning Threat Briefing**:
```bash
# Automated daily run at 8 AM
0 8 * * * cd /path/to/nomad && python nomad_workflow_enhanced.py execute morning_check
```

**Incident Response Support**:
```bash
# Rapid threat assessment for specific CVE
python scripts/run_rss_agent.py --single-feed <vendor-feed> --use-llm
python scripts/run_orchestrator.py --input output.json
```

### Weekly Executive Reporting

**CISO Weekly Brief**:
```bash
# Generate weekly report every Monday
0 9 * * 1 cd /path/to/nomad && python nomad_workflow_enhanced.py execute weekly_report
```

**Board Meeting Preparation**:
```bash
# Custom date range for board meetings
python scripts/run_ciso_report.py --week-start 2025-09-01 --week-end 2025-09-30 --format markdown
```

### Vulnerability Management

**Patch Tuesday Processing**:
```bash
# Focus on Microsoft updates
python scripts/run_rss_agent.py --source-type vendor --use-llm
python scripts/run_orchestrator.py --input output.json --format table
```

**KEV List Monitoring**:
```bash
# Monitor CISA KEV additions
python scripts/run_rss_agent.py --priority high --use-llm
# Orchestrator automatically flags KEV-listed items as TECHNICAL_ALERT
```

### Threat Hunting

**IOC Enrichment**:
```bash
# Collect latest threat intelligence
python scripts/run_rss_agent.py --source-type research --use-llm

# Focus on specific threat actors
grep -i "apt29\|lazarus" data/output/rss_feed_result_*.json
```

**Campaign Tracking**:
```bash
# Monitor specific campaigns
python scripts/run_rss_agent.py --verbose --use-llm | grep -i "campaign_name"
```

## Best Practices

### Operational Excellence

**Daily Workflows**:
- Run `morning_check` every business day
- Review TECHNICAL_ALERT items within SLA
- Monitor watchlist for escalation triggers

**Weekly Workflows**:
- Generate CISO reports for leadership
- Review and tune RSS feed sources
- Analyze routing decision accuracy

**Monthly Workflows**:
- Update organization context (crown jewels, sectors)
- Review and optimize agent performance
- Conduct tabletop exercises with threat intelligence

### Data Quality

**Source Management**:
- Regularly audit RSS feed health
- Remove defunct or low-quality sources
- Add emerging high-value sources

**Validation**:
- Spot-check AI routing decisions
- Validate CVE extraction accuracy
- Monitor false positive rates

**Tuning**:
- Adjust routing thresholds based on organizational risk appetite
- Customize Admiralty ratings for specific sources
- Fine-tune asset exposure mappings

### Performance Optimization

**Resource Management**:
- Use appropriate time ranges (avoid excessive historical data)
- Implement API rate limiting for high-volume sources
- Cache results to reduce redundant API calls

**Monitoring**:
- Track agent execution times
- Monitor API usage and costs
- Set up alerting for workflow failures

**Scalability**:
- Batch process large feed collections
- Use parallel execution for independent agents
- Implement data archival for historical intelligence

### Security Considerations

**API Key Management**:
- Rotate API keys regularly
- Use separate keys for dev/test/prod environments
- Monitor API key usage for anomalies

**Data Protection**:
- Encrypt sensitive threat intelligence at rest
- Implement access controls for output files
- Ensure compliance with data retention policies

**Network Security**:
- Validate RSS feed SSL certificates
- Use secure communication channels
- Monitor for feed compromise indicators

---

## Next Steps

For more detailed information:

- **📖 [Configuration Guide](configuration.md)** - Customize NOMAD for your organization
- **🔄 [Workflow Guide](workflows.md)** - Advanced workflow creation and management
- **🆘 [Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **🔒 [Security Guide](../reference/security.md)** - Security best practices
- **📈 [Performance Guide](../reference/performance.md)** - Optimization and tuning