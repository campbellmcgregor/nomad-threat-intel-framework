# setup-verification

Configure threat intelligence verification settings for validating threats against authoritative sources.

## Usage
/setup-verification

## Description
Interactive wizard to configure NOMAD's verification system, including method selection, API keys, confidence thresholds, and cost limits.

## Interactive Flow

The command guides you through:

1. **Choose Verification Method**
   - Structured APIs Only (free, official sources like NVD/CISA)
   - Jina.ai Grounding Only (paid, comprehensive web verification)
   - Hybrid Approach (recommended - combines both methods)
   - Disabled (no verification for testing/emergency)

2. **Configure Jina.ai (if selected)**
   - Enter API key
   - Set monthly budget limit
   - Configure confidence threshold

3. **Set Confidence Thresholds**
   - Minimum display threshold (default: 50%)
   - Critical threat threshold (default: 70%)
   - Actionable threat threshold (default: 60%)

4. **Configure Cost Limits** (if using Jina.ai)
   - Monthly budget cap
   - Alert threshold
   - Behavior when limit reached

5. **Test Verification**
   - Run sample verification
   - Display results and confidence scores

## Examples

### Initial Setup
```
User: /setup-verification
NOMAD: 🔐 VERIFICATION CONFIGURATION WIZARD

I'll help you set up threat verification to ensure all intelligence is validated against authoritative sources.

Choose your verification method:

1️⃣ **Structured APIs Only** (Free)
   - Uses NVD, CISA KEV, vendor APIs
   - No cost, official sources only
   - Good for budget-conscious teams

2️⃣ **Jina.ai Grounding** (Paid)
   - Real-time web verification
   - $0.001 per request (~$10/month typical)
   - Most comprehensive coverage

3️⃣ **Hybrid Approach** (Recommended)
   - Combines both methods
   - Weighted scoring for best accuracy
   - Balances cost and coverage

4️⃣ **Disabled**
   - No verification (testing only)
   - All threats marked unverified

Which method would you prefer? (1-4):
```

### Jina.ai Configuration
```
User: 3
NOMAD: Great choice! The hybrid approach gives you the best of both worlds.

To use Jina.ai grounding, I'll need your API key.
Get one at: https://jina.ai/api

Enter your Jina.ai API key (or press Enter to skip):
```

### Confidence Thresholds
```
NOMAD: Now let's set your confidence thresholds.

These determine which threats to display based on verification confidence:

• **Minimum Display** (current: 50%)
  Threats below this won't be shown

• **Critical Threshold** (current: 70%)
  Minimum confidence for critical alerts

• **Actionable Threshold** (current: 60%)
  Minimum confidence for remediation recommendations

Keep defaults? (Y/n):
```

### Cost Management
```
NOMAD: Let's configure cost controls for Jina.ai:

Monthly budget (USD): $10
Alert when spending reaches: $8
When limit reached: [Fall back to structured APIs only]

Is this correct? (Y/n):
```

### Test Verification
```
NOMAD: 🧪 Testing verification with a known threat...

Testing CVE-2024-3400 (Palo Alto Networks Critical):
✅ NVD API: Success (CVSS 10.0 confirmed)
✅ CISA KEV: Listed (active exploitation)
✅ Jina.ai: 5 sources found
   - Palo Alto advisory
   - BleepingComputer article
   - CISA alert

Verification Result:
• Confidence: 98%
• Method: Hybrid
• Response time: 3.2 seconds
• Cost: $0.001

✅ Verification system configured successfully!
```

## Configuration Updates

Updates the following in `config/user-preferences.json`:
- `verification_settings.method`
- `verification_settings.providers`
- `verification_settings.confidence_thresholds`
- `verification_settings.cost_tracking`

## Related Commands
- `/verification-status` - Check current verification stats
- `/status` - View overall NOMAD configuration
- `/configure` - Modify other NOMAD settings

## Notes
- Structured API verification is always free
- Jina.ai typically costs $5-15/month for most organizations
- Verification adds 3-6 seconds to threat processing
- Cache hit rate improves performance over time
- You can change methods anytime without losing data