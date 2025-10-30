# Claude Skills Testing Guide

## Overview

This guide provides practical testing procedures for all 8 NOMAD Claude Code skills. Since skills are markdown-based specifications for Claude Code behavior, testing involves creating realistic scenarios and verifying correct execution.

## Testing Philosophy

**Skills are specifications, not code**: Each skill defines how Claude Code should handle specific operations. Testing verifies:
1. ✅ Correct input processing
2. ✅ Expected output format
3. ✅ Performance characteristics
4. ✅ Error handling
5. ✅ Integration with agents/commands

---

## Test 1: CVE Intelligence Analyzer

### Objective
Verify parallel CVE enrichment with multi-source data fetching

### Test Scenario A: Known CVE Analysis
```
Test: Analyze CVE-2024-3094 (XZ Utils backdoor)

Command to test:
"Analyze CVE-2024-3094"
or
"/cve CVE-2024-3094"

Expected behavior:
1. Parse and normalize CVE ID ✓
2. Parallel fetch from:
   - NVD (CVSS, description, affected products)
   - EPSS (exploit prediction score)
   - CISA KEV (if listed)
3. Crown jewel correlation (if XZ Utils used)
4. Priority score calculation
5. Response time: 5-10 seconds (vs 30-60s sequential)

Success criteria:
✅ All data sources queried in parallel
✅ CVSS v3.1 score displayed (9.8)
✅ EPSS score shown
✅ KEV status indicated
✅ Crown jewel impact assessed
✅ Processing time < 15 seconds
✅ Remediation guidance provided
```

### Test Scenario B: CVE ID Flexibility
```
Test different CVE ID formats:

Inputs to test:
- "CVE-2024-3094" (standard)
- "2024-3094" (missing prefix)
- "cve 2024 3094" (spaces, lowercase)

Expected: All normalize to CVE-2024-3094 ✓
```

### Test Scenario C: Non-existent CVE
```
Test: CVE-2099-99999 (future/invalid)

Expected behavior:
❌ Status: "not_found"
📝 Helpful error message
💡 Suggested similar CVEs (if possible)
```

### Test Scenario D: Performance Measurement
```
Test: Compare to baseline

Without skill (sequential):
1. WebFetch NVD → wait
2. WebFetch EPSS → wait
3. WebFetch KEV → wait
Total: ~30-60 seconds

With skill (parallel):
All three in parallel → 5-10 seconds

Measure: Time from query to response
Target: <15 seconds for full enrichment
```

---

## Test 2: Threat Data Validator

### Objective
Verify schema validation, normalization, and quality scoring

### Test Scenario A: Valid Threat
```
Test data (valid threat):
{
  "title": "Critical RCE in Product X",
  "source_name": "CISA",
  "source_type": "cert",
  "published_utc": "2024-10-24T10:30:00Z",
  "admiralty_source_reliability": "A",
  "admiralty_info_credibility": 1,
  "cves": ["CVE-2024-12345"],
  "cvss_v3": 9.8
}

Command:
"Validate this threat data: [paste JSON]"

Expected:
✅ Status: "valid"
✅ Quality score: 90-100 (excellent)
✅ No issues reported
✅ Dedupe key generated
✅ All required fields present
```

### Test Scenario B: Invalid/Incomplete Threat
```
Test data (missing fields):
{
  "title": "Some vulnerability",
  "description": "CVE-2024-99999 affects something"
}

Expected behavior:
⚠️ Status: "warnings" or "invalid"
🔧 Auto-corrections (if enabled):
  - source_type: inferred → "custom"
  - source_name: extracted if possible
  - admiralty_source_reliability: inferred → "D"
  - admiralty_info_credibility: inferred → 4
  - cves: extracted ["CVE-2024-99999"]
  - id: auto-generated
  - dedupe_key: generated
✅ Quality score: 40-60 (poor but usable)
📋 Issues list provided
```

