# Creating Custom NOMAD Agents

This guide demonstrates how to create custom agents to extend NOMAD's capabilities for your specific threat intelligence needs.

## Table of Contents
- [Agent Architecture](#agent-architecture)
- [Creating Your First Custom Agent](#creating-your-first-custom-agent)
- [Advanced Agent Features](#advanced-agent-features)
- [Prompt Engineering for Agents](#prompt-engineering-for-agents)
- [Testing Custom Agents](#testing-custom-agents)
- [Real-World Examples](#real-world-examples)

## Agent Architecture

### Base Agent Structure

Every NOMAD agent inherits from the `BaseAgent` class:

```python
from src.agents.base_agent import BaseAgent
from typing import Dict, Any, Optional

class CustomAgent(BaseAgent):
    """Template for custom agent implementation."""

    def __init__(self, config: Dict):
        """Initialize the custom agent."""
        super().__init__(config)
        self.agent_type = "custom_agent"
        self.prompt_file = "prompts/agents/custom-agent-prompt.md"

    def process(self, input_data: Dict) -> Dict:
        """Main processing method."""
        # Validate input
        self._validate_input(input_data)

        # Process with or without LLM
        if self.config.get('use_llm', False):
            result = self.process_with_llm(input_data)
        else:
            result = self._process_locally(input_data)

        # Validate output
        self._validate_output(result)

        return result

    def _validate_input(self, data: Dict):
        """Validate input data structure."""
        required_fields = ['items', 'config']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

    def _validate_output(self, data: Dict):
        """Validate output data structure."""
        if 'processed_items' not in data:
            raise ValueError("Output must contain 'processed_items'")

    def _process_locally(self, input_data: Dict) -> Dict:
        """Process without LLM (fallback or testing)."""
        # Implement your logic here
        return {'processed_items': input_data['items']}
```

## Creating Your First Custom Agent

### Example: Threat Actor Attribution Agent

```python
#!/usr/bin/env python3
"""
Custom agent for attributing threats to known threat actors.
"""

from src.agents.base_agent import BaseAgent
from typing import Dict, List, Optional
import re

class ThreatActorAttributionAgent(BaseAgent):
    """Attribute threats to known threat actors based on TTPs."""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.agent_type = "threat_actor_attribution"
        self.prompt_file = "prompts/agents/threat-actor-attribution-prompt.md"

        # Load threat actor database
        self.threat_actors = self._load_threat_actors()

    def _load_threat_actors(self) -> Dict:
        """Load threat actor profiles and TTPs."""
        return {
            'APT28': {
                'aliases': ['Fancy Bear', 'Sofacy', 'Sednit'],
                'ttps': ['T1566.001', 'T1583.006', 'T1071.001'],
                'targets': ['government', 'military', 'defense'],
                'tools': ['X-Agent', 'X-Tunnel', 'Mimikatz'],
                'indicators': ['sofacy', 'fancy bear', 'apt28']
            },
            'APT29': {
                'aliases': ['Cozy Bear', 'The Dukes', 'CozyDuke'],
                'ttps': ['T1055', 'T1070.004', 'T1027'],
                'targets': ['government', 'think tanks', 'healthcare'],
                'tools': ['WellMess', 'WellMail', 'Sunburst'],
                'indicators': ['cozy bear', 'apt29', 'nobelium']
            },
            'Lazarus': {
                'aliases': ['Hidden Cobra', 'Guardians of Peace'],
                'ttps': ['T1566.002', 'T1055.001', 'T1574.002'],
                'targets': ['financial', 'cryptocurrency', 'entertainment'],
                'tools': ['DRATzarus', 'Bankshot', 'WannaCry'],
                'indicators': ['lazarus', 'hidden cobra', 'dprk']
            }
        }

    def process(self, input_data: Dict) -> Dict:
        """Attribute threats to actors."""

        items = input_data.get('items', [])
        attributed_items = []

        for item in items:
            # Try local attribution first
            attribution = self._attribute_locally(item)

            # Use LLM for complex attribution
            if not attribution and self.config.get('use_llm', False):
                attribution = self._attribute_with_llm(item)

            # Add attribution to item
            item['threat_actor_attribution'] = attribution
            attributed_items.append(item)

        return {
            'items': attributed_items,
            'attribution_stats': self._calculate_stats(attributed_items)
        }

    def _attribute_locally(self, item: Dict) -> Optional[Dict]:
        """Attempt local attribution based on indicators."""

        text_to_analyze = f"{item.get('title', '')} {item.get('summary', '')}".lower()
        attributions = []

        for actor_name, profile in self.threat_actors.items():
            confidence = 0

            # Check for direct indicators
            for indicator in profile['indicators']:
                if indicator in text_to_analyze:
                    confidence += 40

            # Check for tool mentions
            for tool in profile['tools']:
                if tool.lower() in text_to_analyze:
                    confidence += 20

            # Check target alignment
            for target in profile['targets']:
                if target in text_to_analyze:
                    confidence += 10

            if confidence >= 50:
                attributions.append({
                    'actor': actor_name,
                    'confidence': min(confidence, 100),
                    'aliases': profile['aliases'],
                    'reasoning': 'Pattern matching on indicators and tools'
                })

        # Return highest confidence attribution
        if attributions:
            return max(attributions, key=lambda x: x['confidence'])

        return None

    def _attribute_with_llm(self, item: Dict) -> Optional[Dict]:
        """Use LLM for sophisticated attribution analysis."""

        prompt_data = {
            'threat_intel': item,
            'known_actors': self.threat_actors,
            'analysis_request': 'Analyze TTPs and attribute to threat actor'
        }

        result = self.process_with_llm(prompt_data)

        if result and 'attribution' in result:
            return result['attribution']

        return None

    def _calculate_stats(self, items: List[Dict]) -> Dict:
        """Calculate attribution statistics."""

        stats = {
            'total_items': len(items),
            'attributed': 0,
            'high_confidence': 0,
            'actor_breakdown': {}
        }

        for item in items:
            if item.get('threat_actor_attribution'):
                stats['attributed'] += 1
                attribution = item['threat_actor_attribution']

                if attribution['confidence'] >= 80:
                    stats['high_confidence'] += 1

                actor = attribution['actor']
                stats['actor_breakdown'][actor] = stats['actor_breakdown'].get(actor, 0) + 1

        return stats
```

### Creating the Prompt Template

```markdown
# Threat Actor Attribution Agent

## Role
You are an expert threat intelligence analyst specializing in threat actor attribution and TTP analysis.

## Input Schema
```json
{
  "threat_intel": {
    "title": "string",
    "summary": "string",
    "cves": ["CVE-YYYY-XXXX"],
    "affected_products": [...],
    "evidence_excerpt": "string"
  },
  "known_actors": {
    "actor_name": {
      "aliases": [...],
      "ttps": [...],
      "targets": [...],
      "tools": [...]
    }
  }
}
```

## Task
Analyze the threat intelligence and attribute it to a known threat actor if possible.

## Analysis Steps
1. Extract TTPs from the threat description
2. Identify targeted sectors or organizations
3. Recognize tools, malware, or infrastructure
4. Compare with known threat actor profiles
5. Assess confidence level (0-100)

## Output Schema
```json
{
  "attribution": {
    "actor": "string or null",
    "confidence": 0-100,
    "aliases": ["string"],
    "reasoning": "detailed explanation",
    "ttps_identified": ["TXXXX.XXX"],
    "alternative_attributions": [
      {
        "actor": "string",
        "confidence": 0-100,
        "reasoning": "string"
      }
    ]
  },
  "analysis": {
    "sophistication_level": "low|medium|high|advanced",
    "likely_motivation": "financial|espionage|hacktivism|destruction",
    "targeted_sectors": ["string"],
    "campaign_indicators": ["string"]
  }
}
```

## Guidelines
- Only attribute with confidence >= 50
- Provide alternative attributions when multiple actors are possible
- Include detailed reasoning for transparency
- Consider false flag operations
- Note: "Unknown" is a valid attribution when evidence is insufficient
```

## Advanced Agent Features

### Async Processing Support

```python
import asyncio
from typing import List, Dict

class AsyncCustomAgent(BaseAgent):
    """Agent with async processing capabilities."""

    async def process_async(self, input_data: Dict) -> Dict:
        """Asynchronous processing method."""

        items = input_data['items']

        # Process items concurrently
        tasks = [self._process_item_async(item) for item in items]
        processed_items = await asyncio.gather(*tasks)

        return {'processed_items': processed_items}

    async def _process_item_async(self, item: Dict) -> Dict:
        """Process single item asynchronously."""

        # Simulate async operation (e.g., API call)
        await asyncio.sleep(0.1)

        # Add your processing logic
        item['processed'] = True
        item['timestamp'] = datetime.utcnow().isoformat()

        return item
```

### State Management

```python
class StatefulAgent(BaseAgent):
    """Agent that maintains state across invocations."""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load persistent state from storage."""
        state_file = Path(f"data/state/{self.agent_type}.json")

        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)

        return {
            'last_run': None,
            'items_processed': 0,
            'error_count': 0
        }

    def _save_state(self):
        """Persist state to storage."""
        state_file = Path(f"data/state/{self.agent_type}.json")
        state_file.parent.mkdir(parents=True, exist_ok=True)

        with open(state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def process(self, input_data: Dict) -> Dict:
        """Process with state management."""

        # Update state
        self.state['last_run'] = datetime.utcnow().isoformat()
        self.state['items_processed'] += len(input_data.get('items', []))

        try:
            result = self._process_items(input_data)
        except Exception as e:
            self.state['error_count'] += 1
            raise
        finally:
            self._save_state()

        return result
```

## Prompt Engineering for Agents

### Structured Prompt Design

```python
class PromptEngineeredAgent(BaseAgent):
    """Agent with advanced prompt engineering."""

    def build_prompt(self, input_data: Dict) -> str:
        """Build optimized prompt for LLM."""

        # Load base prompt template
        with open(self.prompt_file, 'r') as f:
            base_prompt = f.read()

        # Add context-specific instructions
        context = self._build_context(input_data)

        # Add few-shot examples
        examples = self._get_relevant_examples(input_data)

        # Combine into final prompt
        final_prompt = f"""
{base_prompt}

## Context
{json.dumps(context, indent=2)}

## Examples
{self._format_examples(examples)}

## Input Data
{json.dumps(input_data, indent=2)}

## Instructions
- Follow the output schema exactly
- Include confidence scores for all assessments
- Provide reasoning for decisions
- Return valid JSON only
"""
        return final_prompt

    def _build_context(self, input_data: Dict) -> Dict:
        """Build contextual information for prompt."""
        return {
            'organization': self.config.get('ORG_NAME'),
            'crown_jewels': self.config.get('CROWN_JEWELS'),
            'risk_tolerance': self.config.get('RISK_TOLERANCE'),
            'timestamp': datetime.utcnow().isoformat()
        }

    def _get_relevant_examples(self, input_data: Dict) -> List[Dict]:
        """Retrieve relevant few-shot examples."""
        # Implementation would retrieve similar examples
        # from a database or file
        return []
```

## Testing Custom Agents

### Unit Testing Framework

```python
import unittest
from unittest.mock import patch, MagicMock

class TestCustomAgent(unittest.TestCase):
    """Test suite for custom agents."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            'ANTHROPIC_API_KEY': 'test-key',
            'use_llm': False
        }
        self.agent = CustomAgent(self.config)

    def test_input_validation(self):
        """Test input validation."""
        # Test missing required fields
        with self.assertRaises(ValueError):
            self.agent.process({})

        # Test valid input
        valid_input = {
            'items': [],
            'config': {}
        }
        # Should not raise
        self.agent._validate_input(valid_input)

    def test_local_processing(self):
        """Test processing without LLM."""
        input_data = {
            'items': [
                {'id': 1, 'title': 'Test threat'},
                {'id': 2, 'title': 'Another threat'}
            ],
            'config': {}
        }

        result = self.agent.process(input_data)

        self.assertIn('processed_items', result)
        self.assertEqual(len(result['processed_items']), 2)

    @patch('src.agents.base_agent.BaseAgent.process_with_llm')
    def test_llm_processing(self, mock_llm):
        """Test processing with LLM."""
        # Configure mock
        mock_llm.return_value = {
            'processed_items': [{'id': 1, 'enriched': True}]
        }

        # Enable LLM
        self.agent.config['use_llm'] = True

        input_data = {'items': [{'id': 1}], 'config': {}}
        result = self.agent.process(input_data)

        # Verify LLM was called
        mock_llm.assert_called_once()
        self.assertTrue(result['processed_items'][0]['enriched'])
```

### Integration Testing

```python
#!/usr/bin/env python3
"""
Integration test for custom agent.
"""

import json
from pathlib import Path

def test_agent_integration():
    """Test agent in realistic scenario."""

    # Load test data
    test_data = Path('tests/fixtures/sample_threats.json')
    with open(test_data, 'r') as f:
        input_data = json.load(f)

    # Initialize agent
    from src.agents.custom_agent import CustomAgent
    agent = CustomAgent(config)

    # Process data
    result = agent.process(input_data)

    # Validate results
    assert 'processed_items' in result
    assert len(result['processed_items']) > 0

    # Check output format
    for item in result['processed_items']:
        assert 'id' in item
        assert 'processed' in item

    print(f"✅ Integration test passed: {len(result['processed_items'])} items processed")

if __name__ == "__main__":
    test_agent_integration()
```

## Real-World Examples

### IOC Extraction Agent

```python
class IOCExtractionAgent(BaseAgent):
    """Extract Indicators of Compromise from threat intelligence."""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.agent_type = "ioc_extraction"

        # Compile regex patterns for IOCs
        self.patterns = {
            'ipv4': re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'ipv6': re.compile(r'(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}', re.IGNORECASE),
            'domain': re.compile(r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b', re.IGNORECASE),
            'url': re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+', re.IGNORECASE),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'md5': re.compile(r'\b[a-f0-9]{32}\b', re.IGNORECASE),
            'sha1': re.compile(r'\b[a-f0-9]{40}\b', re.IGNORECASE),
            'sha256': re.compile(r'\b[a-f0-9]{64}\b', re.IGNORECASE)
        }

    def process(self, input_data: Dict) -> Dict:
        """Extract IOCs from threat intelligence."""

        items = input_data.get('items', [])
        extracted_iocs = []

        for item in items:
            text = f"{item.get('title', '')} {item.get('summary', '')} {item.get('evidence_excerpt', '')}"
            iocs = self._extract_iocs(text)

            if iocs:
                extracted_iocs.append({
                    'source_id': item.get('dedupe_key'),
                    'source_title': item.get('title'),
                    'iocs': iocs,
                    'extraction_timestamp': datetime.utcnow().isoformat()
                })

        return {
            'extracted_iocs': extracted_iocs,
            'total_iocs': sum(len(item['iocs']) for item in extracted_iocs),
            'ioc_types': self._summarize_ioc_types(extracted_iocs)
        }

    def _extract_iocs(self, text: str) -> Dict[str, List[str]]:
        """Extract IOCs using regex patterns."""

        iocs = {}

        for ioc_type, pattern in self.patterns.items():
            matches = pattern.findall(text)
            if matches:
                # Deduplicate and clean
                unique_matches = list(set(matches))
                iocs[ioc_type] = unique_matches

        return iocs
```

### Risk Scoring Agent

```python
class RiskScoringAgent(BaseAgent):
    """Calculate custom risk scores based on organization context."""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.agent_type = "risk_scoring"
        self.crown_jewels = config.get('CROWN_JEWELS', '').split(',')

    def process(self, input_data: Dict) -> Dict:
        """Calculate risk scores for threats."""

        items = input_data.get('items', [])
        scored_items = []

        for item in items:
            risk_score = self._calculate_risk_score(item)
            item['risk_score'] = risk_score
            item['risk_level'] = self._get_risk_level(risk_score)
            scored_items.append(item)

        # Sort by risk score
        scored_items.sort(key=lambda x: x['risk_score'], reverse=True)

        return {
            'scored_items': scored_items,
            'high_risk_count': len([i for i in scored_items if i['risk_level'] == 'CRITICAL']),
            'average_risk_score': sum(i['risk_score'] for i in scored_items) / len(scored_items) if scored_items else 0
        }

    def _calculate_risk_score(self, item: Dict) -> float:
        """Calculate risk score (0-100)."""

        score = 0

        # Base score from CVSS
        cvss = item.get('cvss_v3') or item.get('cvss_v4') or 0
        score += cvss * 5  # Max 50 points from CVSS

        # EPSS probability
        epss = item.get('epss', 0)
        score += epss * 20  # Max 20 points from EPSS

        # KEV listing
        if item.get('kev_listed'):
            score += 15

        # Exploit status
        exploit_status = item.get('exploit_status', '')
        if exploit_status == 'ITW':
            score += 15
        elif exploit_status == 'PoC':
            score += 10

        # Crown jewel impact
        affected_products = item.get('affected_products', [])
        for product in affected_products:
            product_name = product.get('product', '').lower()
            if any(jewel.lower() in product_name for jewel in self.crown_jewels):
                score += 10
                break

        return min(score, 100)  # Cap at 100

    def _get_risk_level(self, score: float) -> str:
        """Map score to risk level."""
        if score >= 80:
            return 'CRITICAL'
        elif score >= 60:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'
```

## Best Practices

### 1. Error Handling

```python
class RobustAgent(BaseAgent):
    """Agent with comprehensive error handling."""

    def process(self, input_data: Dict) -> Dict:
        """Process with error recovery."""

        try:
            # Validate input
            self._validate_input(input_data)
        except ValueError as e:
            # Try to fix common issues
            input_data = self._fix_input(input_data)

        results = []
        errors = []

        for item in input_data.get('items', []):
            try:
                processed = self._process_item(item)
                results.append(processed)
            except Exception as e:
                # Log error but continue processing
                errors.append({
                    'item_id': item.get('id'),
                    'error': str(e)
                })

        return {
            'successful': results,
            'errors': errors,
            'success_rate': len(results) / (len(results) + len(errors)) if results or errors else 0
        }
```

### 2. Performance Monitoring

```python
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor agent performance."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()

        try:
            result = func(self, *args, **kwargs)
            duration = time.time() - start_time

            # Log performance metrics
            self._log_performance({
                'method': func.__name__,
                'duration': duration,
                'items_processed': len(result.get('items', [])),
                'items_per_second': len(result.get('items', [])) / duration if duration > 0 else 0
            })

            return result
        except Exception as e:
            duration = time.time() - start_time
            self._log_performance({
                'method': func.__name__,
                'duration': duration,
                'error': str(e)
            })
            raise

    return wrapper
```

## Next Steps

- Review [Agent Development Guide](../developer-guide/agent-development.md) for detailed specifications
- Check [Testing Guide](../developer-guide/testing.md) for comprehensive testing strategies
- See [API Documentation](../reference/api.md) for integration interfaces