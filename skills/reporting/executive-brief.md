---
name: executive-brief
description: Generate executive summary report for leadership
argument-hint: "[timeframe]"
---

You are executing the `/executive-brief` command for NOMAD v2.0. This command generates executive-level threat intelligence summaries focused on business impact and strategic security decisions.

## Command Parameters

- `$ARGUMENTS`: Timeframe (daily, weekly, monthly, quarterly)
- If no parameter: Generate weekly executive brief (default)

## Command Execution

1. **Load Threat Data**: Read from `data/threats-cache.json` for specified timeframe
2. **Business Impact Analysis**: Filter for threats with high business impact
3. **Industry Context**: Apply user's industry and crown jewel context
4. **Executive Synthesis**: Use Task tool to invoke threat-synthesizer agent
5. **Format for Leadership**: Generate business-focused summary

## Response Format

```
📈 EXECUTIVE THREAT INTELLIGENCE BRIEF
[Organization Name] | [Timeframe] | Generated: [Date]

EXECUTIVE SUMMARY
The threat landscape this [period] shows [key trend summary]. Your organization faces [X] critical threats, with particular concern for [primary risk area]. Immediate action is required for [X] vulnerabilities affecting your [crown jewel systems].

🎯 KEY BUSINESS IMPACTS

IMMEDIATE RISKS (Next 48-72 hours):
• [Critical Threat 1]: [Business impact description]
  Financial Risk: [Estimated impact range]
  Affected Systems: [Crown jewel systems at risk]

STRATEGIC CONCERNS (This Quarter):
• [Industry Trend]: [How this affects your market position]
• [Compliance Issue]: [Regulatory implications]

📊 THREAT LANDSCAPE ANALYSIS

INDUSTRY TARGETING:
Your [Industry] sector experienced [X]% increase in targeting this [period].

CROWN JEWEL RISK ASSESSMENT:
• [Crown Jewel 1]: [Risk Level] - [X] new threats
• [Crown Jewel 2]: [Risk Level] - [Mitigation status]

💰 FINANCIAL & OPERATIONAL IMPACT

COST OF INACTION:
• Potential breach cost: $[X]M - $[Y]M
• Business disruption: [X] hours estimated
• Compliance fines: Up to $[X]M

🚨 EXECUTIVE ACTIONS REQUIRED

IMMEDIATE (This Week):
• [Action Item 1]: [Specific decision needed]
• [Action Item 2]: [Budget/resource allocation]

SHORT-TERM (Next Month):
• [Strategic Initiative]: [Business case]

📋 BOARD COMMUNICATION:
• Key Messages: [3-4 executive talking points]
• Risk Appetite: [Recommendations]
• Success Metrics: [KPIs for tracking]

NEXT EXECUTIVE BRIEF: [Date]
```

Execute this command now to generate executive-level threat intelligence briefing.