### Test Scenario C: CVE Extraction
```
Test: Automatic CVE extraction from text

Input threat:
{
  "title": "Multiple vulnerabilities disclosed",
  "description": "CVE-2024-1111 and CVE-2024-2222 affect versions 1.0-3.5. Also see CVE-2024-3333.",
  "source_name": "SecurityBlog"
}

Expected:
✅ cves: ["CVE-2024-1111", "CVE-2024-2222", "CVE-2024-3333"]
✅ Duplicates removed
✅ Normalized to uppercase
```

### Test Scenario D: Deduplication
```
Test: Detect duplicate threats

Threat 1:
{
  "title": "Critical vulnerability in Apache",
  "cves": ["CVE-2024-5555"],
  "published_utc": "2024-10-20T10:00:00Z",
  "source_name": "CISA"
}

Threat 2 (duplicate, different source):
{
  "title": "Critical vulnerability in apache",
  "cves": ["CVE-2024-5555"],
  "published_utc": "2024-10-20T10:00:00Z",
  "source_name": "NVD"
}

Expected:
🔄 Same dedupe_key generated
📊 Duplicate detected
✅ Sources merged: ["CISA", "NVD"]
```

---

## Test 3: CSV Handler

### Objective
Test CSV import/export for feeds and threat data

### Test Scenario A: Feed Import from CSV
```
Step 1: Create test CSV file
File: test-feeds.csv

name,url,priority,description,category
"CISA Test Feed","https://www.cisa.gov/cybersecurity-advisories/all.xml","critical","US gov advisories","government"
"Microsoft Test","https://api.msrc.microsoft.com/update-guide/rss","high","MS security updates","vendor"
"Invalid Feed","http://invalid-url-test.local/rss","medium","Test invalid URL","custom"

Step 2: Import command
"/import-feeds test-feeds.csv"

Expected output:
📥 FEED IMPORT RESULTS

Import Summary:
• Total Entries: 3
• Successfully Imported: 2
• Validation Warnings: 0
• Failed Imports: 1

✅ SUCCESSFULLY IMPORTED:
• CISA Test Feed → Critical, Government ✓
• Microsoft Test → High, Vendor ✓

❌ FAILED IMPORTS:
• Invalid Feed → URL inaccessible (HTTP error)

Updated: config/threat-sources.json
```

### Test Scenario B: Threat Export to CSV
```
Command:
"/export csv 7d critical"

Expected:
✅ CSV file generated
📊 Columns: CVE, Title, CVSS, EPSS, KEV_Listed, Crown_Jewel_Impact, Published_Date, Source
🔢 Only threats from last 7 days
🎯 Only critical severity (CVSS ≥9.0 or KEV)
📁 File format: valid CSV (RFC 4180)
🔤 UTF-8 encoding with BOM (Excel compatible)
```

### Test Scenario C: SIEM Export Format
```
Test: Export for Splunk/Sentinel ingestion

Command:
"/export csv 24h critical --format siem"

Expected CSV columns:
- Standard: CVE, Title, CVSS, EPSS, KEV_Listed
- SIEM-specific: Priority, Category, Severity_Label, IOCs
- Timestamp format: ISO 8601
- Severity labels: CRITICAL, HIGH, MEDIUM, LOW
```

---

## Test 4: OPML Feed Processor

### Objective
Test OPML import/export for RSS feed management

### Test Scenario A: Import from OPML
```
Step 1: Create test OPML file
File: test-feeds.opml

<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head>
    <title>Security Feeds</title>
    <dateCreated>2024-10-24</dateCreated>
  </head>
  <body>
    <outline text="Government Sources">
      <outline text="CISA Advisories"
               xmlUrl="https://www.cisa.gov/cybersecurity-advisories/all.xml"
               type="rss"/>
      <outline text="NCSC UK"
               xmlUrl="https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml"
               type="rss"/>
    </outline>
    <outline text="Vendor Advisories">
      <outline text="Microsoft MSRC"
               xmlUrl="https://api.msrc.microsoft.com/update-guide/rss"
               type="rss"/>
    </outline>
  </body>
</opml>

Step 2: Import command
"/import-feeds test-feeds.opml"

Expected output:
📥 FEED IMPORT RESULTS

File Format: OPML
Total Entries: 3

CATEGORIES FOUND:
• Government Sources: 2 feeds
• Vendor Advisories: 1 feed

✅ SUCCESSFULLY IMPORTED:
• CISA Advisories → Priority: Critical, Category: Government ✓
• NCSC UK → Priority: Critical, Category: Government ✓
• Microsoft MSRC → Priority: High, Category: Vendor ✓

Updated: config/threat-sources.json
```

