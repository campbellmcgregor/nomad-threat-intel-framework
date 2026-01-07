---
name: refresh
description: Force refresh of threat intelligence data from all sources
---

You are executing the `/refresh` command for NOMAD v2.0. This command forces an immediate refresh of threat intelligence data from all configured feeds, bypassing normal caching intervals.

## Command Execution

1. **Show Current Status**: Display last refresh time and cache status
2. **Feed Health Check**: Validate all configured feeds are accessible
3. **Force Collection**: Use Task tool to invoke threat-collector agent for immediate data gathering
4. **Process Intelligence**: Route new threats through intelligence-processor
5. **Update Cache**: Refresh `data/threats-cache.json` with latest data
6. **Generate Summary**: Show refresh results and new threats discovered

## Response Format

```
🔄 INITIATING THREAT INTELLIGENCE REFRESH

CURRENT STATUS:
• Last Refresh: [Timestamp]
• Cache Age: [X] minutes ago
• Cached Threats: [X] items
• Feed Sources: [X] configured

FEED HEALTH CHECK:
✅ Accessible: [X] feeds
⚠️ Slow Response: [X] feeds (>[500]ms)
❌ Unreachable: [X] feeds

COLLECTING FRESH INTELLIGENCE...
• CISA Advisories: [Progress indicator]
• Microsoft Security: [Progress indicator]
• Red Hat Security: [Progress indicator]
• GitHub Advisories: [Progress indicator]
• [Additional feeds...]

PROCESSING NEW THREATS...
• CVE Enrichment: [X] vulnerabilities processed
• EPSS Scoring: [X] threats scored
• KEV Verification: [X] threats checked
• Deduplication: [X] duplicates removed

📊 REFRESH RESULTS:

NEW THREATS DISCOVERED: [X]
• Critical (CVSS ≥9.0): [X] threats
• High (CVSS 7.0-8.9): [X] threats
• KEV Listed: [X] threats
• Your Industry: [X] relevant threats
• Crown Jewel Impact: [X] threats

UPDATED INTELLIGENCE:
• EPSS Score Changes: [X] threats
• Exploitation Status: [X] updates
• New CVE Assignments: [X] threats

FEED PERFORMANCE:
• Fastest: [Feed Name] ([X]ms)
• Slowest: [Feed Name] ([X]ms)
• Failed: [List of failed feeds]

YOUR PRIORITY ACTIONS:
• [X] critical threats require immediate attention
• [X] crown jewel systems have new vulnerabilities
• [X] industry-specific threats detected

NEXT STEPS:
1. Run `/critical` to see urgent threats
2. Check `/threats` for your personalized briefing
3. Use `/crown-jewel [system]` for asset-specific threats

Cache updated with [X] new threats. Refresh completed in [X] seconds.
```

## Refresh Triggers

The refresh command is useful when:
- **Scheduled Refresh Failed**: Normal automation didn't run
- **Major Security Event**: Need immediate intelligence on breaking news
- **Feed Configuration Changes**: After adding new sources
- **Manual Override**: Force collection outside normal intervals
- **Quality Concerns**: Validate feed health and data freshness

## Performance Considerations

- **Rate Limiting**: Respects feed source rate limits
- **Parallel Collection**: Processes multiple feeds simultaneously
- **Error Handling**: Continues if some feeds fail
- **Cache Protection**: Maintains previous data if refresh fails
- **Resource Management**: Monitors system resources during collection

## Refresh Intervals

Default refresh schedule:
- **Critical Feeds**: Every 15 minutes
- **High Priority**: Every 30 minutes
- **Medium Priority**: Every 2 hours
- **Low Priority**: Every 6 hours
- **Manual Refresh**: On-demand with this command

Execute this command now to force immediate threat intelligence collection and processing from all configured sources.