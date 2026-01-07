---
name: pdf-report-generator
description: Generate executive-ready PDF reports from threat intelligence data
version: 1.0
---

# PDF Report Generator Skill

## Purpose
Transform threat intelligence data into professional, executive-ready PDF reports with charts, tables, risk matrices, and visual insights suitable for stakeholder presentations and compliance documentation.

## Capabilities
- Executive summary reports for leadership
- Technical security alerts for SOC teams
- Weekly/monthly threat landscape summaries
- CVE-specific detailed analysis reports
- Compliance documentation with threat mapping
- Multi-page reports with branding and formatting
- Embedded charts, graphs, and risk matrices
- Table of contents and navigation
- Export-ready PDF/A format for archival

## Input Schema

```json
{
  "report_type": "executive|technical|weekly|monthly|cve|compliance|custom",
  "title": "string (report title)",
  "subtitle": "string (optional)",
  "data": {
    "threats": ["array of threat objects"],
    "cvss_scores": ["array for charts"],
    "trend_data": ["array for time-series"],
    "crown_jewel_impacts": ["array for correlation"],
    "summary_stats": {
      "total_threats": "number",
      "critical_count": "number",
      "high_count": "number",
      "medium_count": "number",
      "low_count": "number",
      "kev_count": "number"
    }
  },
  "metadata": {
    "organization": "string",
    "prepared_for": "string (recipient name/role)",
    "prepared_by": "NOMAD v2.0",
    "report_period": "string (e.g., 'October 1-31, 2024')",
    "classification": "INTERNAL|CONFIDENTIAL|PUBLIC",
    "logo_path": "string (optional path to logo image)"
  },
  "options": {
    "include_toc": "boolean (default: true for multi-page)",
    "include_charts": "boolean (default: true)",
    "include_executive_summary": "boolean (default: true)",
    "include_technical_details": "boolean (default: varies by type)",
    "include_recommendations": "boolean (default: true)",
    "page_numbers": "boolean (default: true)",
    "color_scheme": "professional|high-contrast|grayscale"
  },
  "output_path": "string (destination file path)"
}
```

## Output Schema

```json
{
  "status": "success|failed",
  "output_file": "string (path to generated PDF)",
  "summary": {
    "pages": "number",
    "file_size_bytes": "number",
    "charts_included": "number",
    "tables_included": "number"
  },
  "generation_time_ms": "number",
  "pdf_metadata": {
    "title": "string",
    "author": "NOMAD v2.0",
    "subject": "Threat Intelligence Report",
    "keywords": ["threat intelligence", "security"],
    "created_date": "ISO 8601"
  }
}
```

## Report Type Templates

### Executive Summary Report

**Target Audience**: C-level executives, board members, non-technical leadership

**Structure**:
1. **Cover Page**:
   - Report title
   - Organization name/logo
   - Report period
   - Classification marking
   - Prepared by/for information

2. **Executive Summary** (1 page):
   - Key findings (3-5 bullet points)
   - Critical threat count with business impact
   - Top 3 recommended actions
   - Risk level indicator (Critical/High/Medium/Low)

3. **Threat Landscape Overview** (1-2 pages):
   - Severity distribution pie chart
   - Trend over time line chart
   - Crown jewel impact summary table
   - Industry-specific threats highlight

4. **Priority Threats** (2-3 pages):
   - Top 5 critical threats table:
     - Threat name
     - Business impact
     - Affected systems
     - Status/Timeline
   - Brief description of each
   - Visual risk matrix

5. **Recommendations** (1 page):
   - Immediate actions (next 24-48 hours)
   - Short-term initiatives (next 1-2 weeks)
   - Strategic improvements (next quarter)
   - Resource requirements

6. **Appendix** (optional):
   - Methodology
   - Data sources
   - Glossary of terms
   - Contact information

**Formatting**:
- Large fonts (14-18pt headings, 11-12pt body)
- Minimal technical jargon
- High-level visualizations
- Business impact focus
- ~6-10 pages total

### Technical Security Alert

**Target Audience**: SOC analysts, security engineers, IT administrators

**Structure**:
1. **Alert Header**:
   - Alert ID and timestamp
   - Severity indicator (color-coded)
   - TLP (Traffic Light Protocol) marking
   - Distribution list

2. **Threat Overview**:
   - CVE identifiers with CVSS scores
   - Attack vector description
   - Affected products/versions table
   - Exploitation status (KEV, EPSS)

3. **Technical Details**:
   - Vulnerability description
   - Attack chain diagram
   - Proof-of-concept availability
   - Known threat actors/campaigns

