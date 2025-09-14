# 🚀 NOMAD Quick Start Guide

**Get threat intelligence in 5 minutes.** This guide gets you running fast.

## What is NOMAD?

NOMAD collects security threats from 40+ sources (CISA, Microsoft, Cisco, etc.) and tells you what matters for your organization. It's like having a security analyst reading all advisories 24/7.

---

## ⚡ 5-Minute Setup

### Step 1: Clone and Enter Directory
```bash
git clone https://github.com/yourusername/nomad-threat-intel-framework.git
cd nomad-threat-intel-framework
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install pyyaml feedparser python-dateutil requests
```

### Step 4: Test It Works
```bash
python nomad.py list-feeds --priority high
```

You should see a list of security feeds. **You're ready!**

---

## 🎯 Your First Threat Hunt (2 minutes)

### Find Today's Critical Threats
```bash
# Get all high-priority threats from the last 24 hours
python nomad.py rss --since $(date -d "yesterday" '+%Y-%m-%d') --priority high
```

**What this does:**
- Checks CISA, Microsoft, Cisco, and other critical sources
- Finds CVEs and security advisories
- Saves results to `data/output/intel_rss_*.json`

### See What Was Found
```bash
# Look at the output
ls -la data/output/
cat data/output/intel_rss_*.json | grep -o "CVE-[0-9]*-[0-9]*" | sort -u
```

**Real example output:**
```
CVE-2024-12345 - Microsoft Exchange RCE
CVE-2024-67890 - VMware Critical Authentication Bypass
CVE-2024-11111 - Cisco ASA Vulnerability
```

---

## 📅 Daily Security Workflow (5 minutes/day)

### Morning Security Check
This is what most security teams should run daily:

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Collect last 24 hours of threats
python nomad.py rss --since $(date -d "yesterday" '+%Y-%m-%d') --priority high

# 3. See what was found
echo "=== TODAY'S THREATS ==="
cat data/output/intel_rss_*.json | python -m json.tool | grep '"title"' | head -10
```

### Check Specific Vendors
```bash
# Just Microsoft advisories
python nomad.py rss --source-type vendor --since $(date -d "yesterday" '+%Y-%m-%d') | grep -i microsoft

# Just CISA/CERT advisories
python nomad.py rss --source-type cert --since $(date -d "yesterday" '+%Y-%m-%d')
```

### Weekly Report
```bash
# Get everything from the past week
python nomad.py rss --since $(date -d "7 days ago" '+%Y-%m-%d')
```

---

## 🤖 Using with Claude Code (Advanced)

If you're using Claude Code, it can orchestrate everything for you:

### Natural Language Commands
Just tell Claude Code:
- "Check for critical threats from today"
- "Find any Microsoft vulnerabilities"
- "Run the morning security check"
- "Generate a weekly threat report"

### Using Agent Workflows
```bash
# List available automated workflows
python claude_workflow.py list

# Run morning security check workflow
python claude_workflow.py run morning_check
```

### Prepare for Claude Code Agents
```bash
# This shows Claude Code exactly what to run
python run_agent.py rss --since $(date -d "yesterday" '+%Y-%m-%d')
```

---

## 📋 Quick Command Reference

### Essential Commands
```bash
# List all feeds
python nomad.py list-feeds

# List high-priority feeds only
python nomad.py list-feeds --priority high

# Collect from all feeds (last 7 days default)
python nomad.py rss

# Collect high-priority only
python nomad.py rss --priority high

# Collect from specific date
python nomad.py rss --since 2024-01-13

# Test a specific feed
python nomad.py test-feed "https://www.cisa.gov/cybersecurity-advisories/all.xml"

# Run full pipeline
python nomad.py pipeline
```

### Filter Options
```bash
# By priority
--priority high|medium|low

# By source type
--source-type cert|vendor|research|news|database

# By date range
--since YYYY-MM-DD
--until YYYY-MM-DD
```

### Output Files
All results are saved with timestamps in:
```
data/output/
├── intel_rss_20240113_093021.json     # RSS collection
├── test_feed_20240113_094512.json     # Feed tests
└── pipeline_intel_20240113_095234.json # Pipeline results
```

---

## ❓ Troubleshooting

### "Module not found" Error
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # You should see (venv) in your prompt
```

### "No feeds found" Error
```bash
# Check config file exists
ls config/rss_feeds.yaml
```

### Feed Parsing Warnings
Normal - some feeds have format issues. The tool handles them gracefully.

### Want to Add Your Own Feeds?
Edit `config/rss_feeds.yaml` and add:
```yaml
- name: "Your Feed Name"
  url: "https://example.com/feed.xml"
  priority: high
  source_type: vendor
  enabled: true
```

---

## 🎉 What's Next?

### You Can Now:
✅ Collect threat intelligence from 40+ sources
✅ Filter by priority and vendor
✅ Track CVEs and advisories
✅ Generate daily/weekly reports

### Advanced Features to Explore:
- **Orchestrator Agent**: Routes threats based on your assets
- **Enrichment Agent**: Adds CVSS scores and exploit data
- **Alert Generation**: Creates SOC tickets
- **CISO Reports**: Executive summaries

### Learn More:
- `USAGE.md` - Detailed usage guide
- `CLAUDE_CODE_USAGE.md` - Claude Code integration
- `PROMPTS_USAGE.md` - Using with any LLM

---

## 💡 Pro Tips

1. **Start your day with:** `python nomad.py rss --since yesterday --priority high`
2. **Focus on your vendors:** Use `--source-type vendor` for targeted checks
3. **Save important finds:** Output files in `data/output/` are timestamped
4. **Automate with cron:** Add daily checks to your crontab
5. **Use with Claude Code:** Let AI orchestrate the entire pipeline

---

## 🆘 Need Help?

- **Quick help:** `python nomad.py --help`
- **List commands:** `python nomad.py`
- **Check feeds:** `python nomad.py list-feeds`
- **GitHub Issues:** Report bugs or request features

---

**You're ready to hunt threats!** Start with the daily workflow above and expand from there. 🎯