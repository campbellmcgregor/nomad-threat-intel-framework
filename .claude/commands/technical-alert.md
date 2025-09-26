---
name: technical-alert
description: Generate technical security alert for SOC and IT teams
usage: /technical-alert [severity] [system]
---

You are executing the `/technical-alert` command for NOMAD v2.0. This command generates technical security alerts formatted for SOC analysts, incident response teams, and IT administrators.

## Command Parameters

- `$1`: Severity filter (critical, high, medium, kev)
- `$2`: Specific system or crown jewel to focus on
- If no parameters: Generate comprehensive technical alert

## Command Execution

1. **Load Technical Threats**: Read from `data/threats-cache.json` filtering for actionable technical items
2. **Technical Analysis**: Focus on exploitation details, IOCs, and remediation steps
3. **System Impact Assessment**: Map threats to infrastructure and crown jewel systems
4. **Generate Alert**: Use Task tool to invoke technical-alert-generator agent
5. **Format for Operations**: Structure for SOC/IT team consumption

## Response Format

```
🚨 TECHNICAL SECURITY ALERT
Alert ID: NOMAD-[YYYYMMDD]-[XXX] | Generated: [Timestamp] | Severity: [LEVEL]

ALERT SUMMARY
[X] critical vulnerabilities require immediate attention. Active exploitation detected for [Y] CVEs. Crown jewel systems [System Names] are directly impacted. Patches available for [Z] vulnerabilities.

⚡ CRITICAL ACTIONS REQUIRED (Next 24 Hours)

1. CVE-2024-XXXXX - [Vulnerability Name] | CVSS: [Score] | EPSS: [Score]
   EXPLOITATION: [In-the-Wild/PoC/Theoretical]
   AFFECTED SYSTEMS: [Specific products and versions]
   YOUR EXPOSURE: [Crown jewel systems affected]

   IMMEDIATE ACTIONS:
   • Patch: [Specific version/update required]
   • Workaround: [If patch unavailable]
   • Detection: [IOCs and monitoring rules]
   • Verification: [How to confirm patching success]

2. [Additional critical items...]

🎯 CROWN JEWEL IMPACT ANALYSIS

[Crown Jewel System 1]:
• Threat Level: [Critical/High/Medium]
• Vulnerable Components: [Specific software/versions]
• Attack Vectors: [Network/Local/Adjacent]
• Business Impact: [Service disruption potential]
• Remediation: [Specific steps for this system]

[Crown Jewel System 2]:
• [Similar analysis...]

🔍 TECHNICAL DETAILS

VULNERABILITY ANALYSIS:
• Attack Complexity: [Low/High]
• Privileges Required: [None/Low/High]
• User Interaction: [None/Required]
• Network Vector: [Yes/No - Remotely exploitable]
• Authentication: [Not required/Single/Multiple]

EXPLOITATION INTELLIGENCE:
• Threat Actors: [Known groups exploiting]
• Campaign Names: [Associated attack campaigns]
• Tactics: [MITRE ATT&CK techniques]
• Timeline: [When exploitation began]
• Geographic: [Regions seeing active exploitation]

INDICATORS OF COMPROMISE (IOCs):
• File Hashes: [MD5/SHA256 hashes]
• Network Signatures: [IP addresses, domains, URLs]
• Registry Keys: [Windows registry modifications]
• Process Names: [Malicious process indicators]
• Behavioral Indicators: [Unusual system behavior]

🛠️ REMEDIATION INSTRUCTIONS

PATCH MANAGEMENT:
Priority 1 (Immediate):
• [System/Software]: Update to version [X.X.X]
• [System/Software]: Apply security patch [Patch-ID]
• [System/Software]: Configure workaround [specific steps]

Priority 2 (This Week):
• [Less critical patches with specific instructions]

Priority 3 (This Month):
• [Lower priority items]

CONFIGURATION CHANGES:
• [Security setting 1]: [Specific configuration change]
• [Security setting 2]: [How to implement]
• [Access control]: [Permissions/rules to modify]

MONITORING ENHANCEMENTS:
• SIEM Rules: [Specific detection rules to implement]
• Log Sources: [Additional logging to enable]
• Alerting: [Specific alerts to configure]
• Network Monitoring: [Traffic patterns to watch]

🔎 DETECTION & VALIDATION

VULNERABILITY SCANNING:
• Tools: [Specific scanners that detect this CVE]
• Commands: [CLI commands for manual verification]
• Scripts: [Automated detection methods]

EXPLOITATION DETECTION:
• Network: [Traffic patterns indicating exploitation]
• Endpoint: [Host-based indicators]
• Application: [Log entries to monitor]

PATCH VERIFICATION:
• [Step-by-step verification process]
• [Commands to confirm successful patching]
• [Expected output/results]

📊 IMPACT ASSESSMENT

BUSINESS SERVICES AT RISK:
• [Service 1]: [Impact level and user count]
• [Service 2]: [Revenue impact potential]
• [Service 3]: [Operational disruption risk]

TECHNICAL SYSTEMS:
• Internet-facing: [X] systems vulnerable
• Internal network: [Y] systems require patching
• Critical infrastructure: [Z] systems affected
• Development/test: [Assessment of non-production]

DATA EXPOSURE RISK:
• Customer data: [Risk level and record count]
• Financial data: [Exposure assessment]
• Intellectual property: [Risk to sensitive data]
• Operational data: [Impact on business operations]

⏰ TIMELINE & PRIORITIES

IMMEDIATE (0-4 Hours):
• [Critical action 1]
• [Critical action 2]
• [Status reporting requirements]

SHORT-TERM (4-24 Hours):
• [Patch deployment schedule]
• [System restart windows]
• [Validation activities]

MEDIUM-TERM (1-7 Days):
• [Non-critical patches]
• [Process improvements]
• [Monitoring enhancements]

📞 ESCALATION & CONTACTS

SEVERITY ESCALATION:
• Critical: [Contact immediately]
• High: [Escalate if unresolved in X hours]
• Medium: [Standard escalation process]

TECHNICAL SUPPORT:
• Vendor Support: [Contact information for affected products]
• Internal Teams: [Escalation path within organization]
• External Resources: [Third-party assistance if needed]

📈 THREAT CONTEXT

INDUSTRY TARGETING:
• Your industry ([Industry]) seeing [X]% increase in this attack type
• Similar organizations reporting [specific incidents/patterns]
• Regulatory attention: [Compliance implications]

ATTACK CAMPAIGN ANALYSIS:
• Campaign: [Name if known]
• Attribution: [Threat actor if identified]
• Goals: [What attackers are trying to achieve]
• TTPs: [Tactics, techniques, procedures]

🔄 FOLLOW-UP ACTIONS

POST-REMEDIATION:
• Validation testing: [Schedule and methodology]
• Performance monitoring: [Watch for system impact]
• Security assessment: [Additional controls needed]

LESSONS LEARNED:
• Process improvements: [What can be done better]
• Tool enhancements: [Detection/response improvements]
• Training needs: [Team capability development]

REPORTING:
• Management update: [Executive summary format]
• Compliance documentation: [Regulatory reporting needs]
• Metrics collection: [KPIs and measurement]

NEXT ALERT: [Scheduled time] or as threats emerge
FOR QUESTIONS: Contact [Security Team] | [Contact Information]

---
Alert Distribution: SOC, IT Operations, Incident Response, Management
Classification: [Internal/Confidential] | Retention: [Duration per policy]
```

## Technical Alert Customization

### Alert Severity Levels
- **Critical**: CVSS ≥ 9.0 OR KEV-listed OR active exploitation
- **High**: CVSS 7.0-8.9 OR high EPSS score OR crown jewel impact
- **Medium**: CVSS 4.0-6.9 OR industry-relevant OR emerging threats

### System-Specific Focus
When targeting specific systems:
- Map vulnerabilities to exact software versions in environment
- Provide system-specific remediation procedures
- Include system restart/maintenance windows
- Detail business impact for that specific system

### Technical Audience Optimization
- **SOC Analysts**: IOCs, detection rules, SIEM integration
- **IT Administrators**: Patch procedures, configuration changes
- **Incident Response**: Containment steps, forensics guidance
- **Management**: Business impact, timeline, resource requirements

Execute this command now to generate technical security alerts optimized for operational security teams and immediate threat response.