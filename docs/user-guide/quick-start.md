# NOMAD Quick Start Guide

Get up and running with NOMAD (Notable Object Monitoring And Analysis Director) in under 10 minutes.

## What is NOMAD?

NOMAD is an AI-powered threat intelligence orchestration framework that:
- 🔍 Collects threats from RSS feeds, vendor advisories, and security bulletins
- 🧠 Uses AI to analyze and prioritize threats
- 🎯 Routes intelligence to the right teams (SOC, Vulnerability Management, IT Ops)
- 📊 Generates executive reports for leadership

## Prerequisites

- Python 3.8+ installed
- Anthropic Claude API key (get one at [console.anthropic.com](https://console.anthropic.com/))
- 10 minutes of setup time

## 🚀 Quick Setup

### 1. Clone and Setup Environment

```bash
# Clone the repository (if you haven't already)
git clone <repository-url>
cd nomad-threat-intel-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API key
nano .env  # or use your preferred editor
```

Add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Test the Setup

```bash
# Test API connectivity
python -c "from config.environment import config; print('✓ API key configured' if config.anthropic_api_key else '❌ API key missing')"

# List available workflows
python nomad_workflow_enhanced.py list
```

## 🎯 Your First Threat Intelligence Run

### Option 1: Automated Workflow (Recommended)
Run the complete morning security check:

```bash
python nomad_workflow_enhanced.py execute morning_check
```

This will:
1. Collect high-priority threats from the last 24 hours
2. Analyze and route them using AI
3. Generate an executive summary
4. Save results to `data/output/`

### Option 2: Step-by-Step Execution
Run each agent individually to understand the process:

```bash
# Step 1: Collect RSS feeds
python scripts/run_rss_agent.py --priority high --use-llm --format summary

# Step 2: Route intelligence (use the RSS output file)
python scripts/run_orchestrator.py --input data/output/rss_feed_result_*.json --format summary

# Step 3: Generate CISO report (use the orchestrator output file)
python scripts/run_ciso_report.py --decisions data/output/orchestrator_result_*.json --format executive
```

## 📁 Understanding Your Results

After running NOMAD, check these locations:

### Output Files
```
data/output/
├── rss_feed_result_20250913_143022.json      # Raw intelligence items
├── orchestrator_result_20250913_143045.json  # Routing decisions
└── ciso_report_20250913_143112.json         # Executive summary
```

### Key Metrics to Look For
- **Technical Alerts**: High-priority items requiring immediate action
- **CISO Report Items**: Strategic threats for executive awareness
- **Watchlist**: Lower-priority items to monitor
- **CVE Count**: Number of vulnerabilities identified
- **Source Reliability**: Quality ratings (A-F scale)

## 🎛️ Common Commands

### View Available Workflows
```bash
python nomad_workflow_enhanced.py list
```

### Generate Execution Plan
```bash
# See what would be executed without running it
python nomad_workflow_enhanced.py plan morning_check --mode=direct
```

### Test Individual Components
```bash
# Test RSS collection only
python scripts/run_rss_agent.py --single-feed https://feeds.feedburner.com/eset/blog --use-llm

# Generate sample CISO report template
python scripts/run_ciso_report.py --template

# Dry run (no API calls)
python scripts/run_rss_agent.py --priority high --dry-run
```

## ⚡ Quick Customization

### Change Time Range
```bash
# Collect threats from last 7 days
python scripts/run_rss_agent.py --since 2025-09-06 --until 2025-09-13 --use-llm

# Weekly CISO report
python scripts/run_ciso_report.py --week-start 2025-09-06 --week-end 2025-09-13
```

### Filter by Source Type
```bash
# Only vendor advisories
python scripts/run_rss_agent.py --source-type vendor --use-llm

# Only high-priority feeds
python scripts/run_rss_agent.py --priority high --use-llm
```

### Different Output Formats
```bash
# Table format for easier reading
python scripts/run_rss_agent.py --use-llm --format table

# Markdown report
python scripts/run_ciso_report.py --decisions data/output/orchestrator_result_*.json --format markdown
```

## 🔧 Basic Configuration

### Organization Settings
Edit `.env` to customize for your organization:

```bash
ORG_NAME=Your Company Name
CROWN_JEWELS=Exchange,Active Directory,Database,Web Applications
BUSINESS_SECTORS=Financial Services,Healthcare
```

### RSS Feed Sources
Add your feeds to `config/rss_feeds.yaml`:

```yaml
feeds:
  - name: "Your Security Blog"
    url: "https://yourblog.com/security/feed.xml"
    source_type: "research"
    priority: "medium"
    enabled: true
```

## 🆘 Quick Troubleshooting

### Common Issues

**"❌ No ANTHROPIC_API_KEY found"**
- Check your `.env` file exists and contains `ANTHROPIC_API_KEY=your_key_here`
- Make sure there are no spaces around the `=` sign

**"❌ Script not found"**
- Ensure you're running commands from the project root directory
- Check that script files are executable: `chmod +x scripts/*.py`

**"API timeout" or "Rate limit"**
- The system will automatically retry with backoff
- Consider reducing batch sizes: use `--since` with shorter time ranges

**No intelligence items found**
- Check your RSS feed URLs in `config/rss_feeds.yaml`
- Try testing with a single feed: `--single-feed <url>`
- Use `--verbose` flag for detailed logging

## 📚 Next Steps

Now that you have NOMAD running:

1. **📖 Read the [User Manual](user-manual.md)** for detailed features
2. **⚙️ Customize [Configuration](configuration.md)** for your organization
3. **🔄 Learn about [Workflows](workflows.md)** for advanced usage
4. **🛡️ Review [Security Best Practices](../reference/security.md)**
5. **📈 Set up [Performance Monitoring](../reference/performance.md)**

## 🎉 Success Indicators

You'll know NOMAD is working correctly when you see:

✅ **RSS Agent**: "✓ RSS Feed Agent completed successfully - Processed X intelligence items"

✅ **Orchestrator**: Routing decisions showing TECHNICAL_ALERT, CISO_REPORT, or WATCHLIST routes

✅ **CISO Report**: Executive summary with headline, metrics, and actionable insights

✅ **Files Created**: JSON output files in `data/output/` directory with structured threat intelligence

**🎯 You're ready to start using NOMAD for automated threat intelligence!**

---

**Need Help?**
- 📖 Check the [Troubleshooting Guide](troubleshooting.md)
- 🔧 Review [Configuration Options](configuration.md)
- 💬 See [Examples](../examples/) for advanced use cases