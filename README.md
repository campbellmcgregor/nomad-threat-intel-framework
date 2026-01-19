# NOMAD v2.1 - Claude Code Threat Intelligence Framework

🛡️ **Transform threat intelligence from overwhelming to actionable using Claude Code's native plugin architecture.**

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.ai/code)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.1.0-orange.svg)](CHANGELOG.md)

## What is NOMAD?

NOMAD (Notable Object Monitoring And Analysis Director) is a Claude Code-native threat intelligence framework. Built on the modern plugin architecture, it uses **skills**, **hooks**, **agents**, and **MCP integrations** to deliver personalized, actionable threat intelligence through natural conversation.

### Key Features

- 🎯 **25 Skills** organized into 5 groups (threats, feeds, config, reporting, system)
- 🤖 **10 Specialized Agents** for multi-step threat intelligence workflows
- 🔗 **7 Hooks** for validation, security, and audit logging
- 🔔 **Multi-Channel Notifications** (Slack, Teams, Discord, Email, PagerDuty)
- 📊 **Interactive Threat Dashboard** with heat maps and trend analysis
- 🕵️ **Proactive Threat Hunting** with MITRE ATT&CK mapping
- 🌐 **MCP Integration** for real-time NVD, EPSS, and CISA KEV data
- 👑 **Crown Jewel Correlation** for asset-specific threat prioritization

## Quick Start

### 1. Clone & Launch
```bash
git clone https://github.com/campbellmcgregor/nomad-actual.git
cd nomad-actual
claude
```

### 2. Run Setup
```
/setup
```

### 3. Get Your First Briefing
```
/threats
```

## Architecture

```
nomad-actual/
├── agents/               # 10 specialized agents
├── skills/               # 25 commands in 5 groups
│   ├── threat-intelligence/
│   ├── feed-management/
│   ├── configuration/
│   ├── reporting/
│   ├── system/
│   └── deployment/
├── hooks/                # Validation & security
├── src/                  # Core infrastructure
│   ├── cache/            # SQLite threat database
│   └── notifications/    # Alert dispatching
├── web-intake-gui/       # Dashboard & Reports
│   ├── app/              # FastAPI application
│   └── docker-compose.yml
├── deployment/           # Ansible automation
└── config/               # User configuration
```

## Commands

### Threat Intelligence
| Command | Description |
|---------|-------------|
| `/threats` | Personalized threat briefing |
| `/critical` | Critical and KEV-listed threats |
| `/cve [CVE-ID]` | Detailed CVE analysis |
| `/crown-jewel [system]` | Asset-specific threats |
| `/trending` | Trending attack vectors |
| `/hunt` | **NEW** Run proactive threat hunting sweeps |

### Feed Management
| Command | Description |
|---------|-------------|
| `/add-feeds [industry]` | Add industry feed packages |
| `/feed-quality` | Feed performance dashboard |
| `/import-feeds` | Import OPML/JSON/CSV |
| `/refresh` | Force intelligence refresh |

### Configuration
| Command | Description |
|---------|-------------|
| `/setup` | Interactive setup wizard |
| `/configure [setting]` | Quick config updates |
| `/add-crown-jewel` | Add critical system |
| `/update-profile` | Update organization info |
| `/alert-config` | **NEW** Configure notification channels |

### Reporting & Actions
| Command | Description |
|---------|-------------|
| `/executive-brief` | Executive summary |
| `/technical-alert` | SOC/IT alert format |
| `/weekly-summary` | Weekly threat landscape |
| `/create-ticket` | **NEW** Create Jira/ServiceNow tickets |
| `/compliance-map` | **NEW** Map threats to NIST/CIS/ISO |

### System
| Command | Description |
|---------|-------------|
| `/status` | System health dashboard |
| `/export [format]` | Export data/config |
| `/help [command]` | Command reference |
| `/verification-status` | Verification metrics |

