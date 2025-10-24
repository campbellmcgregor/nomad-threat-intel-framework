---
name: excel-generator
description: Create multi-worksheet Excel reports with threat analytics and interactive features
version: 1.0
---

# Excel Workbook Generator Skill

## Purpose
Generate comprehensive multi-worksheet Excel workbooks with threat intelligence data, featuring pivot tables, conditional formatting, charts, and interactive dashboards for in-depth analysis and team collaboration.

## Capabilities
- Multi-sheet workbooks with related data
- Interactive pivot tables for analysis
- Conditional formatting for risk visualization
- Embedded charts and sparklines
- Data validation and dropdown lists
- Formula-driven calculations
- Protected sheets with unlocked input cells
- Freeze panes and filtered views
- Cell comments and notes
- Hyperlinks to external resources

## Input Schema

```json
{
  "workbook_type": "threat-analysis|weekly-report|feed-quality|cve-deep-dive|compliance|custom",
  "output_path": "string (destination .xlsx file)",
  "data": {
    "threats": ["array of threat objects"],
    "feeds": ["array of feed objects"],
    "crown_jewels": ["array from user preferences"],
    "cve_details": ["array of enriched CVE data"],
    "metrics": {/* custom metrics */}
  },
  "metadata": {
    "organization": "string",
    "report_title": "string",
    "report_period": "string",
    "prepared_by": "NOMAD v2.0",
    "created_date": "ISO 8601"
  },
  "options": {
    "include_pivot_tables": "boolean (default: true)",
    "include_charts": "boolean (default: true)",
    "conditional_formatting": "boolean (default: true)",
    "freeze_header_rows": "boolean (default: true)",
    "auto_filter": "boolean (default: true)",
    "protect_sheets": "boolean (default: false)",
    "include_formulas": "boolean (default: true)"
  },
  "custom_sheets": [
    {
      "name": "string",
      "data": "array of row objects",
      "columns": ["array of column definitions"]
    }
  ]
}
```

## Output Schema

```json
{
  "status": "success|failed",
  "output_file": "string (path to .xlsx file)",
  "summary": {
    "sheets": "number",
    "rows": "number (total across all sheets)",
    "charts": "number",
    "pivot_tables": "number",
    "file_size_bytes": "number"
  },
  "sheets_created": [
    {
      "name": "string",
      "rows": "number",
      "columns": "number",
      "features": ["pivot_table", "chart", "conditional_format"]
    }
  ],
  "generation_time_ms": "number"
}
```

## Workbook Type Templates

### Threat Analysis Workbook

**Sheets**:

1. **Summary Dashboard**:
   - Threat count by severity (with sparklines)
   - KEV status summary
   - Crown jewel impact overview
   - Trend indicators (▲▼ arrows)
   - Quick stats cards
   - Links to detail sheets

2. **Threats Detail**:
   - Columns: CVE, Title, CVSS, EPSS, KEV, Severity, Source, Published Date, Crown Jewel Impact, Status
   - Conditional formatting:
     - CVSS ≥9.0: Red fill
     - CVSS 7.0-8.9: Orange fill
     - CVSS 4.0-6.9: Yellow fill
     - KEV = Yes: Bold red text
   - Auto-filter enabled
   - Freeze top row
   - Sortable columns
   - Data validation for Status column (New|In Progress|Remediated|Accepted Risk)

3. **CVE Analysis**:
   - Detailed CVE information
   - Columns: CVE, Description, Affected Products, Remediation, Priority, Assigned To, Due Date
   - Hyperlinks to NVD, vendor advisories
   - Priority scoring formulas
   - Color-coded priority levels

4. **Crown Jewel Matrix**:
   - Rows: Crown jewel systems
   - Columns: Threat count, Critical count, High count, Remediation status
   - Conditional formatting: Heat map
   - Pivot table: Threats by crown jewel
   - Chart: Bar chart of threats per system

5. **Industry Analysis**:
   - Industry-specific threats
   - Sector comparison
   - Compliance mapping
   - Pivot table: By industry tag

