# verification-status

Display current verification configuration and performance statistics.

## Usage
/verification-status

## Description
Shows comprehensive verification system status including method configuration, API usage, cache performance, costs, and recent failures.

## Output Sections

### Current Configuration
- Active verification method
- Enabled providers and weights
- Confidence thresholds
- Fallback behavior

### Performance Metrics
- Total verifications performed
- Success/failure rates by method
- Average response times
- Cache hit rates

### Cost Tracking (if using Jina.ai)
- Current month usage
- Daily/monthly trends
- Budget utilization
- Projected monthly cost

### Recent Activity
- Last 5 verification attempts
- Recent failures and errors
- API availability status

## Example Output

```
User: /verification-status

NOMAD: 📊 VERIFICATION SYSTEM STATUS

═══════════════════════════════════════════
CURRENT CONFIGURATION
═══════════════════════════════════════════

Method: Hybrid (Structured 60% + Jina 40%)
Status: ✅ Operational

Providers:
• NVD API: ✅ Online (100% uptime)
• CISA KEV: ✅ Updated 2 hours ago
• EPSS: ✅ Online (99.8% uptime)
• Jina.ai: ✅ API key valid

Thresholds:
• Min Display: 50%
• Critical: 70%
• Actionable: 60%

═══════════════════════════════════════════
PERFORMANCE METRICS (Last 30 Days)
═══════════════════════════════════════════

Total Verifications: 1,247
• Successful: 1,201 (96.3%)
• Failed: 46 (3.7%)

By Method:
┌─────────────┬──────┬────────┬──────────┐
│ Method      │ Used │ Success│ Avg Time │
├─────────────┼──────┼────────┼──────────┤
│ Structured  │ 892  │ 99.2%  │ 2.1s     │
│ Jina.ai     │ 231  │ 94.8%  │ 4.3s     │
│ Hybrid      │ 124  │ 97.6%  │ 5.2s     │
└─────────────┴──────┴────────┴──────────┘

Cache Performance:
• Hit Rate: 82.4%
• Cache Size: 42.3 MB / 100 MB
• Avg Age: 14.2 hours

═══════════════════════════════════════════
COST TRACKING (January 2025)
═══════════════════════════════════════════

Jina.ai Usage:
• Requests: 231
• Cost to Date: $0.23
• Daily Average: $0.01
• Projected Monthly: $0.31

Budget Status: ✅ Within limits
• Monthly Budget: $10.00
• Alert Threshold: $8.00 (23% used)

═══════════════════════════════════════════
RECENT VERIFICATIONS
═══════════════════════════════════════════

1. CVE-2025-12345 ✅ 96% (2 min ago)
   Method: Hybrid | Time: 4.8s

2. CVE-2025-11111 ✅ 88% (15 min ago)
   Method: Structured | Time: 1.9s

3. CVE-2024-99999 ❌ Failed (1 hour ago)
   Error: CVE not found in NVD

4. CVE-2025-22222 ✅ 92% (2 hours ago)
   Method: Jina | Time: 3.7s | Cost: $0.001

5. CVE-2025-33333 ⚠️ 67% (3 hours ago)
   Method: Structured | Time: 2.3s
   Note: Low confidence - vendor advisory only

═══════════════════════════════════════════
API HEALTH STATUS
═══════════════════════════════════════════

• NVD: 🟢 Healthy (50ms latency)
• CISA: 🟢 Healthy (120ms latency)
• EPSS: 🟢 Healthy (80ms latency)
• Jina: 🟢 Healthy (230ms latency)

Last Error: None in past 24 hours

═══════════════════════════════════════════
RECOMMENDATIONS
═══════════════════════════════════════════

✅ System performing optimally
• Cache hit rate above target (80%)
• All APIs responding normally
• Well within budget limits

💡 Tips:
• Consider increasing cache TTL for better performance
• Current settings are well-balanced
```

## Status Indicators

### Method Status
- ✅ Operational - All systems working
- ⚠️ Degraded - Some providers unavailable
- ❌ Failed - Critical issues detected

### API Health
- 🟢 Healthy - Normal operation
- 🟡 Slow - Higher than normal latency
- 🔴 Down - Not responding

### Budget Status
- ✅ Within limits - Normal spending
- ⚠️ Approaching limit - >80% of budget
- ❌ Limit exceeded - Jina disabled

## Related Commands
- `/setup-verification` - Configure verification settings
- `/refresh` - Update threat intelligence with verification
- `/status` - Overall NOMAD system status

## Notes
- Metrics reset monthly
- Cache statistics are cumulative
- Failed verifications fall back gracefully
- Cost tracking only applies to Jina.ai usage