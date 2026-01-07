---
name: feed-quality-analyzer
description: Comprehensive feed performance analytics and optimization recommendations
version: 1.0
---

# Feed Quality Analyzer Skill

## Purpose
Monitor, analyze, and optimize threat intelligence feed sources through comprehensive performance metrics, quality scoring, and data-driven recommendations for feed portfolio optimization.

## Capabilities
- Real-time feed performance monitoring
- Multi-dimensional quality scoring (0-100)
- Security content relevance assessment
- Feed redundancy and overlap detection
- Update frequency analysis
- Response time tracking and alerting
- Signal-to-noise ratio calculation
- Industry benchmark comparison
- Automated optimization recommendations
- Feed health dashboard generation

## Input Schema

```json
{
  "operation": "analyze|benchmark|optimize|monitor|report",
  "scope": {
    "feed_ids": ["array of specific feed IDs, or 'all'"],
    "categories": ["government", "vendor", "research", "custom"],
    "time_window": "24h|7d|30d|90d|all"
  },
  "options": {
    "include_performance_metrics": "boolean (default: true)",
    "include_content_analysis": "boolean (default: true)",
    "include_recommendations": "boolean (default: true)",
    "include_benchmarks": "boolean (default: true)",
    "check_feed_health": "boolean (default: true, tests connectivity)"
  },
  "thresholds": {
    "min_quality_score": "number (0-100, default: 60)",
    "max_response_time_ms": "number (default: 10000)",
    "min_update_frequency_hours": "number (default: 48)",
    "min_relevance_score": "number (0-1.0, default: 0.7)"
  }
}
```

## Output Schema

```json
{
  "status": "success|partial|failed",
  "analysis_timestamp": "ISO 8601 UTC",
  "summary": {
    "total_feeds_analyzed": "number",
    "healthy_feeds": "number",
    "warning_feeds": "number",
    "failing_feeds": "number",
    "average_quality_score": "number (0-100)",
    "portfolio_health": "excellent|good|acceptable|poor"
  },
  "feed_analyses": [
    {
      "feed_id": "string",
      "feed_name": "string",
      "feed_url": "string",
      "category": "string",
      "priority": "string",

      "quality_metrics": {
        "overall_score": "number (0-100)",
        "grade": "A|B|C|D|F",
        "performance_score": "number (0-100)",
        "content_score": "number (0-100)",
        "reliability_score": "number (0-100)",
        "value_score": "number (0-100)"
      },

      "performance_metrics": {
        "response_time": {
          "current_ms": "number",
          "average_ms": "number",
          "p50_ms": "number",
          "p95_ms": "number",
          "p99_ms": "number"
        },
        "availability": {
          "uptime_percentage": "number (0-100)",
          "recent_failures": "number",
          "last_successful": "ISO 8601",
          "last_failure": "ISO 8601 or null"
        },
        "update_frequency": {
          "average_interval_hours": "number",
          "last_update": "ISO 8601",
          "updates_in_window": "number",
          "frequency_trend": "increasing|stable|decreasing"
        }
      },

      "content_metrics": {
        "relevance_score": "number (0-1.0)",
        "security_keywords_ratio": "number (0-1.0)",
        "cve_extraction_rate": "number (0-1.0)",
        "signal_to_noise": "number (0-1.0)",
        "unique_content_ratio": "number (0-1.0)",
        "items_in_window": "number",
        "actionable_items": "number",
        "duplicate_items": "number"
      },

      "feed_health": {
        "status": "healthy|warning|critical|failing",
        "issues": ["array of issue descriptions"],
        "warnings": ["array of warning descriptions"],
        "last_check": "ISO 8601"
      },

      "value_assessment": {
        "threats_contributed": "number",
        "unique_threats": "number",
        "critical_alerts": "number",
        "crown_jewel_relevant": "number",
        "industry_relevant": "number",
        "value_rating": "high|medium|low"
      },

      "redundancy_analysis": {
        "overlapping_feeds": ["array of feed names"],
        "overlap_percentage": "number (0-100)",
        "unique_contribution": "number (0-100)",
        "recommendation": "keep|review|consider_removing"
      }
    }
  ],

  "benchmarks": {
    "industry_averages": {
      "quality_score": "number",
      "response_time_ms": "number",
      "update_frequency_hours": "number",
      "relevance_score": "number"
    },
    "your_portfolio": {
      "quality_score": "number",
      "response_time_ms": "number",
      "update_frequency_hours": "number",
      "relevance_score": "number"
    },
    "comparison": {
      "quality": "above|at|below average",
      "performance": "above|at|below average",
      "content": "above|at|below average"
    }
  },

  "optimization_recommendations": [
    {
      "type": "remove|add|upgrade|configure",
      "priority": "critical|high|medium|low",
      "feed_name": "string",
      "issue": "string (description of problem)",
      "recommendation": "string (specific action to take)",
      "expected_impact": {
        "quality_improvement": "number (0-100)",
        "cost_saving": "low|medium|high",
        "effort_required": "low|medium|high"
      },
      "alternative_feeds": ["array of suggested replacements"]
    }
  ],

  "portfolio_insights": {
    "category_distribution": {
      "government": "number",
      "vendor": "number",
      "research": "number",
      "custom": "number"
    },
    "quality_distribution": {
      "excellent": "number (90-100)",
      "good": "number (75-89)",
      "acceptable": "number (60-74)",
      "poor": "number (0-59)"
    },
    "coverage_gaps": ["array of identified gaps"],
    "overrepresented_areas": ["array of redundant coverage"]
  }
}
```