### Test Scenario B: Export to OPML
```
Command:
"/export opml --group-by priority"

Expected OPML structure:
<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head>
    <title>NOMAD Threat Intelligence Feeds</title>
    <ownerName>NOMAD v2.0</ownerName>
  </head>
  <body>
    <outline text="Critical Priority">
      <outline text="CISA Advisories" xmlUrl="..." type="rss"/>
      <outline text="CISA KEV" xmlUrl="..." type="rss"/>
    </outline>
    <outline text="High Priority">
      <outline text="Microsoft MSRC" xmlUrl="..." type="rss"/>
    </outline>
  </body>
</opml>

✅ Valid OPML format
✅ Grouped by priority
✅ Compatible with RSS readers
```

### Test Scenario C: Format Conversion
```
Test: OPML → JSON → CSV round-trip

Step 1: Start with OPML file
Step 2: Convert to JSON: "/convert feeds.opml feeds.json"
Step 3: Convert to CSV: "/convert feeds.json feeds.csv"
Step 4: Convert back to OPML: "/convert feeds.csv feeds-final.opml"

Expected:
✅ No data loss
✅ All feeds preserved
✅ Metadata maintained
```

---

## Test 5: PDF Report Generator

### Objective
Test professional PDF report generation

### Test Scenario A: Executive Brief
```
Command:
"/executive-brief"

Expected output:
✅ PDF Generated: executive-brief-2024-10-24.pdf

Report structure:
📄 Page 1: Cover page with branding
📊 Page 2: Executive summary dashboard
   - Key metrics cards
   - Severity distribution pie chart
   - Top 3 threats
📈 Page 3-4: Threat landscape
   - Trend line chart
   - Crown jewel impact table
📋 Page 5-6: Priority threats (top 5)
   - Risk matrix
   - Business impact
✅ Page 7: Recommendations
📚 Page 8: Appendix

File properties:
• Format: PDF 1.7 or PDF/A-2
• Resolution: 300 DPI
• File size: 1-3 MB (typical)
• Pages: 6-10
• Charts: 5+
```

### Test Scenario B: Technical Alert
```
Test: Generate SOC-focused technical alert

Command:
"/technical-alert CVE-2024-12345"

Expected output:
🚨 Technical Alert Generated

alert-CVE-2024-12345.pdf

Content:
• Alert header with severity badge
• CVSS breakdown with radar chart
• Technical vulnerability details
• Affected systems table
• IOCs and detection signatures
• Remediation steps with patch links
• References (NVD, vendor advisories)

Format:
• Dense technical content
• Monospace fonts for code/signatures
• Color-coded severity indicators
• 3-5 pages
```

### Test Scenario C: Weekly Summary
```
Command:
"/weekly-summary pdf"

Expected:
📊 weekly-summary-2024-W43.pdf

Content validation:
✅ Cover page with week range
✅ Summary dashboard (metrics, trends)
✅ Notable threats section (top 10)
✅ Crown jewel analysis
✅ Industry intelligence
✅ Charts: pie, line, bar, matrix
✅ Recommendations and next steps
✅ 10-15 pages
✅ Table of contents
✅ Page numbers
```

---

## Test 6: Excel Workbook Generator

### Objective
Test multi-worksheet Excel generation with analytics

