---
name: executive-brief
description: Generate executive summary report for leadership
usage: /executive-brief [timeframe]
---

You are executing the `/executive-brief` command for NOMAD v2.0. This command generates executive-level threat intelligence summaries focused on business impact and strategic security decisions.

## Command Parameters

- `$1`: Timeframe (daily, weekly, monthly, quarterly)
- If no parameter: Generate weekly executive brief (default)

## Command Execution

1. **Load Threat Data**: Read from `data/threats-cache.json` for specified timeframe
2. **Business Impact Analysis**: Filter for threats with high business impact
3. **Industry Context**: Apply user's industry and crown jewel context
4. **Executive Synthesis**: Use Task tool to invoke executive-synthesizer agent
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
  Mitigation Status: [Current action status]

• [Critical Threat 2]: [Business impact description]
  Operational Risk: [Service disruption potential]
  Customer Impact: [External facing impact]
  Timeline: [Urgency level and deadlines]

STRATEGIC CONCERNS (This Quarter):
• [Industry Trend]: [How this affects your market position]
• [Technology Risk]: [Impact on digital transformation initiatives]
• [Compliance Issue]: [Regulatory implications]

📊 THREAT LANDSCAPE ANALYSIS

INDUSTRY TARGETING:
Your [Industry] sector experienced [X]% increase in targeting this [period].
Key Attack Patterns:
• [Attack Type 1]: [X]% of incidents
• [Attack Type 2]: [X]% of incidents
• [Attack Type 3]: [X]% of incidents

CROWN JEWEL RISK ASSESSMENT:
• [Crown Jewel 1]: [Risk Level] - [X] new threats identified
• [Crown Jewel 2]: [Risk Level] - [Mitigation recommendations]
• [Crown Jewel 3]: [Risk Level] - [Strategic considerations]

COMPETITIVE INTELLIGENCE:
• Peer organizations in [industry] reporting [X]% increase in incidents
• [Competitor/Similar Org] disclosed breach affecting [system type]
• Industry best practices evolving around [security domain]

💰 FINANCIAL & OPERATIONAL IMPACT

COST OF INACTION:
• Potential breach cost: $[X]M - $[Y]M (industry average)
• Business disruption: [X] hours of downtime per incident
• Compliance fines: Up to $[X]M for [specific violations]
• Reputation damage: [X]% customer trust decline (industry data)

INVESTMENT PRIORITIES:
1. [Top Priority]: $[Budget] - [ROI/Risk reduction]
2. [Second Priority]: $[Budget] - [Strategic value]
3. [Third Priority]: $[Budget] - [Long-term benefit]

🚨 EXECUTIVE ACTIONS REQUIRED

IMMEDIATE (This Week):
• [Action Item 1]: [Specific executive decision needed]
• [Action Item 2]: [Budget/resource allocation required]
• [Action Item 3]: [Policy or process change]

SHORT-TERM (Next Month):
• [Strategic Initiative]: [Business case and timeline]
• [Technology Investment]: [Justification and implementation plan]
• [Process Improvement]: [Organizational change management]

LONG-TERM (Next Quarter):
• [Strategic Planning]: [Board-level decisions required]
• [Digital Transformation]: [Security integration requirements]
• [Risk Management]: [Enterprise risk appetite adjustments]

📈 INDUSTRY BENCHMARKING

SECURITY MATURITY:
• Your Organization: [Maturity Level] vs Industry Average: [Level]
• Gap Analysis: [Key areas for improvement]
• Competitive Advantage: [Areas where you lead]

THREAT PREPAREDNESS:
• Detection Capability: [Rating] vs Peers: [Rating]
• Response Time: [Your Time] vs Industry: [Benchmark]
• Recovery Capability: [Assessment vs standards]

🔮 STRATEGIC OUTLOOK

EMERGING THREATS (Next 6 Months):
• [Technology Trend]: [Impact on your business model]
• [Geopolitical Risk]: [Supply chain/operational implications]
• [Regulatory Change]: [Compliance timeline and requirements]

INVESTMENT RECOMMENDATIONS:
• [Technology Area]: [Strategic justification]
• [Process Improvement]: [Operational efficiency gains]
• [Talent/Training]: [Capability development needs]

BOARD COMMUNICATION:
• Key Messages: [3-4 executive talking points]
• Risk Appetite: [Recommendations for risk tolerance]
• Success Metrics: [KPIs for security investment tracking]

📋 ACTION ITEMS & NEXT STEPS

FOR CEO/LEADERSHIP TEAM:
• [Decision Required]: [By Date] - [Impact if delayed]
• [Budget Approval]: [Amount] - [Business justification]
• [Policy Decision]: [Area] - [Strategic implications]

FOR SECURITY TEAM:
• [Technical Implementation]: [Timeline and resources]
• [Process Update]: [Change management requirements]
• [Monitoring Enhancement]: [Capability improvements]

FOR BOARD REPORTING:
• [Risk Update]: [Quarterly board presentation items]
• [Compliance Status]: [Regulatory reporting requirements]
• [Competitive Position]: [Market advantage maintenance]

NEXT EXECUTIVE BRIEF: [Date]
For immediate concerns, contact: [Security Team Contact]

---
This brief reflects threats specifically relevant to [Organization Name]'s [Industry] operations and [Crown Jewel] systems. Analysis based on [X] threat intelligence sources and industry benchmarking data.
```

## Executive Brief Customization

### Industry-Specific Focus
- **Financial**: Regulatory compliance, payment systems, fraud prevention
- **Healthcare**: Patient data, medical devices, HIPAA compliance
- **Technology**: Intellectual property, customer data, platform security
- **Manufacturing**: Industrial control, supply chain, operational technology
- **Energy**: Critical infrastructure, NERC CIP, operational continuity

### Business Impact Categories
- **Revenue Impact**: Direct financial losses, customer churn
- **Operational Impact**: Service disruption, productivity loss
- **Reputation Impact**: Brand damage, customer trust
- **Compliance Impact**: Regulatory fines, audit findings
- **Strategic Impact**: Competitive disadvantage, market position

### Executive Communication Style
- **Business Language**: Avoid technical jargon
- **Risk Quantification**: Financial and operational metrics
- **Strategic Context**: Industry trends and competitive landscape
- **Action Orientation**: Clear decisions and investments needed
- **Timeline Focus**: Immediate, short-term, and strategic horizons

Execute this command now to generate executive-level threat intelligence briefing tailored for business leadership decision-making.