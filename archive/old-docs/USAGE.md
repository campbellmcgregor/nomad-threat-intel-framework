# NOMAD Framework - Claude Code Usage Guide

## Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Or create a virtual environment first
python -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

## Available Commands for Claude Code

### 1. Collect RSS Feeds
```bash
# Collect all feeds from the last 7 days (default)
python nomad.py rss

# Collect high-priority feeds only
python nomad.py rss --priority high

# Collect feeds from a specific date range
python nomad.py rss --since 2024-01-01 --until 2024-01-07

# Collect only CERT/CSIRT feeds
python nomad.py rss --source-type cert

# Collect vendor security advisories
python nomad.py rss --source-type vendor --priority high
```

### 2. List Available Feeds
```bash
# List all configured feeds
python nomad.py list-feeds

# List only high-priority feeds
python nomad.py list-feeds --priority high

# List only enabled feeds
python nomad.py list-feeds --enabled-only

# List feeds by type
python nomad.py list-feeds --source-type vendor
```

### 3. Test a Single Feed
```bash
# Test a specific feed URL
python nomad.py test-feed "https://www.cisa.gov/cybersecurity-advisories/all.xml"

# Test Microsoft Security Response Center feed
python nomad.py test-feed "https://api.msrc.microsoft.com/update-guide/rss"
```

### 4. Run Full Pipeline (Partial Implementation)
```bash
# Run the full pipeline from the last 7 days
python nomad.py pipeline

# Run pipeline from a specific date
python nomad.py pipeline --since 2024-01-01
```

## Claude Code Integration Examples

When using Claude Code, you can ask it to:

### Example 1: Check for Critical Threats
```
"Check for any critical security threats from the last 24 hours"
```
Claude Code will run:
```bash
python nomad.py rss --since 2024-01-13 --priority high
```

### Example 2: Monitor Specific Vendors
```
"Get the latest Microsoft and VMware security advisories"
```
Claude Code can:
1. Filter the feeds configuration for specific vendors
2. Run RSS collection for those feeds
3. Parse and present the results

### Example 3: Weekly Security Report
```
"Generate a weekly threat intelligence summary"
```
Claude Code will:
1. Collect feeds from the past week
2. Process through the pipeline
3. Generate summary output

## Output Files

All outputs are saved to `data/output/` with timestamps:
- `intel_rss_YYYYMMDD_HHMMSS.json` - RSS collection results
- `pipeline_intel_YYYYMMDD_HHMMSS.json` - Pipeline outputs
- `test_feed_YYYYMMDD_HHMMSS.json` - Feed test results

## Feed Configuration

The RSS feeds are configured in `config/rss_feeds.yaml`. Each feed has:
- **name**: Display name
- **url**: Feed URL
- **priority**: high/medium/low
- **source_type**: cert/vendor/research/news/database
- **enabled**: true/false
- **check_frequency**: hourly/daily/weekly

### Feed Priority Guidelines
- **High Priority**: CERT advisories, major vendor security bulletins, KEV updates
- **Medium Priority**: Security research, additional vendor feeds
- **Low Priority**: Security news, supplementary sources

### Admiralty Grading
The system automatically assigns Admiralty ratings:
- **Source Reliability**:
  - A: Official CERT/vendor advisories
  - B: Major security organizations
  - C: Reputable media/researchers
  - D: Community/unverified sources

- **Information Credibility**:
  - 1: Primary evidence with confirmation
  - 2: Advisory with cited evidence
  - 3: Research organization report
  - 4: Unverified/social media

## Extending the Framework

### Adding New Feeds
Edit `config/rss_feeds.yaml` and add:
```yaml
- name: "New Feed Name"
  url: "https://example.com/feed.xml"
  priority: medium
  source_type: vendor
  enabled: true
  check_frequency: daily
  description: "Description of the feed"
```

### Implementing Additional Agents

The framework is designed for easy extension. Pending agents include:
- **Orchestrator**: Routes items based on policy rules
- **Enrichment**: Adds CVSS, EPSS, KEV data
- **Deduplication**: Removes duplicate items
- **Technical Alert**: Generates SOC alerts
- **CISO Report**: Creates executive summaries
- **Watchlist Digest**: Tracks lower-priority items
- **Evidence Vault**: Archives evidence

## Troubleshooting

### Common Issues

1. **Feed parsing errors**: Some feeds may have format issues. Use `test-feed` to debug.
2. **Date filtering**: Ensure dates are in YYYY-MM-DD format
3. **Missing dependencies**: Run `pip install -r requirements.txt`

### Logging

Detailed logs are output to the console. Adjust logging level in `nomad.py` if needed.

## Next Steps

1. Test RSS feed collection with high-priority feeds
2. Review collected intelligence in `data/output/`
3. Implement additional agents as needed
4. Configure organization-specific asset exposure
5. Set up automated scheduling for regular collection