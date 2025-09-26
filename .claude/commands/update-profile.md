---
name: update-profile
description: Update organization profile and preferences
usage: /update-profile [field] [value]
---

You are executing the `/update-profile` command for NOMAD v2.0. This command allows updates to your organization profile, industry settings, and threat intelligence preferences.

## Command Parameters

- `$1`: Profile field (name, industry, sectors, description, size, geography)
- `$2`: New value for the field
- If no parameters: Interactive profile update wizard

## Command Execution

1. **Load Current Profile**: Read `config/user-preferences.json`
2. **Parse Update Request**: Identify field and new value
3. **Validation**: Ensure new values are valid and properly formatted
4. **Update Configuration**: Apply changes and save updated profile
5. **Impact Assessment**: Show how changes affect threat intelligence

## Response Format

### Interactive Profile Wizard (No Parameters):
```
👤 ORGANIZATION PROFILE UPDATE

CURRENT PROFILE:
• Organization: [Current Name]
• Industry: [Current Industry]
• Business Sectors: [Sector 1, Sector 2, ...]
• Organization Size: [Small/Medium/Large/Enterprise]
• Geography: [Primary regions]
• Crown Jewels: [X] systems
• Profile Updated: [Last update date]

UPDATEABLE FIELDS:
1. Organization Name
2. Primary Industry
3. Business Sectors
4. Organization Size
5. Geographic Focus
6. Risk Tolerance
7. Alert Preferences

Which field would you like to update? [1-7]

Or use direct commands:
/update-profile name "New Organization Name"
/update-profile industry healthcare
/update-profile sectors "Healthcare, Technology, SaaS"
/update-profile size enterprise
/update-profile geography "North America, Europe"
```

### Specific Field Update:
```
✅ PROFILE UPDATED: [Field Name]

CHANGE SUMMARY:
• Field: [Field Name]
• Previous: [Old Value]
• New: [New Value]
• Updated: [Timestamp]

IMPACT ON THREAT INTELLIGENCE:
• [Specific impact description for the changed field]
• [How this affects threat prioritization]
• [Any new feed sources or categories now relevant]

RECOMMENDATIONS:
• [Suggested actions based on the profile change]
• [Additional configuration that might be beneficial]

Profile changes will take effect on the next threat intelligence collection.
```

### Industry Change Impact:
```
✅ INDUSTRY PROFILE UPDATED: [Old Industry] → [New Industry]

INDUSTRY-SPECIFIC CHANGES:
• New Threat Categories: [X] additional categories now monitored
• Feed Sources: [X] new industry feeds available
• Crown Jewel Suggestions: [Systems typical for new industry]
• Regulatory Focus: [Compliance frameworks for new industry]

AVAILABLE INDUSTRY ENHANCEMENTS:
• Add industry feed package: /add-feeds [new-industry]
• Update crown jewels: /add-crown-jewel [industry-specific-system]
• View industry trends: /trending (now filtered for [new-industry])

Would you like to:
1. Add [new-industry] specific feed sources?
2. Review crown jewel recommendations?
3. Update alert thresholds for [new-industry] risk profile?
```

## Supported Profile Fields

### Organization Information
- **name**: Organization/company name
- **industry**: Primary industry (healthcare, financial, technology, etc.)
- **sectors**: Additional business sectors or focus areas
- **size**: Organization size (startup, small, medium, large, enterprise)
- **geography**: Primary operating regions

### Threat Intelligence Preferences
- **risk_tolerance**: Conservative, moderate, or aggressive alert thresholds
- **alert_frequency**: Real-time, daily, or weekly digest
- **focus_areas**: Specific security domains to emphasize
- **compliance**: Regulatory frameworks (SOX, HIPAA, PCI-DSS, etc.)

## Profile Impact on Intelligence

Profile updates automatically adjust:
- **Threat Prioritization**: Industry-relevant threats ranked higher
- **Feed Selection**: Industry-specific sources added/emphasized
- **Crown Jewel Correlation**: Threats mapped to typical industry assets
- **Alert Thresholds**: Risk tolerance applied to CVSS/EPSS scoring
- **Compliance Focus**: Regulatory threats highlighted
- **Geographic Context**: Region-specific threats and actors

## Validation Rules

- Organization names must be 3-100 characters
- Industry must match supported categories
- Sectors should be comma-separated list
- Size must be valid category
- Geography should use standard region names

Execute this command now to maintain current organization profile information for optimal threat intelligence personalization.