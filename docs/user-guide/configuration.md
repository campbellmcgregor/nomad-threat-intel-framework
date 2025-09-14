# NOMAD Configuration Guide

Complete guide to configuring NOMAD for your organization's specific requirements.

## Table of Contents

- [Environment Configuration](#environment-configuration)
- [Organization Settings](#organization-settings)
- [RSS Feed Management](#rss-feed-management)
- [Agent Configuration](#agent-configuration)
- [Workflow Customization](#workflow-customization)
- [Security Configuration](#security-configuration)
- [Performance Tuning](#performance-tuning)
- [Multi-Environment Setup](#multi-environment-setup)

## Environment Configuration

### Primary Configuration File (`.env`)

The `.env` file contains all environment-specific settings. Start with the template:

```bash
cp .env.example .env
```

### Essential Settings

#### LLM Configuration
```bash
# Primary API key (required)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Alternative LLM (future use)
OPENAI_API_KEY=your_openai_api_key_here

# Model selection
DEFAULT_MODEL=claude-3-sonnet-20240229

# API behavior
API_TIMEOUT=300
MAX_RETRIES=3
RATE_LIMIT_RPM=60
```

#### File System Paths
```bash
# Output directories
OUTPUT_DIR=data/output
INPUT_DIR=data/input
CACHE_DIR=data/cache

# Caching settings
ENABLE_CACHE=true
CACHE_TTL=3600
ENCRYPT_CACHE=false
```

#### Logging Configuration
```bash
# Logging levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO
VERBOSE_LOGGING=false

# External logging (optional)
SYSLOG_SERVER=
SYSLOG_PORT=514
```

### Development vs Production Settings

#### Development Configuration
```bash
DEV_MODE=true
USE_TEST_DATA=true
MOCK_APIS=true
VERBOSE_LOGGING=true
LOG_LEVEL=DEBUG
RATE_LIMIT_RPM=30  # Lower rate for testing
```

#### Production Configuration
```bash
DEV_MODE=false
USE_TEST_DATA=false
MOCK_APIS=false
VERBOSE_LOGGING=false
LOG_LEVEL=INFO
RATE_LIMIT_RPM=60  # Full rate for production
ENCRYPT_CACHE=true
```

## Organization Settings

### Basic Organization Configuration
```bash
# Organization identity
ORG_NAME=Acme Corporation
BUSINESS_SECTORS=Financial Services,Healthcare,Technology

# Crown jewel systems (comma-separated)
CROWN_JEWELS=Exchange Email,Active Directory,Customer Database,Payment Gateway,Trading Platform

# Asset exposure categories
ASSET_EXPOSURE=Internet-facing,Internal Network,Cloud Infrastructure,Partner Networks
```

### Industry-Specific Examples

#### Financial Services
```bash
ORG_NAME=SecureBank Inc
BUSINESS_SECTORS=Financial Services,Banking,Payments
CROWN_JEWELS=Core Banking System,Payment Gateway,Trading Platform,Customer Portal,ATM Network
ASSET_EXPOSURE=Internet Banking,Internal Network,Partner APIs,Cloud Services,Mobile Apps
```

#### Healthcare Organization
```bash
ORG_NAME=MedCenter Health System
BUSINESS_SECTORS=Healthcare,Medical Devices
CROWN_JEWELS=Electronic Health Records,PACS System,Patient Portal,Medical Devices,Pharmacy System
ASSET_EXPOSURE=Patient Network,Administrative Network,Medical IoT,Cloud EMR,Telehealth Platform
```

#### Technology Company
```bash
ORG_NAME=TechCorp Solutions
BUSINESS_SECTORS=Technology,Software Development,Cloud Services
CROWN_JEWELS=Production Infrastructure,Customer Data,Source Code,CI/CD Pipeline,SaaS Platform
ASSET_EXPOSURE=Public APIs,Customer Portals,Development Environment,Cloud Infrastructure
```

### Risk Tolerance Configuration

#### Conservative (High Security)
```bash
# Lower EPSS threshold for alerts
ALERT_EPSS_THRESHOLD=0.30

# Lower CVSS threshold for CISO reports
ALERT_CVSS_THRESHOLD=7.0

# Shorter SLA times
SLA_HOURS_CRITICAL=24
SLA_HOURS_HIGH=48
SLA_HOURS_MEDIUM=168
```

#### Moderate (Balanced)
```bash
# Standard thresholds
ALERT_EPSS_THRESHOLD=0.70
ALERT_CVSS_THRESHOLD=9.0

# Standard SLA times
SLA_HOURS_CRITICAL=48
SLA_HOURS_HIGH=120
SLA_HOURS_MEDIUM=336
```

#### Aggressive (Performance Focus)
```bash
# Higher thresholds to reduce noise
ALERT_EPSS_THRESHOLD=0.90
ALERT_CVSS_THRESHOLD=9.5

# Longer SLA times
SLA_HOURS_CRITICAL=72
SLA_HOURS_HIGH=168
SLA_HOURS_MEDIUM=720
```

## RSS Feed Management

### Feed Configuration File

Edit `config/rss_feeds.yaml` to manage your intelligence sources:

```yaml
feeds:
  # High-priority government sources
  - name: "CISA Known Exploited Vulnerabilities"
    url: "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.xml"
    source_type: "cert"
    priority: "high"
    enabled: true
    update_frequency: "hourly"

  - name: "US-CERT Current Activity"
    url: "https://us-cert.cisa.gov/ncas/current-activity.xml"
    source_type: "cert"
    priority: "high"
    enabled: true
    update_frequency: "daily"

  # Major vendor advisories
  - name: "Microsoft Security Response Center"
    url: "https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct"
    source_type: "vendor"
    priority: "high"
    enabled: true
    parser: "microsoft_msrc"

  - name: "VMware Security Advisories"
    url: "https://blogs.vmware.com/security/feed"
    source_type: "vendor"
    priority: "high"
    enabled: true

  - name: "Cisco Security Advisories"
    url: "https://tools.cisco.com/security/center/contentxml.x?id=2"
    source_type: "vendor"
    priority: "medium"
    enabled: true
```

### Feed Categories and Priorities

#### High Priority Feeds
- Government CERTs (CISA, NCSC, etc.)
- Major vendor security advisories
- Critical infrastructure alerts
- Active exploitation reports

#### Medium Priority Feeds
- Security research organizations
- Threat intelligence vendors
- Industry-specific sources
- Regional CERTs

#### Low Priority Feeds
- General security news
- Community blogs
- Academic research
- Conference presentations

### Custom Feed Examples

#### Industry-Specific Feeds

**Financial Services**:
```yaml
- name: "Financial Services ISAC"
  url: "https://www.fsisac.com/feed"
  source_type: "research"
  priority: "high"
  enabled: true
  industry_tags: ["finance", "banking"]

- name: "PCI Security Standards Council"
  url: "https://blog.pcisecuritystandards.org/feed"
  source_type: "research"
  priority: "medium"
  enabled: true
```

**Healthcare**:
```yaml
- name: "Health-ISAC"
  url: "https://h-isac.org/feed"
  source_type: "research"
  priority: "high"
  enabled: true
  industry_tags: ["healthcare", "medical"]

- name: "FDA Medical Device Safety"
  url: "https://www.fda.gov/medical-devices/safety-communications/rss"
  source_type: "cert"
  priority: "medium"
  enabled: true
```

#### Threat Intelligence Feeds
```yaml
- name: "MITRE ATT&CK Updates"
  url: "https://attack.mitre.org/resources/updates/feed.xml"
  source_type: "research"
  priority: "medium"
  enabled: true

- name: "Recorded Future Blog"
  url: "https://www.recordedfuture.com/feed"
  source_type: "research"
  priority: "low"
  enabled: true

- name: "FireEye Threat Research"
  url: "https://www.fireeye.com/blog/threat-research/feed"
  source_type: "research"
  priority: "medium"
  enabled: true
```

### Feed Validation and Health Monitoring

#### Automated Feed Testing
```bash
# Test all enabled feeds
for feed in $(yq eval '.feeds[] | select(.enabled == true) | .url' config/rss_feeds.yaml); do
  echo "Testing: $feed"
  curl -s --head "$feed" | head -n 1
done

# Test single feed with NOMAD
python scripts/run_rss_agent.py --single-feed "https://example.com/feed.xml" --dry-run
```

#### Feed Health Metrics
Monitor these indicators:
- **Last Updated**: Feed freshness
- **Item Count**: Content volume
- **Error Rate**: Parsing failures
- **Response Time**: Feed performance
- **Content Quality**: Admiralty ratings

## Agent Configuration

### Agent-Specific Settings

#### RSS Agent Configuration
```yaml
rss_agent:
  default_lookback_days: 7
  max_items_per_feed: 100
  timeout_seconds: 60
  retry_failed_feeds: true
  dedupe_window_hours: 24

  # CVE extraction settings
  cve_patterns:
    - "CVE-\\d{4}-\\d{4,7}"
    - "cve-\\d{4}-\\d{4,7}"

  # Product extraction
  extract_products: true
  product_confidence_threshold: 0.8
```

#### Orchestrator Configuration
```yaml
orchestrator:
  # Routing thresholds
  technical_alert_epss_threshold: 0.70
  technical_alert_cvss_threshold: 8.5
  ciso_report_cvss_threshold: 9.0

  # SLA settings (hours)
  critical_sla: 48
  high_sla: 120
  medium_sla: 336
  low_sla: 720

  # Asset exposure weights
  asset_weights:
    "Internet-facing": 1.0
    "Internal Network": 0.7
    "Cloud Infrastructure": 0.8
    "Partner Networks": 0.6
```

#### CISO Report Configuration
```yaml
ciso_report:
  # Report frequency
  default_period_days: 7

  # Included sections
  include_sections:
    - executive_summary
    - top_risks
    - decisions_made
    - sla_performance
    - threat_landscape
    - next_week_priorities

  # Metrics to include
  key_metrics:
    - alerts_created
    - alerts_closed
    - median_patch_time
    - sla_compliance_rate
    - kev_vulnerabilities_addressed
```

### Custom Agent Parameters

#### Environment-Specific Overrides
```bash
# Development environment - more verbose
DEV_RSS_AGENT_TIMEOUT=120
DEV_MAX_ITEMS_PER_FEED=50
DEV_ENABLE_DEBUG_OUTPUT=true

# Production environment - optimized
PROD_RSS_AGENT_TIMEOUT=60
PROD_MAX_ITEMS_PER_FEED=200
PROD_ENABLE_BATCH_PROCESSING=true
```

## Workflow Customization

### Custom Workflow Definition

Create custom workflows in `config/claude_agent_config.yaml`:

```yaml
workflows:
  # Custom daily morning check
  morning_check_enhanced:
    name: "Enhanced Morning Security Check"
    description: "Comprehensive morning threat assessment with vendor focus"
    schedule: "0 8 * * 1-5"  # Weekdays at 8 AM
    steps:
      - agent: rss_feed
        config:
          priority: high
          source_type: vendor
          since: "24 hours ago"
      - agent: enrichment
        config:
          include_epss: true
          include_kev_status: true
      - agent: orchestrator
        config:
          asset_exposure_required: true
      - conditional:
          - condition: "route == TECHNICAL_ALERT"
            agent: technical_alert
          - condition: "route == CISO_REPORT"
            agent: ciso_report

  # Weekly executive briefing
  executive_briefing:
    name: "Weekly Executive Briefing"
    description: "Comprehensive weekly report for leadership"
    schedule: "0 9 * * 1"  # Mondays at 9 AM
    steps:
      - agent: rss_feed
        config:
          since: "7 days ago"
          priority: all
      - agent: enrichment
      - agent: orchestrator
      - agent: ciso_report
        config:
          format: executive
          include_trends: true

  # Incident response support
  incident_response:
    name: "Incident Response Intelligence"
    description: "Rapid threat intelligence for active incidents"
    trigger: manual
    steps:
      - agent: rss_feed
        config:
          since: "72 hours ago"
          priority: high
          source_type: all
      - agent: enrichment
        config:
          deep_analysis: true
      - agent: orchestrator
        config:
          emergency_mode: true
      - parallel:
          - agent: technical_alert
          - agent: evidence_vault
```

### Conditional Logic

#### Asset-Based Routing
```yaml
conditional_routing:
  - condition: "asset_exposure == 'Internet-facing' AND cvss_v3 >= 7.0"
    route: TECHNICAL_ALERT
    sla_hours: 24

  - condition: "crown_jewel_affected == true"
    route: CISO_REPORT
    sla_hours: 12
    escalation: immediate

  - condition: "exploit_status == 'ITW' AND asset_exposure != 'None'"
    route: TECHNICAL_ALERT
    sla_hours: 6
    priority: critical
```

## Security Configuration

### API Key Management

#### Multiple Environment Keys
```bash
# Development
DEV_ANTHROPIC_API_KEY=dev_key_here

# Staging
STAGING_ANTHROPIC_API_KEY=staging_key_here

# Production
PROD_ANTHROPIC_API_KEY=prod_key_here
```

#### Key Rotation Schedule
```bash
# Key rotation tracking
API_KEY_CREATED_DATE=2025-09-01
API_KEY_ROTATION_DAYS=90
API_KEY_WARNING_DAYS=7
```

### Data Encryption

#### Cache Encryption
```bash
ENCRYPT_CACHE=true
CACHE_ENCRYPTION_KEY=base64_encoded_32_byte_key_here

# Generate encryption key
openssl rand -base64 32
```

#### Output File Protection
```bash
# File permissions for sensitive outputs
OUTPUT_FILE_PERMISSIONS=600  # Owner read/write only
ARCHIVE_ENCRYPTION=true
```

### Network Security

#### SSL/TLS Configuration
```bash
# SSL verification for RSS feeds
VERIFY_SSL_CERTIFICATES=true
SSL_CERT_PATH=/etc/ssl/certs/ca-certificates.crt

# Proxy configuration
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=https://proxy.company.com:8080
NO_PROXY=localhost,127.0.0.1,.company.com
```

#### API Access Control
```bash
# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW=60

# IP allowlisting (if applicable)
ALLOWED_IPS=192.168.1.0/24,10.0.0.0/8
```

## Performance Tuning

### Resource Optimization

#### Memory Management
```bash
# Python memory settings
PYTHONHASHSEED=0
PYTHON_GC_THRESHOLD=700,10,10

# Agent memory limits
RSS_AGENT_MAX_MEMORY_MB=512
ORCHESTRATOR_MAX_MEMORY_MB=256
CISO_AGENT_MAX_MEMORY_MB=256
```

#### Processing Limits
```bash
# Concurrent processing
MAX_CONCURRENT_FEEDS=10
MAX_CONCURRENT_ITEMS=100

# Batch sizes
RSS_BATCH_SIZE=50
ORCHESTRATOR_BATCH_SIZE=25
```

### Caching Strategy

#### Response Caching
```bash
# API response caching
ENABLE_API_CACHE=true
API_CACHE_TTL=3600  # 1 hour
API_CACHE_MAX_SIZE=1000

# Feed caching
ENABLE_FEED_CACHE=true
FEED_CACHE_TTL=1800  # 30 minutes
```

#### Database Caching
```bash
# SQLite optimization
SQLITE_CACHE_SIZE=2000
SQLITE_TEMP_STORE=memory
SQLITE_JOURNAL_MODE=WAL
```

### Performance Monitoring

#### Metrics Collection
```bash
# Enable performance metrics
COLLECT_METRICS=true
METRICS_INTERVAL=60
METRICS_RETENTION_DAYS=30

# Performance thresholds
ALERT_ON_SLOW_FEEDS=true
SLOW_FEED_THRESHOLD_SEC=30
```

## Multi-Environment Setup

### Environment Separation

#### Directory Structure
```
nomad-threat-intel-framework/
├── environments/
│   ├── development/
│   │   ├── .env
│   │   ├── rss_feeds.yaml
│   │   └── agent_config.yaml
│   ├── staging/
│   │   ├── .env
│   │   ├── rss_feeds.yaml
│   │   └── agent_config.yaml
│   └── production/
│       ├── .env
│       ├── rss_feeds.yaml
│       └── agent_config.yaml
```

#### Environment Loading
```bash
# Set active environment
export NOMAD_ENV=development
export NOMAD_CONFIG_PATH=environments/${NOMAD_ENV}

# Load environment-specific config
python scripts/run_rss_agent.py --config-path $NOMAD_CONFIG_PATH
```

### Configuration Management

#### Version Control Strategy
```bash
# Track configuration changes
git add src/config/
git commit -m "Update RSS feeds for Q4 threat landscape"

# Environment-specific branches
git checkout production
git merge staging  # After testing in staging
```

#### Configuration Validation
```bash
# Validate configuration before deployment
python src/utils/validate_config.py --env production
python src/utils/test_feeds.py --config environments/production/rss_feeds.yaml
```

### Deployment Automation

#### Configuration Deployment
```bash
#!/bin/bash
# deploy_config.sh

ENVIRONMENT=$1
CONFIG_PATH="environments/${ENVIRONMENT}"

# Validate configuration
python src/utils/validate_config.py --config-path $CONFIG_PATH

# Deploy configuration
cp ${CONFIG_PATH}/.env .env
cp ${CONFIG_PATH}/rss_feeds.yaml src/config/
cp ${CONFIG_PATH}/agent_config.yaml src/config/

# Restart services
systemctl restart nomad-scheduler
systemctl restart nomad-agents

echo "Configuration deployed to ${ENVIRONMENT}"
```

---

## Configuration Examples by Use Case

### Small Security Team (< 10 people)
- **Focus**: High-signal, low-noise configuration
- **Feeds**: 20-30 high-priority sources
- **Thresholds**: Conservative (lower CVSS/EPSS thresholds)
- **Workflows**: Daily morning check, weekly CISO report
- **SLA**: Shorter response times

### Enterprise SOC (> 100 people)
- **Focus**: Comprehensive coverage with automation
- **Feeds**: 100+ sources across all categories
- **Thresholds**: Moderate (standard thresholds)
- **Workflows**: Multiple daily runs, automated routing
- **SLA**: Tiered response based on asset criticality

### MSSP/Consultant
- **Focus**: Multi-tenant configuration
- **Feeds**: Broad coverage for diverse clients
- **Thresholds**: Configurable per client
- **Workflows**: Client-specific workflows
- **SLA**: Contract-based SLA management

---

## Next Steps

Once you've configured NOMAD:

1. **🧪 Test Configuration**: Run dry-run workflows to validate settings
2. **📊 Monitor Performance**: Track metrics and optimize as needed
3. **🔄 Iterate**: Regularly review and update configuration based on results
4. **📖 Review [Workflows Guide](workflows.md)** for advanced workflow patterns
5. **🆘 Check [Troubleshooting](troubleshooting.md)** for configuration issues