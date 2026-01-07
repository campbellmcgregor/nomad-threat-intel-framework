---
name: configure
description: Quick configuration updates for preferences and settings
argument-hint: "[setting]"
---

You are executing the `/configure` command for NOMAD v2.0. This command provides quick configuration updates without running the full setup wizard.

## Command Parameters

- `$ARGUMENTS`: Setting to modify (optional)
- If no parameter: Show configurable settings

## Configurable Settings

- `industry` - Change industry sector
- `thresholds` - Modify alert thresholds
- `verification` - Update verification settings
- `alerts` - Configure alert preferences
- `schedule` - Set refresh schedule

## Response Format

### Show Settings:
```
⚙️ NOMAD CONFIGURATION

CURRENT SETTINGS:

📋 Organization Profile:
• Organization: [Name]
• Industry: [Sector]
• Business Focus: [Description]

🛡️ Crown Jewels: [X] systems
• [System 1]
• [System 2]

📊 Alert Thresholds:
• Minimum Severity: [Level]
• CVSS Threshold: [Score]
• EPSS Threshold: [Score]

✅ Verification Settings:
• Method: [hybrid/structured/jina/disabled]
• Min Confidence: [X]%
• Monthly Budget: $[X]

🔄 Refresh Schedule:
• Auto-refresh: [X] hours
• Last refresh: [Timestamp]

QUICK CHANGES:
• `/configure industry [new-industry]`
• `/configure thresholds [high/medium/low]`
• `/configure verification [method]`

Which setting would you like to modify?
```

### Update Setting:
```
✅ CONFIGURATION UPDATED

Changed: [Setting Name]
From: [Old Value]
To: [New Value]

This change will affect:
• [Impact 1]
• [Impact 2]

Run `/threats` to see your updated briefing.
```

Execute this command now to view or modify NOMAD configuration settings.
