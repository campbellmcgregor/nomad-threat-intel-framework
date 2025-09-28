---
name: import-feeds
description: Import threat intelligence feeds from OPML/JSON/CSV files
usage: /import-feeds [file-path]
---

You are executing the `/import-feeds` command for NOMAD v2.0. This command imports threat intelligence feeds from various file formats.

## Command Parameters

- `$1`: File path to import (OPML, JSON, or CSV format)
- If no parameter: Guide user through import process

## Command Execution

1. **File Format Detection**: If file path provided:
   - Detect format by extension (.opml, .json, .csv)
   - Validate file exists and is readable
   - Parse file structure to confirm format

2. **Import Processing**: Use Task tool to invoke feed-manager agent with:
   - File path and format
   - Current user configuration
   - Request for feed import and validation

3. **Validation & Quality Check**: For each imported feed:
   - Validate URL accessibility
   - Check RSS/Atom format compliance
   - Assess security relevance score
   - Detect duplicates with existing feeds

4. **Integration**: Merge with current configuration:
   - Avoid duplicates
   - Categorize by source type
   - Apply appropriate priority levels
   - Update user feed configuration

## Supported Import Formats

### OPML (XML Format)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
  <head><title>Security Feeds</title></head>
  <body>
    <outline text="CISA" xmlUrl="https://www.cisa.gov/..."/>
    <outline text="Microsoft" xmlUrl="https://api.msrc.microsoft.com/..."/>
  </body>
</opml>
```

### JSON Format
```json
{
  "feeds": [
    {
      "name": "Custom Security Feed",
      "url": "https://example.com/security.xml",
      "priority": "medium",
      "description": "Company-specific security feed"
    }
  ]
}
```

### CSV Format
```
name,url,priority,description,category
"Custom Feed","https://example.com/feed.xml","medium","Internal security feed","custom"
"Security Blog","https://blog.example.com/rss","low","Vendor blog","vendor"
```

## Response Format

### Successful Import:
```
📥 FEED IMPORT RESULTS

IMPORT SUMMARY:
• File Format: [OPML/JSON/CSV]
• Total Entries: [X]
• Successfully Imported: [X]
• Validation Warnings: [X]
• Failed Imports: [X]

✅ SUCCESSFULLY IMPORTED ([X] feeds):
• [Feed Name]: [Priority] - [URL] ✓ Validated
• [Feed Name]: [Priority] - [URL] ✓ Validated
• [Feed Name]: [Priority] - [URL] ✓ Validated

⚠️ VALIDATION WARNINGS ([X] feeds):
• [Feed Name]: Slow response time ([X]ms)
  Action: Feed added but monitoring recommended
• [Feed Name]: Low security content relevance ([X]%)
  Action: Feed added with reduced priority

❌ FAILED IMPORTS ([X] feeds):
• [Feed Name]: URL inaccessible (HTTP [Error Code])
• [Feed Name]: Invalid RSS/Atom format
• [Feed Name]: Duplicate of existing feed "[Existing Name]"

📊 UPDATED CONFIGURATION:
• Total Active Feeds: [X] ([Y] new)
• Feed Categories: [X] Government, [X] Vendor, [X] Research, [X] Custom
• Quality Score: [X]/100 (portfolio health)

🔧 OPTIMIZATION SUGGESTIONS:
• [X] imported feeds have low quality scores
• Consider removing [X] duplicate feeds
• [X] feeds overlap with existing premium sources

NEXT STEPS:
1. Run `/feed-quality` to validate all imported feeds
2. Use `/optimize-feeds` to remove duplicates and improve performance
3. Try `/threats` to see updated intelligence with new sources

Import completed in [X] seconds.
```

### Import Guidance (No File Specified):
```
📥 FEED IMPORT WIZARD

NOMAD can import threat intelligence feeds from:

📄 SUPPORTED FORMATS:
• OPML (.opml) - From RSS readers like Feedly, Inoreader
• JSON (.json) - Custom feed configurations
• CSV (.csv) - Spreadsheet format with feed lists

📋 REQUIRED INFORMATION:
• Feed Name (descriptive title)
• Feed URL (RSS/Atom endpoint)
• Priority (critical/high/medium/low) [optional]
• Description [optional]

🔍 EXAMPLE USAGE:
/import-feeds ~/Downloads/my-feeds.opml
/import-feeds ./custom-feeds.json
/import-feeds feeds-list.csv

📁 FILE PREPARATION TIPS:

OPML Files:
• Export from your RSS reader (Feedly: Settings → OPML)
• Ensure xmlUrl attributes contain RSS/Atom URLs

JSON Files:
• Use the schema: {"feeds": [{"name": "", "url": "", "priority": ""}]}
• Include optional "description" and "category" fields

CSV Files:
• Columns: name,url,priority,description,category
• Use quotes for text containing commas
• Priority: critical/high/medium/low

🛡️ QUALITY ASSURANCE:
• All URLs validated before import
• Duplicate detection against existing feeds
• Security relevance scoring
• Performance testing included

Ready to import? Provide the file path: /import-feeds [your-file-path]
```

## File Processing Logic

1. **Format Detection**: Extension-based with content validation
2. **Schema Validation**: Verify required fields present
3. **URL Validation**: Test accessibility and format compliance
4. **Duplicate Detection**: Compare against existing feeds
5. **Quality Scoring**: Assess security relevance and performance
6. **Integration**: Merge with existing configuration seamlessly

Execute this command now to enable seamless import of threat intelligence feeds from multiple file formats.