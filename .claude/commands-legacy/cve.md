---
name: cve
description: Get detailed analysis of specific CVE vulnerability
usage: /cve [CVE-ID]
---

You are executing the `/cve` command for NOMAD v2.0. This command provides detailed analysis of a specific CVE vulnerability.

## Command Parameters

- `$1`: The CVE identifier (e.g., "CVE-2024-12345", "2024-12345", or "12345")

## Command Execution

1. **Parse CVE ID**:
   - Accept formats: "CVE-YYYY-NNNNN", "YYYY-NNNNN", or just "NNNNN"
   - Normalize to full CVE format: "CVE-YYYY-NNNNN"
   - If malformed, provide format guidance

2. **Search Local Cache**: Check `data/threats-cache.json` for:
   - Exact CVE match in threats array
   - CVE mentioned in related threats
   - Associated threat intelligence

3. **Enhance if Needed**: If CVE not in cache or lacks detail:
   - Use Task tool to invoke intelligence-processor agent
   - Fetch data from NVD, EPSS, KEV databases
   - Enrich with current threat intelligence

4. **User Context Analysis**:
   - Check if CVE affects user's crown jewels
   - Assess impact to user's industry/technology stack
   - Determine priority level for this organization

5. **Generate Detailed Report**: Use threat-synthesizer for comprehensive CVE analysis

## Response Format

```
🔍 CVE ANALYSIS: [CVE-ID]

VULNERABILITY OVERVIEW:
Title: [Vulnerability Title]
Description: [Detailed description]
Affected Products: [List of affected systems/versions]

RISK ASSESSMENT:
• CVSS v3.1: [Score] ([Severity Level])
• EPSS Score: [Score] ([Percentile])
• KEV Status: [Yes/No] [Date added if applicable]
• Exploit Status: [None/PoC/ITW]

YOUR ORGANIZATION IMPACT:
• Affects Crown Jewels: [Yes/No - which systems]
• Asset Exposure: [Internet-facing/Internal/Cloud]
• Business Impact: [High/Medium/Low]
• Priority Level: [Critical/High/Medium/Low]

TECHNICAL DETAILS:
• Attack Vector: [Network/Adjacent/Local/Physical]
• Attack Complexity: [Low/High]
• Privileges Required: [None/Low/High]
• User Interaction: [None/Required]
• CWE Categories: [CWE-XXX: Description]

THREAT INTELLIGENCE:
• First Seen: [Date]
• Threat Actors: [Known actors exploiting this CVE]
• Attack Campaigns: [Associated campaigns]
• Exploitation Timeline: [When exploitation began]

REMEDIATION:
Priority Actions:
1. [Primary remediation step]
2. [Secondary remediation step]
3. [Monitoring/detection recommendations]

Vendor Resources:
• Advisory: [Link to vendor advisory]
• Patches: [Available patches/versions]
• Workarounds: [Temporary mitigations if available]

RELATED THREATS:
[Other CVEs commonly exploited together or in campaigns]
```

## Error Handling

- If CVE not found: Search broader threat databases
- If CVE format invalid: Provide format examples
- If no impact to user: Still provide general analysis but note low relevance

Execute this command now to provide comprehensive analysis of the specified CVE with personalized impact assessment.