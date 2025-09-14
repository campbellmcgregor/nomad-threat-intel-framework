# NOMAD Advanced Workflows

This guide demonstrates complex multi-agent workflows and advanced usage patterns for the NOMAD framework.

## Table of Contents
- [Multi-Agent Pipelines](#multi-agent-pipelines)
- [Conditional Routing](#conditional-routing)
- [Parallel Processing](#parallel-processing)
- [Custom Workflow Creation](#custom-workflow-creation)
- [Integration Patterns](#integration-patterns)
- [Performance Optimization](#performance-optimization)

## Multi-Agent Pipelines

### Complex Intelligence Processing Pipeline

```python
#!/usr/bin/env python3
"""
Advanced pipeline that processes multiple intelligence sources,
enriches data, deduplicates, and generates multiple output formats.
"""

import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

from src.agents.rss_feed import RSSFeedAgent
from src.agents.vendor_parser import VendorParserAgent
from src.agents.enrichment import EnrichmentAgent
from src.agents.deduplication import DeduplicationAgent
from src.agents.orchestrator import OrchestratorAgent
from src.config.environment import config

async def advanced_intelligence_pipeline():
    """Run complete intelligence processing pipeline."""

    # Initialize agents
    rss_agent = RSSFeedAgent(config)
    vendor_agent = VendorParserAgent(config)
    enrichment_agent = EnrichmentAgent(config)
    dedup_agent = DeduplicationAgent(config)
    orchestrator = OrchestratorAgent(config)

    # Step 1: Collect from multiple sources in parallel
    print("Step 1: Collecting intelligence from multiple sources...")

    async def collect_rss():
        return await rss_agent.collect_feeds_async(
            priority='high',
            since=(datetime.utcnow() - timedelta(hours=24)).isoformat()
        )

    async def collect_vendor():
        return await vendor_agent.parse_bulletins_async(
            vendors=['microsoft', 'cisco', 'vmware']
        )

    # Parallel collection
    rss_data, vendor_data = await asyncio.gather(
        collect_rss(),
        collect_vendor()
    )

    # Step 2: Merge and deduplicate
    print("Step 2: Merging and deduplicating...")
    all_items = rss_data['items'] + vendor_data['items']
    deduplicated = await dedup_agent.process_async({
        'items': all_items,
        'similarity_threshold': 0.85
    })

    # Step 3: Enrich with threat intelligence
    print("Step 3: Enriching with threat intelligence...")
    enriched = await enrichment_agent.enrich_batch_async(
        deduplicated['unique_items'],
        sources=['nvd', 'epss', 'kev', 'mitre']
    )

    # Step 4: Route through orchestrator
    print("Step 4: Routing through orchestrator...")
    routing_decisions = await orchestrator.process_async({
        'items': enriched,
        'policy_config': {
            'cvss_threshold': config.ALERT_CVSS_THRESHOLD,
            'epss_threshold': config.ALERT_EPSS_THRESHOLD,
            'crown_jewels': config.CROWN_JEWELS
        }
    })

    # Step 5: Generate outputs based on routing
    print("Step 5: Generating outputs...")
    await generate_outputs(routing_decisions)

    return routing_decisions

async def generate_outputs(routing_decisions):
    """Generate different outputs based on routing decisions."""

    from src.agents.technical_alert import TechnicalAlertAgent
    from src.agents.ciso_report import CISOReportAgent
    from src.agents.watchlist_digest import WatchlistDigestAgent

    tech_alert_agent = TechnicalAlertAgent(config)
    ciso_agent = CISOReportAgent(config)
    watchlist_agent = WatchlistDigestAgent(config)

    # Filter items by routing decision
    tech_items = [item for item in routing_decisions['items']
                  if item['routing_decision'] == 'TECHNICAL_ALERT']
    ciso_items = [item for item in routing_decisions['items']
                  if item['routing_decision'] == 'CISO_REPORT']
    watchlist_items = [item for item in routing_decisions['items']
                       if item['routing_decision'] == 'WATCHLIST']

    # Generate outputs in parallel
    tasks = []

    if tech_items:
        tasks.append(tech_alert_agent.generate_alerts_async(tech_items))
    if ciso_items:
        tasks.append(ciso_agent.generate_report_async(ciso_items))
    if watchlist_items:
        tasks.append(watchlist_agent.generate_digest_async(watchlist_items))

    if tasks:
        await asyncio.gather(*tasks)

# Run the pipeline
if __name__ == "__main__":
    asyncio.run(advanced_intelligence_pipeline())
```

## Conditional Routing

### Dynamic Workflow Based on Threat Level

```python
#!/usr/bin/env python3
"""
Conditional workflow that adjusts processing based on threat severity.
"""

from src.utils.workflow_validator import WorkflowValidator
from src.agents.orchestrator import OrchestratorAgent

def conditional_threat_workflow(input_file):
    """Execute different workflows based on threat analysis."""

    validator = WorkflowValidator()
    orchestrator = OrchestratorAgent(config)

    # Load and validate input
    data = validator.load_json(input_file)

    # Initial assessment
    assessment = orchestrator.assess_threat_level(data)

    if assessment['level'] == 'CRITICAL':
        # Immediate response workflow
        execute_critical_response(data)
    elif assessment['level'] == 'HIGH':
        # Standard high-priority workflow
        execute_high_priority_workflow(data)
    elif assessment['level'] == 'MEDIUM':
        # Regular processing with monitoring
        execute_standard_workflow(data)
    else:
        # Low priority - batch processing
        queue_for_batch_processing(data)

def execute_critical_response(data):
    """Emergency response for critical threats."""

    # 1. Immediate notification
    send_critical_alert(data)

    # 2. Automated containment
    if config.AUTO_CONTAINMENT_ENABLED:
        initiate_containment_measures(data)

    # 3. Evidence collection
    collect_forensic_evidence(data)

    # 4. Stakeholder notification
    notify_stakeholders(data, priority='IMMEDIATE')

    # 5. Create incident ticket
    ticket_id = create_incident_ticket(data, priority='P1')

    return ticket_id
```

## Parallel Processing

### Concurrent Multi-Feed Processing

```python
#!/usr/bin/env python3
"""
Process multiple RSS feeds concurrently for improved performance.
"""

import concurrent.futures
from typing import List, Dict

def process_feeds_parallel(feed_urls: List[str]) -> Dict:
    """Process multiple feeds in parallel."""

    results = {
        'successful': [],
        'failed': [],
        'total_items': 0
    }

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all feeds for processing
        future_to_feed = {
            executor.submit(process_single_feed, url): url
            for url in feed_urls
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_feed):
            feed_url = future_to_feed[future]
            try:
                feed_data = future.result(timeout=30)
                results['successful'].append({
                    'url': feed_url,
                    'items': feed_data['items'],
                    'count': len(feed_data['items'])
                })
                results['total_items'] += len(feed_data['items'])
            except Exception as e:
                results['failed'].append({
                    'url': feed_url,
                    'error': str(e)
                })

    return results

def process_single_feed(feed_url: str) -> Dict:
    """Process a single RSS feed."""
    from src.agents.rss_feed import RSSFeedAgent

    agent = RSSFeedAgent(config)
    return agent.process_feed(feed_url, use_llm=True)
```

## Custom Workflow Creation

### Define Custom Workflow Configuration

```yaml
# custom_workflow.yaml
name: "zero_day_hunter"
description: "Specialized workflow for hunting zero-day vulnerabilities"
schedule: "*/30 * * * *"  # Every 30 minutes

stages:
  - name: "collect_bleeding_edge"
    agent: "rss_feed"
    config:
      sources:
        - "https://googleprojectzero.blogspot.com/feeds/posts/default"
        - "https://www.zerodayinitiative.com/rss/published"
      priority: "critical"

  - name: "cross_reference"
    agent: "enrichment"
    config:
      sources: ["nvd", "mitre", "exploit-db"]
      check_exploits: true

  - name: "threat_scoring"
    agent: "custom_scorer"
    config:
      algorithm: "zero_day_probability"
      threshold: 0.7

  - name: "alert_generation"
    agent: "technical_alert"
    condition: "threat_score >= 0.7"
    config:
      template: "zero_day_alert"
      notify: ["soc", "ciso", "vendor_relations"]

outputs:
  - type: "webhook"
    url: "${WEBHOOK_URL}"
  - type: "email"
    recipients: "${SECURITY_TEAM_EMAIL}"
  - type: "ticket"
    system: "jira"
```

### Custom Workflow Executor

```python
#!/usr/bin/env python3
"""
Execute custom workflow defined in YAML configuration.
"""

import yaml
from typing import Dict, Any

class CustomWorkflowExecutor:
    """Execute custom-defined workflows."""

    def __init__(self, workflow_file: str):
        with open(workflow_file, 'r') as f:
            self.workflow = yaml.safe_load(f)
        self.agents = self._initialize_agents()

    def _initialize_agents(self) -> Dict:
        """Initialize all required agents."""
        agents = {}
        for stage in self.workflow['stages']:
            agent_type = stage['agent']
            if agent_type not in agents:
                agents[agent_type] = self._create_agent(agent_type)
        return agents

    def execute(self) -> Dict[str, Any]:
        """Execute the complete workflow."""
        context = {'workflow': self.workflow['name']}

        for stage in self.workflow['stages']:
            # Check conditions
            if 'condition' in stage:
                if not self._evaluate_condition(stage['condition'], context):
                    continue

            # Execute stage
            result = self._execute_stage(stage, context)
            context[stage['name']] = result

        # Generate outputs
        self._generate_outputs(context)

        return context

    def _execute_stage(self, stage: Dict, context: Dict) -> Any:
        """Execute a single workflow stage."""
        agent = self.agents[stage['agent']]
        config = stage.get('config', {})

        # Substitute variables
        config = self._substitute_variables(config, context)

        # Execute agent
        return agent.process(config)
```

## Integration Patterns

### SOAR Platform Integration

```python
#!/usr/bin/env python3
"""
Integrate NOMAD with SOAR platforms (Splunk Phantom, Demisto, etc.)
"""

class SOARIntegration:
    """SOAR platform integration for NOMAD."""

    def __init__(self, platform: str, api_config: Dict):
        self.platform = platform
        self.api_config = api_config
        self.client = self._init_client()

    def send_to_soar(self, nomad_output: Dict):
        """Send NOMAD output to SOAR platform."""

        if self.platform == 'phantom':
            return self._send_to_phantom(nomad_output)
        elif self.platform == 'demisto':
            return self._send_to_demisto(nomad_output)
        elif self.platform == 'resilient':
            return self._send_to_resilient(nomad_output)

    def _send_to_phantom(self, data: Dict):
        """Send to Splunk Phantom."""

        # Transform to Phantom event format
        phantom_event = {
            'name': f"NOMAD Alert - {data['title']}",
            'type': 'threat_intelligence',
            'severity': self._map_severity(data['cvss_score']),
            'artifacts': self._create_artifacts(data),
            'custom_fields': {
                'nomad_id': data['dedupe_key'],
                'routing_decision': data['routing_decision'],
                'admiralty_rating': f"{data['admiralty_source']}{data['admiralty_info']}"
            }
        }

        # Create container
        response = self.client.create_container(phantom_event)

        # Trigger playbook if critical
        if data['routing_decision'] == 'TECHNICAL_ALERT':
            self.client.run_playbook(
                container_id=response['id'],
                playbook_name='nomad_threat_response'
            )

        return response
```

### Slack/Teams Notification Integration

```python
#!/usr/bin/env python3
"""
Send NOMAD alerts to Slack or Microsoft Teams.
"""

import json
import requests
from typing import Dict

class ChatNotification:
    """Send notifications to chat platforms."""

    def __init__(self, platform: str, webhook_url: str):
        self.platform = platform
        self.webhook_url = webhook_url

    def send_alert(self, alert_data: Dict):
        """Send formatted alert to chat platform."""

        if self.platform == 'slack':
            message = self._format_slack_message(alert_data)
        elif self.platform == 'teams':
            message = self._format_teams_message(alert_data)
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

        response = requests.post(
            self.webhook_url,
            json=message,
            headers={'Content-Type': 'application/json'}
        )

        return response.status_code == 200

    def _format_slack_message(self, data: Dict) -> Dict:
        """Format message for Slack."""

        severity_emoji = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }

        return {
            'blocks': [
                {
                    'type': 'header',
                    'text': {
                        'type': 'plain_text',
                        'text': f"{severity_emoji.get(data['severity'], '⚪')} NOMAD Security Alert"
                    }
                },
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f"*{data['title']}*\n{data['summary']}"
                    }
                },
                {
                    'type': 'section',
                    'fields': [
                        {'type': 'mrkdwn', 'text': f"*CVEs:*\n{', '.join(data['cves'])}"},
                        {'type': 'mrkdwn', 'text': f"*CVSS:*\n{data['cvss_score']}"},
                        {'type': 'mrkdwn', 'text': f"*EPSS:*\n{data['epss']:.2%}"},
                        {'type': 'mrkdwn', 'text': f"*Status:*\n{data['exploit_status']}"}
                    ]
                },
                {
                    'type': 'actions',
                    'elements': [
                        {
                            'type': 'button',
                            'text': {'type': 'plain_text', 'text': 'View Details'},
                            'url': data['source_url']
                        },
                        {
                            'type': 'button',
                            'text': {'type': 'plain_text', 'text': 'Create Ticket'},
                            'url': f"{config.TICKET_SYSTEM_URL}/create?nomad_id={data['dedupe_key']}"
                        }
                    ]
                }
            ]
        }
```

## Performance Optimization

### Caching Strategy

```python
#!/usr/bin/env python3
"""
Implement caching for improved performance.
"""

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

class IntelligenceCache:
    """Cache intelligence data to reduce API calls."""

    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str, max_age_hours: int = 24) -> Optional[Dict]:
        """Retrieve cached data if not expired."""

        cache_file = self.cache_dir / f"{self._hash_key(key)}.json"

        if not cache_file.exists():
            return None

        # Check age
        file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if file_age > timedelta(hours=max_age_hours):
            cache_file.unlink()  # Delete expired cache
            return None

        with open(cache_file, 'r') as f:
            return json.load(f)

    def set(self, key: str, data: Dict):
        """Store data in cache."""

        cache_file = self.cache_dir / f"{self._hash_key(key)}.json"

        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _hash_key(self, key: str) -> str:
        """Generate cache key hash."""
        return hashlib.sha256(key.encode()).hexdigest()[:16]

# Use cache in agents
class CachedEnrichmentAgent:
    """Enrichment agent with caching."""

    def __init__(self, config):
        self.config = config
        self.cache = IntelligenceCache()

    def enrich_cve(self, cve_id: str) -> Dict:
        """Enrich CVE with caching."""

        # Check cache first
        cached = self.cache.get(f"cve:{cve_id}", max_age_hours=48)
        if cached:
            return cached

        # Fetch from API
        enriched = self._fetch_cve_data(cve_id)

        # Store in cache
        self.cache.set(f"cve:{cve_id}", enriched)

        return enriched
```

### Batch Processing Optimization

```python
#!/usr/bin/env python3
"""
Optimize processing with batching strategies.
"""

from typing import List, Dict
import asyncio

class BatchProcessor:
    """Process items in optimized batches."""

    def __init__(self, batch_size: int = 50):
        self.batch_size = batch_size

    async def process_items(self, items: List[Dict], processor_func) -> List[Dict]:
        """Process items in batches for optimal performance."""

        results = []

        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]

            # Process batch concurrently
            batch_results = await asyncio.gather(
                *[processor_func(item) for item in batch]
            )

            results.extend(batch_results)

            # Brief delay between batches to avoid rate limiting
            if i + self.batch_size < len(items):
                await asyncio.sleep(0.5)

        return results
```

## Next Steps

- Explore [Custom Agent Development](custom-agents.md) to extend NOMAD
- Review [API Documentation](../reference/api.md) for integration details
- See [Performance Guide](../reference/performance.md) for optimization tips