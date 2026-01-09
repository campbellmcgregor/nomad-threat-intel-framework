# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

NOMAD (Notable Object Monitoring And Analysis Director) v2.1 is a Claude Code-native threat intelligence framework designed for conversational interaction. It processes threat data from RSS feeds, vendor advisories, and security bulletins into actionable intelligence using a modern multi-agent plugin architecture.

## Architecture (v2.1 Plugin System)

NOMAD v2.1 uses the modern Claude Code plugin architecture with:

### Directory Structure
```
.claude-plugin/
├── plugin.json           # Main plugin manifest
├── README.md             # Plugin documentation
├── agents/               # 8 specialized agents with YAML frontmatter
├── skills/               # 6 skill groups (25 commands)
│   ├── threat-intelligence/
│   ├── feed-management/
│   ├── configuration/
│   ├── reporting/
│   ├── system/
│   └── deployment/       # Web GUI deployment skills
├── hooks/                # Validation and security hooks
│   ├── hooks.json
│   └── scripts/
└── .mcp.json             # MCP server configuration

.claude/
├── settings.json         # Project permissions and environment
└── commands-legacy/      # Archived v2.0 commands

web-intake-gui/           # Docker-based report sharing web app
├── app/                  # FastAPI application
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

deployment/               # Hetzner Cloud deployment via Ansible
└── ansible/
    ├── playbooks/        # provision, deploy, destroy, backup, logs, status
    ├── inventory/
    └── templates/
```

### Agent System (8 Agents)
Agents are invoked via the Task tool with YAML frontmatter defining behavior:

| Agent | Purpose | Color |
|-------|---------|-------|
| `query-handler` | Main orchestration, query routing | blue |
| `threat-collector` | RSS/feed data collection | green |
| `intelligence-processor` | CVSS/EPSS enrichment | orange |
| `threat-synthesizer` | Response generation | purple |
| `truth-verifier` | CVE verification | red |
| `feed-manager` | Feed subscriptions | cyan |
| `feed-quality-monitor` | Feed health tracking | yellow |
| `setup-wizard` | Progressive onboarding | magenta |

### Skills System (21 Skills in 5 Groups)

Skills are invoked with `/command` syntax:

**Threat Intelligence:**
- `/threats` - Latest personalized briefing
- `/critical` - Critical and KEV-listed threats
- `/cve [CVE-ID]` - Detailed CVE analysis
- `/crown-jewel [system]` - Threats to specific systems
- `/trending` - Trending threats and vectors

**Feed Management:**
- `/add-feeds [industry]` - Add industry-specific feeds
- `/feed-quality` - Feed performance dashboard
- `/import-feeds` - Import OPML/JSON/CSV
- `/refresh` - Force intelligence refresh

**Configuration:**
- `/setup` - Interactive setup wizard
- `/configure [setting]` - Quick config updates
- `/add-crown-jewel` - Add critical system
- `/update-profile` - Update organization info

**Reporting:**
- `/executive-brief` - Executive summary
- `/technical-alert` - SOC/IT alert format
- `/weekly-summary` - Weekly threat landscape

**System:**
- `/status` - System health dashboard
- `/export [format]` - Export data/config
- `/help [command]` - Command reference
- `/setup-verification` - Verification settings
- `/verification-status` - Verification metrics

**Deployment (Web GUI):**
- `/deploy-gui [action]` - Provision, update, or destroy Hetzner server
- `/gui-status` - Check deployment health and metrics
- `/gui-logs [lines]` - View application logs
- `/publish-report [type]` - Push report to web GUI and get share link

### Hooks System

NOMAD uses hooks for validation and security:

| Hook | Event | Purpose |
|------|-------|---------|
| `load-nomad-context` | SessionStart | Load config, check cache |
| `validate-cve-format` | UserPromptSubmit | Validate CVE identifiers |
| `check-setup-completion` | UserPromptSubmit | Ensure setup before ops |
| `verify-threat-source` | PreToolUse (WebFetch) | Verify legitimate sources |
| `check-api-keys` | PreToolUse (WebFetch) | Check API key config |
| `log-threat-query` | PostToolUse (WebFetch) | Audit logging |
| `verify-cache-saved` | Stop | Cache integrity check |

### MCP Server Integration

Real-time threat intelligence APIs:
- **NVD API**: CVE lookup and search
- **EPSS API**: Exploit probability scoring
- **CISA KEV**: Known exploited vulnerabilities
- **Jina.ai**: Web grounding for verification

### Data Flow
1. User query → Query Handler (routes to appropriate agents)
2. Threat collection → RSS feeds parsed → Intelligence processing
3. Enrichment → Deduplication → Asset correlation
4. Synthesis → Personalized response generation

## Key Configuration Files

- **config/user-preferences.json**: Organization profile, crown jewels, verification settings
- **config/threat-sources.json**: Active RSS/threat feed configurations
- **config/threat-sources-premium.json**: 30+ premium feed templates
- **config/threat-sources-templates.json**: Industry-specific feed packages
- **data/threats-cache.json**: Cached threat intelligence data
- **data/feed-quality-metrics.json**: Feed performance tracking
- **data/verification-cache.json**: CVE verification cache
- **data/audit-log.json**: Threat query audit trail

