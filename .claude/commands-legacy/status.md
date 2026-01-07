---
name: status
description: Display comprehensive system health and configuration status
---

You are executing the `/status` command for NOMAD v2.0. This command provides a comprehensive overview of system health, configuration status, and operational metrics.

## Command Execution

1. **System Health Check**: Assess all system components and data files
2. **Configuration Validation**: Verify all config files are present and valid
3. **Feed Status Analysis**: Check health of all threat intelligence sources
4. **Cache Status**: Evaluate data freshness and cache performance
5. **Generate Status Report**: Comprehensive system overview with health indicators

## Response Format

```
📊 NOMAD SYSTEM STATUS

SYSTEM HEALTH: [🟢 Excellent | 🟡 Good | 🟠 Issues | 🔴 Critical]

CONFIGURATION STATUS:
✅ User Profile: Configured ([Organization Name])
✅ Crown Jewels: [X] systems identified
✅ Feed Sources: [X] feeds active ([Y] premium)
✅ Cache System: Operational ([X] MB, [Y] threats)

THREAT INTELLIGENCE PIPELINE:
• Last Collection: [Timestamp] ([X] minutes ago)
• Collection Success Rate: [X]% (last 24h)
• Processing Latency: [X]ms average
• Cache Hit Rate: [X]%

FEED SOURCE HEALTH:
🟢 Healthy ([X] feeds):
• Response time: <500ms
• Success rate: >95%
• Content quality: High

🟡 Degraded ([X] feeds):
• [Feed Name]: Slow response ([X]ms)
• [Feed Name]: Low quality score ([X]/100)

🔴 Failed ([X] feeds):
• [Feed Name]: HTTP [Error Code] - [Error Description]
• [Feed Name]: Parse error - Invalid RSS format

DATA FRESHNESS:
• Critical Feeds: [X] sources updated in last 15min
• High Priority: [X] sources updated in last 30min
• Medium Priority: [X] sources updated in last 2h
• Stale Sources: [X] not updated in >24h

PERFORMANCE METRICS:
• Total Threats Tracked: [X,XXX]
• CVEs in Database: [X,XXX]
• Average Query Time: [X]ms
• Storage Usage: [X] MB / [Y] GB available
• Memory Usage: [X] MB

YOUR ORGANIZATION METRICS:
• Industry-Relevant Threats: [X] ([Y]% of total)
• Crown Jewel Matches: [X] threats
• Critical Alerts: [X] pending review
• Last Threat Briefing: [Timestamp]

ALERTS & NOTIFICATIONS:
• Alert Queue: [X] pending
• Failed Deliveries: [X] in last 24h
• Threshold Violations: [X] feeds below quality standards
• Maintenance Required: [X] items

RECENT ACTIVITY:
• Threats Added: [X] in last hour
• CVEs Updated: [X] with new EPSS scores
• Feed Changes: [X] sources added/removed
• Config Updates: [X] changes in last 24h

RECOMMENDATIONS:
[If issues detected]
🔧 IMMEDIATE ACTIONS NEEDED:
1. [Specific action required]
2. [Another action if applicable]

💡 OPTIMIZATION SUGGESTIONS:
• [Performance improvement suggestion]
• [Configuration optimization]
• [Feed management recommendation]

NEXT MAINTENANCE:
• Scheduled Cleanup: [Timestamp]
• Feed Rotation: [Timestamp]
• Cache Optimization: [Timestamp]

QUICK FIXES:
• Refresh stale data: /refresh
• Check feed health: /feed-quality
• Update configuration: /configure
• View critical issues: /critical

System status check completed. All major components operational.
```

## Health Indicators

**System Health Levels:**
- 🟢 **Excellent**: All systems operational, no issues
- 🟡 **Good**: Minor issues, system stable
- 🟠 **Issues**: Some problems affecting performance
- 🔴 **Critical**: Major problems requiring immediate attention

**Component Status:**
- ✅ **Operational**: Working as expected
- ⚠️ **Degraded**: Working but with reduced performance
- ❌ **Failed**: Not working, requires attention

## Status Categories

### Configuration Health
- User preferences validation
- Crown jewel system verification
- Feed source configuration check
- Alert threshold validation

### Data Pipeline Status
- Collection process health
- Processing latency metrics
- Error rates and failures
- Cache performance indicators

### Feed Source Monitoring
- Response time analysis
- Success rate tracking
- Content quality assessment
- SSL certificate validation

### Performance Metrics
- Query response times
- Storage utilization
- Memory consumption
- Network bandwidth usage

Execute this command now to get comprehensive visibility into NOMAD system health and operational status.