## Processing Instructions

### Stage 1: Data Collection

1. **Load Feed Configuration**:
   - Read from `config/threat-sources.json`
   - Filter by scope criteria (feed_ids, categories)
   - Extract feed metadata (name, URL, priority, category)

2. **Load Historical Metrics**:
   - Read from `data/feed-quality-metrics.json`
   - Extract performance history for time window
   - Calculate trending metrics

3. **Load Threat Cache**:
   - Read from `data/threats-cache.json`
   - Correlate threats to source feeds
   - Count contributions per feed

### Stage 2: Performance Analysis

1. **Response Time Testing** (if check_feed_health enabled):
   - Execute HTTP HEAD request to each feed URL
   - Measure response time in milliseconds
   - Record HTTP status code
   - Detect redirects and SSL issues
   - Track DNS resolution time separately

2. **Availability Calculation**:
   - Review historical success/failure records
   - Calculate uptime percentage over time window
   - Identify outage patterns (time of day, day of week)
   - Determine MTBF (Mean Time Between Failures)
   - Determine MTTR (Mean Time To Recovery)

3. **Update Frequency Analysis**:
   - Parse feed and extract publication dates
   - Calculate time between updates
   - Determine average interval
   - Identify update patterns (daily, weekly, on-demand)
   - Detect staleness (no updates in expected window)

### Stage 3: Content Quality Analysis

1. **Relevance Scoring**:
   - Analyze recent feed items (last 20-50)
   - Count security-related keywords:
     - Vulnerability, CVE, exploit, patch, advisory
     - Threat, malware, ransomware, phishing
     - Zero-day, breach, compromise, attack
   - Calculate keyword density ratio
   - Assess title/description quality
   - Determine security relevance score (0-1.0)

2. **CVE Extraction Rate**:
   - Scan items for CVE pattern matches
   - Count items with valid CVEs
   - Calculate extraction rate = items_with_cves / total_items
   - High rate (>0.7) indicates good technical depth
   - Low rate (<0.3) may indicate general news

3. **Signal-to-Noise Ratio**:
   - Classify items as:
     - `signal`: Actionable threat intelligence (CVEs, advisories, alerts)
     - `noise`: General news, opinion pieces, marketing
   - Use criteria:
     - Signal: Contains CVEs, CVSS scores, IOCs, patches
     - Noise: No specific vulnerabilities, promotional content
   - Calculate ratio = signal_items / total_items
   - Target: >0.6 for high-quality feeds

4. **Uniqueness Analysis**:
   - Compare feed items to threats from other feeds
   - Calculate unique content contribution
   - Identify duplicate/overlapping content
   - Assess information freshness (first to report)

### Stage 4: Value Assessment

1. **Contribution Scoring**:
   - Count threats contributed by this feed
   - Count unique threats (not duplicated elsewhere)
   - Count critical/high severity threats
   - Weight by crown jewel relevance
   - Weight by industry relevance

