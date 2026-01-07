---
name: csv-handler
description: Handle CSV import/export for threat feeds and intelligence data
version: 1.0
---

# CSV Handler Skill

## Purpose
Bidirectional CSV operations for threat intelligence feeds and data export with validation and schema enforcement.

## Capabilities
- Parse CSV feed lists with automatic validation
- Export threat data to CSV with customizable columns
- Handle large datasets efficiently
- Automatic schema detection and validation
- Support for SIEM/ticketing system formats

## Input Schema

### For CSV Import (Feed Lists)
```json
{
  "operation": "import_feeds",
  "file_path": "string (path to CSV file)",
  "validate_urls": "boolean (default: true)",
  "deduplicate": "boolean (default: true)"
}
```

Expected CSV columns for feed import:
- `name` (required): Feed display name
- `url` (required): RSS/Atom feed URL
- `priority` (optional): critical|high|medium|low
- `description` (optional): Feed description
- `category` (optional): vendor|government|research|custom
- `source_reliability` (optional): A|B|C|D

### For CSV Export (Threat Data)
```json
{
  "operation": "export_threats",
  "output_path": "string (destination file path)",
  "timeframe": "string (24h|7d|30d|all)",
  "filter": {
    "min_cvss": "number (optional)",
    "kev_only": "boolean (optional)",
    "crown_jewel_impact": "boolean (optional)",
    "industry_relevant": "boolean (optional)"
  },
  "columns": ["array of column names to include"],
  "format": "standard|siem|ticketing"
}
```

## Output Schema

### Import Results
```json
{
  "status": "success|partial|failed",
  "summary": {
    "total_entries": "number",
    "successfully_imported": "number",
    "validation_warnings": "number",
    "failed_imports": "number"
  },
  "imported_feeds": [
    {
      "name": "string",
      "url": "string",
      "priority": "string",
      "validation_status": "valid|warning|failed",
      "validation_message": "string"
    }
  ],
  "warnings": ["array of validation warnings"],
  "errors": ["array of import errors"],
  "updated_config_path": "config/threat-sources.json"
}
```

### Export Results
```json
{
  "status": "success|failed",
  "output_file": "string (path to generated CSV)",
  "summary": {
    "total_threats": "number",
    "exported_records": "number",
    "file_size_bytes": "number",
    "timeframe_covered": "string"
  },
  "columns_included": ["array of column names"],
  "filter_applied": "object (copy of filter criteria)"
}
```

## Processing Instructions

### CSV Import Processing

1. **File Validation**:
   - Verify file exists and is readable
   - Check for CSV format (detect delimiter: comma, semicolon, tab)
   - Validate headers match expected schema
   - Handle UTF-8 encoding, BOM markers

2. **Row Processing**:
   - Parse each row into feed object
   - Normalize field values (trim whitespace, lowercase priorities)
   - Apply default values for optional fields
   - Generate stable feed IDs

3. **URL Validation** (if enabled):
   - Check URL format validity (HTTP/HTTPS)
   - Test URL accessibility (HTTP HEAD request)
   - Validate RSS/Atom format (parse feed headers)
   - Measure response time

4. **Deduplication** (if enabled):
   - Load existing feeds from `config/threat-sources.json`
   - Compare by URL (normalized)
   - Flag duplicates, keep higher priority version
   - Detect URL redirects (301/302)

5. **Quality Scoring**:
   - Accessibility: Response time < 5s (good), < 10s (warning), > 10s (slow)
   - Format compliance: Valid RSS/Atom structure
   - Security relevance: Presence of security keywords in recent entries
   - Update frequency: Check publication dates of recent items

6. **Integration**:
   - Read current `config/threat-sources.json`
   - Merge new feeds into `rss_feeds` array
   - Preserve existing feed configurations
   - Write updated configuration
   - Create backup of previous config

### CSV Export Processing

1. **Data Loading**:
   - Read `data/threats-cache.json`
   - Read `config/user-preferences.json` for context
   - Apply timeframe filter to threat timestamps

2. **Filtering**:
   - Apply CVSS threshold if specified
   - Filter for KEV-listed threats if requested
   - Match crown jewel correlations if enabled
   - Apply industry relevance filters

3. **Column Selection**:
   - Standard columns: CVE, Title, CVSS, EPSS, KEV_Listed, Published_Date, Source
   - SIEM format: Add Priority, Category, Severity_Label, IOCs
   - Ticketing format: Add Ticket_Summary, Assignee_Suggestion, SLA_Priority

4. **Data Transformation**:
   - Escape CSV special characters (quotes, commas, newlines)
   - Format dates consistently (ISO 8601)
   - Convert arrays to delimited strings (CVEs, affected products)
   - Normalize boolean values (Yes/No or True/False based on format)

5. **File Generation**:
   - Write UTF-8 with BOM for Excel compatibility
   - Use proper CSV quoting (RFC 4180)
   - Include header row with column names
   - Add metadata comment row (optional)

## Example Usage

### Import Feeds from CSV
```
Input CSV (feeds.csv):
name,url,priority,description,category
"CISA Advisories","https://www.cisa.gov/cybersecurity-advisories/all.xml","critical","US government advisories","government"
"Microsoft MSRC","https://api.msrc.microsoft.com/update-guide/rss","high","Microsoft security updates","vendor"

Skill invocation result:
✅ Successfully imported 2 feeds
• CISA Advisories: Valid (response time: 1.2s)
• Microsoft MSRC: Valid (response time: 2.1s)

Updated: config/threat-sources.json
```

### Export Threats to CSV
```
Export critical threats from last 7 days to CSV:

Output (critical-threats-7d.csv):
CVE,Title,CVSS,EPSS,KEV_Listed,Crown_Jewel_Impact,Published_Date,Source
CVE-2024-12345,"Authentication Bypass in Product X",9.8,0.85,Yes,"Customer Database",2024-10-20T10:30:00Z,"CISA"
CVE-2024-54321,"Remote Code Execution in Service Y",9.1,0.72,Yes,"Payment Systems",2024-10-19T14:20:00Z,"Microsoft"

Summary: 2 critical threats exported, 156KB file size
```

## Error Handling

### Import Errors
- **Invalid file format**: Return error with format guidance
- **Malformed CSV**: Identify problematic rows, continue with valid rows
- **Invalid URLs**: Flag as warnings, include in report, skip validation
- **Duplicate feeds**: Warn user, provide merge strategy options
- **Unreachable feeds**: Warning (not error), suggest retry later

### Export Errors
- **No matching threats**: Return success with empty export, warn user
- **Invalid filter criteria**: Return error with valid options
- **File write permission**: Return error with path resolution help
- **Data corruption**: Validate cache, suggest refresh operation

## Integration Points

### Files Used
- **Reads from**:
  - `config/threat-sources.json` (existing feeds for deduplication)
  - `data/threats-cache.json` (threat data for export)
  - `config/user-preferences.json` (crown jewels, industry for filtering)

- **Writes to**:
  - `config/threat-sources.json` (merged feed configuration)
  - `config/threat-sources.json.backup` (backup before changes)
  - User-specified export paths

### Command Integration
- Used by: `/import-feeds` command
- Used by: `/export` command (CSV format)
- Used by: `agents/feed-manager.md` (feed management operations)

## Performance Characteristics
- Import: ~100 feeds/minute with validation
- Export: ~1000 threats/second for CSV generation
- Memory: Streaming for large datasets (>10MB)
- Validation: Parallel URL checking (up to 10 concurrent)

## Quality Assurance
- Schema validation before processing
- Rollback capability (backup configs)
- Detailed error reporting
- Progress indicators for large operations
- Dry-run mode for testing imports
