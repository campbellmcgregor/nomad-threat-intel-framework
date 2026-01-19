---
name: update-profile
description: Update organization profile and preferences
argument-hint: "[field]"
---

You are executing the `/update-profile` command for NOMAD v2.0. This command updates specific fields in your organization profile.

## Command Parameters

- `$ARGUMENTS`: Field to update (optional)
- If no parameter: Show current profile with update options

## Updatable Fields

- `name` - Organization name
- `industry` - Industry sector
- `business` - Business description
- `exposure` - Asset exposure types
- `focus` - Threat focus areas

## Response Format

### Show Profile:
```
👤 ORGANIZATION PROFILE

📋 CURRENT PROFILE:
• Organization: [Name]
• Industry: [Sector]
• Business: [Description]
• Asset Exposure: [Types]
• Threat Focus: [Areas]

🛡️ CROWN JEWELS: [X] systems
[List of crown jewels]

UPDATE OPTIONS:
• `/update-profile name [New Name]`
• `/update-profile industry [New Industry]`
• `/update-profile business [New Description]`
• `/update-profile exposure [Types]`
• `/update-profile focus [Areas]`

Which field would you like to update?
```

### Update Field:
```
✅ PROFILE UPDATED

Field: [Field Name]
Previous: [Old Value]
Updated: [New Value]

📊 IMPACT:
This change affects how NOMAD filters and prioritizes threats:
• [Impact description 1]
• [Impact description 2]

The following threat categories are now emphasized:
• [Category 1]
• [Category 2]

Run `/threats` to see your updated personalized briefing.
```

Execute this command now to view or update your organization profile.
