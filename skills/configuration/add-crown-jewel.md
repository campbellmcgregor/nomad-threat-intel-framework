---
name: add-crown-jewel
description: Add a new crown jewel system to your organization profile
argument-hint: "[system-name]"
---

You are executing the `/add-crown-jewel` command for NOMAD v2.0. This command adds a new critical system to your crown jewels for enhanced threat monitoring.

## Command Parameters

- `$ARGUMENTS`: Name and description of the crown jewel system
- Format: `[Name]: [Description]` or just `[Name]`

## Command Execution

1. **Parse System Input**: Extract system name and optional description
2. **Load Current Config**: Read `config/user-preferences.json`
3. **Validate System**: Check for duplicates and suggest categorization
4. **Update Configuration**: Add to crown_jewels array
5. **Confirm Addition**: Show updated crown jewel list

## Response Format

```
🛡️ CROWN JEWEL ADDED

NEW SYSTEM:
• Name: [System Name]
• Description: [System Description]
• Category: [Suggested Category]
• Technologies: [Auto-detected technologies]

CURRENT CROWN JEWELS ([X] total):
1. [System 1] - [Brief description]
2. [System 2] - [Brief description]
3. [NEW] [System Name] - [Description]

🎯 THREAT INTELLIGENCE IMPACT:
• Threats will now be filtered for [System Name] relevance
• CVEs affecting [detected technologies] will be flagged
• Crown jewel correlation now includes [X] systems

💡 RELATED THREATS:
I found [X] existing threats that may affect [System Name]:
• [Threat 1]: [Brief description]
• [Threat 2]: [Brief description]

Would you like to see detailed analysis of threats to [System Name]?
Run: `/crown-jewel [System Name]`
```

## Crown Jewel Categories

- **Data Systems**: Databases, data lakes, customer data
- **Authentication**: Identity, access management, SSO
- **Network**: Internet-facing, cloud, internal networks
- **Applications**: Business-critical applications
- **Infrastructure**: Core infrastructure, cloud platforms

Execute this command now to add a critical system to your crown jewels.