### Test Scenario A: Threat Analysis Workbook
```
Command:
"/export excel threat-analysis"

Expected output:
📊 Excel Workbook Generated

threat-analysis-2024-10-24.xlsx

Sheets validation:
✅ Summary Dashboard
   - Threat count cards with sparklines
   - Severity distribution
   - Links to detail sheets

✅ Threats Detail
   - Full threat data table
   - Auto-filter enabled
   - Freeze panes on header row
   - Conditional formatting (CVSS-based colors)
   - Data validation dropdowns (Status column)

✅ CVE Analysis
   - Detailed CVE data
   - Hyperlinks to NVD, advisories
   - Priority scoring formulas

✅ Crown Jewel Matrix
   - Heat map formatting
   - Pivot table
   - Bar chart

✅ Timeline View
   - Time-series data
   - Line chart
   - Sparklines

✅ Remediation Tracker
   - Editable fields (Status, Owner, Due Date)
   - Overdue highlighting (conditional format)
   - Formula: Days until due

File validation:
• Format: .xlsx (Excel 2007+)
• Compatibility: Excel, Google Sheets, LibreOffice
• File size: 1-2 MB (typical)
• Sheets: 8
• Charts: 6+
• Pivot tables: 3+
```

### Test Scenario B: Feed Quality Workbook
```
Command:
"/feed-quality export excel"

Expected sheets:
✅ Quality Dashboard (summary metrics)
✅ Feed Details (with grade-based coloring)
✅ Performance Metrics (response times, uptime)
✅ Content Analysis (relevance, signal-to-noise)
✅ Recommendations
✅ Benchmark Comparison

Features:
• Sparklines for trends
• Conditional formatting (grade colors)
• Interactive filters
• Charts: distribution, trends, benchmarks
```

### Test Scenario C: Formulas & Interactivity
```
Test: Formula calculations work correctly

In Remediation Tracker sheet:
Column: "Days Until Due"
Formula: =DueDate - TODAY()

Test:
1. Open Excel file
2. Navigate to Remediation Tracker
3. Check formula in "Days Until Due" column
4. Verify formula auto-updates daily

Expected:
✅ Formula visible in formula bar
✅ Calculation correct
✅ Conditional format: Red if overdue (< 0)
```

---

## Test 7: Feed Quality Analyzer

### Objective
Test comprehensive feed performance analysis

### Test Scenario A: Full Portfolio Analysis
```
Command:
"/feed-quality"

Expected output:
📊 FEED QUALITY ANALYSIS

Portfolio Summary:
• Total Feeds: 15
• Healthy: 12 (80%)
• Warning: 2 (13%)
• Failing: 1 (7%)
• Average Quality Score: 78/100 (Good)

Top Performers (Grade A):
1. CISA Advisories - Score: 98/100
   Response: 1.2s | Uptime: 99.9% | Daily updates
   Unique threats: 45 | Critical: 8

2. Microsoft MSRC - Score: 94/100
   Response: 2.1s | Uptime: 99.5% | 3x/week updates

Needs Attention:
❌ SlowFeed - Score: 38/100 (F)
   Issues:
   - Response time: 18.5s (too slow)
   - Only 2 updates in 30 days
   - 85% overlap with faster feeds
   Recommendation: REMOVE

Optimization Opportunities:
🎯 Remove 1 feed → Save 15s per refresh
🎯 Add "Rapid7 Blog" → Fill research gap

Metrics validated:
✅ Response times measured
✅ Uptime percentage calculated
✅ Update frequency tracked
✅ Content relevance scored
✅ Redundancy detected
✅ Quality scores computed (0-100)
```

### Test Scenario B: Benchmark Comparison
```
Command:
"/feed-quality benchmark"

Expected:
📈 PORTFOLIO BENCHMARK

YOUR PORTFOLIO vs. INDUSTRY:

Government Feeds:
  Quality: 92 vs. Industry: 88 ✅ Above
  Speed: 1.8s vs. Industry: 2.5s ✅ Faster

Vendor Feeds:
  Quality: 79 vs. Industry: 82 ⚠️ Below
  Speed: 4.2s vs. Industry: 3.8s ⚠️ Slower

Overall: Grade B+ (Above Average)
```