6. **Timeline View**:
   - Threats by publication date
   - Columns: Date, Count, Critical, High, Medium, Low
   - Line chart: Threat volume over time
   - Sparklines for each severity

7. **Feed Sources**:
   - Source breakdown
   - Columns: Source Name, Threats Count, Quality Score, Unique Contributions
   - Pie chart: Threats by source category

8. **Remediation Tracker**:
   - Columns: CVE, Asset, Owner, Status, Due Date, Notes
   - Conditional formatting: Overdue = Red
   - Dropdown data validation for Status, Owner
   - Formula: Days until due / Days overdue

**Features**:
- Master pivot table on Summary sheet
- Dynamic charts that update with data
- Protected structure with unlocked data entry cells
- Print-ready formatting

### Weekly Report Workbook

**Sheets**:

1. **Executive Summary**:
   - KPIs: Total threats, Critical/High counts, KEV additions
   - Comparison to previous week (% change)
   - Top 5 threats table
   - Action items checklist

2. **Detailed Threats**:
   - All threats from the week
   - Full threat data with sorting/filtering

3. **Trend Analysis**:
   - Daily threat counts
   - Severity distribution chart
   - Week-over-week comparison
   - Moving averages

4. **Crown Jewel Impact**:
   - Which systems affected
   - Risk scores per system
   - Priority actions

5. **Recommendations**:
   - Prioritized action list
   - Owner assignments
   - Due dates
   - Status tracking

### Feed Quality Workbook

**Sheets**:

1. **Quality Dashboard**:
   - Overall portfolio health score
   - Feed count by grade (A/B/C/D/F)
   - Performance summary
   - Charts: Quality distribution, Response times

2. **Feed Details**:
   - Columns: Feed Name, Category, Quality Score, Grade, Response Time, Uptime %, Update Freq, Relevance, Value
   - Conditional formatting: Grade-based coloring
   - Sparklines: Response time trends

3. **Performance Metrics**:
   - Response time statistics (avg, p50, p95, p99)
   - Availability data
   - Update frequency analysis
   - Charts: Performance trends

4. **Content Analysis**:
   - Relevance scores
   - CVE extraction rates
   - Signal-to-noise ratios
   - Unique content contributions
   - Charts: Content quality metrics

5. **Recommendations**:
   - Feeds to remove
   - Feeds to add
   - Configuration changes
   - Expected impact

6. **Benchmark Comparison**:
   - Your feeds vs. industry averages
   - Category-level comparison
   - Gap analysis

### CVE Deep Dive Workbook

**Sheets**:

1. **CVE Overview**:
   - Summary card with key metrics
   - Risk assessment
   - Organizational impact
   - Priority score

2. **CVSS Breakdown**:
   - Vector components table
   - Score calculation
   - Radar chart visualization

3. **Exploitation Intel**:
   - EPSS data
   - KEV status
   - Known campaigns
   - Threat actors
   - Exploit availability

4. **Affected Assets**:
   - Crown jewel correlation
   - Product/version matrix
   - Exposure assessment
   - Business impact

5. **Remediation Plan**:
   - Patch information
   - Workarounds
   - Detection guidance
   - Action items with timeline

6. **References**:
   - Vendor advisories (hyperlinked)
   - Research papers
   - NVD/KEV links
   - Internal documentation

## Excel Features Implementation

### Pivot Tables

Create interactive pivot tables for multi-dimensional analysis:

```
Pivot Table: Threats by Severity and Crown Jewel
Rows: Crown Jewel System
Columns: Severity Level
Values: Count of Threats
Filters: Date Range, Source, KEV Status

Features:
- Drill-down capability
- Sortable rows/columns
- Collapsible groups
- Calculated fields
- Multiple value aggregations
```

### Conditional Formatting

Visual risk indicators:

