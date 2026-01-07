---
name: feed-quality
description: Display feed performance dashboard and recommendations
---

You are executing the `/feed-quality` command for NOMAD v2.0. This command displays a comprehensive feed quality dashboard showing performance metrics, health status, and optimization recommendations.

## Command Execution

1. **Load Feed Configuration**: Read `config/threat-sources.json` for active feeds
2. **Gather Quality Metrics**: Read `data/feed-quality-metrics.json` for performance data
3. **Run Health Analysis**: Use Task tool to invoke feed-quality-monitor agent
4. **Generate Dashboard**: Present comprehensive quality report

## Response Format

```
📊 FEED QUALITY DASHBOARD

OVERALL PORTFOLIO HEALTH: [Score]/100 ([Excellent/Good/Fair/Poor])

✅ HIGH PERFORMING ([X] feeds):
• [Feed Name]: [Score]/100 - [Brief status]
• [Feed Name]: [Score]/100 - [Brief status]

⚠️ NEEDS ATTENTION ([X] feeds):
• [Feed Name]: [Score]/100 - [Issue description]
• [Feed Name]: [Score]/100 - [Issue description]

❌ FAILED/DEGRADED ([X] feeds):
• [Feed Name]: [Error description]
• [Feed Name]: [Error description]

📈 QUALITY METRICS:
• Accessibility: [X]% average uptime
• Relevance: [X]% security content
• Timeliness: [X] avg update frequency
• Uniqueness: [X]% non-duplicate content

🔧 OPTIMIZATION OPPORTUNITIES:
• Remove [X] redundant feeds for [X]% efficiency gain
• Add [X] missing feeds for [coverage area]
• Upgrade [X] feeds to premium versions

💡 RECOMMENDATIONS:
1. [Primary recommendation]
2. [Secondary recommendation]
3. [Long-term improvement]

Last Assessment: [Timestamp]
Next Scheduled Check: [Timestamp]
```

## Quality Scoring Algorithm

```
Feed Quality Score = (Accessibility × 0.25) + (Relevance × 0.30) + (Timeliness × 0.25) + (Uniqueness × 0.20)
```

Execute this command now to view comprehensive feed quality analysis and optimization recommendations.