### Test Scenario C: Feed Health Check
```
Command:
"/feed-quality monitor --check-health"

Expected behavior:
1. HTTP HEAD request to each feed
2. Response time measurement
3. Status code checking
4. SSL validation
5. Redirect detection

Output:
🏥 FEED HEALTH CHECK

✅ All 15 feeds operational
Average response: 2.8s
No SSL errors
No redirects detected

OR (if issues):
⚠️ Issues detected:
• FeedX: Slow response (12.3s)
• FeedY: HTTP 503 (temporary outage)
```

---

## Test 8: Threat Pattern Analyzer

### Objective
Test trend detection, campaign correlation, and predictions

### Test Scenario A: Trending Threats (30-day window)
```
Command:
"/trending"

Expected output:
📈 THREAT TREND ANALYSIS (30 days)

TOP TRENDING THREATS:

1. 🔥 CVE-2024-12345: Auth Bypass
   Trend Score: 95/100 (Emerging - Rapid Rise)
   • Frequency: 45 mentions (+1400%) 📈
   • CVSS: 9.1 (increasing)
   • Sources: 12 feeds
   • Industries: Financial, Healthcare
   • Your Risk: HIGH (affects Payment Systems)
   • First seen: Oct 15 | Peak: Oct 22

2. 📊 Supply Chain Campaign
   Trend Score: 82/100 (Rising)
   • Associated CVEs: 6
   • Threat actor: APT-29
   • Timeline: Accelerating since Oct 10

Analysis validation:
✅ Time-series data processed
✅ Frequency changes calculated
✅ Trend direction determined
✅ Industry correlation applied
✅ Crown jewel impact assessed
```

### Test Scenario B: Campaign Correlation
```
Command:
"/trending campaigns"

Expected:
🎯 ATTACK CAMPAIGN ANALYSIS

Detected Campaigns: 3

Campaign 1: "Exchange Server Wave"
   • Confidence: 0.92 (High)
   • Duration: Jul 15 - Sep 30
   • CVEs: 8 (Exchange RCE family)
   • Threat Actors: APT-28, ransomware groups
   • Status: Declining (patching effective)

Campaign 2: "Supply Chain Q4" [ACTIVE]
   • Confidence: 0.85
   • Duration: Oct 1 - Present
   • CVEs: 6 (update mechanisms)
   • Status: EMERGING - Rapid expansion ⚠️
   • Your risk: HIGH

Validation:
✅ CVEs grouped by temporal proximity
✅ Techniques correlated
✅ Threat actors attributed
✅ Campaign timeline constructed
```

### Test Scenario C: Anomaly Detection
```
Command:
"/trending anomalies"

Expected:
🚨 THREAT ANOMALY REPORT

Anomalies detected: 4

1. ⚠️ CRITICAL: Severity Spike (Oct 22)
   • Baseline CVSS: 6.2
   • Observed: 9.1 (+47%, 5.8σ deviation)
   • Cause: 7 critical 0-days released
   • Action: Emergency review

2. 📊 Volume Spike (Oct 18-20)
   • Baseline: 12-18 threats/day
   • Observed: 45-52/day (+250%, 4.2σ)
   • Cause: Patch Tuesday + conference

Validation:
✅ Statistical baseline calculated
✅ Standard deviations computed
✅ Outliers identified (>3σ)
✅ Potential causes suggested
```

### Test Scenario D: Predictions
```
Command:
"/trending predictions"

Expected:
🔮 THREAT PREDICTIONS (Next 30 days)

1. Campaign Expansion (Confidence: 0.78)
   • Prediction: Supply Chain → Banking sector
   • Timeframe: 14-21 days
   • Your risk: HIGH
   • Recommended actions:
     1. Audit supply chain dependencies
     2. Deploy campaign IOCs
     3. Prepare incident response

2. Volume Increase (Confidence: 0.65)
   • Prediction: 20-30% more threats
   • Timeframe: Next 2 weeks
   • Reason: Historical pattern (monthly cycle)

Validation:
✅ Time-series forecasting applied
✅ Confidence scores calculated
✅ Timeline estimates provided
✅ Recommendations generated
```