## Usage

### Quick Start
```bash
git clone <repository-url>
cd nomad-actual
claude code

# First time setup
/setup

# Get your first briefing
/threats
```

### Natural Language Queries

The system responds to natural language in addition to commands:
- "What's critical today?" → `/critical`
- "Tell me about CVE-2024-12345" → `/cve CVE-2024-12345`
- "Threats to my web servers" → `/crown-jewel`
- "Brief me for leadership" → `/executive-brief`

### Verification Methods

NOMAD supports three verification methods:

| Method | Cost | Best For |
|--------|------|----------|
| `structured` | Free | NVD/CISA APIs only |
| `jina` | ~$0.001/req | Web grounding |
| `hybrid` | ~$5-10/mo | Production (recommended) |

Configure with `/setup-verification`.

## Key Data Schemas

### Threat Intelligence Item
```json
{
  "id": "unique-id",
  "source_type": "rss|vendor|cert",
  "source_name": "string",
  "title": "string",
  "cves": ["CVE-YYYY-XXXXX"],
  "cvss_v3": 0.0,
  "epss": 0.0,
  "kev_listed": true|false,
  "affected_products": [...],
  "admiralty_credibility": "A1-F6",
  "verification": {
    "confidence": 0.85,
    "sources": ["nvd", "cisa"],
    "last_verified": "2024-01-01T00:00:00Z"
  }
}
```

### Routing Decision Logic
- **CRITICAL**: KEV-listed, EPSS ≥0.70, or CVSS ≥9.0 with exposure
- **HIGH**: CVSS ≥7.0 with asset correlation
- **WATCHLIST**: Credible but not immediately actionable
- **DROP**: Low reliability (E/F rating) or credibility ≥5

## Development

### Adding New Agent
1. Create markdown file in `.claude-plugin/agents/`
2. Add YAML frontmatter with name, description, model, color, tools
3. Include `<example>` blocks in description for discovery
4. Define clear input/output schemas in body

### Adding New Skill
1. Create markdown file in appropriate `.claude-plugin/skills/[group]/`
2. Add YAML frontmatter with name, description, argument-hint
3. Update group's `SKILL.md` trigger patterns if needed

### Adding New Hook
1. Add hook definition to `.claude-plugin/hooks/hooks.json`
2. Create shell script in `.claude-plugin/hooks/scripts/`
3. Make script executable: `chmod +x script.sh`

## Performance Considerations

- Designed for 1000+ items/hour processing
- Threat cache refreshed every 4 hours by default
- Verification cache reduces API calls by ~60%
- Deduplication reduces alerts by ~70%
- Feed quality monitoring identifies problematic sources

## Web Intake GUI

A Docker-based web application for sharing threat intelligence reports with stakeholders.

### Features
- **Link-only access**: Reports only viewable with share links (not browsable)
- **PDF export**: Professional formatting via WeasyPrint
- **Password protection**: Optional for sensitive reports
- **Expiring links**: Configurable TTL (default 72 hours)
- **Hetzner deployment**: Automated via Ansible (~€4.50/month)

### Architecture
```
┌──────────────┐         ┌─────────────────────────────────────┐
│ Claude Code  │  POST   │     Hetzner CX22 (~€4.50/mo)        │
│              │────────►│  ┌─────────────────────────────┐    │
│ /publish-    │         │  │ FastAPI + SQLite            │    │
│  report      │         │  │ - Report storage            │    │
│              │         │  │ - Share link generation     │    │
│              │         │  │ - PDF rendering             │    │
└──────────────┘         │  └─────────────────────────────┘    │
                         │  Caddy (auto-TLS)                   │
                         └─────────────────────────────────────┘
```

### Quick Start
```bash
# Set up environment
export HETZNER_API_TOKEN="your-token"
export NOMAD_WEB_API_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"

# Deploy to Hetzner
/deploy-gui provision

# Publish a report
/publish-report executive-brief

# Check status
/gui-status
```

### API Endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `POST /api/v1/reports` | Token | Submit report |
| `GET /api/v1/reports` | Token | List reports |
| `POST /api/v1/reports/{id}/share` | Token | Create share link |
| `GET /s/{token}` | None | View shared report |
| `GET /s/{token}/pdf` | None | Download PDF |

### Configuration

Add to `config/user-preferences.json`:
```json
{
  "web_gui": {
    "enabled": true,
    "base_url": "https://nomad.example.com",
    "api_token": "${NOMAD_WEB_API_TOKEN}",
    "default_share_hours": 72
  }
}
```

## Admiralty Rating System

All intelligence is rated using the NATO Admiralty Code:
- **Source Reliability**: A (Completely reliable) to F (Cannot be judged)
- **Information Credibility**: 1 (Confirmed) to 6 (Cannot be judged)

Example: "A2" = Completely reliable source, probably true information
