# NOMAD API Documentation

Comprehensive API reference for integrating with and extending the NOMAD Threat Intelligence Framework.

## Table of Contents

- [API Overview](#api-overview)
- [Python API](#python-api)
- [CLI Interface](#cli-interface)
- [Agent APIs](#agent-apis)
- [Configuration API](#configuration-api)
- [Data Schemas](#data-schemas)
- [Error Handling](#error-handling)
- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Integration Examples](#integration-examples)
- [SDK Usage](#sdk-usage)

## API Overview

NOMAD provides multiple API layers for different integration needs:

- **Python API**: Direct programmatic access to agents and workflows
- **CLI Interface**: Command-line execution of agents and workflows
- **Configuration API**: Runtime configuration management
- **File-based API**: JSON input/output for agent chaining

### API Design Principles

- **Schema-First**: All data structures follow JSON schemas
- **Agent-Centric**: APIs organized around agent capabilities
- **Error-Safe**: Comprehensive error handling and validation
- **Extensible**: Plugin architecture for custom agents

### Supported Formats

- **Input**: JSON, YAML, Environment Variables
- **Output**: JSON, CSV, Markdown, Plain Text
- **Configuration**: YAML, Environment Variables

## Python API

### Core Classes

#### BaseAgent

Base class for all NOMAD agents with Claude AI integration.

```python
from agents.base_agent import BaseAgent

class BaseAgent:
    """Base agent with Claude AI integration"""

    def __init__(self, agent_name: str):
        """Initialize agent with configuration"""
        pass

    def run(self, **kwargs) -> Dict[str, Any]:
        """Execute agent logic - override in subclasses"""
        raise NotImplementedError

    def process_with_llm(self, input_data: Dict,
                        custom_prompt: str = None) -> Dict[str, Any]:
        """Process data using Claude AI"""
        pass

    def validate_input(self, input_data: Dict) -> bool:
        """Validate input against agent schema"""
        pass

    def validate_output(self, output_data: Dict) -> bool:
        """Validate output against agent schema"""
        pass
```

**Usage Example:**
```python
from agents.rss_feed_agent import RSSFeedAgent

# Initialize agent
rss_agent = RSSFeedAgent()

# Run with parameters
result = rss_agent.run(
    since="2025-09-12T00:00:00Z",
    until="2025-09-13T00:00:00Z",
    priority="high",
    use_llm=True
)

print(f"Found {len(result['intelligence'])} intelligence items")
```

#### EnvironmentConfig

Centralized configuration management.

```python
from config.environment import EnvironmentConfig

class EnvironmentConfig:
    """Environment configuration manager"""

    def __init__(self):
        """Load configuration from environment"""
        pass

    def get_api_key(self, service: str) -> str:
        """Get API key for service"""
        pass

    def validate_api_access(self) -> Dict[str, bool]:
        """Validate all API connections"""
        pass

    def get_organization_context(self) -> Dict[str, Any]:
        """Get organization-specific context"""
        pass
```

**Usage Example:**
```python
from config.environment import config

# Validate API access
api_status = config.validate_api_access()
if not api_status['anthropic']:
    raise ValueError("Claude API not accessible")

# Get organization context
org_context = config.get_organization_context()
print(f"Organization: {org_context['name']}")
```

#### WorkflowEngine

Orchestrate multi-agent workflows.

```python
from nomad_workflow_enhanced import NomadWorkflowEnhanced

class NomadWorkflowEnhanced:
    """Enhanced workflow execution engine"""

    def list_workflows(self) -> List[str]:
        """List available workflows"""
        pass

    def execute_workflow(self, workflow_name: str,
                        **kwargs) -> Dict[str, Any]:
        """Execute named workflow"""
        pass

    def execute_agent_direct(self, agent_name: str,
                           **kwargs) -> Dict[str, Any]:
        """Execute single agent directly"""
        pass
```

**Usage Example:**
```python
from nomad_workflow_enhanced import NomadWorkflowEnhanced

# Initialize workflow engine
workflow = NomadWorkflowEnhanced()

# List available workflows
workflows = workflow.list_workflows()
print("Available workflows:", workflows)

# Execute morning check workflow
result = workflow.execute_workflow(
    'morning_check',
    date_range_days=1,
    priority='high'
)
```

### Agent-Specific APIs

#### RSS Feed Agent

Collect and process RSS feed intelligence.

```python
from agents.rss_feed_agent import RSSFeedAgent

class RSSFeedAgent(BaseAgent):
    def run(self, since: str, until: str, priority: str = "medium",
            source_type: str = "rss", use_llm: bool = True,
            single_feed: str = None, dry_run: bool = False) -> Dict[str, Any]:
        """
        Collect RSS feed intelligence

        Args:
            since: Start datetime (ISO format)
            until: End datetime (ISO format)
            priority: Filter level (low/medium/high)
            source_type: Source type filter
            use_llm: Enable Claude AI processing
            single_feed: Process only specified feed URL
            dry_run: Validate without processing

        Returns:
            Dict containing intelligence items and metadata
        """
        pass
```

**API Response Schema:**
```json
{
  "agent_type": "rss_feed",
  "timestamp": "2025-09-13T10:00:00Z",
  "parameters": {
    "since": "2025-09-12T00:00:00Z",
    "until": "2025-09-13T00:00:00Z",
    "priority": "high"
  },
  "intelligence": [
    {
      "source_type": "rss",
      "source_name": "CISA Known Exploited Vulnerabilities",
      "source_url": "https://www.cisa.gov/...",
      "title": "CISA Adds Three Known Exploited Vulnerabilities to Catalog",
      "summary": "CISA added CVE-2024-12345 to KEV catalog...",
      "published_utc": "2025-09-13T08:00:00Z",
      "cves": ["CVE-2024-12345"],
      "cvss_v3": null,
      "kev_listed": true,
      "admiralty_source_reliability": "A",
      "admiralty_info_credibility": 1,
      "dedupe_key": "abc123..."
    }
  ],
  "stats": {
    "total_items": 25,
    "deduped_items": 23,
    "processing_time_seconds": 45.2
  }
}
```

#### Orchestrator Agent

Route intelligence to appropriate teams.

```python
from agents.orchestrator import OrchestratorAgent

class OrchestratorAgent(BaseAgent):
    def run(self, input_file: str) -> Dict[str, Any]:
        """
        Process and route intelligence items

        Args:
            input_file: Path to intelligence JSON file

        Returns:
            Dict containing routing decisions
        """
        pass
```

**API Response Schema:**
```json
{
  "agent_type": "orchestrator",
  "timestamp": "2025-09-13T10:15:00Z",
  "decisions": [
    {
      "intelligence_id": "abc123...",
      "routing_decision": "TECHNICAL_ALERT",
      "reasoning": "KEV-listed vulnerability affecting Windows systems",
      "owner_team": "SOC",
      "sla_hours": 24,
      "priority": "P1"
    }
  ],
  "routing_stats": {
    "total_items": 23,
    "technical_alert": 8,
    "ciso_report": 2,
    "watchlist": 10,
    "dropped": 3
  }
}
```

#### CISO Report Agent

Generate executive intelligence reports.

```python
from agents.ciso_report_agent import CISOReportAgent

class CISOReportAgent(BaseAgent):
    def run(self, week_start: str, week_end: str,
            decisions_file: str = None) -> Dict[str, Any]:
        """
        Generate CISO intelligence report

        Args:
            week_start: Start date (YYYY-MM-DD)
            week_end: End date (YYYY-MM-DD)
            decisions_file: Optional decisions JSON file

        Returns:
            Dict containing formatted report
        """
        pass
```

#### Technical Alert Agent

Create technical team alerts.

```python
from agents.technical_alert_agent import TechnicalAlertAgent

class TechnicalAlertAgent(BaseAgent):
    def run(self, input_file: str) -> Dict[str, Any]:
        """
        Generate technical alerts for SOC/IT teams

        Args:
            input_file: Path to routing decisions JSON

        Returns:
            Dict containing formatted alerts
        """
        pass
```

## CLI Interface

### Global CLI Options

All CLI scripts support these global options:

```bash
# Output format
--format json|csv|markdown|summary

# Verbose logging
--verbose

# Dry run mode
--dry-run

# Custom configuration file
--config /path/to/config.yml
```

### RSS Feed Agent CLI

```bash
# Basic usage
python scripts/run_rss_agent.py --since 2025-09-12T00:00:00Z --until 2025-09-13T00:00:00Z

# High priority items only
python scripts/run_rss_agent.py --priority high --use-llm

# Single feed testing
python scripts/run_rss_agent.py --single-feed https://feeds.feedburner.com/eset/blog

# Output to specific file
python scripts/run_rss_agent.py --output-file /path/to/output.json --format json
```

**CLI Parameters:**
- `--since`: Start datetime (ISO 8601 format)
- `--until`: End datetime (ISO 8601 format)
- `--priority`: Filter level (low/medium/high)
- `--source-type`: Source type filter
- `--use-llm`: Enable Claude AI processing
- `--single-feed`: Process single feed URL
- `--dry-run`: Validate configuration only
- `--output-file`: Output file path
- `--format`: Output format

### Orchestrator CLI

```bash
# Process intelligence file
python scripts/run_orchestrator.py --input data/output/rss_feed_result_20250913.json

# Custom organization context
python scripts/run_orchestrator.py --input intelligence.json --org-context my_org.yml
```

### CISO Report CLI

```bash
# Weekly report
python scripts/run_ciso_report.py --week-start 2025-09-07 --week-end 2025-09-13

# Custom decisions input
python scripts/run_ciso_report.py --week-start 2025-09-07 --week-end 2025-09-13 \
  --decisions-file custom_decisions.json
```

### Workflow Engine CLI

```bash
# List workflows
python nomad_workflow_enhanced.py list

# Execute workflow
python nomad_workflow_enhanced.py execute morning_check

# Execute with parameters
python nomad_workflow_enhanced.py execute morning_check --date-range-days 7

# Direct agent execution
python nomad_workflow_enhanced.py agent rss_feed --since 2025-09-12T00:00:00Z --priority high
```

## Agent APIs

### Agent Registration

Custom agents must register with the framework:

```python
from agents.base_agent import BaseAgent
from agents import agent_registry

class CustomAgent(BaseAgent):
    """Custom threat intelligence agent"""

    def __init__(self):
        super().__init__("custom_agent")
        self.schema = self._load_schema()

    def run(self, **kwargs) -> Dict[str, Any]:
        # Custom agent implementation
        pass

# Register agent
agent_registry.register("custom", CustomAgent)
```

### Agent Discovery

```python
from agents import agent_registry

# List all registered agents
agents = agent_registry.list_agents()
print("Available agents:", agents)

# Get agent class
agent_class = agent_registry.get_agent("rss_feed")
agent = agent_class()
```

### Agent Lifecycle Hooks

Agents can implement lifecycle hooks:

```python
class CustomAgent(BaseAgent):
    def pre_run(self, **kwargs):
        """Called before run() execution"""
        self.logger.info("Starting custom agent")

    def post_run(self, result: Dict, **kwargs):
        """Called after run() execution"""
        self.logger.info(f"Custom agent completed with {len(result)} items")

    def on_error(self, error: Exception, **kwargs):
        """Called on execution error"""
        self.logger.error(f"Custom agent failed: {error}")
```

## Configuration API

### Runtime Configuration

```python
from config.environment import config

# Get current configuration
current_config = config.get_all_settings()

# Update configuration
config.update_setting("rss_feeds.enable_caching", True)

# Validate configuration
validation_result = config.validate_configuration()
if not validation_result.valid:
    print("Configuration errors:", validation_result.errors)
```

### Dynamic Feed Management

```python
from config.rss_feeds import RSSFeedManager

feed_manager = RSSFeedManager()

# Add new feed
feed_manager.add_feed({
    "name": "Custom Security Blog",
    "url": "https://example.com/security/feed.xml",
    "priority": "medium",
    "tags": ["vendor", "patches"]
})

# Remove feed
feed_manager.remove_feed("Custom Security Blog")

# Update feed configuration
feed_manager.update_feed("CISA KEV", {"priority": "high"})

# Get all feeds
feeds = feed_manager.get_all_feeds()
```

### Organization Context API

```python
from config.environment import config

# Update organization context
config.update_organization_context({
    "name": "Acme Corporation",
    "crown_jewels": ["Exchange Server", "Active Directory"],
    "business_sectors": ["Financial Services", "Healthcare"],
    "compliance_frameworks": ["SOX", "HIPAA"]
})

# Get asset exposure mapping
asset_exposure = config.get_asset_exposure()
```

## Data Schemas

### Intelligence Item Schema

**Complete Schema Definition:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "source_type", "source_name", "source_url", "title",
    "published_utc", "admiralty_source_reliability",
    "admiralty_info_credibility", "dedupe_key"
  ],
  "properties": {
    "source_type": {
      "type": "string",
      "enum": ["rss", "vendor", "cert", "api"]
    },
    "source_name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "source_url": {
      "type": "string",
      "format": "uri"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 500
    },
    "summary": {
      "type": ["string", "null"],
      "maxLength": 300
    },
    "published_utc": {
      "type": "string",
      "format": "date-time"
    },
    "cves": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^CVE-\\d{4}-\\d{4,7}$"
      }
    },
    "cvss_v3": {
      "type": ["number", "null"],
      "minimum": 0.0,
      "maximum": 10.0
    },
    "cvss_v4": {
      "type": ["number", "null"],
      "minimum": 0.0,
      "maximum": 10.0
    },
    "epss": {
      "type": ["number", "null"],
      "minimum": 0.0,
      "maximum": 1.0
    },
    "kev_listed": {
      "type": ["boolean", "null"]
    },
    "kev_date_added": {
      "type": ["string", "null"],
      "format": "date"
    },
    "exploit_status": {
      "type": ["string", "null"],
      "enum": ["ITW", "PoC", "None", null]
    },
    "affected_products": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["vendor", "product"],
        "properties": {
          "vendor": {"type": "string"},
          "product": {"type": "string"},
          "versions": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    },
    "admiralty_source_reliability": {
      "type": "string",
      "enum": ["A", "B", "C", "D", "E", "F"]
    },
    "admiralty_info_credibility": {
      "type": "integer",
      "minimum": 1,
      "maximum": 6
    },
    "admiralty_reason": {
      "type": "string",
      "maxLength": 500
    },
    "dedupe_key": {
      "type": "string",
      "minLength": 32,
      "maxLength": 64
    }
  }
}
```

### Agent Output Schema

**Standard Agent Response:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["agent_type", "timestamp", "status"],
  "properties": {
    "agent_type": {
      "type": "string",
      "enum": ["rss_feed", "orchestrator", "technical_alert", "ciso_report"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "status": {
      "type": "string",
      "enum": ["success", "partial", "failure"]
    },
    "parameters": {
      "type": "object"
    },
    "intelligence": {
      "type": "array",
      "items": {"$ref": "#/definitions/IntelligenceItem"}
    },
    "decisions": {
      "type": "array",
      "items": {"$ref": "#/definitions/RoutingDecision"}
    },
    "stats": {
      "type": "object",
      "properties": {
        "processing_time_seconds": {"type": "number"},
        "total_items": {"type": "integer"},
        "successful_items": {"type": "integer"},
        "failed_items": {"type": "integer"}
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "error_type": {"type": "string"},
          "message": {"type": "string"},
          "details": {"type": "object"}
        }
      }
    }
  }
}
```

### Routing Decision Schema

```json
{
  "type": "object",
  "required": ["intelligence_id", "routing_decision", "reasoning"],
  "properties": {
    "intelligence_id": {"type": "string"},
    "routing_decision": {
      "type": "string",
      "enum": ["DROP", "WATCHLIST", "TECHNICAL_ALERT", "CISO_REPORT"]
    },
    "reasoning": {"type": "string"},
    "owner_team": {
      "type": "string",
      "enum": ["SOC", "Vuln Mgmt", "IT Ops", "CISO"]
    },
    "sla_hours": {"type": "integer"},
    "priority": {
      "type": "string",
      "enum": ["P0", "P1", "P2", "P3", "P4"]
    },
    "business_impact": {
      "type": "string",
      "enum": ["Critical", "High", "Medium", "Low"]
    }
  }
}
```

## Error Handling

### Error Response Format

All API errors follow this standard format:

```json
{
  "error": true,
  "error_type": "ValidationError",
  "message": "Input validation failed",
  "details": {
    "field": "published_utc",
    "value": "invalid-date",
    "expected": "ISO 8601 datetime format"
  },
  "timestamp": "2025-09-13T10:00:00Z",
  "agent": "rss_feed",
  "request_id": "req-abc123"
}
```

### Error Types

**Common Error Types:**
- `ValidationError`: Input/output validation failed
- `AuthenticationError`: API key invalid or expired
- `RateLimitError`: API rate limits exceeded
- `NetworkError`: Network connectivity issues
- `ProcessingError`: Agent processing failed
- `ConfigurationError`: Configuration invalid
- `TimeoutError`: Operation timed out

### Error Handling in Python

```python
from agents.exceptions import NomadError, ValidationError

try:
    result = rss_agent.run(since="invalid-date")
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"Field: {e.field}, Value: {e.value}")
except NomadError as e:
    print(f"NOMAD error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Retry Logic

Automatic retry for transient errors:

```python
from utils.retry import retry_with_backoff

@retry_with_backoff(max_attempts=3, backoff_factor=2)
def call_claude_api(prompt):
    # API call with automatic retry
    pass

# Usage
result = call_claude_api("Analyze this threat intelligence")
```

## Authentication

### API Key Management

**Environment Configuration:**
```bash
# Required API keys
ANTHROPIC_API_KEY=sk-ant-api03-...
VIRUSTOTAL_API_KEY=...
SHODAN_API_KEY=...

# Optional API keys
CIRCL_API_KEY=...
ALIENVAULT_API_KEY=...
```

**Programmatic Access:**
```python
from config.environment import config

# Validate API key
if not config.validate_api_key('anthropic'):
    raise ValueError("Invalid Anthropic API key")

# Get API key
api_key = config.get_api_key('anthropic')
```

### Service Authentication

**Claude API Authentication:**
```python
import anthropic

# Client initialization with key validation
client = anthropic.Anthropic(api_key=config.get_api_key('anthropic'))

# Test authentication
try:
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=10,
        messages=[{"role": "user", "content": "test"}]
    )
    print("Claude API authenticated successfully")
except anthropic.AuthenticationError:
    print("Claude API authentication failed")
```

## Rate Limiting

### Rate Limit Configuration

```yaml
# src/config/rate_limits.yml
rate_limits:
  anthropic:
    requests_per_minute: 100
    requests_per_day: 10000
    tokens_per_minute: 50000

  virustotal:
    requests_per_minute: 4  # Free tier
    requests_per_day: 1000

  default:
    requests_per_minute: 60
    requests_per_hour: 1000
```

### Rate Limiting in Code

```python
from utils.rate_limiter import RateLimiter

# Initialize rate limiter
limiter = RateLimiter()

# Check rate limit before API call
if not limiter.check_limit('anthropic'):
    wait_time = limiter.get_wait_time('anthropic')
    print(f"Rate limited. Wait {wait_time} seconds.")
    time.sleep(wait_time)

# Make API call
response = client.messages.create(...)

# Record API call
limiter.record_request('anthropic')
```

### Rate Limit Headers

API responses include rate limit information:

```json
{
  "data": {...},
  "rate_limit": {
    "requests_remaining": 95,
    "requests_limit": 100,
    "reset_time": "2025-09-13T11:00:00Z",
    "retry_after": null
  }
}
```

## Integration Examples

### External System Integration

**SIEM Integration:**
```python
import requests

class SIEMIntegration:
    def __init__(self, siem_endpoint, api_key):
        self.endpoint = siem_endpoint
        self.api_key = api_key

    def send_alert(self, intelligence_item):
        """Send intelligence to SIEM system"""
        payload = {
            'timestamp': intelligence_item['published_utc'],
            'source': intelligence_item['source_name'],
            'title': intelligence_item['title'],
            'severity': self._map_severity(intelligence_item),
            'cves': intelligence_item.get('cves', []),
            'tags': ['threat-intel', 'nomad']
        }

        response = requests.post(
            f"{self.endpoint}/api/alerts",
            json=payload,
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        response.raise_for_status()

# Usage
siem = SIEMIntegration('https://siem.company.com', api_key)
for item in intelligence_items:
    siem.send_alert(item)
```

**Ticketing System Integration:**
```python
class TicketingIntegration:
    def create_ticket(self, routing_decision):
        """Create ticket from routing decision"""
        ticket_data = {
            'title': f"Security Alert: {routing_decision['title']}",
            'description': self._format_description(routing_decision),
            'priority': routing_decision['priority'],
            'assignee': self._get_assignee(routing_decision['owner_team']),
            'labels': ['security', 'threat-intel', 'nomad'],
            'due_date': self._calculate_due_date(routing_decision['sla_hours'])
        }

        # Create ticket via API
        response = self.ticket_api.create(ticket_data)
        return response['ticket_id']
```

### Webhook Integration

**Incoming Webhooks:**
```python
from flask import Flask, request
from agents.rss_feed_agent import RSSFeedAgent

app = Flask(__name__)

@app.route('/api/webhook/threat-intel', methods=['POST'])
def threat_intel_webhook():
    """Process incoming threat intelligence webhooks"""
    data = request.get_json()

    # Validate webhook data
    if not validate_webhook_signature(request):
        return {'error': 'Invalid signature'}, 403

    # Process intelligence
    rss_agent = RSSFeedAgent()
    result = rss_agent.process_external_intelligence(data)

    return {'status': 'processed', 'items': len(result['intelligence'])}

def validate_webhook_signature(request):
    """Validate webhook HMAC signature"""
    # Implementation depends on webhook provider
    pass
```

**Outgoing Webhooks:**
```python
class WebhookSender:
    def __init__(self, webhook_urls):
        self.webhook_urls = webhook_urls

    def send_intelligence_update(self, intelligence_items):
        """Send intelligence updates to configured webhooks"""
        payload = {
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'nomad',
            'event_type': 'intelligence_update',
            'data': {
                'items_count': len(intelligence_items),
                'high_priority_count': len([i for i in intelligence_items
                                           if i.get('priority') == 'high']),
                'items': intelligence_items[:10]  # Send sample
            }
        }

        for url in self.webhook_urls:
            try:
                requests.post(url, json=payload, timeout=30)
            except Exception as e:
                self.logger.warning(f"Webhook delivery failed: {url} - {e}")
```

## SDK Usage

### Python SDK

**Installation:**
```bash
pip install nomad-threat-intel
```

**Basic Usage:**
```python
from nomad import NomadClient

# Initialize client
client = NomadClient(api_key='your-anthropic-key')

# Collect intelligence
intelligence = client.collect_intelligence(
    since='2025-09-12T00:00:00Z',
    priority='high'
)

# Route intelligence
decisions = client.route_intelligence(intelligence)

# Generate reports
report = client.generate_ciso_report(
    week_start='2025-09-07',
    week_end='2025-09-13',
    decisions=decisions
)
```

**Advanced Usage:**
```python
# Custom agent configuration
config = {
    'organization': {
        'name': 'Acme Corp',
        'crown_jewels': ['Exchange', 'Database'],
        'business_sectors': ['Financial Services']
    },
    'rss_feeds': [
        {'url': 'https://custom-feed.com/rss', 'priority': 'high'}
    ]
}

client = NomadClient(config=config)

# Custom processing workflow
workflow = client.create_workflow([
    ('collect', {'agent': 'rss_feed', 'priority': 'high'}),
    ('enrich', {'agent': 'enrichment', 'sources': ['nvd', 'cisa']}),
    ('route', {'agent': 'orchestrator'}),
    ('alert', {'agent': 'technical_alert'})
])

result = client.execute_workflow(workflow)
```

### REST API Client

**JavaScript/Node.js:**
```javascript
const NomadClient = require('nomad-client');

const client = new NomadClient({
    baseUrl: 'https://nomad-api.company.com',
    apiKey: process.env.NOMAD_API_KEY
});

// Collect intelligence
const intelligence = await client.intelligence.collect({
    since: '2025-09-12T00:00:00Z',
    priority: 'high'
});

// Route decisions
const decisions = await client.intelligence.route(intelligence.data);

console.log(`Processed ${intelligence.data.length} intelligence items`);
console.log(`Generated ${decisions.data.length} routing decisions`);
```

**cURL Examples:**
```bash
# Collect intelligence
curl -X POST https://nomad-api.company.com/api/v1/intelligence/collect \
  -H "Authorization: Bearer $NOMAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "since": "2025-09-12T00:00:00Z",
    "until": "2025-09-13T00:00:00Z",
    "priority": "high"
  }'

# Get agent status
curl -H "Authorization: Bearer $NOMAD_API_KEY" \
  https://nomad-api.company.com/api/v1/src/agents/status

# Generate CISO report
curl -X POST https://nomad-api.company.com/api/v1/reports/ciso \
  -H "Authorization: Bearer $NOMAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "week_start": "2025-09-07",
    "week_end": "2025-09-13"
  }'
```

---

## API Versioning

### Version Strategy

NOMAD APIs use semantic versioning:
- **Major version**: Breaking changes
- **Minor version**: New features (backward compatible)
- **Patch version**: Bug fixes

**Current Version:** `v1.0.0`

### Version Headers

Include version in all requests:
```bash
curl -H "API-Version: v1" https://api.nomad.com/intelligence
```

### Deprecation Policy

- Deprecated features: 6 months notice
- Breaking changes: Major version increment
- Migration guides provided

---

## OpenAPI Specification

### Complete OpenAPI 3.0 Schema

```yaml
openapi: 3.0.0
info:
  title: NOMAD Threat Intelligence API
  description: API for the NOMAD Threat Intelligence Framework
  version: 1.0.0
  contact:
    name: NOMAD Development Team
    url: https://github.com/nomad-threat-intel

servers:
  - url: https://api.nomad.local/v1
    description: Local development server
  - url: https://nomad-api.company.com/v1
    description: Production server

paths:
  /intelligence/collect:
    post:
      summary: Collect threat intelligence
      description: Collect and process threat intelligence from RSS feeds
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/IntelligenceRequest'
      responses:
        '200':
          description: Intelligence collected successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IntelligenceResponse'

  /intelligence/route:
    post:
      summary: Route intelligence items
      description: Process intelligence items and generate routing decisions
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RoutingRequest'
      responses:
        '200':
          description: Routing completed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RoutingResponse'

components:
  schemas:
    IntelligenceRequest:
      type: object
      required:
        - since
        - until
      properties:
        since:
          type: string
          format: date-time
          description: Start datetime for intelligence collection
        until:
          type: string
          format: date-time
          description: End datetime for intelligence collection
        priority:
          type: string
          enum: [low, medium, high]
          default: medium
        source_type:
          type: string
          enum: [rss, vendor, cert, api]
        use_llm:
          type: boolean
          default: true

    IntelligenceResponse:
      type: object
      properties:
        agent_type:
          type: string
        timestamp:
          type: string
          format: date-time
        intelligence:
          type: array
          items:
            $ref: '#/components/schemas/IntelligenceItem'
        stats:
          $ref: '#/components/schemas/ProcessingStats'

    IntelligenceItem:
      type: object
      required:
        - source_type
        - source_name
        - source_url
        - title
        - published_utc
        - admiralty_source_reliability
        - admiralty_info_credibility
        - dedupe_key
      properties:
        source_type:
          type: string
          enum: [rss, vendor, cert, api]
        source_name:
          type: string
        source_url:
          type: string
          format: uri
        title:
          type: string
        summary:
          type: string
          maxLength: 300
        published_utc:
          type: string
          format: date-time
        cves:
          type: array
          items:
            type: string
            pattern: '^CVE-\d{4}-\d{4,7}$'
        cvss_v3:
          type: number
          minimum: 0
          maximum: 10
        kev_listed:
          type: boolean
        admiralty_source_reliability:
          type: string
          enum: [A, B, C, D, E, F]
        admiralty_info_credibility:
          type: integer
          minimum: 1
          maximum: 6
        dedupe_key:
          type: string

  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Authorization
      description: API key authentication (Bearer token)

security:
  - ApiKeyAuth: []
```

---

This comprehensive API documentation provides all the information needed to integrate with and extend the NOMAD Threat Intelligence Framework. For additional examples and implementation details, refer to the source code and other documentation sections.