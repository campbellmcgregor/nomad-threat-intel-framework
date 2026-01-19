---
name: technical-alert
description: Generate technical security alert for SOC and IT teams
argument-hint: "[threat-id or CVE]"
---

You are executing the `/technical-alert` command for NOMAD v2.0. This command generates detailed technical security alerts for SOC analysts and IT teams.

## Command Parameters

- `$ARGUMENTS`: Threat ID or CVE to generate alert for
- If no parameter: Generate alerts for all critical threats

## Command Execution

1. **Identify Target Threat**: Parse threat ID or CVE from arguments
2. **Load Threat Data**: Get detailed threat information
3. **Enrich Technical Details**: Include IOCs, TTPs, detection rules
4. **Generate Alert**: Format for technical consumption

## Response Format

```
🚨 TECHNICAL SECURITY ALERT

ALERT ID: [Generated ID]
GENERATED: [Timestamp]
SEVERITY: [Critical/High/Medium]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THREAT IDENTIFICATION:
• CVE ID: [CVE-YYYY-XXXXX]
• Title: [Vulnerability Title]
• Threat Type: [Category]

VERIFICATION STATUS:
• Confidence: [X]% ✅
• Method: [hybrid/structured/jina]
• Sources: [Source list]

RISK METRICS:
• CVSS v3.1: [Score] ([Vector])
• EPSS: [Score] ([Percentile]%)
• KEV Status: [Yes/No - Date if applicable]
• Exploit Status: [None/PoC/ITW]

AFFECTED SYSTEMS:
• [Product/Version 1]
• [Product/Version 2]

YOUR ENVIRONMENT:
• Crown Jewels Affected: [Systems]
• Asset Exposure: [Internet-facing/Internal]
• Technology Match: [Matching technologies]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNICAL DETAILS:

VULNERABILITY DESCRIPTION:
[Detailed technical description]

ATTACK VECTOR:
• Entry Point: [Attack vector description]
• Prerequisites: [Required conditions]
• Exploitation Complexity: [Low/High]

CWE CATEGORIES:
• [CWE-XXX]: [Category Name]

INDICATORS OF COMPROMISE (IOCs):
• File Hashes: [MD5/SHA256]
• Network Indicators: [IPs/Domains]
• Registry Keys: [If applicable]
• Behavioral Indicators: [Process/file activity]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THREAT INTELLIGENCE:

THREAT ACTORS:
• [Actor Name]: [Known TTPs]

ATTACK CAMPAIGNS:
• [Campaign Name]: [Description]

MITRE ATT&CK MAPPING:
• [Tactic]: [Technique ID] - [Technique Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REMEDIATION:

IMMEDIATE ACTIONS:
1. [Priority action with specific steps]
2. [Secondary action]
3. [Monitoring/detection steps]

DETECTION RULES:
```
[YARA/Sigma/Snort rule example]
```

PATCHES:
• Vendor: [Vendor Name]
• Advisory: [URL]
• Patch Version: [Version]

WORKAROUNDS:
• [Temporary mitigation if patch unavailable]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESOURCES:
• Vendor Advisory: [URL]
• NVD Entry: [URL]
• CISA Advisory: [URL if applicable]

RELATED ALERTS: [X] additional alerts
```

Execute this command now to generate technical security alerts.
