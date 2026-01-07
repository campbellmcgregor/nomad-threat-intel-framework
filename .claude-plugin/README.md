# NOMAD Threat Intelligence Plugin

A Claude Code-native threat intelligence framework for personalized security briefings.

## Overview

NOMAD (Notable Object Monitoring And Analysis Director) v2.1 transforms raw threat data from RSS feeds, vendor advisories, and security bulletins into actionable intelligence personalized to your organization's crown jewels and technology stack.

## Features

- **Multi-Agent Architecture**: 8 specialized agents for collection, processing, verification, and synthesis
- **Personalized Intelligence**: Filtered based on your crown jewels, industry, and asset exposure
- **Verification System**: Multi-method validation using NVD, CISA KEV, and Jina.ai grounding
- **Feed Quality Monitoring**: Automatic health tracking and optimization recommendations
- **Progressive Setup**: One-question-at-a-time onboarding in under 3 minutes

## Agents

| Agent | Purpose |
|-------|---------|
| query-handler | Main orchestration and query routing |
| threat-collector | RSS feed collection and normalization |
| intelligence-processor | CVE enrichment (CVSS, EPSS, KEV) |
| threat-synthesizer | Personalized response generation |
| truth-verifier | Multi-source threat validation |
| feed-manager | Feed subscription management |
| feed-quality-monitor | Feed health and performance tracking |
| setup-wizard | Progressive onboarding flow |

## Skills

### Threat Intelligence
- `/threats` - Personalized threat briefing
- `/critical` - Critical and KEV-listed threats
- `/cve [CVE-ID]` - Detailed CVE analysis
- `/crown-jewel [system]` - Asset-specific threats
- `/trending` - Trending attack vectors

### Feed Management
- `/add-feeds [industry]` - Add industry-specific feeds
- `/feed-quality` - Feed performance dashboard
- `/import-feeds` - Import OPML/JSON/CSV
- `/refresh` - Force intelligence refresh

### Configuration
- `/setup` - Initial configuration wizard
- `/configure` - Quick config updates
- `/add-crown-jewel` - Add critical system
- `/update-profile` - Update organization info

### Reporting
- `/executive-brief` - Leadership summary
- `/technical-alert` - SOC/IT alert format
- `/weekly-summary` - Weekly threat landscape

### System
- `/status` - System health dashboard
- `/export` - Export data/config
- `/help` - Command reference

## Hooks

| Hook | Purpose |
|------|---------|
| SessionStart | Load NOMAD context, check cache freshness |
| UserPromptSubmit | Validate CVE format, check setup completion |
| PreToolUse | Verify WebFetch targets are legitimate sources |
| PostToolUse | Log threat queries for audit trail |

## Configuration Files

- `config/user-preferences.json` - Organization profile and crown jewels
- `config/threat-sources.json` - Active feed configuration
- `config/setup-state.json` - Setup progress tracking
- `data/threats-cache.json` - Cached threat intelligence

## Quick Start

```bash
# Clone and open in Claude Code
git clone https://github.com/campbellmcgregor/nomad-actual
cd nomad-actual
claude

# Run setup (auto-triggered if not configured)
/setup

# Get your first briefing
/threats
```

## License

MIT