4. **Impact Assessment**:
   - Affected crown jewel systems table
   - Asset exposure (internal/external/cloud)
   - Potential consequences
   - Business impact severity

5. **Immediate Actions**:
   - Detection guidance (signatures, IOCs)
   - Containment steps
   - Remediation procedures
   - Patch information with URLs

6. **References**:
   - Vendor advisories
   - NVD/CISA links
   - Research papers
   - Internal ticket references

**Formatting**:
- Dense information layout
- Code blocks for commands/signatures
- Technical terminology appropriate
- Monospace fonts for technical content
- ~3-5 pages

### Weekly/Monthly Summary

**Target Audience**: Security managers, risk teams, compliance officers

**Structure**:
1. **Cover Page & Contents**

2. **Summary Dashboard** (1 page):
   - Key metrics cards:
     - Total threats reviewed
     - Critical/High priority count
     - KEV additions
     - Trends vs. previous period
   - Executive summary paragraph

3. **Threat Trends** (2-3 pages):
   - Time-series chart (threats over period)
   - Severity distribution over time
   - Top attack vectors bar chart
   - Industry threat comparison

4. **Notable Threats** (3-5 pages):
   - Top 10 threats table with:
     - CVE/Identifier
     - CVSS/EPSS
     - Crown jewel impact
     - Status
   - Detailed view of top 3-5 threats

5. **Crown Jewel Analysis** (1-2 pages):
   - Threats by crown jewel system
   - Impact correlation matrix
   - Protection status

6. **Industry Intelligence** (1-2 pages):
   - Industry-specific threats
   - Peer comparison
   - Compliance implications

7. **Recommendations & Next Steps** (1 page):
   - Priority actions
   - Feed optimization suggestions
   - Process improvements

**Formatting**:
- Balanced technical/executive content
- Rich visualizations
- Summary tables
- Trend analysis focus
- ~10-15 pages

### CVE Analysis Report

**Target Audience**: Security teams, vendors, risk management

**Structure**:
1. **CVE Summary Card**:
   - CVE ID with official title
   - CVSS score badge
   - KEV status indicator
   - Publication date

2. **Risk Metrics Dashboard**:
   - CVSS breakdown chart (radar/spider)
   - EPSS score with percentile
   - Exploitation timeline
   - Severity indicators

3. **Vulnerability Details**:
   - Description
   - Affected products table
   - CWE categories
   - Attack vector description

4. **Organizational Impact**:
   - Crown jewel correlation
   - Asset exposure assessment
   - Business impact summary
   - Priority score calculation

5. **Threat Intelligence**:
   - Exploitation status
   - Known campaigns
   - Threat actor attribution
   - Public exploits

6. **Remediation**:
   - Patch availability
   - Vendor advisories
   - Workarounds
   - Detection guidance

7. **References**:
   - NVD, EPSS, KEV links
   - Vendor URLs
   - Research links

**Formatting**:
- Single CVE focus
- Dense information
- Visual risk representation
- Technical depth
- ~5-8 pages

## Chart Types & Visualizations

### Severity Distribution Pie Chart
```
Critical (10%) - Red
High (25%) - Orange
Medium (45%) - Yellow
Low (20%) - Blue
```

### Threat Trend Line Chart
```
X-axis: Time (days/weeks)
Y-axis: Threat count
Lines: Total, Critical, High
```

### Risk Matrix (Heat Map)
```
         Likelihood →
Impact   Low  Medium  High
  ↓
Critical  [Y]   [O]   [R]
High      [G]   [Y]   [O]
Medium    [G]   [G]   [Y]
Low       [G]   [G]   [G]

Colors: [R]ed, [O]range, [Y]ellow, [G]reen
```

### Crown Jewel Impact Bar Chart
```
Customer DB      ████████████ (12 threats)
Payment Systems  ████████ (8 threats)
Email Infra      ████ (4 threats)
Auth Systems     ██ (2 threats)
```

### CVSS Breakdown Radar Chart
```
       Attack Vector
            /\
           /  \
Attack Complexity  User Interaction
           \  /
            \/
        Impact
```

### Exploitation Status Gauge
```
EPSS: 0.85/1.0 (85th percentile)
[████████████████░░░░] 85%
Status: Active Exploitation (KEV)
```

## PDF Generation Instructions

### Using Markdown-to-PDF Approach

1. **Generate Markdown Content**:
   - Create structured markdown with report content
   - Use markdown tables for data
   - Include Mermaid.js diagrams for charts
   - Add page breaks with `\pagebreak`

