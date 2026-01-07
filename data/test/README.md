# NOMAD Test Data Files

This directory contains test data files for validating Claude Code skills functionality.

## Test Files

### Feed Import Tests

**test-feeds.csv**
- Format: CSV
- Contains: 5 test feeds (4 valid, 1 invalid)
- Use for: Testing csv-handler skill
- Command: `/import-feeds data/test/test-feeds.csv`

**test-feeds.opml**
- Format: OPML 2.0
- Contains: 6 feeds organized in 3 categories
- Use for: Testing opml-processor skill
- Command: `/import-feeds data/test/test-feeds.opml`

### Threat Validation Tests

**test-threat-valid.json**
- Format: JSON
- Contains: Fully valid threat with all fields
- Use for: Testing threat-validator skill with complete data
- Expected: Quality score 90-100, no issues

**test-threat-incomplete.json**
- Format: JSON
- Contains: Incomplete threat missing required fields
- Use for: Testing threat-validator skill auto-correction
- Expected: Quality score 40-60, auto-corrections applied

## Quick Test Commands

### Test CVE Analysis
```
Analyze CVE-2024-3094
/cve CVE-2024-3094
```

### Test Feed Import (CSV)
```
/import-feeds data/test/test-feeds.csv
```

### Test Feed Import (OPML)
```
/import-feeds data/test/test-feeds.opml
```

### Test Threat Validation
```
Validate this threat data: [paste contents of test-threat-valid.json]
```

### Test Feed Quality Analysis
```
/feed-quality
```

### Test Trending Analysis
```
/trending
```

### Test Report Generation
```
/executive-brief
/weekly-summary
/technical-alert CVE-2024-3094
```

### Test Export Operations
```
/export csv 7d critical
/export excel
/export opml
```

## Expected Results

See `SKILLS_TESTING_GUIDE.md` in the root directory for detailed expected outputs and validation criteria for each test scenario.

## Creating Custom Test Data

To create your own test files:

1. **CSV Format**: Follow the schema in test-feeds.csv
   - Columns: name, url, priority, description, category
   - Priority: critical|high|medium|low
   - Category: government|vendor|research|custom

2. **OPML Format**: Follow the structure in test-feeds.opml
   - Required attributes: text, xmlUrl
   - Optional: htmlUrl, type, description
   - Can nest outlines for categories

3. **Threat JSON**: Follow NOMAD schema
   - Required: source_type, source_name, title, published_utc, admiralty ratings
   - Recommended: summary, cves, dedupe_key
   - Optional: cvss_v3, epss, kev_listed, affected_products, etc.

## Test Data Maintenance

- Keep test data current and realistic
- Update CVE references to recent, known CVEs
- Verify test feed URLs are still accessible
- Review test data quarterly

---

**Version**: 1.0
**Last Updated**: 2024-10-24