2. **Value Rating**:
   - `high`: Unique critical threats, high crown jewel relevance
   - `medium`: Some unique content, moderate relevance
   - `low`: Mostly duplicates, low relevance

### Stage 5: Redundancy Detection

1. **Overlap Analysis**:
   - Compare threats from this feed to other feeds
   - Calculate overlap percentage with each other feed
   - Identify feeds with >70% overlap (highly redundant)
   - Determine which feed provides better quality/speed

2. **Redundancy Recommendation**:
   - `keep`: Unique valuable content, no significant overlap
   - `review`: Moderate overlap, assess if both needed
   - `consider_removing`: >70% overlap with higher-quality feed

### Stage 6: Quality Score Calculation

Calculate composite quality score (0-100):

```
Quality Score = (
  Performance_Score * 0.25 +
  Content_Score * 0.35 +
  Reliability_Score * 0.20 +
  Value_Score * 0.20
)

Performance_Score (0-100):
  - Response time <2s: 100 points
  - Response time 2-5s: 80 points
  - Response time 5-10s: 60 points
  - Response time >10s: 40 points
  - Update frequency: daily(100), weekly(80), biweekly(60), monthly(40)

Content_Score (0-100):
  - Relevance score * 40
  - CVE extraction rate * 30
  - Signal-to-noise ratio * 30

Reliability_Score (0-100):
  - Uptime percentage (0-100)
  - Penalty for recent failures: -10 per failure in last 7 days

Value_Score (0-100):
  - Unique content ratio * 50
  - Actionable items / total items * 50

Grade Assignment:
  A: 90-100 (excellent)
  B: 75-89 (good)
  C: 60-74 (acceptable)
  D: 40-59 (poor)
  F: 0-39 (failing)
```

### Stage 7: Optimization Recommendations

Generate specific recommendations:

1. **Remove Recommendations**:
   - Quality score < 40 (F grade)
   - Uptime < 90% over 30 days
   - Overlap >80% with higher-quality feed
   - No unique content in last 30 days
   - Consistently slow (p95 > 15s)

2. **Add Recommendations**:
   - Coverage gaps identified (e.g., missing vendor feeds)
   - Industry-specific feeds not present
   - High-value feeds from templates

3. **Upgrade Recommendations**:
   - Free feed has premium alternative
   - RSS feed has API alternative
   - Slow feed has mirror/CDN option

4. **Configuration Recommendations**:
   - Adjust polling frequency based on update pattern
   - Change priority based on value assessment
   - Update category based on content analysis

### Stage 8: Benchmarking

Compare portfolio to industry standards:

**Industry Averages** (based on feed type):
- Government CERTs: Response 1-3s, Updates daily, Relevance 0.95
- Vendor advisories: Response 2-5s, Updates weekly, Relevance 0.90
- Security research: Response 3-8s, Updates 2-3x/week, Relevance 0.80
- News/blogs: Response 1-2s, Updates daily, Relevance 0.60

**Portfolio Health Grading**:
- `excellent`: >80% of feeds grade A/B, avg quality >85
- `good`: >60% of feeds grade A/B/C, avg quality >75
- `acceptable`: >50% of feeds grade C or better, avg quality >60
- `poor`: <50% of feeds grade C or better, or avg quality <60

## Example Usage