2. **Enhanced Markdown Features**:
```markdown
# Report Title {.title-page}

## Executive Summary {.executive}

| Severity | Count | Percentage |
|----------|-------|------------|
| Critical | 10    | 15%        |
| High     | 25    | 35%        |

![Severity Distribution](chart:pie:severity)

\pagebreak
```

3. **Chart Generation**:
   - Use mermaid.js for diagrams
   - Generate chart data in JSON
   - Include base64-encoded images for complex visuals
   - Provide ASCII-art fallbacks for accessibility

4. **Styling & Formatting**:
   - Apply CSS for professional appearance
   - Use color scheme from options
   - Set margins, headers, footers
   - Add page numbers and TOC

5. **PDF Conversion**:
   - Convert markdown to PDF using available tools
   - Preserve formatting and images
   - Generate bookmarks for navigation
   - Embed fonts for consistency

### Metadata & Properties

Set PDF metadata for professional output:
```
Title: [Report Title]
Author: NOMAD v2.0 Threat Intelligence Framework
Subject: Cybersecurity Threat Intelligence Report
Keywords: threat intelligence, security, [CVEs], [organization]
Creator: NOMAD v2.0
Producer: Claude Code
CreationDate: [ISO 8601]
```

### Accessibility Features
- Alt text for charts/images
- Proper heading hierarchy
- Tagged PDF structure (PDF/UA)
- High contrast mode option
- Screen reader compatible

## Example Usage

### Generate Executive Brief
```
Input:
{
  "report_type": "executive",
  "title": "Weekly Threat Intelligence Briefing",
  "subtitle": "October 15-22, 2024",
  "data": {
    "threats": [/* 45 threats */],
    "summary_stats": {
      "total_threats": 45,
      "critical_count": 3,
      "high_count": 12,
      "kev_count": 5
    }
  },
  "metadata": {
    "organization": "Acme Corp",
    "prepared_for": "CISO",
    "report_period": "October 15-22, 2024"
  }
}

Output:
✅ PDF Report Generated

executive-brief-2024-10-22.pdf
- Pages: 8
- File size: 2.4 MB
- Charts: 5 (pie, line, bar, matrix, gauge)
- Tables: 3
- Generation time: 3.2 seconds

Content includes:
📄 Cover page with branding
📊 Executive summary dashboard
📈 Threat trends analysis
🎯 Top 5 priority threats
✅ Recommended actions
```

### Generate Technical Alert
```
Input:
{
  "report_type": "technical",
  "title": "CRITICAL: Authentication Bypass in Product X",
  "data": {
    "threats": [{
      "cve": "CVE-2024-12345",
      "cvss": 9.8,
      "epss": 0.85,
      "kev_listed": true
    }]
  }
}

Output:
🚨 Technical Security Alert Generated

alert-CVE-2024-12345.pdf
- Pages: 4
- Severity: CRITICAL
- Distribution: SOC Team, IT Admins
- Generation time: 1.8 seconds

Sections:
- Threat overview with CVSS breakdown
- Technical exploit details
- Affected systems (Customer DB, Auth System)
- Immediate remediation steps
- Detection signatures and IOCs
```

## Error Handling

### Generation Errors
- **No data provided**: Return error with required data format
- **Chart generation failure**: Include text-based summary, skip chart
- **PDF conversion error**: Return markdown version, log error
- **File write permission**: Return error with path resolution help

### Data Quality Issues
- **Missing critical fields**: Use defaults, flag in report footer
- **Invalid chart data**: Skip chart, include data table instead
- **Oversized report**: Paginate or summarize, warn user

## Integration Points

### Files Used
- **Reads from**:
  - `data/threats-cache.json` (threat data)
  - `config/user-preferences.json` (organization info, crown jewels)
  - `assets/logo.png` (optional branding)

- **Writes to**:
  - User-specified output path
  - `data/output/reports/` (default location)

### Command Integration
- Used by: `/executive-brief` command
- Used by: `/weekly-summary` command
- Used by: `/technical-alert` command
- Used by: `/export pdf` command
- Used by: `agents/threat-synthesizer.md` (report generation)

## Performance Characteristics
- **Simple report** (3-5 pages): 1-2 seconds
- **Complex report** (10-15 pages): 3-5 seconds
- **With charts** (5+ visualizations): +1-2 seconds
- **Memory usage**: <20MB per report
- **Concurrent generation**: Up to 3 reports simultaneously

## Quality Standards
- **Resolution**: 300 DPI for print quality
- **Color space**: RGB for screen, CMYK for print
- **Font embedding**: Yes (for consistency)
- **Compression**: Balanced (quality vs. size)
- **PDF version**: PDF 1.7 (PDF/A-2 for archival)
- **Accessibility**: WCAG 2.1 AA compliant