### Web GUI & Deployment
| Command | Description |
|---------|-------------|
| `/deploy-gui` | Deploy dashboard to Hetzner |
| `/publish-report` | Push report to Web GUI |
| `/gui-status` | Check dashboard health |

## Natural Language Interface

NOMAD understands natural language queries:

```
"What's critical today?"          → /critical
"Tell me about CVE-2024-12345"    → /cve CVE-2024-12345
"Threats to my web servers"       → /crown-jewel
"Brief me for leadership"         → /executive-brief
"Add healthcare feeds"            → /add-feeds healthcare
```

## Configuration

### Organization Profile (`config/user-preferences.json`)

```json
{
  "organization": {
    "name": "Your Organization",
    "industry": "Technology"
  },
  "crown_jewels": [
    "Web Application Servers",
    "Database Systems",
    "Authentication Infrastructure"
  ],
  "threat_preferences": {
    "minimum_severity": "medium",
    "focus_areas": ["Remote code execution", "Authentication bypass"]
  }
}
```

### Verification Methods

| Method | Cost | Description |
|--------|------|-------------|
| `structured` | Free | NVD, CISA KEV APIs only |
| `jina` | ~$0.001/req | Web grounding verification |
| `hybrid` | ~$5-10/mo | Both methods combined |

Configure with `/setup-verification`.

## Data Sources

### Government CERTs
- CISA Cybersecurity Advisories
- CISA Known Exploited Vulnerabilities (KEV)
- NCSC UK, CERT-EU, Canadian Cyber Centre
- Australian Cyber Security Centre

### Vendor Advisories
- Microsoft Security Response Center
- Cisco Security Advisories
- And more via RSS feeds

### Enrichment APIs
- **NVD**: CVE details and CVSS scores
- **EPSS**: Exploit probability scoring
- **CISA KEV**: Active exploitation status

## Hooks System

NOMAD includes 7 hooks for validation and security:

| Hook | Event | Purpose |
|------|-------|---------|
| `load-nomad-context` | SessionStart | Load config, check cache |
| `validate-cve-format` | UserPromptSubmit | CVE format validation |
| `check-setup-completion` | UserPromptSubmit | Setup verification |
| `verify-threat-source` | PreToolUse | Source allowlist check |
| `check-api-keys` | PreToolUse | API key validation |
| `log-threat-query` | PostToolUse | Audit logging |
| `verify-cache-saved` | Stop | Cache integrity |

## Multi-Agent Architecture

NOMAD uses 10 specialized agents:

| Agent | Purpose |
|-------|---------|
| `query-handler` | Main orchestration |
| `threat-collector` | RSS/feed collection |
| `intelligence-processor` | CVSS/EPSS enrichment |
| `threat-synthesizer` | Response generation |
| `truth-verifier` | CVE verification |
| `feed-manager` | Feed subscriptions |
| `feed-quality-monitor` | Feed health tracking |
| `setup-wizard` | Progressive onboarding |
| `notification-dispatcher` | **NEW** Multi-channel alerting |
| `threat-hunter` | **NEW** Proactive analysis |

## Admiralty Rating System

All intelligence is rated using the NATO Admiralty Code:

- **Source Reliability**: A (Completely reliable) → F (Cannot be judged)
- **Information Credibility**: 1 (Confirmed) → 6 (Cannot be judged)

Example: `A1` = Completely reliable source, confirmed information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new skills in `.claude-plugin/skills/`
4. Add new agents in `.claude-plugin/agents/`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [CISA](https://www.cisa.gov/) for KEV and advisory data
- [NIST NVD](https://nvd.nist.gov/) for CVE information
- [FIRST.org](https://www.first.org/epss/) for EPSS scoring
- [Anthropic](https://www.anthropic.com/) for Claude Code

---

**Built with Claude Code Plugin Architecture v2.1**

*Transform threat intelligence into actionable insights with natural conversation.*
