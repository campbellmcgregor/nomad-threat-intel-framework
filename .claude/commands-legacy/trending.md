---
name: trending
description: Show trending threats and attack vectors
---

You are executing the `/trending` command for NOMAD v2.0. This command identifies and presents trending threats, attack vectors, and emerging patterns in the current threat landscape.

## Command Execution

1. **Analyze Threat Patterns**: Read `data/threats-cache.json` and identify:
   - Most frequently mentioned CVEs
   - Recurring threat actors
   - Common attack vectors
   - Vendor/technology targets
   - Geographic or industry targeting patterns

2. **Temporal Analysis**: Look for:
   - Threats with recent publication dates (last 7-14 days)
   - Escalating EPSS scores
   - New KEV additions
   - Evolving exploitation status (PoC → ITW)

3. **Industry Context**: Apply user context from `config/user-preferences.json`:
   - Filter trends relevant to user's industry
   - Highlight patterns affecting user's technology stack
   - Show trends impacting crown jewel systems

4. **Generate Trend Report**: Use threat-synthesizer to create comprehensive trending analysis

## Response Format

```
📈 THREAT LANDSCAPE TRENDS

TRENDING CVEs (Last 7 Days):
• CVE-YYYY-XXXXX: [Brief description] - [X] mentions
• CVE-YYYY-XXXXX: [Brief description] - [X] mentions
• CVE-YYYY-XXXXX: [Brief description] - [X] mentions

EMERGING ATTACK VECTORS:
1. [Attack Vector Name]: [X]% increase
   • Description: [How it works]
   • Targets: [What systems/industries]
   • Mitigation: [Key defensive measures]

2. [Attack Vector Name]: [X]% increase
   • Description: [How it works]
   • Targets: [What systems/industries]
   • Mitigation: [Key defensive measures]

ACTIVE THREAT ACTORS:
• [Actor Name]: Targeting [industries/regions]
  Recent campaigns: [Campaign names/descriptions]

• [Actor Name]: Focusing on [attack types]
  Attribution: [Confidence level and evidence]

VENDOR/TECHNOLOGY SPOTLIGHT:
🎯 Most Targeted This Week:
• [Vendor/Product]: [X] vulnerabilities
• [Vendor/Product]: [X] vulnerabilities

INDUSTRY IMPACT TRENDS:
• [Industry]: [X] new threats ([X]% increase)
• [Industry]: [X] new threats ([X]% increase)

YOUR ORGANIZATION RELEVANCE:
• [Industry] Threats: [X] new items affecting your sector
• Crown Jewel Risks: [Systems] seeing increased targeting
• Technology Stack: [X] threats to your [technology] infrastructure

GEOPOLITICAL FACTORS:
• [Region/Nation]: [Threat activity description]
• Supply Chain: [Notable supply chain incidents/trends]

PREDICTION INSIGHTS:
📊 EPSS Trending Up:
• CVE-YYYY-XXXXX: EPSS increased from [X] to [Y]
• CVE-YYYY-XXXXX: EPSS increased from [X] to [Y]

⚡ Watch List (Likely to escalate):
• [Threat/CVE]: [Reason for watching]
• [Threat/CVE]: [Reason for watching]

STRATEGIC RECOMMENDATIONS:
1. Focus on [specific area] due to [trend explanation]
2. Enhance monitoring for [specific indicators]
3. Consider additional protections for [systems/processes]
```

## Analysis Methodology

- **Frequency Analysis**: Count mentions, references, and related threats
- **Temporal Weighting**: Recent threats weighted higher
- **Impact Scoring**: Combine CVSS, EPSS, exploitation status
- **Pattern Recognition**: Identify recurring themes and connections
- **Industry Filtering**: Emphasize trends relevant to user's context

Execute this command now to provide current threat landscape trend analysis with actionable insights for strategic security planning.