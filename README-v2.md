# NOMAD v2.0 - 2-Minute Setup Guide

🛡️ **Transform threat intelligence from overwhelming to actionable in under 2 minutes.**

## What is NOMAD v2.0?

NOMAD (Notable Object Monitoring And Analysis Director) v2.0 is a Claude Code-native threat intelligence assistant. No Python setup, no complex configurations - just clone and ask questions like "Show me latest threats" to get personalized, actionable intelligence.

## Quick Start (2 Minutes)

### Step 1: Clone & Launch (30 seconds)
```bash
git clone <your-repo-url>
cd nomad-threat-intel-framework
claude code
```

### Step 2: First Query (30 seconds)
When Claude Code launches, simply ask:
```
Show me latest threats
```

NOMAD will automatically:
- ✅ Fetch threat intelligence from 10 premium sources
- ✅ Process and prioritize threats for your organization
- ✅ Generate personalized briefings based on your profile

### Step 3: Customize Your Profile (60 seconds)
Update your organization details in `config/user-preferences.json`:

```json
{
  "organization": {
    "name": "Your Company",
    "industry": "Your Industry",
    "business_sectors": ["Technology", "Finance", "Healthcare"]
  },
  "crown_jewels": [
    "Customer Database",
    "Payment Systems",
    "Email Infrastructure",
    "Authentication Systems"
  ]
}
```

## What You Get Immediately

✨ **Natural Language Interface**
- "Show me latest threats"
- "What's critical today?"
- "Threats to my customer database"
- "Tell me about CVE-2024-12345"

🎯 **Personalized Intelligence**
- Filtered by your industry and crown jewels
- Prioritized using CVSS, EPSS, and KEV data
- Executive and technical briefings
- Actionable remediation guidance

🔄 **Auto-Updating Feeds**
- CISA cybersecurity advisories
- Vendor security bulletins (Microsoft, Cisco, etc.)
- Government CERT feeds (US, UK, EU, Canada, Australia)
- Automatic enrichment with vulnerability databases

## Example Interactions

### Basic Threat Briefing
**You:** `Show me latest threats`

**NOMAD:**
```
🔴 CRITICAL THREATS: 2 requiring immediate attention
🟠 HIGH PRIORITY: 5 threats needing action within 48 hours
🟡 MEDIUM PRIORITY: 3 threats for planned remediation

KEY THREATS TO YOUR CROWN JEWELS:
• CVE-2024-12345: Authentication bypass affecting your Customer Database
• CVE-2024-54321: RCE in cloud services affecting Payment Systems

IMMEDIATE ACTIONS:
1. Emergency patch authentication servers (4-hour window)
2. Review cloud access controls
3. Monitor for unusual authentication patterns
```

### Asset-Specific Analysis
**You:** `What threatens our customer database?`

**NOMAD:**
```
🛡️ CUSTOMER DATABASE THREAT ANALYSIS

DIRECT THREATS (3 found):
• SQL injection vulnerabilities (High priority)
• Authentication bypass risks (Critical)
• Lateral movement vectors (Medium priority)

PROTECTIVE MEASURES:
✅ Recommended: Enhanced database monitoring
✅ Recommended: Network segmentation review
✅ Recommended: Access privilege audit
```

## Advanced Usage

### Query Types You Can Ask
- **Current Intelligence**: "Latest threats", "What's critical?"
- **Asset-Specific**: "Threats to [crown jewel]", "Email system vulnerabilities"
- **CVE Lookup**: "Tell me about CVE-2024-12345"
- **Configuration**: "Update my preferences", "Add new crown jewel"
- **Data Refresh**: "Update threat feeds", "Refresh intelligence"

### Configuration Options
Customize threat filtering in `config/user-preferences.json`:
- **Industries**: Focus on sector-specific threats
- **Crown Jewels**: Your most critical business systems
- **Alert Thresholds**: CVSS/EPSS scoring preferences
- **Response Style**: Technical vs executive briefings

### Data Sources
NOMAD v2.0 monitors these premium sources:
- **Government**: CISA, NCSC UK, CERT-EU, Canadian CCCS, Australian ACSC
- **Vendors**: Microsoft MSRC, Cisco Security, Oracle Critical Patch Updates
- **Standards**: NVD (CVSS scores), FIRST.org (EPSS), CISA KEV catalog

## Architecture Benefits

### No Setup Complexity
- ❌ No Python virtual environments
- ❌ No API key management
- ❌ No complex agent pipelines
- ✅ Pure Claude Code integration

### Intelligent Processing
- 🧠 Admiralty source reliability ratings
- 📊 Multi-factor risk scoring (CVSS + EPSS + KEV)
- 🎯 Crown jewel correlation analysis
- 🔄 Automatic threat prioritization

### Learning System
- 📈 Learns from your query patterns
- 🎯 Improves personalization over time
- 💡 Suggests relevant follow-up questions
- 📋 Tracks interaction preferences

## Troubleshooting

**Q: No threat data showing?**
A: Say "Refresh feeds" to collect latest intelligence

**Q: Want more technical details?**
A: Ask "Give me technical details for [threat]" for SOC-level information

**Q: Need executive summary?**
A: Request "Executive briefing on this week's threats" for leadership

**Q: How to add new crown jewel?**
A: Say "Add [system name] to my crown jewels" and NOMAD will guide you

## What Makes v2.0 Different

| Traditional TI Tools | NOMAD v2.0 |
|---------------------|------------|
| Complex setup | 2-minute start |
| Technical interfaces | Natural conversation |
| Generic reports | Personalized intelligence |
| Manual correlation | Automated crown jewel analysis |
| Static configurations | Learning preferences |

## Next Steps

1. **Try basic queries** to get familiar with NOMAD's capabilities
2. **Customize your profile** for more relevant intelligence
3. **Set up regular briefings** by asking for weekly summaries
4. **Explore advanced features** like supply chain analysis

---

🚀 **You're ready!** NOMAD v2.0 transforms complex threat intelligence into conversational, actionable insights that help you make informed security decisions quickly and confidently.

*Questions? Just ask NOMAD: "How do I configure preferences?" or "What can you help me with?"*