```
Severity-based Cell Coloring:
- Critical (CVSS ≥9.0): Dark Red fill, White text
- High (CVSS 7.0-8.9): Orange fill, Black text
- Medium (CVSS 4.0-6.9): Yellow fill, Black text
- Low (CVSS <4.0): Green fill, Black text

Icon Sets:
- KEV Status: ⚠️ if Yes, ✓ if No
- Trend: ▲ Increasing, ▬ Stable, ▼ Decreasing
- Priority: 🔴 P0, 🟠 P1, 🟡 P2, 🟢 P3/P4

Data Bars:
- EPSS scores: Horizontal bar (0.0-1.0)
- Quality scores: Gradient bar (0-100)
- Timeline: Days until due date

Color Scales:
- Heat maps for crown jewel impact matrix
- Risk matrices (likelihood × impact)
```

### Charts & Visualizations

Embedded interactive charts:

```
Chart Types:
1. Column Chart: Threat count by severity
2. Line Chart: Threat trends over time
3. Pie Chart: Threat distribution by source
4. Bar Chart: Crown jewel impact comparison
5. Scatter Plot: CVSS vs. EPSS correlation
6. Combo Chart: Threats + Remediation rate
7. Radar Chart: CVSS vector breakdown
8. Sparklines: Inline trend indicators

Chart Styling:
- Professional color scheme (blue, orange, gray)
- Clear labels and legends
- Data labels for key values
- Gridlines for readability
```

### Formulas & Calculations

Dynamic calculations:

```
Priority Score:
=IF(KEV="Yes", 90, CVSS*5 + EPSS*100*3 + CrownJewel*10)

Days Until Due:
=DueDate - TODAY()

Overdue Indicator:
=IF(DaysUntilDue<0, "OVERDUE", IF(DaysUntilDue<7, "URGENT", "OK"))

Remediation Progress:
=COUNTIF(Status,"Remediated")/COUNTA(Status)

Risk Level:
=IF(CVSS>=9, "CRITICAL", IF(CVSS>=7, "HIGH", IF(CVSS>=4, "MEDIUM", "LOW")))
```

### Data Validation

Dropdown lists and input validation:

```
Status Column:
Dropdown: New | In Progress | Remediated | Accepted Risk | Deferred

Owner Column:
Dropdown: SOC Team | IT Security | Network Team | Application Team

Priority Column:
Dropdown: P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low) | P4 (Planned)

Date Validation:
Must be >= Today for due dates

Number Validation:
CVSS: 0.0 to 10.0
EPSS: 0.0 to 1.0
```

### Sheet Protection

Protect analysis while allowing data entry:

```
Protected Elements:
- Headers and labels (locked)
- Formulas and calculations (locked)
- Charts and pivot tables (locked)
- Conditional formatting rules (locked)

Unlocked Elements:
- Status column (editable)
- Owner column (editable)
- Due date column (editable)
- Notes column (editable)

Password: Optional (for enterprise use)
Permissions: Select unlocked cells, Use pivot tables, Use filters
```

### Freeze Panes & Filters

Enhanced navigation:

```
Freeze Panes:
- Top row (headers) always visible
- First column (identifier) always visible
- Split panes for large datasets

Auto-Filter:
- Enabled on all data tables
- Filter by severity, status, date range
- Multi-select filters
- Search within filters

Sort Options:
- Primary: CVSS (descending)
- Secondary: Published Date (descending)
- Custom sort orders available
```

## Excel Generation Process

### Step 1: Workbook Creation
- Initialize Excel workbook object
- Set document properties (title, author, subject)
- Configure default styles and themes

### Step 2: Sheet Generation
For each sheet in template:
- Create worksheet with name
- Set column widths (auto-fit or specified)
- Apply header formatting (bold, background color)
- Set print settings (orientation, scaling, margins)

### Step 3: Data Population
- Write headers to row 1
- Populate data rows starting at row 2
- Apply number formats:
  - Dates: "YYYY-MM-DD HH:MM"
  - CVSS: "0.0"
  - EPSS: "0.000"
  - Percentages: "0%"
- Insert hyperlinks where applicable

