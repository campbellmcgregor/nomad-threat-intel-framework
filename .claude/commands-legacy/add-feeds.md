---
name: add-feeds
description: Add industry-specific threat intelligence feed package
usage: /add-feeds [industry]
---

You are executing the `/add-feeds` command for NOMAD v2.0. This command adds pre-configured industry-specific threat intelligence feed packages to the user's configuration.

## Command Parameters

- `$1`: Industry name (healthcare, financial, manufacturing, technology, energy, government)
- If no parameter: Show available industry packages

## Command Execution

1. **Parse Industry Parameter**:
   - If `$1` provided: Match against available industry templates
   - If no `$1`: Display list of available industry packages with descriptions
   - Accept variations (e.g., "health", "finance", "tech", "manufacturing", "gov")

2. **Load Industry Template**: Read `config/threat-sources-templates.json` and:
   - Find matching industry template
   - Extract feed configuration and crown jewel suggestions
   - Validate all feed URLs are accessible

3. **Check Current Configuration**: Read `config/threat-sources.json` to:
   - Identify already configured feeds
   - Prevent duplicate additions
   - Calculate new feeds to be added

4. **Execute Feed Manager**: Use Task tool to invoke feed-manager agent with:
   - Industry template to apply
   - Current user configuration
   - Request for feed addition and optimization

## Available Industry Packages

```
AVAILABLE INDUSTRY PACKAGES:

🏥 healthcare - Healthcare & Life Sciences
   • HHS Healthcare Cybersecurity
   • FDA Medical Device Security
   • ICS-CERT Medical Advisories
   • ECRI Institute Research
   Crown Jewels: EHR, Medical Devices, Patient Portal, Lab Systems

💰 financial - Financial Services & Banking
   • FS-ISAC Cybersecurity
   • FinCEN Cybersecurity
   • PCI Security Standards
   • SWIFT Security
   Crown Jewels: Core Banking, Payment Systems, Trading Platforms

🏭 manufacturing - Manufacturing & Industrial
   • ICS-CERT Advisories
   • Schneider Electric Security
   • Siemens Security Advisories
   • Rockwell Automation Security
   Crown Jewels: Production Control, SCADA, Manufacturing Execution Systems

💻 technology - Technology & Software Development
   • GitHub Security Advisories
   • npm/PyPI Security Advisories
   • OWASP Updates
   • Docker/Kubernetes Security
   Crown Jewels: Source Code, CI/CD, API Systems, Cloud Infrastructure

⚡ energy - Energy & Utilities
   • NERC CIP Security
   • DOE Cybersecurity
   • API Oil & Gas Security
   Crown Jewels: Generation Control, Distribution Management, Pipeline Control

🏛️ government - Government & Public Sector
   • CISA Government Advisories
   • FedRAMP Security
   • NIST Cybersecurity Framework
   Crown Jewels: Citizen Data, Government Portals, Emergency Response
```

## Response Format

### When Adding Industry Package:
```
✅ INDUSTRY PACKAGE ADDED: [Industry Name]

FEEDS ADDED ([X] new sources):
• [Feed Name]: [Priority Level] - [Description]
• [Feed Name]: [Priority Level] - [Description]
• [Feed Name]: [Priority Level] - [Description]

📊 FEED CONFIGURATION UPDATED:
• Total Active Feeds: [X] ([Y] new)
• Industry-Specific Feeds: [X]
• Premium Sources: [X]

💡 CROWN JEWEL SUGGESTIONS:
Consider adding these systems to your crown jewels:
• [Suggested System 1]: [Reason/Description]
• [Suggested System 2]: [Reason/Description]

⚙️ NEXT STEPS:
1. Run `/feed-quality` to validate new feeds
2. Use `/crown-jewel [system]` to see relevant threats
3. Try `/threats` for updated briefing

Would you like to:
• Add suggested crown jewels to your profile?
• Configure industry-specific alert thresholds?
• View threats relevant to your new industry focus?
```

### When No Industry Specified:
Display the available industry packages list above.

## Industry Matching Logic

- Exact match: "healthcare" → healthcare template
- Partial match: "health" → healthcare template
- Synonyms: "finance" → financial, "tech" → technology, "gov" → government
- Case insensitive matching
- If no match: Suggest closest matches and show available options

Execute this command now to add industry-specific threat intelligence feeds with intelligent configuration management.