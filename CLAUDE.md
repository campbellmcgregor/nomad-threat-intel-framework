# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

NOMAD (Notable Object Monitoring And Analysis Director) v2.0 is a Claude Code-native threat intelligence framework designed for conversational interaction. It processes threat data from RSS feeds, vendor advisories, and security bulletins into actionable intelligence using a multi-agent architecture.

## Core Architecture

The framework uses a multi-agent pipeline with specialized agents defined as markdown prompt templates in the `agents/` directory:

### Primary Agents
- **query-handler.md**: Main orchestration agent that routes natural language queries
- **threat-collector.md**: Collects and normalizes threat data from configured sources
- **intelligence-processor.md**: Enriches and validates collected threats
- **threat-synthesizer.md**: Generates personalized briefings and responses
- **feed-manager.md**: Manages RSS/threat feed subscriptions and optimizations
- **feed-quality-monitor.md**: Tracks feed performance and health metrics
- **setup-wizard.md**: Guides initial configuration and customization

### Claude Code Skills
NOMAD v2.0 includes 8 specialized skills in `.claude/skills/` for high-performance operations:
- **cve-analyzer.md**: Parallel CVE enrichment (6x faster than sequential)
- **threat-validator.md**: Schema enforcement and data quality scoring
- **csv-handler.md**: CSV import/export for feeds and threat data
- **opml-processor.md**: OPML import/export for RSS feed management
- **pdf-report-generator.md**: Executive-ready PDF reports with charts
- **excel-generator.md**: Multi-worksheet Excel workbooks with analytics
- **feed-quality-analyzer.md**: Feed performance monitoring and optimization
- **threat-pattern-analyzer.md**: Trend detection, campaign correlation, predictions

See `.claude/skills/README.md` for detailed skill documentation.

### Data Flow
1. User query → Query Handler (routes to appropriate agents)
2. Threat collection → RSS feeds parsed → Intelligence processing
3. Enrichment → Deduplication → Asset correlation → **Skills invoked for optimization**
4. Synthesis → Personalized response generation → **Skills for report generation**

## Key Configuration Files

- **config/user-preferences.json**: Organization profile, crown jewels, alert preferences
- **config/threat-sources.json**: Active RSS/threat feed configurations
- **config/threat-sources-premium.json**: 30+ premium feed templates
- **config/threat-sources-templates.json**: Industry-specific feed packages
- **data/threats-cache.json**: Cached threat intelligence data
- **data/feed-quality-metrics.json**: Feed performance tracking

## Usage (Claude Code v2.0)

### Zero Setup Required
```bash
# Clone and launch - that's it!
git clone <repository-url>
cd nomad-threat-intel-framework
claude code
```

### Core Interaction
NOMAD v2.0 runs entirely within Claude Code using natural language:
- No Python installation required
- No dependencies to manage
- No command-line scripts to run
- Pure conversational interface

## Natural Language Query Patterns

The system responds to these query types:

### Data Collection
- "Update threat feeds" / "Refresh intelligence" / "Check for new threats"

### Current Intelligence
- "Show latest threats" / "What's critical?" / "Brief me on threats"

### Specific Searches
- "Tell me about CVE-YYYY-XXXXX" / "[Vendor] threats" / "[Threat type] this week"

### Asset-Specific
- "Threats to [crown jewel]" / "[Technology] vulnerabilities" / "Internet-facing risks"

### Feed Management
- "Add [industry] feeds" / "Import my OPML" / "Show feed quality" / "Optimize feeds"

### Configuration
- "Update preferences" / "Add crown jewel" / "Configure for [industry]"

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
  "admiralty_credibility": "A1-F6"
}
```

### Routing Decision Logic
- **CRITICAL**: KEV-listed, EPSS ≥0.70, or CVSS ≥9.0 with exposure
- **HIGH**: CVSS ≥7.0 with asset correlation
- **WATCHLIST**: Credible but not immediately actionable
- **DROP**: Low reliability (E/F rating) or credibility ≥5

## Development Workflow

1. **User makes natural language query** → Query handler interprets intent
2. **Agents are invoked** → Each agent follows its markdown prompt template
3. **Data flows through pipeline** → Collection → Processing → Synthesis
4. **Response generated** → Personalized to user's organization profile

## Testing Approach

- Agent behavior is defined by markdown prompt templates in `agents/`
- Test by making natural language queries to Claude Code
- Feed quality monitoring built into the system
- No external testing framework required

## Important Implementation Notes

1. **v2.0 Design**: Optimized for Claude Code interaction, not standalone Python execution
2. **Agent Templates**: Markdown files in `agents/` define behavior, not Python code
3. **Conversational Interface**: Primary interaction through natural language, not CLI commands
4. **Feed Management**: 30+ premium feeds pre-configured, industry templates available
5. **Crown Jewels Focus**: Intelligence filtering based on critical business assets
6. **Admiralty Grading**: All intelligence rated A-F (source) and 1-6 (information)

## Common Development Tasks

### Adding New Threat Feeds
1. Edit `config/threat-sources.json` or use "Add [source] feed" query
2. Premium templates available in `config/threat-sources-premium.json`
3. Industry packages in `config/threat-sources-templates.json`

### Customizing Organization Profile
1. Update `config/user-preferences.json`
2. Define crown jewels (critical systems)
3. Set industry sectors for targeted intelligence

### Implementing New Agent
1. Create markdown prompt template in `agents/`
2. Define clear input/output schemas
3. Update query-handler routing logic
4. Test with example queries

### Debugging Feed Issues
- Ask: "Show feed quality" for performance analysis
- Ask: "Check feed status" for accessibility issues
- Ask: "Optimize my feeds" for recommendations

### Working with Skills
Skills are reusable components in `.claude/skills/` that provide optimized implementations for common operations:

1. **Skills are automatically invoked** by agents and slash commands as needed
2. **Key skills**:
   - `cve-analyzer`: 6x faster CVE enrichment (parallel NVD/EPSS/KEV fetching)
   - `threat-validator`: Ensures data quality and schema compliance
   - `csv-handler` / `opml-processor`: Feed import/export automation
   - `pdf-report-generator` / `excel-generator`: Professional reporting
   - `feed-quality-analyzer`: Performance monitoring and optimization
   - `threat-pattern-analyzer`: Trend detection and predictions

3. **Agents invoke skills** when specialized operations are needed:
   - Intelligence processor → Uses `cve-analyzer` for CVE enrichment
   - Threat collector → Uses `threat-validator` for data quality
   - Feed manager → Uses `opml-processor` and `csv-handler` for imports
   - Threat synthesizer → Uses report generators for output

4. **Skills vs Agents**:
   - Agents: Orchestrate workflows, handle conversation, maintain context
   - Skills: Perform specific technical operations, optimized for performance

See `.claude/skills/README.md` for detailed documentation of all skills.

## Performance Considerations

- Designed for 1000+ items/hour processing
- Threat cache refreshed every 4 hours by default
- Deduplication reduces alerts by ~70%
- Feed quality monitoring identifies problematic sources
- **Skills provide performance optimizations**:
  - CVE analysis: 30-60s → 5-10s (6x faster with parallel fetching)
  - Feed validation: Automated with 95%+ accuracy
  - Report generation: Professional PDF/Excel in 3-5 seconds