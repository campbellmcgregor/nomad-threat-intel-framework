---
name: refresh
description: Force refresh of threat intelligence data from all sources
---

You are executing the `/refresh` command for NOMAD v2.0. This command forces an immediate refresh of threat intelligence data from all configured sources.

## Command Execution

1. **Initiate Collection**: Use Task tool to invoke threat-collector agent
2. **Process Intelligence**: Invoke intelligence-processor for enrichment
3. **Verify Data**: Use truth-verifier for validation
4. **Update Cache**: Write refreshed data to `data/threats-cache.json`
5. **Report Results**: Show collection summary

## Response Format

```
🔄 THREAT INTELLIGENCE REFRESH

STATUS: [In Progress/Completed/Partial]

COLLECTION PHASE:
📡 Processing [X] feed sources...
• ✅ [Source]: [X] new items
• ✅ [Source]: [X] new items
• ⚠️ [Source]: Slow response ([X]s)
• ❌ [Source]: [Error message]

Sources processed: [X]/[Y]
New threats collected: [X]
Processing time: [X] seconds

ENRICHMENT PHASE:
🔍 Enriching collected threats...
• CVEs enriched: [X]
• EPSS scores updated: [X]
• KEV status checked: [X]
• Crown jewel correlation: [X] matches

VERIFICATION PHASE:
✅ Verifying threat accuracy...
• Verified: [X] threats
• Confidence scores: avg [X]%
• API cost: $[X.XX]

📊 REFRESH SUMMARY:
• Total threats in cache: [X,XXX]
• New since last refresh: [X]
• Critical alerts: [X]
• High priority: [X]
• Affecting crown jewels: [X]

⏱️ Cache Freshness:
• Last refresh: Just now
• Next auto-refresh: [Time]
• Cache valid for: 6 hours

💡 QUICK ACTIONS:
• `/threats` - View updated briefing
• `/critical` - See new critical items
• `/feed-quality` - Check source health
```

## Refresh Options

- **Full Refresh**: All sources (default)
- **Critical Only**: High-priority feeds first
- **Selective**: Specific source categories

Execute this command now to force a full refresh of threat intelligence data.
