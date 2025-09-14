# NOMAD Agent Development Guide

Complete guide to creating custom agents for the NOMAD Threat Intelligence Framework.

## Table of Contents

- [Agent Development Overview](#agent-development-overview)
- [Creating Your First Agent](#creating-your-first-agent)
- [Agent Implementation Patterns](#agent-implementation-patterns)
- [Prompt Engineering](#prompt-engineering)
- [Testing Agents](#testing-agents)
- [Integration and Deployment](#integration-and-deployment)

## Agent Development Overview

### What is an Agent?

A NOMAD agent is a specialized module that performs a specific function in the threat intelligence pipeline:

- **Collection Agents**: Gather raw intelligence from external sources
- **Processing Agents**: Transform, enrich, or analyze intelligence data
- **Output Agents**: Generate reports, alerts, or formatted output
- **Utility Agents**: Provide supporting functionality (validation, archival, etc.)

### Agent Characteristics

All NOMAD agents share these characteristics:

- **Single Responsibility**: Each agent has one clear purpose
- **Standardized Interface**: Consistent input/output patterns
- **AI-Enhanced**: Can leverage Claude AI for intelligent processing
- **Configurable**: Support environment-specific configuration
- **Observable**: Comprehensive logging and error handling

### Agent Lifecycle

1. **Initialization**: Load configuration and setup dependencies
2. **Input Validation**: Verify input data meets requirements
3. **Processing**: Execute agent-specific logic
4. **AI Integration**: Optionally process with Claude AI
5. **Output Generation**: Format results according to schema
6. **Cleanup**: Log results and handle cleanup

## Creating Your First Agent

### Step 1: Agent Class Implementation

Create a new agent by inheriting from `BaseAgent`:

```python
# agents/threat_hunter.py
"""
Threat Hunter Agent - Identifies potential threats from intelligence data
"""

from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent
from config.environment import config

class ThreatHunterAgent(BaseAgent):
    """Agent for proactive threat hunting analysis"""

    def __init__(self):
        super().__init__("threat-hunter")

        # Agent-specific configuration
        self.hunting_patterns = self._load_hunting_patterns()
        self.ioc_extractors = self._setup_ioc_extractors()

    def run(self, input_file: str = None, hunting_focus: str = "apt",
            timeframe_days: int = 30) -> Dict[str, Any]:
        """
        Execute threat hunting analysis

        Args:
            input_file: Path to intelligence data file
            hunting_focus: Focus area (apt, malware, ransomware, etc.)
            timeframe_days: Analysis timeframe in days

        Returns:
            Threat hunting results with IOCs and TTPs
        """

        # Step 1: Load and validate input
        intelligence_data = self._load_input_data(input_file)

        # Step 2: Apply hunting patterns
        threat_indicators = self._extract_threat_indicators(
            intelligence_data, hunting_focus
        )

        # Step 3: Process with AI for enhanced analysis
        if self.claude_client:
            enhanced_analysis = self._enhance_with_ai(
                threat_indicators, hunting_focus
            )
        else:
            enhanced_analysis = self._basic_analysis(threat_indicators)

        # Step 4: Generate hunting report
        hunting_report = self._generate_hunting_report(
            enhanced_analysis, hunting_focus, timeframe_days
        )

        return {
            "agent_type": "threat_hunter",
            "processed_at_utc": self.get_timestamp(),
            "hunting_focus": hunting_focus,
            "timeframe_days": timeframe_days,
            "threat_indicators": threat_indicators,
            "hunting_report": hunting_report,
            "iocs_discovered": len(enhanced_analysis.get("iocs", [])),
            "ttps_identified": len(enhanced_analysis.get("ttps", []))
        }

    def _load_input_data(self, input_file: str) -> Dict[str, Any]:
        """Load intelligence data from input file"""
        if not input_file:
            raise ValueError("Input file required for threat hunting")

        return self.load_input(input_file)

    def _extract_threat_indicators(self, data: Dict[str, Any],
                                 focus: str) -> List[Dict]:
        """Extract threat indicators from intelligence data"""
        indicators = []

        intelligence_items = data.get("intelligence", [])
        for item in intelligence_items:
            # Extract IOCs using regex patterns
            iocs = self._extract_iocs(item.get("title", ""))
            iocs.extend(self._extract_iocs(item.get("summary", "")))

            if iocs:
                indicators.append({
                    "source_item": item.get("title"),
                    "source_url": item.get("source_url"),
                    "iocs": iocs,
                    "cves": item.get("cves", []),
                    "published_utc": item.get("published_utc")
                })

        return indicators

    def _extract_iocs(self, text: str) -> List[Dict]:
        """Extract IOCs from text using pattern matching"""
        iocs = []

        # IP addresses
        import re
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        for match in re.finditer(ip_pattern, text):
            iocs.append({
                "type": "ip",
                "value": match.group(),
                "context": text[max(0, match.start()-20):match.end()+20]
            })

        # Domain names
        domain_pattern = r'\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b'
        for match in re.finditer(domain_pattern, text):
            domain = match.group()
            if self._is_likely_malicious_domain(domain):
                iocs.append({
                    "type": "domain",
                    "value": domain,
                    "context": text[max(0, match.start()-20):match.end()+20]
                })

        # File hashes
        hash_patterns = {
            "md5": r'\b[a-f0-9]{32}\b',
            "sha1": r'\b[a-f0-9]{40}\b',
            "sha256": r'\b[a-f0-9]{64}\b'
        }

        for hash_type, pattern in hash_patterns.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                iocs.append({
                    "type": hash_type,
                    "value": match.group().lower(),
                    "context": text[max(0, match.start()-20):match.end()+20]
                })

        return iocs

    def _is_likely_malicious_domain(self, domain: str) -> bool:
        """Basic heuristics to identify potentially malicious domains"""
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf']
        suspicious_keywords = ['malware', 'phish', 'spam', 'temp']

        domain_lower = domain.lower()

        # Check for suspicious TLDs
        for tld in suspicious_tlds:
            if domain_lower.endswith(tld):
                return True

        # Check for suspicious keywords
        for keyword in suspicious_keywords:
            if keyword in domain_lower:
                return True

        return False

    def _enhance_with_ai(self, indicators: List[Dict], focus: str) -> Dict[str, Any]:
        """Use Claude AI to enhance threat analysis"""

        hunting_input = {
            "hunting_focus": focus,
            "threat_indicators": indicators,
            "analysis_request": "threat_hunting_analysis",
            "context": config.get_context_for_agents()
        }

        result = self.process_with_llm(hunting_input)

        if result.get("status") == "success":
            return result.get("response", {})
        else:
            self.logger.warning("AI enhancement failed, using basic analysis")
            return self._basic_analysis(indicators)

    def _basic_analysis(self, indicators: List[Dict]) -> Dict[str, Any]:
        """Basic threat analysis without AI enhancement"""

        # Group IOCs by type
        ioc_summary = {}
        for indicator in indicators:
            for ioc in indicator.get("iocs", []):
                ioc_type = ioc["type"]
                if ioc_type not in ioc_summary:
                    ioc_summary[ioc_type] = []
                ioc_summary[ioc_type].append(ioc["value"])

        # Basic threat classification
        threat_level = "LOW"
        if len(indicators) > 10:
            threat_level = "MEDIUM"
        if any("ransomware" in str(indicator).lower() for indicator in indicators):
            threat_level = "HIGH"

        return {
            "threat_level": threat_level,
            "ioc_summary": ioc_summary,
            "total_indicators": len(indicators),
            "analysis_method": "basic_heuristics"
        }

    def _generate_hunting_report(self, analysis: Dict[str, Any],
                               focus: str, timeframe: int) -> Dict[str, Any]:
        """Generate hunting report"""

        return {
            "executive_summary": f"Threat hunting analysis focused on {focus} over {timeframe} days",
            "key_findings": analysis.get("key_findings", []),
            "threat_level": analysis.get("threat_level", "LOW"),
            "recommended_actions": analysis.get("recommendations", []),
            "ioc_summary": analysis.get("ioc_summary", {}),
            "hunting_queries": self._generate_hunting_queries(analysis),
            "next_steps": [
                "Deploy hunting queries to SIEM",
                "Monitor for IOC matches",
                "Investigate positive hits",
                "Update threat intelligence feeds"
            ]
        }

    def _generate_hunting_queries(self, analysis: Dict[str, Any]) -> List[Dict]:
        """Generate SIEM hunting queries based on analysis"""
        queries = []

        ioc_summary = analysis.get("ioc_summary", {})

        # Generate queries for different IOC types
        if "ip" in ioc_summary:
            ips = ioc_summary["ip"][:10]  # Limit to top 10
            query = f"src_ip IN ({', '.join(repr(ip) for ip in ips)}) OR dest_ip IN ({', '.join(repr(ip) for ip in ips)})"
            queries.append({
                "type": "ip_hunting",
                "query": query,
                "description": "Hunt for suspicious IP addresses"
            })

        if "domain" in ioc_summary:
            domains = ioc_summary["domain"][:10]
            query = f"dns_query IN ({', '.join(repr(d) for d in domains)})"
            queries.append({
                "type": "dns_hunting",
                "query": query,
                "description": "Hunt for suspicious domain queries"
            })

        return queries

    def _load_hunting_patterns(self) -> Dict[str, Any]:
        """Load hunting patterns configuration"""
        # This would load from a configuration file
        return {
            "apt_patterns": [],
            "malware_patterns": [],
            "ransomware_patterns": []
        }

    def _setup_ioc_extractors(self) -> Dict[str, Any]:
        """Setup IOC extraction tools"""
        return {
            "regex_patterns": {},
            "ml_classifiers": {}
        }
```

### Step 2: Create Agent Prompt

Create a prompt file for AI-enhanced processing:

```markdown
<!-- threat-hunter-prompt.md -->
# THREAT HUNTER AGENT

You are a threat hunting specialist analyzing intelligence data to identify potential threats and generate hunting hypotheses.

## INPUT FORMAT
```json
{
  "hunting_focus": "apt|malware|ransomware|insider_threat",
  "threat_indicators": [
    {
      "source_item": "Title of source intelligence",
      "source_url": "URL of source",
      "iocs": [
        {"type": "ip|domain|hash", "value": "indicator_value", "context": "surrounding text"}
      ],
      "cves": ["CVE-YYYY-XXXX"],
      "published_utc": "timestamp"
    }
  ],
  "context": {
    "org_name": "Organization name",
    "crown_jewels": ["Critical systems"],
    "business_sectors": ["Industry sectors"]
  }
}
```

## ANALYSIS REQUIREMENTS

1. **IOC Analysis**: Evaluate indicator quality and threat relevance
2. **TTP Mapping**: Map to MITRE ATT&CK techniques where applicable
3. **Threat Attribution**: Identify potential threat actors if patterns match
4. **Hunting Hypotheses**: Generate specific, testable hypotheses
5. **SIEM Queries**: Suggest detection queries for security tools

## OUTPUT FORMAT (Strict JSON)
```json
{
  "threat_assessment": {
    "overall_threat_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "confidence_score": 0.0-1.0,
    "threat_summary": "Brief summary of identified threats"
  },
  "key_findings": [
    {
      "finding": "Description of key finding",
      "evidence": ["Supporting evidence"],
      "threat_level": "LOW|MEDIUM|HIGH"
    }
  ],
  "ioc_analysis": {
    "high_confidence": ["IOCs with high confidence"],
    "medium_confidence": ["IOCs with medium confidence"],
    "false_positives": ["Likely false positive IOCs"]
  },
  "ttp_mapping": [
    {
      "technique": "T1055",
      "technique_name": "Process Injection",
      "evidence": "Evidence linking to this technique"
    }
  ],
  "hunting_hypotheses": [
    {
      "hypothesis": "Testable hunting hypothesis",
      "rationale": "Why this hypothesis is worth investigating",
      "hunting_queries": ["Suggested SIEM/EDR queries"],
      "expected_artifacts": ["What to look for"]
    }
  ],
  "recommendations": [
    "Specific actionable recommendations for threat hunting team"
  ]
}
```

## GUIDELINES

- Focus on actionable intelligence that hunters can investigate
- Prioritize high-confidence IOCs over quantity
- Provide specific, testable hunting hypotheses
- Include rationale for threat level assessments
- Generate SIEM-ready hunting queries when possible
```

### Step 3: Create Execution Script

Create a standalone execution script:

```python
#!/usr/bin/env python3
# scripts/run_threat_hunter.py
"""
Direct execution script for Threat Hunter Agent
"""

import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import agents
sys.path.append(str(Path(__file__).parent.parent))

from agents.threat_hunter import ThreatHunterAgent
from config.environment import config

def main():
    parser = argparse.ArgumentParser(description="Run NOMAD Threat Hunter Agent directly")

    # Input options
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to intelligence data file (or '-' for stdin)"
    )

    # Analysis options
    parser.add_argument(
        "--focus",
        choices=["apt", "malware", "ransomware", "insider_threat", "all"],
        default="apt",
        help="Threat hunting focus area"
    )

    parser.add_argument(
        "--timeframe",
        type=int,
        default=30,
        help="Analysis timeframe in days"
    )

    # Output options
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: auto-generated)"
    )

    parser.add_argument(
        "--format",
        choices=["json", "report", "queries"],
        default="json",
        help="Output format"
    )

    # Processing options
    parser.add_argument(
        "--use-ai",
        action="store_true",
        help="Use AI enhancement for analysis"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    import logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("🔍 NOMAD Threat Hunter Agent - Direct Execution")
    print("=" * 50)

    try:
        # Initialize agent
        agent = ThreatHunterAgent()
        print(f"✓ Threat Hunter Agent initialized")

        # Validate API access if using AI
        if args.use_ai and not config.anthropic_api_key:
            print("❌ AI enhancement requested but no ANTHROPIC_API_KEY found")
            print("   Set your API key in .env file or disable --use-ai")
            return 1

        # Load input data
        if args.input == "-":
            print("📥 Reading input from stdin...")
            input_data = json.loads(sys.stdin.read())
            input_file = None
        else:
            input_file = args.input
            if not Path(input_file).exists():
                print(f"❌ Input file not found: {input_file}")
                return 1
            print(f"📥 Loading input from: {input_file}")

        print(f"🎯 Hunting focus: {args.focus}")
        print(f"📅 Timeframe: {args.timeframe} days")

        # Run threat hunting analysis
        print("🔍 Running threat hunting analysis...")
        result = agent.run(
            input_file=input_file,
            hunting_focus=args.focus,
            timeframe_days=args.timeframe
        )

        # Output results
        _output_results(result, args.format, args.output, args.focus)

        # Print summary
        print(f"✅ Threat Hunter Agent completed successfully")
        ioc_count = result.get("iocs_discovered", 0)
        ttp_count = result.get("ttps_identified", 0)
        print(f"   IOCs discovered: {ioc_count}")
        print(f"   TTPs identified: {ttp_count}")

        return 0

    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running Threat Hunter Agent: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def _output_results(result: dict, format_type: str, output_file: str, focus: str):
    """Output results in requested format"""

    # Generate filename if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/output/threat_hunter_result_{focus}_{timestamp}.json"

    # Ensure output directory exists
    config.ensure_directories()

    if format_type == "json":
        # Save as JSON
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"💾 Results saved to: {output_path}")

    elif format_type == "report":
        # Generate human-readable report
        _generate_hunting_report(result, output_file)

    elif format_type == "queries":
        # Output hunting queries only
        _output_hunting_queries(result, output_file)

def _generate_hunting_report(result: dict, output_file: str):
    """Generate human-readable hunting report"""

    report_file = output_file.replace('.json', '.md')
    hunting_report = result.get("hunting_report", {})

    with open(report_file, 'w') as f:
        f.write(f"# Threat Hunting Report\n\n")
        f.write(f"**Generated:** {result.get('processed_at_utc')}\n")
        f.write(f"**Focus:** {result.get('hunting_focus')}\n")
        f.write(f"**Timeframe:** {result.get('timeframe_days')} days\n\n")

        f.write(f"## Executive Summary\n")
        f.write(f"{hunting_report.get('executive_summary', 'No summary available')}\n\n")

        # Key findings
        key_findings = hunting_report.get('key_findings', [])
        if key_findings:
            f.write(f"## Key Findings\n")
            for finding in key_findings:
                f.write(f"- {finding}\n")
            f.write("\n")

        # IOC Summary
        ioc_summary = hunting_report.get('ioc_summary', {})
        if ioc_summary:
            f.write(f"## IOC Summary\n")
            for ioc_type, iocs in ioc_summary.items():
                f.write(f"- **{ioc_type.upper()}**: {len(iocs)} indicators\n")
            f.write("\n")

        # Hunting queries
        queries = hunting_report.get('hunting_queries', [])
        if queries:
            f.write(f"## Hunting Queries\n")
            for query in queries:
                f.write(f"### {query['type']}\n")
                f.write(f"**Description:** {query['description']}\n")
                f.write(f"```sql\n{query['query']}\n```\n\n")

    print(f"📄 Hunting report saved to: {report_file}")

def _output_hunting_queries(result: dict, output_file: str):
    """Output hunting queries in SQL format"""

    queries_file = output_file.replace('.json', '.sql')
    hunting_report = result.get("hunting_report", {})
    queries = hunting_report.get('hunting_queries', [])

    with open(queries_file, 'w') as f:
        f.write(f"-- Threat Hunting Queries\n")
        f.write(f"-- Generated: {result.get('processed_at_utc')}\n")
        f.write(f"-- Focus: {result.get('hunting_focus')}\n\n")

        for query in queries:
            f.write(f"-- {query['type']}: {query['description']}\n")
            f.write(f"{query['query']};\n\n")

    print(f"🔍 Hunting queries saved to: {queries_file}")

if __name__ == "__main__":
    exit(main())
```

### Step 4: Add to Workflow Configuration

Add your agent to the workflow system:

```yaml
# config/claude_agent_config.yaml
agents:
  threat_hunter:
    name: "Threat Hunter Agent"
    prompt_file: "threat-hunter-prompt.md"
    subagent_type: "general-purpose"
    description: "Proactive threat hunting and IOC analysis"
    input_required:
      - input_file
      - hunting_focus

workflows:
  threat_hunting:
    name: "Proactive Threat Hunting"
    description: "Weekly threat hunting analysis"
    steps:
      - agent: rss_feed
        config:
          since: "7 days ago"
          priority: high
      - agent: threat_hunter
        config:
          focus: apt
          timeframe: 7
      - agent: evidence_vault
```

## Agent Implementation Patterns

### Collection Agent Pattern

```python
class MyCollectionAgent(BaseAgent):
    """Template for collection agents"""

    def run(self, **kwargs) -> Dict[str, Any]:
        # 1. Connect to external source
        # 2. Fetch raw data
        # 3. Parse and normalize
        # 4. Apply deduplication
        # 5. Return standardized format
        pass
```

### Processing Agent Pattern

```python
class MyProcessingAgent(BaseAgent):
    """Template for processing agents"""

    def run(self, input_file: str, **kwargs) -> Dict[str, Any]:
        # 1. Load input data
        # 2. Validate input schema
        # 3. Process data (with optional AI)
        # 4. Apply business rules
        # 5. Return processed results
        pass
```

### Output Agent Pattern

```python
class MyOutputAgent(BaseAgent):
    """Template for output agents"""

    def run(self, input_data: Dict, **kwargs) -> Dict[str, Any]:
        # 1. Load input decisions/data
        # 2. Apply formatting templates
        # 3. Generate output (reports/alerts)
        # 4. Save to designated format
        # 5. Return generation results
        pass
```

## Prompt Engineering

### Effective Prompt Structure

1. **Role Definition**: Clearly define the AI's role and expertise
2. **Input Schema**: Specify exact input format expected
3. **Processing Requirements**: Detail what analysis to perform
4. **Output Schema**: Define exact JSON output structure
5. **Guidelines**: Provide specific guidance for edge cases

### Prompt Best Practices

```markdown
# Good Prompt Example

You are [SPECIFIC ROLE] with expertise in [DOMAIN].

## INPUT FORMAT
[Exact JSON schema with examples]

## ANALYSIS REQUIREMENTS
1. [Specific requirement with success criteria]
2. [Another specific requirement]

## OUTPUT FORMAT (Strict JSON)
[Exact expected output schema]

## GUIDELINES
- [Specific guideline for edge cases]
- [Quality criteria]
- [Error handling approach]
```

## Testing Agents

### Unit Testing

```python
# tests/test_threat_hunter.py
import pytest
from unittest.mock import patch, MagicMock
from agents.threat_hunter import ThreatHunterAgent

@pytest.fixture
def sample_intelligence_data():
    return {
        "intelligence": [
            {
                "title": "Malware Campaign Uses 192.168.1.100",
                "summary": "Threat actors using malicious-domain.tk",
                "source_url": "https://example.com/threat-report",
                "cves": ["CVE-2025-1234"],
                "published_utc": "2025-09-13T10:00:00Z"
            }
        ]
    }

def test_threat_hunter_initialization():
    agent = ThreatHunterAgent()
    assert agent.agent_name == "threat-hunter"
    assert hasattr(agent, 'hunting_patterns')

@patch('agents.threat_hunter.ThreatHunterAgent.load_input')
def test_ioc_extraction(mock_load, sample_intelligence_data):
    mock_load.return_value = sample_intelligence_data

    agent = ThreatHunterAgent()
    result = agent.run(input_file="test_file.json", hunting_focus="malware")

    assert result["agent_type"] == "threat_hunter"
    assert result["hunting_focus"] == "malware"
    assert "threat_indicators" in result

def test_ioc_extraction_patterns():
    agent = ThreatHunterAgent()

    # Test IP extraction
    iocs = agent._extract_iocs("Malicious IP 192.168.1.100 detected")
    ip_iocs = [ioc for ioc in iocs if ioc["type"] == "ip"]
    assert len(ip_iocs) == 1
    assert ip_iocs[0]["value"] == "192.168.1.100"

    # Test domain extraction
    iocs = agent._extract_iocs("Command and control server: evil-domain.tk")
    domain_iocs = [ioc for ioc in iocs if ioc["type"] == "domain"]
    assert len(domain_iocs) >= 1

@patch('agents.threat_hunter.ThreatHunterAgent.process_with_llm')
def test_ai_enhancement(mock_process_llm, sample_intelligence_data):
    mock_process_llm.return_value = {
        "status": "success",
        "response": {
            "threat_level": "HIGH",
            "key_findings": ["APT campaign detected"],
            "ioc_summary": {"ip": ["192.168.1.100"]}
        }
    }

    agent = ThreatHunterAgent()
    with patch.object(agent, 'load_input', return_value=sample_intelligence_data):
        result = agent.run(input_file="test.json")

    assert "hunting_report" in result
```

### Integration Testing

```python
# tests/test_threat_hunter_integration.py
import tempfile
import json
from pathlib import Path
from agents.threat_hunter import ThreatHunterAgent

def test_full_agent_execution():
    """Test complete agent execution with real data"""

    # Create test input file
    test_data = {
        "intelligence": [
            {
                "title": "APT29 Campaign Targets Financial Sector",
                "summary": "Threat actors using cozy-bear-c2.tk for C2 communications",
                "source_url": "https://example.com/apt29-report",
                "cves": [],
                "published_utc": "2025-09-13T10:00:00Z"
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name

    try:
        # Run agent
        agent = ThreatHunterAgent()
        result = agent.run(
            input_file=temp_file,
            hunting_focus="apt",
            timeframe_days=30
        )

        # Validate results
        assert result["agent_type"] == "threat_hunter"
        assert result["hunting_focus"] == "apt"
        assert "threat_indicators" in result
        assert "hunting_report" in result

        # Check IOC extraction
        assert result["iocs_discovered"] >= 0

    finally:
        # Clean up
        Path(temp_file).unlink()
```

## Integration and Deployment

### Adding to Workflow System

1. **Update Agent Registry**: Add to `config/claude_agent_config.yaml`
2. **Create Execution Script**: Add to `scripts/` directory
3. **Update Documentation**: Document agent capabilities
4. **Add Tests**: Create comprehensive test suite

### Deployment Checklist

- [ ] Agent class implements `BaseAgent` interface
- [ ] Prompt file created and tested
- [ ] Execution script with proper argument parsing
- [ ] Unit tests with good coverage
- [ ] Integration tests with real data
- [ ] Configuration added to workflow system
- [ ] Documentation updated
- [ ] Error handling implemented
- [ ] Logging configured properly

### Performance Considerations

1. **Memory Usage**: Monitor memory consumption with large datasets
2. **API Rate Limits**: Implement proper rate limiting for external APIs
3. **Caching**: Cache expensive operations when possible
4. **Batch Processing**: Process items in batches for efficiency
5. **Error Recovery**: Implement retry logic for transient failures

### Security Considerations

1. **Input Validation**: Validate all input data
2. **Output Sanitization**: Sanitize output to prevent injection
3. **API Key Security**: Never log or expose API keys
4. **Data Privacy**: Handle sensitive data appropriately
5. **Error Messages**: Don't expose sensitive info in errors

---

Your custom agent is now ready for integration into the NOMAD framework! The modular architecture makes it easy to add new capabilities while maintaining consistency with existing agents.