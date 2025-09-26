---
name: configure
description: Quick configuration updates for preferences and settings
usage: /configure [setting] [value]
---

You are executing the `/configure` command for NOMAD v2.0. This command allows quick updates to configuration settings without running the full setup wizard.

## Command Parameters

- `$1`: Setting category (organization, alerts, feeds, crown-jewels, industry)
- `$2`: Specific setting or value to modify
- If no parameters: Show current configuration summary

## Command Execution

1. **Parse Parameters**:
   - If no parameters: Display configuration overview
   - If single parameter: Show category-specific settings
   - If two parameters: Update specific setting

2. **Load Current Config**: Read `config/user-preferences.json` and `config/threat-sources.json`

3. **Apply Changes**: Update configuration files with new values

4. **Validate Settings**: Ensure all changes maintain system integrity

## Response Format

### Configuration Overview (No Parameters):
```
⚙️ CURRENT NOMAD CONFIGURATION

ORGANIZATION:
• Name: [Organization Name]
• Industry: [Industry Sector]
• Business Sectors: [Sector 1, Sector 2, ...]

CROWN JEWELS ([X] systems):
• [System 1]: [Description]
• [System 2]: [Description]
• [System 3]: [Description]

FEED SOURCES:
• Active Feeds: [X] ([Y] premium, [Z] custom)
• Quality Score: [Score]/100
• Last Refresh: [Timestamp]

ALERT SETTINGS:
• Critical CVSS: ≥[X] (default: 9.0)
• EPSS Threshold: ≥[X] (default: 0.7)
• KEV Alerts: [Enabled/Disabled]
• Alert Frequency: [Real-time/Daily/Weekly]

QUICK CONFIGURE OPTIONS:
/configure organization [new-name]
/configure industry [healthcare|financial|technology|etc]
/configure alerts critical [7.0-10.0]
/configure alerts epss [0.1-1.0]
/configure feeds add [category]
```

### Category-Specific Settings:
```
⚙️ [CATEGORY] CONFIGURATION

Current Settings:
• [Setting 1]: [Current Value]
• [Setting 2]: [Current Value]
• [Setting 3]: [Current Value]

Available Updates:
/configure [category] [setting] [new-value]

Examples:
/configure alerts critical 8.5
/configure organization "New Company Name"
/configure industry healthcare
```

### Setting Update Confirmation:
```
✅ CONFIGURATION UPDATED

Changed: [Setting Category] → [Setting Name]
From: [Old Value]
To: [New Value]

IMPACT:
• [Description of what this change affects]
• [Any automatic adjustments made]
• [Recommendations for related settings]

Updated configuration saved. Changes will take effect on next threat collection.
```

## Supported Configuration Categories

### Organization Settings
- `name`: Organization name
- `industry`: Primary industry sector
- `sectors`: Additional business sectors

### Alert Thresholds
- `critical`: CVSS threshold for critical alerts (7.0-10.0)
- `epss`: EPSS probability threshold (0.1-1.0)
- `kev`: Enable/disable KEV-listed vulnerability alerts
- `frequency`: Alert delivery frequency

### Feed Management
- `add`: Add feed category or specific feed
- `remove`: Remove feeds by name or category
- `priority`: Adjust feed priority levels

### Crown Jewel Systems
- `add`: Add new crown jewel system
- `remove`: Remove crown jewel by name
- `update`: Modify existing crown jewel description

Execute this command now to enable quick configuration management without full setup wizard interaction.