---

## Integration Testing

### Test 9: End-to-End Workflow

#### Scenario: Complete Threat Intelligence Cycle
```
Step 1: Import feeds
"/import-feeds security-feeds.opml"
Expected: 15 feeds imported ✓

Step 2: Refresh threat data
"/refresh"
Expected: Threats collected from all feeds ✓
  → threat-validator used for quality
  → Duplicates removed

Step 3: Analyze trending threats
"/trending"
Expected: Pattern analyzer identifies top trends ✓
  → CVE-2024-XXXX trending
  → Campaign detected

Step 4: Deep-dive on specific CVE
"/cve CVE-2024-XXXX"
Expected: CVE analyzer enriches data ✓
  → Parallel NVD/EPSS/KEV fetch (5-10s)
  → Crown jewel impact shown

Step 5: Generate executive report
"/executive-brief pdf"
Expected: PDF report generator creates document ✓
  → Uses trend data from step 3
  → Uses CVE data from step 4
  → Professional 8-page PDF

Step 6: Export for SOC team
"/export excel"
Expected: Excel workbook generated ✓
  → Multiple worksheets
  → Interactive pivot tables
  → Remediation tracker

Step 7: Optimize feeds
"/feed-quality"
Expected: Feed analyzer provides insights ✓
  → Quality scores for all 15 feeds
  → Recommendations to remove 2 slow feeds
  → Suggestions to add 3 new feeds

Full cycle validation:
✅ All skills invoked correctly
✅ Data flows between skills
✅ No errors or failures
✅ Performance targets met
```

---

## Performance Testing

### Test 10: Measure Skill Performance

#### CVE Analysis Speed Test
```
Test: Analyze 5 CVEs sequentially

WITHOUT skill (baseline):
CVE-2024-1: 35s
CVE-2024-2: 42s
CVE-2024-3: 38s
CVE-2024-4: 40s
CVE-2024-5: 37s
Total: 192 seconds (3.2 minutes)

WITH cve-analyzer skill:
CVE-2024-1: 6s
CVE-2024-2: 7s
CVE-2024-3: 5s
CVE-2024-4: 8s
CVE-2024-5: 6s
Total: 32 seconds

Improvement: 6x faster ✅
```

#### Feed Import Speed Test
```
Test: Import 20 feeds from OPML

WITHOUT skill:
Manual validation, inconsistent results
Estimated: 5-10 minutes

WITH opml-processor skill:
Parse + Validate + Import: 45 seconds

Improvement: 10x faster ✅
```

#### Report Generation Test
```
Test: Generate weekly summary

Manual markdown formatting: 2-3 minutes
Basic text output

WITH pdf-report-generator:
Professional PDF with charts: 3-5 seconds

Improvement: 40x faster + professional quality ✅
```

---

## Error Testing

### Test 11: Error Handling

#### Invalid Inputs
```
Test: Each skill with invalid input

CVE Analyzer:
- Input: "CVE-INVALID-FORMAT"
- Expected: ❌ Clear error message, format examples

Threat Validator:
- Input: Malformed JSON
- Expected: ❌ Parsing error, schema guidance

CSV Handler:
- Input: File with malformed CSV
- Expected: ⚠️ Partial import, row-level errors

OPML Processor:
- Input: Invalid XML
- Expected: ❌ XML parsing error, recovery attempt

PDF Generator:
- Input: Empty dataset
- Expected: ⚠️ Template with sample data, warning

Excel Generator:
- Input: Missing required fields
- Expected: ⚠️ Use defaults, flag in notes

Feed Quality Analyzer:
- Input: Unreachable feeds
- Expected: ⚠️ Mark as failing, suggest retry

Pattern Analyzer:
- Input: Insufficient data (<7 days)
- Expected: ⚠️ Analysis with caveats
```

#### Network Failures
```
Test: External API unavailable

CVE Analyzer:
- NVD down → Use cache + EPSS only ✓
- EPSS down → Use CVSS + KEV only ✓
- All down → Return cache or error ✓

Feed Quality:
- Feed unreachable → Mark failing, don't crash ✓
```

