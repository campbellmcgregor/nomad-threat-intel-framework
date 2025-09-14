# NOMAD Troubleshooting Guide

Comprehensive guide to diagnosing and resolving common issues with the NOMAD Threat Intelligence Framework.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Installation Issues](#installation-issues)
- [Configuration Problems](#configuration-problems)
- [API and Authentication](#api-and-authentication)
- [Agent Execution Issues](#agent-execution-issues)
- [Workflow Problems](#workflow-problems)
- [Performance Issues](#performance-issues)
- [Data and Output Problems](#data-and-output-problems)
- [Network and Connectivity](#network-and-connectivity)
- [Advanced Troubleshooting](#advanced-troubleshooting)

## Quick Diagnostics

### System Health Check

Run this comprehensive health check first:

```bash
#!/bin/bash
echo "🔍 NOMAD System Health Check"
echo "================================"

# Check Python version
echo "Python Version:"
python --version

# Check virtual environment
echo -e "\nVirtual Environment:"
which python
echo $VIRTUAL_ENV

# Check dependencies
echo -e "\nKey Dependencies:"
pip list | grep -E "(anthropic|feedparser|pyyaml|requests)"

# Check API key
echo -e "\nAPI Configuration:"
python -c "from config.environment import config; print('✓ API key configured' if config.anthropic_api_key else '❌ API key missing')"

# Check directories
echo -e "\nDirectory Structure:"
for dir in data/output data/input data/cache data/logs data/checkpoints; do
    if [ -d "$dir" ]; then
        echo "✓ $dir exists"
    else
        echo "❌ $dir missing"
    fi
done

# Check configuration files
echo -e "\nConfiguration Files:"
for file in .env config/rss_feeds.yaml config/claude_agent_config.yaml; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "❌ $file missing"
    fi
done

# Test basic functionality
echo -e "\nBasic Functionality Test:"
python -c "
try:
    from agents.rss_feed import RSSFeedAgent
    agent = RSSFeedAgent()
    print('✓ RSS Agent can be imported and instantiated')
except Exception as e:
    print(f'❌ RSS Agent error: {e}')
"

echo -e "\nHealth check complete!"
```

### Quick Fix Checklist

Before diving into specific issues, try these quick fixes:

1. **Check your working directory**: Ensure you're in the NOMAD project root
2. **Activate virtual environment**: `source venv/bin/activate`
3. **Update dependencies**: `pip install -r requirements.txt`
4. **Check API key**: Verify `ANTHROPIC_API_KEY` in `.env` file
5. **Create missing directories**: `mkdir -p data/{output,input,cache,logs,checkpoints}`
6. **Check file permissions**: `chmod +x scripts/*.py`

## Installation Issues

### Python Version Compatibility

**Problem**: "Python version not supported" or import errors

**Solution**:
```bash
# Check Python version (requires 3.8+)
python --version

# If using wrong version, create new virtual environment
python3.8 -m venv venv
# or
python3.9 -m venv venv
# or
python3.10 -m venv venv

source venv/bin/activate
pip install -r requirements.txt
```

### Dependency Installation Failures

**Problem**: `pip install` fails with compilation errors

**Solution**:
```bash
# Update pip and setuptools first
pip install --upgrade pip setuptools wheel

# For macOS users with M1/M2 chips
arch -arm64 pip install -r requirements.txt

# For systems with limited resources
pip install --no-cache-dir -r requirements.txt

# Install individual problematic packages
pip install anthropic>=0.18.0
pip install feedparser>=6.0.10
```

### Virtual Environment Issues

**Problem**: Commands not found or wrong Python version

**Solution**:
```bash
# Completely recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Verify activation
which python  # Should show path in venv directory
echo $VIRTUAL_ENV  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

### Import Errors

**Problem**: `ModuleNotFoundError` when running scripts

**Solution**:
```bash
# Check PYTHONPATH
echo $PYTHONPATH

# Run from project root directory
cd /path/to/nomad-threat-intel-framework

# Add project root to Python path if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Alternative: use python -m syntax
python -m scripts.run_rss_agent --help
```

## Configuration Problems

### Environment File Issues

**Problem**: "No ANTHROPIC_API_KEY found"

**Diagnostics**:
```bash
# Check if .env file exists
ls -la .env

# Check file contents (be careful not to expose real keys)
grep -v "^#" .env | grep -v "^$"

# Test environment loading
python -c "
from config.environment import config
print('API Key present:', bool(config.anthropic_api_key))
if config.anthropic_api_key:
    print('Key starts with:', config.anthropic_api_key[:10] + '...')
"
```

**Solutions**:
```bash
# Create .env file from template
cp .env.example .env

# Edit .env file with real values
nano .env

# Ensure no spaces around equals sign
ANTHROPIC_API_KEY=your_actual_key_here

# Check file permissions
chmod 600 .env
```

### YAML Configuration Errors

**Problem**: "YAML parsing error" or workflow not found

**Diagnostics**:
```bash
# Validate YAML syntax
python -c "
import yaml
with open('config/claude_agent_config.yaml', 'r') as f:
    try:
        data = yaml.safe_load(f)
        print('✓ YAML syntax is valid')
        print('Available workflows:', list(data.get('workflows', {}).keys()))
    except yaml.YAMLError as e:
        print(f'❌ YAML error: {e}')
"

# Check RSS feeds YAML
python -c "
import yaml
with open('config/rss_feeds.yaml', 'r') as f:
    try:
        data = yaml.safe_load(f)
        print('✓ RSS feeds YAML is valid')
        feeds = data.get('feeds', [])
        print(f'Configured feeds: {len(feeds)}')
        enabled = [f for f in feeds if f.get('enabled', True)]
        print(f'Enabled feeds: {len(enabled)}')
    except yaml.YAMLError as e:
        print(f'❌ YAML error: {e}')
"
```

**Solutions**:
```bash
# Fix common YAML issues
# 1. Consistent indentation (2 spaces)
# 2. No tabs, only spaces
# 3. Proper quoting of strings with special characters
# 4. Check for missing colons after keys

# Validate and fix indentation
python -m yaml config/claude_agent_config.yaml

# Use online YAML validator for complex issues
```

### RSS Feed Configuration

**Problem**: No intelligence items collected or feed errors

**Diagnostics**:
```bash
# Test individual feed
python scripts/run_rss_agent.py --single-feed "https://feeds.feedburner.com/TheHackersNews" --dry-run

# List configured feeds
python -c "
import yaml
with open('config/rss_feeds.yaml', 'r') as f:
    data = yaml.safe_load(f)
    for feed in data.get('feeds', []):
        status = '✓' if feed.get('enabled', True) else '❌'
        print(f'{status} {feed[\"name\"]}: {feed[\"url\"]}')
"

# Test feed connectivity
for url in $(yq eval '.feeds[].url' config/rss_feeds.yaml); do
    echo "Testing: $url"
    curl -s --head "$url" | head -n 1
done
```

**Solutions**:
```bash
# Update feed URLs (feeds change over time)
# Remove broken feeds from configuration
# Add working alternative feeds
# Check for SSL certificate issues:

# For SSL problems:
PYTHONHTTPSVERIFY=0 python scripts/run_rss_agent.py --single-feed "https://problematic-feed.com"

# Or add to .env:
VERIFY_SSL_CERTIFICATES=false
```

## API and Authentication

### API Key Issues

**Problem**: "Authentication failed" or "Invalid API key"

**Diagnostics**:
```bash
# Test API key directly
python -c "
import os
from anthropic import Anthropic

api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    print('❌ No API key found in environment')
    exit(1)

print(f'API key format: {api_key[:10]}...{api_key[-4:]}')

try:
    client = Anthropic(api_key=api_key)
    # Simple test request
    response = client.messages.create(
        model='claude-3-sonnet-20240229',
        max_tokens=10,
        messages=[{'role': 'user', 'content': 'Hello'}]
    )
    print('✓ API key is working')
except Exception as e:
    print(f'❌ API error: {e}')
"
```

**Solutions**:
```bash
# Get new API key from https://console.anthropic.com/
# Update .env file with new key
# Check for extra whitespace or characters:

# Remove any whitespace
ANTHROPIC_API_KEY=$(echo "$ANTHROPIC_API_KEY" | tr -d '[:space:]')

# Verify key format (should start with 'sk-')
echo $ANTHROPIC_API_KEY | grep -E '^sk-[a-zA-Z0-9-_]+$'
```

### Rate Limiting

**Problem**: "Rate limit exceeded" or timeout errors

**Diagnostics**:
```bash
# Check current rate limit settings
grep RATE_LIMIT .env

# Monitor API usage
python -c "
from config.environment import config
print(f'Rate limit: {config.rate_limit_rpm} requests/minute')
print(f'API timeout: {config.api_timeout} seconds')
"
```

**Solutions**:
```bash
# Adjust rate limiting in .env
RATE_LIMIT_RPM=30  # Reduce from default 60
API_TIMEOUT=300    # Increase timeout

# Use smaller batch sizes
python scripts/run_rss_agent.py --since "12 hours ago"  # Instead of 7 days

# Enable response caching
ENABLE_CACHE=true
CACHE_TTL=3600
```

### Network Connectivity

**Problem**: "Connection timeout" or "Unable to reach API"

**Diagnostics**:
```bash
# Test basic connectivity
curl -I https://api.anthropic.com/

# Test with proxy settings if behind corporate firewall
curl -I https://api.anthropic.com/ --proxy http://proxy.company.com:8080

# Check DNS resolution
nslookup api.anthropic.com

# Test from Python
python -c "
import requests
try:
    response = requests.get('https://api.anthropic.com/', timeout=10)
    print(f'✓ Can reach API (status: {response.status_code})')
except Exception as e:
    print(f'❌ Connection error: {e}')
"
```

**Solutions**:
```bash
# Configure proxy in .env if needed
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080

# Or use system proxy
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Check firewall settings
# Contact network administrator if in corporate environment
```

## Agent Execution Issues

### RSS Agent Problems

**Problem**: "No intelligence items found" or parsing errors

**Diagnostics**:
```bash
# Test with verbose logging
python scripts/run_rss_agent.py --verbose --use-llm --format summary

# Test single feed in detail
python scripts/run_rss_agent.py --single-feed "https://www.cisa.gov/news.xml" --verbose

# Check date range
python scripts/run_rss_agent.py --since "2025-09-01" --until "2025-09-13" --dry-run

# Examine raw feed data
curl -s "https://feeds.feedburner.com/TheHackersNews" | head -50
```

**Solutions**:
```bash
# Common fixes:
# 1. Adjust time range (some feeds have limited history)
python scripts/run_rss_agent.py --since "24 hours ago"

# 2. Check feed URL is current
# 3. Enable different source types
python scripts/run_rss_agent.py --source-type all

# 4. Lower priority filter
python scripts/run_rss_agent.py --priority medium

# 5. Test without LLM processing first
python scripts/run_rss_agent.py --format summary  # No --use-llm flag
```

### Orchestrator Agent Problems

**Problem**: "No routing decisions" or validation errors

**Diagnostics**:
```bash
# Check input file format
python -c "
import json
with open('data/output/rss_feed_result_20250913_143022.json', 'r') as f:
    data = json.load(f)
    print('Input type:', type(data))
    if 'intelligence' in data:
        print('Intelligence items:', len(data['intelligence']))
        if data['intelligence']:
            item = data['intelligence'][0]
            print('Sample item keys:', list(item.keys()))
    else:
        print('Available keys:', list(data.keys()) if isinstance(data, dict) else 'Not a dict')
"

# Test orchestrator with sample data
python scripts/run_orchestrator.py --input data/output/rss_feed_result_*.json --verbose
```

**Solutions**:
```bash
# Ensure RSS agent completed successfully
# Check input file exists and has intelligence items
ls -la data/output/rss_feed_result_*.json

# Use correct input format
python scripts/run_orchestrator.py --input data/output/rss_feed_result_20250913_143022.json

# Test with known good data
python scripts/run_rss_agent.py --single-feed "https://feeds.feedburner.com/eset/blog" --use-llm
python scripts/run_orchestrator.py --input data/output/rss_feed_result_*.json
```

### CISO Report Agent Problems

**Problem**: "No report generated" or template errors

**Diagnostics**:
```bash
# Check input data structure
python -c "
import json
with open('data/output/orchestrator_result_20250913_143045.json', 'r') as f:
    data = json.load(f)
    print('Data structure:', type(data))
    if 'routing_decisions' in data:
        decisions = data['routing_decisions']
        print('Decisions type:', type(decisions))
        if 'response' in decisions:
            response = decisions['response']
            print('Response type:', type(response))
"

# Generate sample template
python scripts/run_ciso_report.py --template

# Test with sample data
python scripts/run_ciso_report.py --decisions sample_decisions.json --verbose
```

**Solutions**:
```bash
# Use sample template first
python scripts/run_ciso_report.py --template
python scripts/run_ciso_report.py --decisions sample_decisions.json

# Check date format
python scripts/run_ciso_report.py --week-start 2025-09-07 --week-end 2025-09-13

# Try different output format
python scripts/run_ciso_report.py --decisions decisions.json --format executive
```

## Workflow Problems

### Workflow Execution Failures

**Problem**: Workflow stops or fails partway through

**Diagnostics**:
```bash
# Check workflow configuration
python nomad_workflow_enhanced.py list

# Generate execution plan
python nomad_workflow_enhanced.py plan morning_check --mode=direct

# Check for missing scripts
ls -la scripts/run_*.py

# Review execution logs
tail -100 data/logs/workflow_execution_*.log
```

**Solutions**:
```bash
# Run individual steps to isolate issue
python scripts/run_rss_agent.py --use-llm --format json
python scripts/run_orchestrator.py --input data/output/rss_feed_result_*.json

# Check checkpoint recovery
ls data/checkpoints/

# Increase timeouts
# Edit config/claude_agent_config.yaml:
settings:
  agent_timeout: 600  # 10 minutes instead of 5
```

### Workflow Configuration Errors

**Problem**: "Unknown workflow" or YAML parsing errors

**Diagnostics**:
```bash
# List available workflows
python -c "
import yaml
with open('config/claude_agent_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    workflows = config.get('workflows', {})
    print('Available workflows:')
    for name in workflows.keys():
        print(f'  - {name}')
"

# Validate workflow definition
python -c "
import yaml
with open('config/claude_agent_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    workflow = config['workflows'].get('morning_check', {})
    print('Morning check steps:')
    for step in workflow.get('steps', []):
        print(f'  - {step}')
"
```

**Solutions**:
```bash
# Check spelling of workflow name
python nomad_workflow_enhanced.py execute morning_check  # not "morning-check"

# Validate YAML syntax
python -m yaml config/claude_agent_config.yaml

# Reset to default configuration
cp config/claude_agent_config.yaml.example config/claude_agent_config.yaml
```

## Performance Issues

### Slow Execution

**Problem**: Agents or workflows taking excessive time

**Diagnostics**:
```bash
# Time individual operations
time python scripts/run_rss_agent.py --use-llm --format json

# Monitor resource usage
top -p $(pgrep -f "python.*nomad")

# Check API response times
python -c "
import time
import requests
start = time.time()
response = requests.get('https://api.anthropic.com/')
end = time.time()
print(f'API response time: {end - start:.2f} seconds')
"

# Examine feed response times
for url in $(head -5 config/rss_feeds.yaml | yq eval '.feeds[].url'); do
    echo "Testing: $url"
    time curl -s --head "$url" > /dev/null
done
```

**Solutions**:
```bash
# Enable caching
ENABLE_CACHE=true
CACHE_TTL=3600

# Reduce batch sizes
python scripts/run_rss_agent.py --since "12 hours ago"  # Smaller time range

# Use parallel processing
MAX_CONCURRENT_FEEDS=3  # In .env file

# Optimize feed selection
# Remove slow or unreliable feeds from config/rss_feeds.yaml

# Increase timeouts for slow networks
API_TIMEOUT=600
RSS_AGENT_TIMEOUT=300
```

### Memory Issues

**Problem**: "Memory error" or system slowdown

**Diagnostics**:
```bash
# Monitor memory usage
ps aux | grep python
free -h

# Check for memory leaks
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"
```

**Solutions**:
```bash
# Process feeds in smaller batches
python scripts/run_rss_agent.py --since "6 hours ago"

# Clear cache periodically
rm -rf data/cache/*

# Restart Python process between large operations
# Set memory limits in environment
PYTHON_GC_THRESHOLD=700,10,10
```

## Data and Output Problems

### Missing or Empty Output Files

**Problem**: Expected output files not created or empty

**Diagnostics**:
```bash
# Check output directory
ls -la data/output/

# Check directory permissions
ls -ld data/output/

# Verify directory creation
python -c "
from config.environment import config
config.ensure_directories()
print('Directories created')
"

# Check for permission errors
python scripts/run_rss_agent.py --use-llm 2>&1 | grep -i permission
```

**Solutions**:
```bash
# Fix directory permissions
sudo chown -R $USER:$USER data/
chmod 755 data/output/

# Create missing directories
mkdir -p data/{output,input,cache,logs,checkpoints}

# Check disk space
df -h .

# Use explicit output paths
python scripts/run_rss_agent.py --output-file custom_output.json
```

### Malformed JSON Output

**Problem**: "JSON decode error" or corrupt output files

**Diagnostics**:
```bash
# Validate JSON files
for file in data/output/*.json; do
    echo "Checking: $file"
    python -m json.tool "$file" > /dev/null && echo "✓ Valid" || echo "❌ Invalid"
done

# Check file contents
head -20 data/output/rss_feed_result_*.json
tail -20 data/output/rss_feed_result_*.json

# Look for truncated files
ls -lh data/output/
```

**Solutions**:
```bash
# Regenerate output files
rm data/output/corrupted_file.json
python scripts/run_rss_agent.py --use-llm

# Check for disk space issues
df -h .

# Use JSON validation
python -c "
import json
with open('data/output/file.json', 'r') as f:
    try:
        data = json.load(f)
        print('✓ JSON is valid')
    except json.JSONDecodeError as e:
        print(f'❌ JSON error at line {e.lineno}: {e.msg}')
"
```

### Data Quality Issues

**Problem**: Poor quality or irrelevant intelligence items

**Diagnostics**:
```bash
# Analyze collected data
python -c "
import json
with open('data/output/rss_feed_result_*.json', 'r') as f:
    data = json.load(f)
    items = data.get('intelligence', [])
    print(f'Total items: {len(items)}')

    # Check source reliability
    reliability = {}
    for item in items:
        rel = item.get('admiralty_source_reliability', 'Unknown')
        reliability[rel] = reliability.get(rel, 0) + 1
    print('Source reliability:', reliability)

    # Check CVE presence
    with_cves = sum(1 for item in items if item.get('cves'))
    print(f'Items with CVEs: {with_cves}')
"

# Check feed quality
python scripts/run_rss_agent.py --single-feed "https://problem-feed.com" --verbose
```

**Solutions**:
```bash
# Tune feed selection
# Edit config/rss_feeds.yaml:
# - Remove low-quality feeds
# - Adjust priority levels
# - Enable only high-reliability sources

# Adjust time ranges
python scripts/run_rss_agent.py --since "24 hours ago"  # More recent, higher quality

# Use source type filtering
python scripts/run_rss_agent.py --source-type vendor --priority high
```

## Network and Connectivity

### Proxy Configuration

**Problem**: Connection failures in corporate environments

**Solution**:
```bash
# Configure proxy in .env
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
NO_PROXY=localhost,127.0.0.1,.company.com

# Test proxy connectivity
curl --proxy http://proxy.company.com:8080 -I https://api.anthropic.com/

# For authenticated proxies
HTTP_PROXY=http://username:password@proxy.company.com:8080
```

### SSL Certificate Issues

**Problem**: "SSL certificate verification failed"

**Solution**:
```bash
# Temporary bypass (not recommended for production)
PYTHONHTTPSVERIFY=0 python scripts/run_rss_agent.py

# Or in .env:
VERIFY_SSL_CERTIFICATES=false

# Better solution - update certificates
pip install --upgrade certifi
```

### DNS Resolution Problems

**Problem**: "Name resolution failed" for RSS feeds

**Solution**:
```bash
# Test DNS resolution
nslookup feeds.feedburner.com
nslookup api.anthropic.com

# Use alternative DNS
echo "nameserver 8.8.8.8" >> /etc/resolv.conf

# Check /etc/hosts for conflicts
grep -v "^#" /etc/hosts
```

## Advanced Troubleshooting

### Debug Mode Execution

Enable comprehensive debugging:

```bash
# Environment variables for debugging
export DEBUG=1
export LOG_LEVEL=DEBUG
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run with maximum verbosity
python scripts/run_rss_agent.py --verbose --use-llm 2>&1 | tee debug.log

# Python debugging
python -u -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from agents.rss_feed import RSSFeedAgent
agent = RSSFeedAgent()
result = agent.run(since='2025-09-13', priority='high')
print('Result:', result)
"
```

### Log Analysis

Analyze logs for patterns:

```bash
# Check error patterns
grep -i error data/logs/*.log

# Check API issues
grep -i "api" data/logs/*.log | grep -i "error\|timeout\|fail"

# Monitor real-time logs
tail -f data/logs/workflow_execution_$(date +%Y%m%d).log

# Analyze performance
grep "completed successfully" data/logs/*.log | grep -o "[0-9]* items" | sort -n
```

### System Resource Monitoring

Monitor system resources during execution:

```bash
# Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash
while true; do
    echo "$(date): CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)% Memory: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
    sleep 10
done
EOF

chmod +x monitor.sh
./monitor.sh &

# Run NOMAD workflow
python nomad_workflow_enhanced.py execute morning_check

# Stop monitoring
killall monitor.sh
```

### Database and Cache Issues

Check SQLite databases and cache:

```bash
# Check cache directory
ls -la data/cache/

# Clear cache if corrupted
rm -rf data/cache/*

# Check SQLite databases (if using)
for db in data/*.db; do
    echo "Checking: $db"
    sqlite3 "$db" "PRAGMA integrity_check;"
done
```

---

## Getting Additional Help

### Log Collection for Support

When reporting issues, collect these logs:

```bash
# Create support bundle
mkdir nomad_support_bundle
cp .env.example nomad_support_bundle/  # Don't include real .env with API keys
cp config/*.yaml nomad_support_bundle/
cp data/logs/*.log nomad_support_bundle/ 2>/dev/null || echo "No logs found"
ls -la data/output/ > nomad_support_bundle/output_files.txt

# System information
python --version > nomad_support_bundle/system_info.txt
pip list >> nomad_support_bundle/system_info.txt
uname -a >> nomad_support_bundle/system_info.txt

# Create archive
tar -czf nomad_support_bundle.tar.gz nomad_support_bundle/
echo "Support bundle created: nomad_support_bundle.tar.gz"
```

### Useful Commands Reference

```bash
# Quick status check
python -c "from config.environment import config; print('API:', bool(config.anthropic_api_key)); import os; print('PWD:', os.getcwd())"

# Reset everything
rm -rf data/output/* data/cache/* data/logs/*
python nomad_workflow_enhanced.py execute morning_check

# Test minimal functionality
python scripts/run_rss_agent.py --single-feed "https://feeds.feedburner.com/eset/blog" --dry-run

# Validate all configurations
python -m yaml config/claude_agent_config.yaml
python -m yaml config/rss_feeds.yaml
python -c "from config.environment import config; config.validate_api_access()"
```

---

**Remember**: Most issues are configuration-related. Check your `.env` file, ensure you're in the right directory, and verify your API key before diving into complex troubleshooting.