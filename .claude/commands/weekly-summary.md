---
name: weekly-summary
description: Generate comprehensive weekly threat landscape summary
usage: /weekly-summary [week-offset]
---

You are executing the `/weekly-summary` command for NOMAD v2.0. This command generates comprehensive weekly threat landscape summaries combining trends, analysis, and actionable intelligence for strategic planning.

## Command Parameters

- `$1`: Week offset (0=this week, -1=last week, -2=two weeks ago)
- If no parameter: Generate summary for current week

## Command Execution

1. **Load Weekly Data**: Read threat data from specified week timeframe
2. **Trend Analysis**: Identify patterns, increases, and significant changes
3. **Industry Context**: Apply user's industry and business context
4. **Strategic Synthesis**: Use Task tool to invoke weekly-synthesizer agent
5. **Format Comprehensive Report**: Balance strategic and tactical insights

## Response Format

```
📊 WEEKLY THREAT INTELLIGENCE SUMMARY
Week of [Start Date] - [End Date] | [Organization Name] | Generated: [Timestamp]

EXECUTIVE SUMMARY
This week's threat landscape was characterized by [key trend]. Your [Industry] sector experienced [X] new critical vulnerabilities, with [Y]% targeting [specific technology/process]. [Key takeaway about crown jewel systems or significant threats]. Immediate attention required for [top priority item].

🎯 WEEK IN NUMBERS

THREAT STATISTICS:
• Total Threats Analyzed: [X,XXX]
• New CVEs Published: [XXX]
• Critical Vulnerabilities (CVSS ≥9.0): [XX]
• KEV Additions: [XX]
• Active Exploitation Reports: [XX]
• Your Industry Relevance: [XX]% ([XXX] threats)
• Crown Jewel Impacts: [XX] direct matches

SEVERITY BREAKDOWN:
• Critical (9.0-10.0): [XX] threats
• High (7.0-8.9): [XXX] threats
• Medium (4.0-6.9): [XXX] threats
• EPSS ≥0.7: [XX] threats
• Proof-of-Concept: [XX] published
• In-The-Wild: [XX] confirmed

📈 THREAT TRENDS & ANALYSIS

TOP THREAT CATEGORIES THIS WEEK:
1. [Category Name]: [XX] threats (+[X]% from last week)
   • Key Pattern: [Description of trend]
   • Impact: [How this affects organizations]
   • Example: [Specific notable threat]

2. [Category Name]: [XX] threats ([trend])
   • [Similar analysis pattern]

3. [Category Name]: [XX] threats ([trend])
   • [Similar analysis pattern]

ATTACK VECTOR ANALYSIS:
• Network (Remote): [XX]% of threats
• Local Access: [XX]% of threats
• Physical: [X]% of threats
• Social Engineering: [X]% of threats

TECHNOLOGY TARGETING:
• Web Applications: [XX] threats
• Operating Systems: [XX] threats
• Network Infrastructure: [XX] threats
• Cloud Services: [XX] threats
• Mobile Platforms: [XX] threats

🏭 INDUSTRY IMPACT ANALYSIS

YOUR INDUSTRY ([Industry Name]):
• Threats This Week: [XXX] ([X]% of total analyzed)
• Week-over-Week Change: [+/-X]%
• Most Targeted Systems: [Technology/System types]
• Emerging Risks: [New threat patterns]

INDUSTRY COMPARISON:
• [Your Industry]: [XXX] threats
• Technology: [XXX] threats
• Financial: [XXX] threats
• Healthcare: [XXX] threats
• Manufacturing: [XXX] threats

SECTOR-SPECIFIC HIGHLIGHTS:
• [Regulatory/Compliance news affecting your industry]
• [Major incidents in peer organizations]
• [Industry-specific vulnerability disclosures]

💎 CROWN JEWEL THREAT ASSESSMENT

[Crown Jewel System 1]:
• Threats This Week: [X]
• Risk Level: [Critical/High/Medium/Low]
• Key Vulnerabilities: [Specific CVEs affecting this system]
• Trend: [Increasing/Stable/Decreasing threat volume]
• Action Required: [Immediate steps if any]

[Crown Jewel System 2]:
• [Similar analysis for each crown jewel]

[Crown Jewel System 3]:
• [Continue for all configured systems]

CROWN JEWEL RISK TRENDS:
• Systems with increasing threats: [X]
• New vulnerabilities discovered: [X]
• Patches/updates available: [X]
• Exploitation attempts: [X]

🌍 THREAT ACTOR & CAMPAIGN ANALYSIS

ACTIVE THREAT ACTORS:
• [Actor Name]: [Activity description and targeting]
• [Actor Name]: [Activity description and targeting]
• [Actor Name]: [Activity description and targeting]

NOTABLE CAMPAIGNS:
• [Campaign Name]: [Target industries and methods]
• [Campaign Name]: [Geographic focus and TTPs]

GEOPOLITICAL FACTORS:
• [Region/Nation]: [Relevant cyber activity]
• [Supply Chain]: [Notable incidents or risks]
• [Critical Infrastructure]: [Targeting patterns]

🔍 VULNERABILITY DEEP DIVE

CRITICAL VULNERABILITIES (CVSS ≥9.0):
• CVE-2024-XXXXX: [Product] - [Brief description]
  EPSS: [Score] | KEV: [Yes/No] | Exploitation: [Status]
  Your Impact: [Crown jewel/industry relevance]

• CVE-2024-XXXXX: [Product] - [Brief description]
  [Similar format for all critical CVEs]

KEV (Known Exploited Vulnerabilities) ADDITIONS:
• [XX] new KEV entries this week
• [Notable KEV additions affecting your environment]
• [CISA deadline and compliance implications]

EXPLOITATION TIMELINE:
• CVE-2024-XXXXX: [Days from disclosure to exploitation]
• CVE-2024-XXXXX: [Timeline and exploitation evolution]
• [Pattern analysis of exploitation timelines]

📊 WEEKLY PERFORMANCE METRICS

THREAT INTELLIGENCE EFFICIENCY:
• Average Detection Time: [X] hours
• Source Coverage: [X] feeds processed
• False Positive Rate: [X]%
• Crown Jewel Match Rate: [X]%

FEED SOURCE PERFORMANCE:
• Top Performing: [Feed Name] ([X] actionable threats)
• Most Timely: [Feed Name] ([X] hour average)
• Quality Leader: [Feed Name] ([XX]/100 score)

ORGANIZATIONAL METRICS:
• Threats Reviewed: [XXX]
• Actions Taken: [XX]
• Patches Applied: [XX]
• Alerts Generated: [XX]

🎯 STRATEGIC INSIGHTS

EMERGING THREAT PATTERNS:
• [Pattern 1]: [Description and implications]
• [Pattern 2]: [Description and business impact]
• [Pattern 3]: [Description and recommended response]

TECHNOLOGY EVOLUTION IMPACTS:
• [Technology Trend]: [Security implications]
• [Platform Change]: [New attack surfaces]
• [Industry Shift]: [Risk landscape changes]

PREDICTIVE ANALYSIS:
• High-probability targets next week: [Systems/technologies]
• Escalating threat actors: [Groups to monitor]
• Vulnerability classes increasing: [Types of flaws trending up]

📋 ACTIONABLE RECOMMENDATIONS

IMMEDIATE ACTIONS (This Week):
1. [High Priority Action]: [Specific steps and timeline]
2. [Medium Priority Action]: [Implementation guidance]
3. [Strategic Action]: [Long-term security posture improvement]

MONITORING ENHANCEMENTS:
• [Detection Rule]: [Implement specific monitoring]
• [Alert Tuning]: [Adjust thresholds for emerging threats]
• [Feed Addition]: [Consider new intelligence sources]

PROCESS IMPROVEMENTS:
• [Workflow Enhancement]: [Improve response efficiency]
• [Communication Update]: [Better stakeholder engagement]
• [Training Need]: [Team capability development]

🔮 WEEK AHEAD PREVIEW

EXPECTED DEVELOPMENTS:
• [Conference/Event]: [Security disclosures expected]
• [Vendor Patch Day]: [Major updates scheduled]
• [Regulatory Deadline]: [Compliance requirements]

MONITORING PRIORITIES:
• [Technology/Product]: [Why this needs special attention]
• [Threat Actor]: [Anticipated activity]
• [Vulnerability Class]: [Types to watch closely]

PLANNED ACTIVITIES:
• [Security Review]: [Scheduled assessments]
• [System Updates]: [Maintenance windows]
• [Team Training]: [Capability building]

📈 COMPARATIVE ANALYSIS

WEEK-OVER-WEEK CHANGES:
• Total Threats: [+/-X]% ([XXX] vs [XXX])
• Critical Threats: [+/-X]% ([XX] vs [XX])
• Industry Relevance: [+/-X]% ([XX] vs [XX])
• Crown Jewel Impacts: [+/-X]% ([XX] vs [XX])

MONTHLY TRENDING:
• [Metric 1]: [4-week trend description]
• [Metric 2]: [Pattern analysis]
• [Metric 3]: [Directional assessment]

YEAR-OVER-YEAR:
• Same week last year: [XXX] threats
• Growth/Change: [+/-X]%
• Pattern Evolution: [How threat landscape has evolved]

🎭 THREAT ACTOR SPOTLIGHT

ACTOR OF THE WEEK: [Threat Actor Name]
• Activity Level: [High/Medium/Low]
• Primary Targets: [Industries/regions]
• Recent Campaigns: [Campaign names and descriptions]
• TTPs: [Tactics, techniques, procedures]
• Your Risk: [Relevance to your organization]

EMERGING GROUPS:
• [New Actor]: [Brief profile and activities]
• [Evolved Group]: [Changes in behavior or capabilities]

📱 TECHNOLOGY FOCUS

TECHNOLOGY SPOTLIGHT: [Technology/Platform]
• Threat Volume: [XX] vulnerabilities this week
• Severity Distribution: [Critical/High/Medium breakdown]
• Your Exposure: [Crown jewel systems using this technology]
• Mitigation Priority: [High/Medium/Low]
• Vendor Response: [Patch availability and timeline]

🔗 RELATED RESOURCES

ADDITIONAL READING:
• [Report/Analysis]: [Brief description and relevance]
• [Industry Update]: [Significance to your sector]
• [Technical Research]: [Implications for security posture]

TOOLS & TECHNIQUES:
• [Detection Method]: [Implementation guidance]
• [Analysis Tool]: [How to use for threat hunting]
• [Response Framework]: [Application to current threats]

---
NEXT WEEKLY SUMMARY: [Date]
FOR IMMEDIATE CONCERNS: Contact [Security Team]
FEEDBACK: [How to improve these summaries]

This summary analyzed [X,XXX] threats from [XX] sources, prioritized for [Organization Name]'s [Industry] operations and [X] crown jewel systems.
```

## Weekly Summary Customization

### Timeframe Analysis
- **Current Week**: Monday-Sunday of current week
- **Previous Weeks**: Historical analysis for trend comparison
- **Rolling Windows**: 7-day periods for consistent analysis
- **Month/Quarter Context**: How weekly trends fit larger patterns

### Strategic Balance
- **25% Executive Summary**: High-level trends and business impact
- **35% Technical Analysis**: Specific vulnerabilities and threats
- **25% Industry Context**: Sector-specific intelligence
- **15% Forward Looking**: Predictions and recommendations

### Audience Optimization
- **Security Leadership**: Strategic trends and resource allocation
- **SOC Teams**: Operational threats and detection guidance
- **IT Management**: Infrastructure risks and patch priorities
- **Executive Briefing**: Business impact and investment needs

Execute this command now to generate comprehensive weekly threat intelligence analysis balancing strategic insights with actionable tactical intelligence.