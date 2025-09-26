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
- "Add healthcare feeds"
- "Import my existing feeds"

🎯 **Personalized Intelligence**
- Filtered by your industry and crown jewels
- Prioritized using CVSS, EPSS, and KEV data
- Executive and technical briefings
- Actionable remediation guidance

🔄 **Premium Feed Collection (30+ Sources)**
- **Government CERTs**: CISA, NCSC UK, CERT-EU, BSI Germany, ANSSI France
- **Vendor Advisories**: Microsoft, Cisco, Oracle, VMware, Adobe, AWS
- **Security Research**: SANS ISC, Qualys, Rapid7, CrowdStrike, FireEye
- **Threat Intelligence**: Unit 42, Talos, AlienVault OTX
- **Industry Templates**: Healthcare, Financial, Manufacturing, Technology

🏭 **Industry-Specific Packages**
- **Healthcare**: HHS, FDA device security, ICS-CERT medical
- **Financial**: FS-ISAC, FinCEN, PCI standards, SWIFT security
- **Manufacturing**: ICS-CERT, Schneider Electric, Siemens, Rockwell
- **Technology**: GitHub Security, npm/PyPI advisories, cloud security

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

### Slash Commands Available
NOMAD v2.0 now includes 19 powerful slash commands for instant access:

**🎯 Threat Intelligence:**
- `/threats` - Latest personalized threat briefing
- `/critical` - Critical and KEV-listed threats only
- `/crown-jewel [system]` - Threats to specific crown jewel systems
- `/cve [CVE-ID]` - Detailed analysis of specific vulnerability
- `/trending` - Trending threats and attack vectors

**📡 Feed Management:**
- `/add-feeds [industry]` - Add industry-specific feed packages
- `/feed-quality` - Feed performance dashboard and recommendations
- `/import-feeds [file]` - Import feeds from OPML/JSON/CSV files

**⚙️ Configuration:**
- `/setup` - Interactive setup wizard for first-time config
- `/configure [setting]` - Quick configuration updates
- `/add-crown-jewel [name]` - Add critical system to your profile
- `/update-profile [field]` - Update organization profile information

**🔧 System & Utility:**
- `/refresh` - Force refresh of threat intelligence data
- `/status` - Display system health and configuration
- `/export [format]` - Export data and configuration
- `/help [command]` - Show command reference and detailed help

**📊 Reporting:**
- `/executive-brief` - Generate executive summary report
- `/technical-alert` - Create technical security alert
- `/weekly-summary` - Weekly threat landscape summary

### Natural Language Interface
You can also use natural conversation:
- **Current Intelligence**: "Latest threats", "What's critical?"
- **Asset-Specific**: "Threats to [crown jewel]", "Email system vulnerabilities"
- **CVE Lookup**: "Tell me about CVE-2024-12345"
- **Configuration**: "Update my preferences", "Add new crown jewel"
- **Data Refresh**: "Update threat feeds", "Refresh intelligence"
- **Feed Management**: "Add healthcare feeds", "Import my OPML", "Show feed quality"

### Configuration Options
Customize threat filtering in `config/user-preferences.json`:
- **Industries**: Focus on sector-specific threats
- **Crown Jewels**: Your most critical business systems
- **Alert Thresholds**: CVSS/EPSS scoring preferences
- **Response Style**: Technical vs executive briefings

### Feed Management Features
NOMAD v2.0 includes advanced feed management capabilities:
- **30+ Premium Sources**: Government CERTs, vendor advisories, security research
- **Industry Templates**: Pre-configured packages for Healthcare, Financial, Manufacturing, Technology
- **Import/Export**: OPML, JSON, CSV support for existing feed collections
- **Quality Monitoring**: Automatic feed health checks and optimization recommendations
- **Smart Recommendations**: AI-suggested feeds based on your crown jewels and industry

### Data Sources
NOMAD v2.0 monitors these premium sources:
- **Government CERTs**: CISA, NCSC UK, CERT-EU, BSI Germany, ANSSI France, JPCERT/CC
- **Vendor Advisories**: Microsoft, Cisco, Oracle, VMware, Adobe, AWS, Google, Red Hat
- **Security Research**: SANS ISC, Qualys, Rapid7, CrowdStrike, FireEye, Kaspersky
- **Threat Intelligence**: Unit 42, Talos Intelligence, AlienVault OTX, ThreatConnect
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

**Q: How to add industry-specific feeds?**
A: Say "Add healthcare feeds" or "Configure for financial services"

**Q: Can I import my existing feeds?**
A: Yes! Say "Import my OPML" or "Import feeds from JSON/CSV"

**Q: How to check feed quality?**
A: Ask "Show feed quality" or "Optimize my feeds" for performance analysis

## What Makes v2.0 Different

| Traditional TI Tools | NOMAD v2.0 |
|---------------------|------------|
| Complex setup | 2-minute start |
| Technical interfaces | Natural conversation |
| Generic reports | Personalized intelligence |
| Manual correlation | Automated crown jewel analysis |
| Static configurations | Learning preferences |
| Limited feed sources | 30+ premium sources |
| Manual feed management | Intelligent feed optimization |
| One-size-fits-all | Industry-specific templates |

## Next Steps

1. **Try basic queries** to get familiar with NOMAD's capabilities
2. **Customize your profile** for more relevant intelligence
3. **Add industry-specific feeds** with "Add [industry] feeds"
4. **Import existing feeds** if you have OPML/feed collections
5. **Set up regular briefings** by asking for weekly summaries
6. **Monitor feed quality** with "Show feed quality" for optimization

---

🚀 **You're ready!** NOMAD v2.0 transforms complex threat intelligence into conversational, actionable insights that help you make informed security decisions quickly and confidently.

## Enhanced Features Summary

✅ **30+ Premium Threat Feeds** - Government CERTs, vendor advisories, security research
✅ **Industry-Specific Templates** - Pre-configured for Healthcare, Financial, Manufacturing, Technology
✅ **Smart Feed Management** - Import OPML/JSON/CSV, quality monitoring, optimization
✅ **Natural Language Interface** - "Add healthcare feeds", "Show feed quality", "Import my OPML"
✅ **Intelligent Recommendations** - AI-suggested feeds based on your crown jewels and industry
✅ **Quality Assurance** - Automatic feed validation and performance optimization

*Questions? Just ask NOMAD: "Setup wizard", "Add industry feeds", or "Import my existing feeds"*