---
name: import-feeds
description: Import threat intelligence feeds from OPML/JSON/CSV files
argument-hint: "[file-path]"
---

You are executing the `/import-feeds` command for NOMAD v2.0. This command imports threat intelligence feeds from external files in OPML, JSON, or CSV format.

## Command Parameters

- `$ARGUMENTS`: Path to feed file or URL (OPML, JSON, or CSV)
- Supported formats: `.opml`, `.xml`, `.json`, `.csv`

## Command Execution

1. **Parse File Location**: Accept file path or URL
2. **Detect Format**: Identify file type from extension or content
3. **Parse Feed Data**: Extract feed definitions using appropriate parser
4. **Validate Feeds**: Check URL accessibility and format validity
5. **Execute Import**: Use Task tool to invoke feed-manager agent

## Supported Formats

**OPML Format:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
  <body>
    <outline text="Feed Name" xmlUrl="https://example.com/feed.xml"/>
  </body>
</opml>
```

**JSON Format:**
```json
{
  "feeds": [
    {"name": "Feed Name", "url": "https://...", "priority": "high"}
  ]
}
```

**CSV Format:**
```csv
name,url,priority,description
"Feed Name","https://...","medium","Description"
```

## Response Format

```
📥 FEED IMPORT RESULTS

SOURCE: [File path or URL]
FORMAT: [OPML/JSON/CSV]

✅ SUCCESSFULLY IMPORTED: [X] feeds
• [Feed Name]: [Priority] - [Status]
• [Feed Name]: [Priority] - [Status]

⚠️ VALIDATION WARNINGS: [X] feeds
• [Feed Name]: [Warning message]

❌ FAILED IMPORTS: [X] feeds
• [Feed Name]: [Error message]

📊 FEED QUALITY SUMMARY:
• High quality (A-B rated): [X] feeds
• Medium quality (C rated): [X] feeds
• Monitoring required: [X] feeds

💡 RECOMMENDATIONS:
• [Import optimization suggestion]

Would you like me to:
• Disable low-quality feeds?
• Find alternatives for failed imports?
• Run quality check on imported feeds?
```

Execute this command now to import feeds from your external feed list.