### Step 4: Formatting Application
- Apply conditional formatting rules
- Add data validation dropdowns
- Create named ranges for formulas
- Insert formulas in calculated columns
- Format cells (alignment, borders, colors)

### Step 5: Visual Elements
- Insert charts with data references
- Create pivot tables
- Add sparklines
- Insert cell comments/notes
- Add sheet-level comments

### Step 6: Navigation & UX
- Freeze panes at appropriate positions
- Enable auto-filters
- Set default zoom level (100% or fit)
- Hide gridlines on dashboard sheets
- Add hyperlinks between sheets

### Step 7: Protection & Finalization
- Lock cells as configured
- Protect sheets if requested
- Set workbook password (optional)
- Calculate all formulas
- Save as .xlsx (Excel 2007+ format)

## Example Usage

### Generate Threat Analysis Workbook
```
Input:
{
  "workbook_type": "threat-analysis",
  "output_path": "./reports/threats-october-2024.xlsx",
  "data": {
    "threats": [/* 50 threats */],
    "crown_jewels": ["Customer DB", "Payment System", "Email"]
  },
  "metadata": {
    "organization": "Acme Corp",
    "report_title": "October 2024 Threat Analysis"
  }
}

Output:
✅ Excel Workbook Generated

threats-october-2024.xlsx
- Sheets: 8 (Summary, Threats, CVE Analysis, Crown Jewels, Industry, Timeline, Sources, Remediation)
- Rows: 387 total
- Charts: 6
- Pivot Tables: 3
- File size: 1.2 MB
- Generation time: 2.4 seconds

Features included:
✓ Conditional formatting (risk-based colors)
✓ Auto-filters on all data tables
✓ Interactive pivot tables
✓ Embedded trend charts
✓ Formula-driven priority scores
✓ Protected with editable status fields
```

### Generate Feed Quality Report
```
Input:
{
  "workbook_type": "feed-quality",
  "data": {
    "feeds": [/* 15 feeds */],
    "metrics": {/* quality metrics */}
  }
}

Output:
📊 Feed Quality Workbook Created

feed-quality-report.xlsx
- Sheets: 6
- Rows: 95 total
- Charts: 8 (distribution, trends, benchmarks)
- Conditional formatting: Grade-based coloring
- Sparklines: Performance trends per feed

Analysis includes:
• Quality dashboard with overall score
• Individual feed performance metrics
• Benchmark comparison vs. industry
• Optimization recommendations
• Historical trend analysis
```

## Error Handling

### Data Issues
- **Empty dataset**: Create template with sample data, warn user
- **Missing required fields**: Use defaults, flag in notes
- **Invalid data types**: Coerce or skip, log warnings

### Excel Generation Errors
- **Formula errors**: Validate formulas, fall back to values
- **Chart data errors**: Skip chart, include data table
- **File write error**: Check permissions, suggest alternative path

## Integration Points

### Files Used
- **Reads from**:
  - `data/threats-cache.json`
  - `config/user-preferences.json`
  - `data/feed-quality-metrics.json`

- **Writes to**:
  - User-specified output path
  - `data/output/reports/` (default location)

### Command Integration
- Used by: `/export excel` command
- Used by: `/weekly-summary excel` command
- Used by: `agents/threat-synthesizer.md` (report generation)
- Integrates with: `pdf-report-generator` (multi-format export)

## Performance Characteristics
- **Simple workbook** (3-5 sheets, 100 rows): 1-2 seconds
- **Complex workbook** (8+ sheets, 500+ rows, charts): 3-5 seconds
- **Large dataset** (1000+ rows): 5-10 seconds
- **Memory usage**: <30MB per workbook

## Excel Compatibility
- **Format**: .xlsx (Excel 2007+, Office Open XML)
- **Compatible with**: Microsoft Excel, Google Sheets, LibreOffice Calc, Apple Numbers
- **Features supported**: All major features across platforms
- **Limitations**: Complex pivot tables may require Excel for full functionality
