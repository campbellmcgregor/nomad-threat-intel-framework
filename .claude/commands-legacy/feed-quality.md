---
name: feed-quality
description: Display feed performance dashboard and recommendations
---

You are executing the `/feed-quality` command for NOMAD v2.0. This command provides a comprehensive dashboard of threat intelligence feed performance, quality metrics, and optimization recommendations.

## Command Execution

1. **Load Quality Metrics**: Read `data/feed-quality-metrics.json` to access:
   - Feed performance scores
   - Response time analytics
   - Update frequency patterns
   - Content quality assessments
   - Reliability ratings

2. **Check Feed Health**: For each configured feed in `config/threat-sources.json`:
   - Validate current accessibility
   - Measure response times
   - Check last update timestamps
   - Assess content relevance

3. **Generate Performance Analysis**: Use Task tool to invoke feed-quality-monitor agent for:
   - Real-time quality scoring
   - Performance trend analysis
   - Optimization recommendations

## Response Format

```
📊 FEED QUALITY DASHBOARD

OVERALL PORTFOLIO HEALTH: [Score]/100 ([Excellent/Good/Needs Attention/Poor])

✅ HIGH PERFORMING FEEDS ([X] feeds):
• [Feed Name]: [Score]/100 - [Response Time]ms
  Status: [Status] | Last Update: [Time] | Priority: [Level]

• [Feed Name]: [Score]/100 - [Response Time]ms
  Status: [Status] | Last Update: [Time] | Priority: [Level]

⚠️ PERFORMANCE ISSUES ([X] feeds):
• [Feed Name]: [Score]/100 - [Issue Description]
  Problem: [Specific issue - slow response/stale content/accessibility]
  Impact: [Effect on threat intelligence]
  Recommendation: [Specific fix or alternative]

❌ OFFLINE/PROBLEM FEEDS ([X] feeds):
• [Feed Name]: [Score]/100 - [Error Description]
  Last Successful: [Timestamp]
  Action Required: [Immediate steps needed]

PERFORMANCE METRICS:
📈 Response Times:
• Average: [X]ms
• Fastest: [Feed Name] ([X]ms)
• Slowest: [Feed Name] ([X]ms)

📅 Update Frequency:
• Daily Updates: [X] feeds
• Weekly Updates: [X] feeds
• Monthly Updates: [X] feeds
• Stale (>30 days): [X] feeds

🎯 Content Quality:
• High Relevance (>80%): [X] feeds
• Medium Relevance (60-80%): [X] feeds
• Low Relevance (<60%): [X] feeds
• Duplicate Content Rate: [X]%

FEED CATEGORIES PERFORMANCE:
• Government CERTs: [Score]/100 ([X] feeds)
• Vendor Advisories: [Score]/100 ([X] feeds)
• Security Research: [Score]/100 ([X] feeds)
• Threat Intelligence: [Score]/100 ([X] feeds)

🔧 OPTIMIZATION RECOMMENDATIONS:

HIGH IMPACT CHANGES:
1. [Recommendation]: [Expected improvement]
   • Action: [Specific steps to take]
   • Impact: [Quantified benefit]

2. [Recommendation]: [Expected improvement]
   • Action: [Specific steps to take]
   • Impact: [Quantified benefit]

FEED MANAGEMENT:
• Remove [X] low-performing feeds (save [X]% processing time)
• Add [X] missing coverage areas for your industry
• Upgrade [X] feeds to premium versions (improve coverage by [X]%)

ALTERNATIVE SOURCES:
• Replace [Feed Name] with [Alternative] (better [metric])
• Consider [New Source] for [Coverage Area] (fills gap in [area])

MAINTENANCE ACTIONS:
• [X] feeds need URL updates
• [X] feeds have SSL certificate issues
• [X] feeds show parsing errors

NEXT STEPS:
1. Run `/optimize-feeds` to apply automated improvements
2. Use `/add-feeds [industry]` to fill coverage gaps
3. Check `/status` for overall system health

Last Quality Check: [Timestamp]
Next Scheduled Check: [Timestamp]
```

## Quality Scoring Algorithm

Feed Quality Score = (Accessibility × 0.25) + (Relevance × 0.30) + (Timeliness × 0.25) + (Uniqueness × 0.20)

Where:
- **Accessibility**: Response time, uptime, SSL validity
- **Relevance**: Security content percentage, keyword density
- **Timeliness**: Update frequency, publication lag
- **Uniqueness**: Non-duplicate content percentage

## Performance Thresholds

- **Excellent**: Score ≥ 90
- **Good**: Score 70-89
- **Needs Attention**: Score 50-69
- **Poor**: Score < 50

Execute this command now to provide comprehensive feed quality analysis with actionable optimization recommendations.