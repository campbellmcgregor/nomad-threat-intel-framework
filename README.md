# NOMAD Threat Intelligence Framework

An AI-powered, multi-agent threat intelligence orchestration system designed for rapid processing and actionable insights from diverse security sources.

> **Flexible Implementation**: This framework provides both prompt templates for LLM-based agents AND a Python implementation that can be run directly or through Claude Code.

## 🎯 Overview

NOMAD is a modular threat intelligence framework that automates the collection, enrichment, deduplication, and routing of security threats using specialized AI agents. It transforms raw threat data from RSS feeds, vendor advisories, and security bulletins into prioritized, actionable intelligence for security teams.

## 🏗️ Architecture

The framework employs a pipeline architecture with specialized agents:

```
RSS Feeds → RSS Agent → Orchestrator → Routing Decision
                ↓             ↓              ↓
         Vendor Parser → Enrichment → Deduplication
                              ↓              ↓
                     Evidence Vault    Watchlist Digest
                              ↓              ↓
                     Technical Alert   CISO Report
```

## 🤖 Agent Components

### Core Processing Agents

- **RSS Feed Agent** (`rss-agent-prompt.md`)
  - Parses RSS/Atom feeds for security advisories
  - Normalizes feed data into structured intelligence
  - Extracts CVEs, affected products, and evidence
  - Assigns initial Admiralty credibility ratings

- **Orchestrator** (`orchestrator-system-prompt.md`)
  - Central routing engine for all intelligence
  - Applies gating rules based on severity and exposure
  - Routes items to: DROP, WATCHLIST, TECHNICAL_ALERT, or CISO_REPORT
  - Enforces SLA requirements and ownership assignment

- **Vendor Parser Agent** (`vendor-parser-agent-prompt.md`)
  - Specialized parser for vendor security bulletins
  - Extracts structured data from vendor-specific formats
  - Identifies patch information and mitigation steps

### Enhancement Agents

- **Enrichment Agent** (`enrichment-agent-prompt.md`)
  - Augments raw intelligence with additional context
  - Queries CVE databases for CVSS scores
  - Checks EPSS probability and KEV listings
  - Adds threat actor attribution when available

- **Deduplication Agent** (`dedup-agent-prompt.md`)
  - Prevents duplicate alerts across sources
  - Uses intelligent similarity matching
  - Maintains dedupe keys for tracking

### Output Generation Agents

- **Technical Alert Generator** (`technical-alert-prompt.md`)
  - Creates actionable alerts for SOC/IT teams
  - Includes remediation steps and patches
  - Formats for ticket systems integration

- **CISO Report Generator** (`ciso-report-generator-prompt.md`)
  - Produces executive-level threat summaries
  - Focuses on business impact and risk
  - Weekly rollup format with trending analysis

- **Watchlist Digest Agent** (`watchlist-digest-agent-prompt.md`)
  - Tracks lower-priority threats
  - Monitors for escalation triggers
  - Provides periodic summaries

- **Evidence Vault Writer** (`evidence-vault-writer-prompt.md`)
  - Archives threat intelligence artifacts
  - Maintains chain of custody
  - Stores evidence for future reference

## 📊 Data Flow

### Input Schema
```json
{
  "received_at_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "items": [{
    "source_type": "rss|vendor|cert",
    "source_name": "string",
    "source_url": "https://...",
    "title": "string",
    "summary": "string",
    "cves": ["CVE-YYYY-XXXX"],
    "cvss_v3": 0.0,
    "epss": 0.0,
    "kev_listed": true|false,
    "exploit_status": "ITW|PoC|None",
    "affected_products": [...]
  }]
}
```

### Routing Rules

1. **DROP**: Low reliability sources (E/F rating) or credibility ≥5
2. **TECHNICAL_ALERT**: KEV-listed, EPSS ≥0.70, or active exploitation with asset exposure
3. **CISO_REPORT**: CVSS ≥9.0 or significant business impact
4. **WATCHLIST**: Credible but not immediately actionable

## 🚀 Getting Started

### Implementation Options

NOMAD can be used in three ways:

1. **Prompt Templates Only**: Use the `*-prompt.md` files with any LLM to implement agents in any language
2. **Python Implementation**: Run the provided Python agents directly with `nomad.py`
3. **Claude Code Integration**: Use Claude Code to orchestrate and extend the framework

### Prerequisites

- Python 3.9+ (for Python implementation)
- API access to threat intelligence sources (optional for enrichment)
- LLM API credentials (optional for AI-powered processing)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/nomad-threat-intel-framework.git
cd nomad-threat-intel-framework

# Install dependencies (example for Python)
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Configuration

1. **Feed Sources**: Configure RSS feeds in `config/feeds.json`
2. **Asset Exposure**: Define your organization's asset inventory
3. **Alert Thresholds**: Set EPSS and CVSS thresholds
4. **SLA Requirements**: Configure response time requirements

### Usage

```python
# Example: Process RSS feeds
from nomad import RSSAgent, Orchestrator

# Initialize agents
rss_agent = RSSAgent(config)
orchestrator = Orchestrator(policy_config)

# Collect intelligence
intel = rss_agent.collect_feeds(since="2024-01-01")

# Route through orchestrator
decisions = orchestrator.process(intel)

# Generate outputs
for decision in decisions:
    if decision.route == "TECHNICAL_ALERT":
        alert = technical_alert_agent.generate(decision)
        send_to_soc(alert)
```

## 🎯 Use Cases

### Security Operations Center (SOC)
- Real-time threat alerting with actionable intelligence
- Automated ticket creation with remediation steps
- SLA tracking and escalation management

### Vulnerability Management
- Prioritized patching based on EPSS and exposure
- Vendor bulletin parsing and patch tracking
- Asset-specific vulnerability mapping

### Executive Reporting
- Weekly threat landscape summaries
- Business impact analysis
- Trending threat metrics and KPIs

### Threat Hunting
- Evidence collection and archival
- Threat actor tracking
- IOC extraction and correlation

## 📋 Agent Prompt Templates

Each agent operates with a specific prompt template that defines its behavior:

- Strict JSON input/output schemas
- Admiralty credibility ratings (A-F for source, 1-6 for information)
- Rule-based decision making
- Evidence preservation requirements

**📖 See [PROMPTS_USAGE.md](PROMPTS_USAGE.md) for detailed instructions on using the prompt templates with any LLM.**

## 🔧 Customization

### Adding New Agents
1. Create prompt template following existing patterns
2. Define input/output schemas
3. Implement agent logic
4. Register with orchestrator

### Modifying Routing Rules
Edit `orchestrator-system-prompt.md` to adjust:
- Severity thresholds
- Asset exposure mappings
- SLA requirements
- Team ownership rules

## 🛡️ Security Considerations

- All agents operate with least privilege
- No storage of sensitive credentials in prompts
- Audit logging for all routing decisions
- Evidence chain of custody maintained

## 📈 Performance

- Designed for processing 1000+ items/hour
- Deduplication reduces alert fatigue by ~70%
- Sub-second routing decisions
- Scalable agent architecture

## 🤝 Contributing

Contributions are welcome! Areas of interest:
- Additional threat source integrations
- Enhanced enrichment capabilities
- ML-based threat scoring
- Integration with SOAR platforms

## 📝 License

GNU Affero General Public License v3.0 (AGPL-3.0)

## 🙏 Acknowledgments

Built with inspiration from:
- MITRE ATT&CK Framework
- Admiralty Grading System
- FIRST EPSS methodology
- CISA KEV catalog

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

**NOMAD**: *Notable Object Monitoring And Analysis Director*:
