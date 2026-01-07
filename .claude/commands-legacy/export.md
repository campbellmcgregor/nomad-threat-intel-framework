---
name: export
description: Export threat intelligence data and configuration
usage: /export [format] [timeframe] [filter]
---

You are executing the `/export` command for NOMAD v2.0. This command exports threat intelligence data, configurations, and reports in various formats for external analysis or backup purposes.

## Command Parameters

- `$1`: Export format (json, csv, pdf, opml, excel)
- `$2`: Time frame (24h, 7d, 30d, all)
- `$3`: Filter (critical, industry, crown-jewel, config)
- If no parameters: Show export wizard

## Command Execution

1. **Parse Export Request**: Determine format, timeframe, and filters
2. **Load Data**: Read from `data/threats-cache.json` and configuration files
3. **Apply Filters**: Filter data based on specified criteria
4. **Format Data**: Convert to requested export format
5. **Generate Export**: Create downloadable file with structured data

## Response Format

### Export Wizard (No Parameters):
```
📤 NOMAD DATA EXPORT WIZARD

AVAILABLE EXPORT FORMATS:
• JSON: Raw threat intelligence data for API integration
• CSV: Spreadsheet format for analysis in Excel/Sheets
• PDF: Executive summary report for stakeholders
• OPML: Feed sources for RSS reader import
• EXCEL: Multi-sheet workbook with analysis

TIMEFRAME OPTIONS:
• 24h: Last 24 hours of threats
• 7d: Last 7 days (recommended for weekly reports)
• 30d: Last 30 days (comprehensive monthly view)
• all: Complete threat database

FILTER OPTIONS:
• critical: Only critical/high severity threats
• industry: Threats relevant to your industry
• crown-jewel: Threats affecting your critical systems
• config: Organization configuration and settings
• feeds: Feed source configuration

QUICK EXPORT COMMANDS:
/export json 7d critical          # Critical threats (JSON, 7 days)
/export pdf 30d industry         # Industry report (PDF, 30 days)
/export csv all                  # Full dataset (CSV)
/export opml config              # Feed sources (OPML)

Which format would you like to export?
```

### Successful Export:
```
✅ EXPORT COMPLETED

EXPORT DETAILS:
• Format: [Format]
• Timeframe: [Timeframe]
• Filter: [Filter Applied]
• Records: [X] threats exported
• File Size: [X] MB
• Generated: [Timestamp]

FILE CONTENTS:
📊 THREAT SUMMARY:
• Total Threats: [X]
• Critical (CVSS ≥9.0): [X]
• KEV Listed: [X]
• Industry Relevant: [X]
• Crown Jewel Impact: [X]

🎯 YOUR ORGANIZATION:
• Organization: [Name]
• Crown Jewels: [X] systems
• Industry Focus: [Industry]
• Export Covers: [Date Range]

EXPORT LOCATION:
• File Name: nomad-export-[timestamp].[format]
• Download: [Generated file path or download link]

EXPORT USES:
• Share with security team for analysis
• Import into SIEM or ticketing system
• Executive briefing preparation
• Compliance documentation
• Backup of threat intelligence

Would you like to:
1. Generate another export with different filters?
2. Schedule automatic exports?
3. View export in different format?
```

## Export Formats

### JSON Format
```json
{
  "export_metadata": {
    "generated_at": "2024-01-15T10:30:00Z",
    "organization": "Your Organization",
    "timeframe": "7d",
    "filter": "critical",
    "total_records": 145
  },
  "threats": [
    {
      "cve": "CVE-2024-12345",
      "title": "Critical vulnerability in...",
      "cvss_score": 9.8,
      "epss_score": 0.85,
      "kev_listed": true,
      "crown_jewel_impact": ["Customer Database"],
      "published_date": "2024-01-14T15:20:00Z"
    }
  ]
}
```

### CSV Format
Columns: CVE, Title, CVSS, EPSS, KEV_Listed, Crown_Jewel_Impact, Industry_Relevant, Published_Date, Source

### PDF Format
Executive summary with charts, graphs, and key insights formatted for presentation

### OPML Format
Feed source export compatible with RSS readers for sharing/backup

### Excel Format
Multiple worksheets:
- Summary (overview and metrics)
- Threats (detailed threat data)
- CVEs (vulnerability-focused view)
- Crown Jewels (asset-specific threats)
- Configuration (settings backup)

## Filter Options

- **critical**: CVSS ≥ 7.0 OR KEV listed OR active exploitation
- **industry**: Threats tagged relevant to user's industry
- **crown-jewel**: Threats affecting configured crown jewel systems
- **config**: Organization profile and configuration settings
- **feeds**: Feed source configuration for backup/sharing

## Export Use Cases

- **Compliance Reporting**: PDF exports for auditors and management
- **SIEM Integration**: JSON/CSV for security tool ingestion
- **Team Collaboration**: Excel for analysis and task assignment
- **Feed Sharing**: OPML for distributing curated sources
- **Backup/Migration**: Complete configuration and data export

Execute this command now to export NOMAD threat intelligence data in your preferred format for external analysis or sharing.