---

## Automated Testing Checklist

### Quick Validation Suite (10 minutes)

```
□ Test 1: CVE Analysis
  □ Analyze known CVE (e.g., CVE-2024-3094)
  □ Verify < 15s response time
  □ Check all data sources fetched

□ Test 2: Feed Import
  □ Create test OPML with 3 feeds
  □ Import via /import-feeds
  □ Verify config updated

□ Test 3: Data Validation
  □ Submit incomplete threat JSON
  □ Verify auto-corrections applied
  □ Check quality score calculated

□ Test 4: Report Generation
  □ Generate /executive-brief
  □ Verify PDF created
  □ Check file size reasonable (1-3 MB)

□ Test 5: Trending Analysis
  □ Run /trending
  □ Verify trends detected
  □ Check predictions provided

□ Test 6: Feed Quality
  □ Run /feed-quality
  □ Verify all feeds scored
  □ Check recommendations provided

□ Test 7: Export Operations
  □ Export CSV
  □ Export Excel
  □ Export OPML
  □ Verify file formats valid

□ Test 8: Error Handling
  □ Test with invalid CVE
  □ Test with malformed file
  □ Verify graceful failures
```

### Comprehensive Test Suite (30 minutes)

Run all 11 detailed test scenarios above, documenting:
- ✅ Pass/Fail for each test
- ⏱️ Actual vs. expected performance
- 📝 Notes on any issues
- 🐛 Bugs discovered

---

## Test Data Files

### Create Test Assets

Create these test files in `data/test/`:

**test-feeds.csv**:
```csv
name,url,priority,description,category
"Test CISA","https://www.cisa.gov/cybersecurity-advisories/all.xml","critical","Test import","government"
"Test Microsoft","https://api.msrc.microsoft.com/update-guide/rss","high","Test import","vendor"
```

**test-feeds.opml**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head><title>Test Feeds</title></head>
  <body>
    <outline text="Test Government">
      <outline text="Test CISA" xmlUrl="https://www.cisa.gov/cybersecurity-advisories/all.xml" type="rss"/>
    </outline>
  </body>
</opml>
```

**test-threat.json**:
```json
{
  "title": "Test Critical Vulnerability",
  "source_name": "Test Source",
  "source_type": "vendor",
  "published_utc": "2024-10-24T10:00:00Z",
  "admiralty_source_reliability": "B",
  "admiralty_info_credibility": 2,
  "cves": ["CVE-2024-9999"],
  "cvss_v3": 8.5,
  "summary": "Test threat for validation"
}
```

---

## Success Criteria Summary

### Overall Skill Quality Metrics

For skills to be considered production-ready:

✅ **Functionality**: All 8 skills execute without errors
✅ **Performance**: Meet or exceed target metrics
  - CVE analysis: <15s (target: 5-10s)
  - Feed import: <60s for 20 feeds
  - Report generation: <10s
  - Validation: >500 threats/second

✅ **Accuracy**:
  - Validation: >95% correct auto-corrections
  - Deduplication: <1% false positives
  - Trend detection: >90% precision

✅ **Integration**: Skills work with agents/commands
✅ **Error Handling**: Graceful failures with helpful messages
✅ **Documentation**: All examples work as documented

---

## Reporting Issues

### If You Find Problems

Document:
1. **Skill name** tested
2. **Test scenario** attempted
3. **Expected behavior** (from this guide)
4. **Actual behavior** observed
5. **Error messages** (if any)
6. **Test data** used
7. **Claude Code version**

Report in GitHub Issues with label: `skill-testing`

---

## Next Steps

After testing:
1. ✅ Mark tests as passing/failing in checklist
2. 📝 Document any performance improvements observed
3. 🐛 Create issues for any bugs found
4. 💡 Suggest enhancements based on usage
5. 📊 Share results with team

---

**Testing Guide Version**: 1.0
**Last Updated**: 2024-10-24
**Skills Version**: 1.0
