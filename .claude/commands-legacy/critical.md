---
name: critical
description: Show only critical and KEV-listed threats requiring immediate attention
---

You are executing the `/critical` command for NOMAD v2.0. This command filters threat intelligence to show only the most critical items requiring immediate action.

## Command Execution

1. **Load User Context**: Read `config/user-preferences.json` for personalization filters

2. **Access Threat Data**: Read `data/threats-cache.json` and filter for:
   - Priority level = "critical"
   - KEV-listed threats (kev_listed = true)
   - CVSS v3.1 scores ≥ 9.0
   - EPSS scores ≥ 0.70
   - Active exploitation status ("active_itw", "active_campaign")

3. **Crown Jewel Correlation**: Highlight threats that specifically affect the user's crown jewel systems

4. **Generate Critical Alert**: Use the Task tool to invoke the threat-synthesizer agent with the filtered critical threats

## Response Format

Present results as an urgent alert format:

```
🚨 CRITICAL THREAT ALERT

IMMEDIATE ACTION REQUIRED: [X] Critical Threats

KEV-LISTED VULNERABILITIES: [X]
• CVE-XXXX-XXXXX: [Description] - Affects: [Crown Jewels]
• CVE-XXXX-XXXXX: [Description] - Affects: [Crown Jewels]

ACTIVE EXPLOITATION: [X]
• [Threat description with actor attribution if available]

CROWN JEWEL IMPACTS:
• [System]: [Number] critical threats
• [System]: [Number] critical threats

EMERGENCY ACTIONS:
1. [Highest priority action]
2. [Second priority action]
3. [Monitoring/containment steps]

TIMELINE: Patch within 24-48 hours for KEV items
```

## Filtering Logic

Only include threats that meet ANY of these criteria:
- CVSS v3.1 ≥ 9.0
- Listed in CISA KEV catalog
- Active exploitation confirmed (ITW status)
- EPSS score ≥ 0.70
- Affects user's crown jewel systems AND has CVSS ≥ 7.0

Execute this command now to provide an urgent, filtered view of only the most critical threats requiring immediate organizational response.