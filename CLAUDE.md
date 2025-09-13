# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

NOMAD (Notable Object Monitoring And Analysis Director) is an AI-powered threat intelligence orchestration framework consisting of specialized agent prompt templates. The framework processes security threats from RSS feeds, vendor advisories, and security bulletins through a pipeline of AI agents to produce actionable intelligence.

## Architecture

The framework follows a pipeline architecture where each agent has a specific role in the intelligence processing workflow:

```
RSS Feeds → RSS Agent → Orchestrator → Routing Decision
                ↓             ↓              ↓
         Vendor Parser → Enrichment → Deduplication
                              ↓              ↓
                     Evidence Vault    Watchlist Digest
                              ↓              ↓
                     Technical Alert   CISO Report
```

### Agent Routing Logic

The Orchestrator applies strict routing rules in order:
1. **DROP**: Source reliability E/F or info credibility ≥5
2. **TECHNICAL_ALERT**: KEV-listed OR EPSS ≥0.70 OR exploit_status=ITW with HIGH/MEDIUM asset exposure
3. **CISO_REPORT**: CVSS ≥9.0 or significant business impact
4. **WATCHLIST**: Credible but not immediately actionable

## Agent Specifications

### Core Processing Agents

**RSS Feed Agent** (`rss-agent-prompt.md`)
- Parses RSS/Atom feeds between specified time ranges
- Assigns Admiralty credibility ratings (A-F source, 1-6 information)
- Extracts CVEs via regex pattern: `CVE-\d{4}-\d{4,7}`
- Creates dedupe_key from hash of title + source_url
- Output: Normalized JSON with strict schema

**Orchestrator** (`orchestrator-system-prompt.md`)
- Central routing engine applying gating rules
- Routes to: DROP, WATCHLIST, TECHNICAL_ALERT, or CISO_REPORT
- Assigns owner_team (SOC, Vuln Mgmt, IT Ops)
- Sets SLA requirements based on criticality
- Uses asset_exposure context for routing decisions

**Vendor Parser Agent** (`vendor-parser-agent-prompt.md`)
- Specialized parsing for vendor-specific formats
- Extracts structured vulnerability data
- Identifies patch information and mitigation steps

### Enhancement Agents

**Enrichment Agent** (`enrichment-agent-prompt.md`)
- Augments with CVSS scores, EPSS probability, KEV status
- Adds threat actor attribution when available
- Queries external threat intelligence sources

**Deduplication Agent** (`dedup-agent-prompt.md`)
- Prevents duplicate alerts across sources
- Uses similarity matching algorithms
- Maintains dedupe keys for tracking

### Output Generation Agents

**Technical Alert** (`technical-alert-prompt.md`)
- Creates actionable SOC/IT team alerts
- Includes remediation steps and patch links
- Formats for ticket system integration

**CISO Report** (`ciso-report-generator-prompt.md`)
- Executive-level threat summaries
- Business impact focus
- Weekly rollup format

**Watchlist Digest** (`watchlist-digest-agent-prompt.md`)
- Tracks lower-priority threats
- Monitors for escalation triggers
- Periodic summary generation

**Evidence Vault Writer** (`evidence-vault-writer-prompt.md`)
- Archives threat intelligence artifacts
- Maintains chain of custody
- Stores evidence for future reference

## Data Schemas

### Standard Intelligence Item Schema
```json
{
  "source_type": "rss|vendor|cert",
  "source_name": "string",
  "source_url": "https://...",
  "title": "string",
  "summary": "string (≤60 words)",
  "published_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "cves": ["CVE-YYYY-XXXX"],
  "cvss_v3": null|float,
  "cvss_v4": null|float,
  "epss": null|float,
  "kev_listed": true|false|null,
  "kev_date_added": "YYYY-MM-DD"|null,
  "exploit_status": "ITW|PoC|None|null",
  "affected_products": [{"vendor":"", "product":"", "versions":[]}],
  "evidence_excerpt": "direct quote",
  "admiralty_source_reliability": "A-F",
  "admiralty_info_credibility": 1-6,
  "admiralty_reason": "justification",
  "dedupe_key": "stable hash"
}
```

### Admiralty Grading System

**Source Reliability:**
- A: Official vendor advisory, CERT/NCSC/CISA
- B: Major security org (MSRC, Talos, Unit42)
- C: Reputable media/researcher blog
- D: Community forum/unverified blog
- E-F: Unreliable sources (auto-DROP)

**Information Credibility:**
- 1: Primary evidence with vendor confirmation
- 2: Advisory/CERT with cited evidence
- 3: Newsroom/researcher report
- 4: Social/unverified
- 5-6: Unreliable (auto-DROP)

## Implementation Notes

### Current State
- Repository contains only prompt templates (`.md` files)
- No implementation code present yet
- Designed for LLM-based agent execution

### Integration Points
When implementing agents:
- Each agent requires strict JSON input/output validation
- Agents should never guess unknown values (use null)
- Deduplication must occur before routing
- Evidence preservation is mandatory for audit trails

### Performance Targets
- Process 1000+ items/hour
- Sub-second routing decisions
- 70% reduction in duplicate alerts
- Scalable agent architecture

## Commands

Since this is currently a specification repository with no implementation:

```bash
# No build/test commands yet - framework is in design phase
# When implementing, suggested structure:

# Python implementation
pip install -r requirements.txt  # Install dependencies
python -m agents.orchestrator    # Run orchestrator
python -m agents.rss_feed       # Run RSS agent

# Node.js implementation
npm install                      # Install dependencies
npm run orchestrator            # Run orchestrator
npm run rss-agent              # Run RSS agent

# Testing (when implemented)
pytest tests/                   # Python tests
npm test                        # Node.js tests
```

## Policy Configuration

When implementing, key policy parameters to configure:
- `alert_epss_threshold`: Default 0.70
- `alert_cvss_threshold`: Default 9.0
- `sla_hours_critical`: Default 48 hours
- `asset_exposure`: Organization-specific asset mapping
- `legal_sector_keywords`: Industry-specific terms for CISO reports
- ensure you use virtualenv only do not use the system python install