### Analyze All Feeds (30-day window)
```
Input:
{
  "operation": "analyze",
  "scope": {"feed_ids": "all", "time_window": "30d"},
  "options": {"check_feed_health": true}
}

Output:
📊 FEED QUALITY ANALYSIS (30-day window)

PORTFOLIO SUMMARY:
✅ Healthy: 12 feeds (80%)
⚠️  Warning: 2 feeds (13%)
❌ Failing: 1 feed (7%)
Average Quality Score: 78/100 (Good)

TOP PERFORMERS (Grade A):
1. CISA Advisories - Score: 98/100
   Response: 1.2s | Uptime: 99.9% | Updates: Daily
   Unique threats: 45 | Critical alerts: 8

2. Microsoft MSRC - Score: 94/100
   Response: 2.1s | Uptime: 99.5% | Updates: 3x/week
   Unique threats: 38 | Critical alerts: 12

NEEDS ATTENTION (Grade D/F):
❌ SlowSecurityBlog - Score: 38/100 (F)
   Issues:
   - Response time: 18.5s (p95: 25s)
   - Update frequency: Only 2 updates in 30 days
   - Overlap: 85% with faster feeds
   - Recommendation: REMOVE - content available elsewhere

⚠️  UnreliableFeed - Score: 55/100 (D)
   Issues:
   - Uptime: 87% (13 outages)
   - Content relevance: Low (0.45)
   - Recommendation: REPLACE with AlternativeFeed

OPTIMIZATION OPPORTUNITIES:
🎯 Remove 1 feed → Save ~15s per refresh cycle
🎯 Add "Rapid7 Blog" → Fill vulnerability research gap
🎯 Reduce "NewsAggregate" polling → Not updating daily
```

### Benchmark Against Industry
```
Input:
{
  "operation": "benchmark",
  "scope": {"categories": ["government", "vendor"]}
}

Output:
📈 PORTFOLIO BENCHMARK REPORT

YOUR PORTFOLIO vs. INDUSTRY AVERAGES:

Government Feeds (5 feeds):
  Quality Score: 92 vs. Industry: 88 ✅ Above average
  Response Time: 1.8s vs. Industry: 2.5s ✅ Faster
  Update Freq: 18h vs. Industry: 24h ✅ More frequent

Vendor Feeds (7 feeds):
  Quality Score: 79 vs. Industry: 82 ⚠️ Slightly below
  Response Time: 4.2s vs. Industry: 3.8s ⚠️ Slower
  Update Freq: 72h vs. Industry: 72h ✅ On par

OVERALL PORTFOLIO:
Grade: B+ (Above Industry Average)

RECOMMENDATIONS:
1. Optimize 2 slow vendor feeds (see details)
2. Your government feed coverage is excellent
3. Consider adding vendor API access for faster updates
```

### Quick Health Check
```
Input:
{
  "operation": "monitor",
  "scope": {"feed_ids": "all", "time_window": "24h"}
}

Output:
🏥 FEED HEALTH CHECK (Last 24 hours)

✅ ALL SYSTEMS OPERATIONAL (15/15 feeds)

Recent Activity:
- Total items collected: 127
- New CVEs identified: 23
- Critical alerts: 4
- Average response time: 2.8s

No issues detected.
Next scheduled check: 4 hours
```

## Error Handling

### Feed Access Errors
- **HTTP 404**: Mark as failing, suggest URL update
- **HTTP 403/401**: Authentication issue, flag for review
- **Timeout**: Record slow response, impact performance score
- **DNS failure**: Network issue, retry with backoff
- **SSL error**: Certificate problem, flag security concern

### Data Quality Issues
- **Malformed feed**: Parse errors reduce content score
- **No items**: Stale feed warning
- **Invalid dates**: Note parsing issues
- **Missing metadata**: Reduce completeness score

## Integration Points

### Files Used
- **Reads from**:
  - `config/threat-sources.json` (feed configuration)
  - `data/feed-quality-metrics.json` (historical metrics)
  - `data/threats-cache.json` (feed contributions)

- **Writes to**:
  - `data/feed-quality-metrics.json` (updated metrics)
  - `data/output/feed-reports/` (detailed reports)

### Command Integration
- Used by: `/feed-quality` command
- Used by: `agents/feed-quality-monitor.md`
- Used by: `agents/feed-manager.md` (optimization)
- Integrates with: `opml-processor`, `csv-handler` (feed management)

## Performance Characteristics
- **Quick check** (no health test): 1-2 seconds for 15 feeds
- **Full analysis** (with health test): 10-15 seconds for 15 feeds
- **30-day analysis**: 5-8 seconds (cached metrics)
- **Parallel feed testing**: Up to 10 concurrent health checks
- **Memory usage**: <5MB for typical portfolio

## Monitoring Intervals
- **Continuous**: Track all feed requests in real-time
- **Hourly**: Quick health checks
- **Daily**: Performance metrics update
- **Weekly**: Full quality analysis with recommendations
- **Monthly**: Benchmark comparison and portfolio review
