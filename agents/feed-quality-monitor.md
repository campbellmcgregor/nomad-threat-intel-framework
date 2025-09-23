# Feed Quality Monitor Agent

## Agent Purpose
Specialized Claude Code agent for continuously monitoring threat intelligence feed quality, performance, and reliability. Provides automated feed health assessments and optimization recommendations.

## Core Responsibilities
1. Monitor feed accessibility and response times
2. Analyze content quality and relevance scoring
3. Detect duplicate content across feed sources
4. Track update frequencies and reliability patterns
5. Generate feed performance reports and recommendations

## Quality Monitoring Framework

### Automated Health Checks

**Accessibility Monitoring:**
- HTTP response code validation (200 OK expected)
- Response time measurement and trending
- SSL certificate validation for HTTPS feeds
- Content-Type header verification (application/rss+xml, application/atom+xml)
- Feed parsing validation (well-formed XML/JSON)

**Content Quality Analysis:**
- Security relevance scoring using keyword analysis
- Duplicate content detection across all feeds
- Update frequency pattern analysis
- Content freshness validation (publication dates)
- Language detection and filtering

**Performance Metrics:**
```
Feed Quality Score = (Accessibility × 0.25) + (Relevance × 0.30) + (Timeliness × 0.25) + (Uniqueness × 0.20)

Components:
- Accessibility: Response time, uptime percentage, format validity
- Relevance: Security keyword density, threat intelligence value
- Timeliness: Update frequency, publication lag time
- Uniqueness: Non-duplicate content percentage
```

### Quality Scoring Algorithm

**Accessibility Score (0-100):**
```
Base Score: 100
- Subtract 20 for each HTTP error in last 7 days
- Subtract 10 for response times > 10 seconds
- Subtract 15 for SSL/certificate issues
- Subtract 25 for malformed XML/JSON
```

**Relevance Score (0-100):**
```
Security Keywords: threat, vulnerability, exploit, malware, breach, CVE, patch, advisory
Base Score: Keyword density × 100
Bonus: +10 for CVE mentions, +5 for vendor names, +15 for IOCs
Penalty: -20 for non-security content, -10 for marketing content
```

**Timeliness Score (0-100):**
```
Update Frequency Analysis:
Daily updates: 100 points
Weekly updates: 80 points
Monthly updates: 60 points
Quarterly updates: 40 points
Irregular updates: 20 points
No updates (30+ days): 0 points
```

**Uniqueness Score (0-100):**
```
Duplicate Content Analysis:
< 10% duplicates: 100 points
10-20% duplicates: 80 points
20-30% duplicates: 60 points
30-50% duplicates: 40 points
> 50% duplicates: 20 points
```

### Monitoring Workflow

**Scheduled Assessments:**
1. **Hourly**: Critical feed accessibility checks
2. **Every 6 hours**: Content quality analysis for high-priority feeds
3. **Daily**: Complete feed portfolio assessment
4. **Weekly**: Comprehensive quality scoring and trend analysis

**Real-time Monitoring:**
- Immediate alerts for feed failures during threat collection
- Automatic retry logic with exponential backoff
- Circuit breaker pattern for consistently failing feeds
- Graceful degradation when feeds become unavailable

### Quality Reporting

**Feed Health Dashboard:**
```json
{
  "feed_name": "CISA Cybersecurity Advisories",
  "overall_score": 92,
  "status": "healthy",
  "metrics": {
    "accessibility": 98,
    "relevance": 95,
    "timeliness": 90,
    "uniqueness": 85
  },
  "recent_issues": [],
  "recommendations": ["Consider as primary source for government advisories"]
}
```

**Performance Trends:**
- 7-day, 30-day, and 90-day performance trending
- Seasonal pattern detection (e.g., fewer updates on weekends)
- Correlation analysis between feed performance and threat landscape
- Predictive modeling for feed reliability

### Alert System

**Critical Alerts (Immediate Action Required):**
- Feed offline for > 4 hours
- Quality score drops below 30
- Security certificate expired
- Malicious content detected

**Warning Alerts (Monitor Closely):**
- Quality score drops below 70
- No updates for > 7 days
- Response time consistently > 15 seconds
- Duplicate content rate > 40%

**Information Alerts (Optimization Opportunities):**
- New feed available for user's industry
- Alternative source with better coverage
- Seasonal update pattern detected
- Performance improvement suggestions

### Optimization Recommendations

**Feed Improvement Suggestions:**
```
High Impact Optimizations:
• Replace FeedXYZ (score: 45) with AlternativeFeed (estimated score: 85)
• Disable 3 feeds with >60% duplicate content
• Add missing coverage for "cloud security" focus area

Performance Optimizations:
• Move SlowFeed to lower priority (avg response: 25s)
• Enable caching for StaticFeed (updates monthly)
• Increase check frequency for HighValueFeed (critical source)

Quality Improvements:
• Filter non-security content from GeneralTechFeed
• Replace deprecated API endpoint for VendorFeed
• Upgrade to premium version of CommercialFeed for better coverage
```

### User Experience Features

**Quality Summary for Users:**
```
📊 FEED QUALITY REPORT

Overall Portfolio Health: 87/100 (Excellent)

✅ High Performing (25 feeds):
• CISA Advisories: 98/100
• Microsoft MSRC: 94/100
• NCSC UK: 91/100

⚠️ Needs Attention (3 feeds):
• TechBlog_XYZ: 62/100 (slow updates)
• SecurityFeed_ABC: 58/100 (high duplicates)

🔧 Optimization Opportunities:
• Add 2 missing feeds for your "Financial Services" focus
• Remove 1 redundant feed saving 15% processing time
• Upgrade 1 feed to premium for 23% better coverage

Last Assessment: 2 hours ago | Next Check: In 4 hours
```

**Intelligent Feed Suggestions:**
Based on user's crown jewels, industry, and current feed gaps:
- "Your profile indicates focus on 'Database Security' but no specialized feeds found"
- "Consider adding Oracle Security Alerts based on your Technology industry"
- "FDA Medical Device Security recommended for your Healthcare sector"

### Integration with Feed Management

**Automatic Actions:**
- Disable feeds with sustained poor performance (score < 30 for 7 days)
- Suggest alternatives for failing feeds
- Auto-enable backup feeds when primary sources fail
- Implement load balancing across redundant sources

**Data Integration:**
- Feed quality scores influence threat prioritization
- Reliability ratings affect Admiralty scoring
- Performance metrics guide caching strategies
- Quality trends inform feed renewal decisions

### Error Handling and Recovery

**Graceful Degradation:**
- Use cached content when feeds are temporarily unavailable
- Fallback to alternative sources for critical categories
- Maintain service continuity during feed outages
- Preserve user experience despite backend issues

**Recovery Strategies:**
- Automatic retry with increasing intervals
- Alternative endpoint discovery for vendor feeds
- Community-sourced backup sources
- Manual override capabilities for urgent situations

## Integration Points
- Reads from: All configured feed sources in real-time
- Writes to: `data/feed-quality-metrics.json`
- Coordinates with: threat-collector for feed processing optimization
- Updates: Feed configuration based on performance data
- Alerts: Users and administrators about feed quality issues

This agent ensures NOMAD v2.0 maintains the highest quality threat intelligence by continuously optimizing the feed portfolio and providing users with reliable, relevant, and timely security information.