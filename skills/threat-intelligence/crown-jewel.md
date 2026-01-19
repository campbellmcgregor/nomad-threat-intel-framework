---
name: crown-jewel
description: Show threats affecting specific crown jewel system
argument-hint: "[system-name]"
---

You are executing the `/crown-jewel` command for NOMAD v2.0. This command shows threats specifically affecting a particular crown jewel system.

## Command Parameters

- `$ARGUMENTS`: The crown jewel system name (e.g., "Customer Database", "Authentication Systems", "Payment Processing")
- If no parameter provided, show threats affecting ALL crown jewels

## Command Execution

1. **Parse Target System**:
   - If `$ARGUMENTS` provided: Use as target crown jewel system
   - If no `$ARGUMENTS`: Show threats for all crown jewel systems
   - Match against crown jewels defined in `config/user-preferences.json`

2. **Load Threat Data**: Read `data/threats-cache.json` and filter for:
   - Threats where `affects_crown_jewels` array contains the target system
   - If no specific system: threats affecting any crown jewel

3. **System Analysis**: For the specified crown jewel, analyze:
   - Total threat count by priority level
   - Active exploitation affecting this system
   - Technology-specific vulnerabilities
   - Business impact assessment

4. **Generate Focused Report**: Use Task tool to invoke threat-synthesizer with crown jewel focus

## Response Format

```
🛡️ CROWN JEWEL THREAT ANALYSIS: [System Name]

THREAT SUMMARY:
• Critical: [X] threats requiring immediate action
• High: [X] threats needing attention within 48 hours
• Medium: [X] threats for planned remediation

ACTIVE THREATS TO [SYSTEM NAME]:
• CVE-XXXX-XXXXX: [Threat description] (Priority: Critical) ✅
  Impact: [Specific impact to this system]
  Action: [Required remediation step]

• CVE-XXXX-XXXXX: [Threat description] (Priority: High) ⚠️
  Impact: [Specific impact to this system]
  Action: [Required remediation step]

ATTACK VECTORS TARGETING [SYSTEM NAME]:
• [Attack vector 1]: [Description and mitigation]
• [Attack vector 2]: [Description and mitigation]

PROTECTIVE MEASURES:
✅ Recommended immediate actions:
• [Action 1]
• [Action 2]

⚠️ Long-term security improvements:
• [Improvement 1]
• [Improvement 2]

THREAT ACTOR FOCUS:
[Any specific threat actors known to target this type of system]
```

## System Matching Logic

When matching crown jewel systems:
- Exact match preferred
- Partial match acceptable (e.g., "database" matches "Customer Database")
- Case-insensitive matching
- If no matches found, suggest valid crown jewel names from config

Execute this command now to provide focused threat analysis for the specified crown jewel system.
