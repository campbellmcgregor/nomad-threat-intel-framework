# NOMAD Prompt Engineering Guide

Comprehensive guide for creating, optimizing, and managing AI prompts in the NOMAD Threat Intelligence Framework.

## Table of Contents

- [Overview](#overview)
- [Prompt Architecture](#prompt-architecture)
- [Agent Prompt Templates](#agent-prompt-templates)
- [Design Principles](#design-principles)
- [Best Practices](#best-practices)
- [Advanced Techniques](#advanced-techniques)
- [Testing and Validation](#testing-and-validation)
- [Performance Optimization](#performance-optimization)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)
- [Custom Development](#custom-development)
- [Version Control](#version-control)
- [Integration](#integration)
- [Examples and Case Studies](#examples-and-case-studies)

## Overview

NOMAD's effectiveness relies heavily on well-crafted prompts that guide Claude AI to process threat intelligence with the precision and context awareness required for cybersecurity operations.

### Prompt Engineering Philosophy

**Domain-Specific Intelligence**
- Prompts are tailored for cybersecurity and threat intelligence
- Include specialized knowledge and terminology
- Focus on actionable intelligence over general information

**Structured Output**
- All prompts enforce JSON schema compliance
- Predictable, parseable responses
- Consistent data formats across agents

**Context Awareness**
- Organization-specific context integration
- Asset and business relevance
- Risk-based prioritization

**Quality Assurance**
- Admiralty rating system integration
- Source reliability assessment
- Evidence-based reasoning

### Key Prompt Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **Collection** | Gather and parse threat data | RSS Agent, Vendor Parser |
| **Analysis** | Process and enrich intelligence | Enrichment Agent, Dedup Agent |
| **Routing** | Make routing decisions | Orchestrator Agent |
| **Reporting** | Generate formatted outputs | CISO Report, Technical Alert |
| **Validation** | Quality control and verification | Validation Agent |

## Prompt Architecture

### Standard Prompt Structure

Every NOMAD prompt follows this consistent structure:

```markdown
# Agent Name

## Role and Objective
[Clear definition of agent's role and primary objective]

## Context
[Relevant background information and domain knowledge]

## Input Format
[Expected input data structure and requirements]

## Processing Instructions
[Step-by-step processing guidelines]

## Output Format
[Required JSON schema and response structure]

## Quality Standards
[Validation rules and quality criteria]

## Examples
[Representative input/output examples]
```

### Prompt Components

**System Message**
```markdown
You are a cybersecurity threat intelligence analyst specialized in [domain].
Your role is to [specific objective] with precision and domain expertise.

You must:
- Follow cybersecurity best practices
- Apply Admiralty rating standards
- Generate structured JSON output
- Provide evidence-based reasoning
```

**Context Section**
```markdown
## Organizational Context
- Organization: {org_name}
- Crown Jewels: {crown_jewels}
- Business Sectors: {business_sectors}
- Risk Tolerance: {risk_tolerance}

## Threat Landscape
- Current threat level: {threat_level}
- Active campaigns: {active_campaigns}
- Priority vulnerabilities: {priority_vulnerabilities}
```

**Processing Guidelines**
```markdown
## Processing Steps
1. Validate input data structure
2. Extract key threat indicators
3. Apply domain expertise and context
4. Assign appropriate ratings and classifications
5. Generate structured output
6. Include reasoning and evidence
```

**Output Schema**
```json
{
  "required_fields": ["field1", "field2"],
  "schema": {
    "type": "object",
    "properties": {
      "field1": {"type": "string"},
      "field2": {"type": "array"}
    }
  }
}
```

## Agent Prompt Templates

### RSS Feed Agent Prompt

The RSS Feed Agent processes RSS/Atom feeds and extracts structured threat intelligence.

**Key Features:**
- CVE extraction and validation
- Admiralty rating assignment
- Deduplication key generation
- Source reliability assessment

**Prompt Structure:**
```markdown
# RSS Feed Threat Intelligence Agent

You are a cybersecurity threat intelligence analyst specializing in RSS/Atom feed processing.

## Objective
Parse RSS/Atom feeds containing security advisories, vulnerability reports, and threat intelligence. Extract and structure information according to the NOMAD intelligence schema.

## Core Competencies
- CVE identification and validation (CVE-YYYY-NNNNN format)
- Admiralty Code assessment (source reliability A-F, information credibility 1-6)
- Threat severity evaluation
- Asset and business impact assessment
- Deduplication and normalization

## Processing Guidelines

### 1. CVE Extraction
- Identify all CVE references using pattern: CVE-\d{4}-\d{4,7}
- Validate CVE format and year ranges (1999-current)
- Extract from title, description, and content

### 2. Admiralty Rating Assignment

**Source Reliability (A-F):**
- A: Official vendor, CERT/NCSC/CISA
- B: Major security organizations (Microsoft MSRC, Cisco Talos, Unit42)
- C: Reputable security media and researchers
- D: Community forums, unverified blogs
- E-F: Unreliable sources (automatically drop)

**Information Credibility (1-6):**
- 1: Primary source with vendor confirmation
- 2: Advisory/CERT with solid evidence
- 3: Newsroom/researcher with citations
- 4: Social media, unverified claims
- 5-6: Unreliable information (automatically drop)

### 3. Business Context Application
Consider organizational context:
- Crown Jewels: {crown_jewels}
- Business Sectors: {business_sectors}
- Risk Tolerance: {risk_tolerance}

## Output Requirements

Generate JSON with this exact structure:

```json
{
  "agent_type": "rss_feed",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "parameters": {
    "since": "datetime",
    "until": "datetime",
    "priority": "string"
  },
  "intelligence": [
    {
      "source_type": "rss",
      "source_name": "string",
      "source_url": "https://...",
      "title": "string",
      "summary": "string (≤60 words)",
      "published_utc": "YYYY-MM-DDTHH:MM:SSZ",
      "cves": ["CVE-YYYY-XXXX"],
      "cvss_v3": null|float,
      "epss": null|float,
      "kev_listed": true|false|null,
      "exploit_status": "ITW|PoC|None|null",
      "affected_products": [
        {
          "vendor": "string",
          "product": "string",
          "versions": ["string"]
        }
      ],
      "evidence_excerpt": "direct quote from source",
      "admiralty_source_reliability": "A-F",
      "admiralty_info_credibility": 1-6,
      "admiralty_reason": "justification",
      "dedupe_key": "sha256 hash of title+source_url"
    }
  ],
  "stats": {
    "total_items": 0,
    "processed_items": 0,
    "dropped_items": 0,
    "deduped_items": 0
  }
}
```

## Quality Standards
- Never guess unknown values (use null)
- Evidence excerpts must be direct quotes
- Admiralty ratings must include reasoning
- All CVEs must match exact pattern
- Dedupe keys must be consistent and unique

## Example Processing
Input RSS item about Windows vulnerability:
- Extract: CVE-2024-12345
- Rate: Source=Microsoft (A), Info=Official advisory (1)
- Summarize: Critical RCE in Windows affecting versions X-Y
- Generate consistent dedupe key
```

### Orchestrator Agent Prompt

The Orchestrator Agent makes routing decisions based on threat intelligence analysis.

**Prompt Structure:**
```markdown
# Orchestrator Threat Intelligence Router

You are a senior cybersecurity analyst responsible for routing threat intelligence to appropriate teams with proper prioritization and SLA assignment.

## Mission-Critical Objective
Analyze threat intelligence items and make precise routing decisions that ensure:
- Critical threats reach appropriate teams within SLA requirements
- Resources are allocated efficiently based on actual risk
- Business context drives decision-making
- False positives are minimized

## Organizational Context
- Organization: {org_name}
- Crown Jewels: {crown_jewels}
- Business Sectors: {business_sectors}
- Compliance Requirements: {compliance_frameworks}

## Routing Logic (Apply in Strict Order)

### 1. DROP Criteria (Immediate)
- Source reliability: E or F
- Information credibility: 5 or 6
- Clearly false positive or irrelevant

### 2. TECHNICAL_ALERT Criteria
Route to SOC/IT Operations if ANY of:
- KEV-listed vulnerabilities (CISA Known Exploited)
- EPSS ≥ 0.70 (high exploitation probability)
- Exploit status: "ITW" (In The Wild) AND affects crown jewels
- CVSS ≥ 9.0 AND affects organization assets

### 3. CISO_REPORT Criteria
Route to executive leadership if ANY of:
- CVSS ≥ 9.0 with business impact
- Affects critical business processes
- Regulatory/compliance implications
- Reputational risk potential
- Nation-state attribution

### 4. WATCHLIST (Default)
Monitor but no immediate action required:
- Medium severity items
- Informational intelligence
- Future threat indicators

## Team Assignment Logic

**SOC Team:** Real-time monitoring, incident response
- Technical alerts requiring immediate action
- Active exploitation scenarios
- IOC implementation needs

**Vuln Mgmt Team:** Patch management, risk assessment
- Vulnerability disclosures
- Patch availability notifications
- Risk scoring updates

**IT Operations:** Infrastructure protection
- System-level vulnerabilities
- Configuration changes needed
- Network security updates

**CISO Team:** Strategic decision-making
- High-impact business decisions
- Executive briefings required
- Policy implications

## SLA Assignment

**P0 (4 hours):** Active exploitation of crown jewels
**P1 (24 hours):** KEV-listed or EPSS ≥ 0.70 affecting assets
**P2 (72 hours):** High CVSS with asset exposure
**P3 (1 week):** Medium severity with context relevance
**P4 (Monitor):** Informational or low relevance

## Output Format

```json
{
  "agent_type": "orchestrator",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "decisions": [
    {
      "intelligence_id": "string",
      "routing_decision": "DROP|WATCHLIST|TECHNICAL_ALERT|CISO_REPORT",
      "reasoning": "detailed justification with specific criteria",
      "owner_team": "SOC|Vuln Mgmt|IT Ops|CISO",
      "sla_hours": 4|24|72|168,
      "priority": "P0|P1|P2|P3|P4",
      "business_impact": "Critical|High|Medium|Low",
      "asset_exposure": "Crown Jewels|Business Critical|Standard|None",
      "recommended_actions": ["specific action items"]
    }
  ],
  "routing_stats": {
    "total_items": 0,
    "dropped": 0,
    "technical_alert": 0,
    "ciso_report": 0,
    "watchlist": 0
  },
  "organizational_risk_factors": ["context-specific risk factors"]
}
```

## Decision Quality Standards
- Every decision must reference specific routing criteria
- Business context must influence routing
- SLA assignment must reflect actual urgency
- Reasoning must be audit-ready and defensible
```

### CISO Report Agent Prompt

**Prompt Structure:**
```markdown
# CISO Executive Report Generator

You are a senior cybersecurity executive assistant specializing in transforming technical threat intelligence into strategic executive communications.

## Executive Communication Objective
Create concise, actionable executive reports that enable C-level decision-making without technical jargon while maintaining accuracy and urgency.

## Report Structure Requirements

### Executive Summary (2-3 bullet points)
- Business impact in terms executives understand
- Immediate actions required
- Risk to business objectives

### Threat Landscape Overview
- Key threats relevant to business
- Trend analysis and implications
- Competitive/industry context

### Immediate Actions Required
- Specific, time-bound recommendations
- Resource requirements
- Success metrics

### Strategic Recommendations
- Long-term security posture improvements
- Investment priorities
- Risk mitigation strategies

## Output Format

```json
{
  "agent_type": "ciso_report",
  "report_period": {
    "week_start": "YYYY-MM-DD",
    "week_end": "YYYY-MM-DD"
  },
  "executive_summary": {
    "key_threats": ["executive-friendly threat descriptions"],
    "business_impact": "quantified risk in business terms",
    "immediate_actions": ["specific actions with timelines"],
    "confidence_level": "High|Medium|Low"
  },
  "threat_landscape": {
    "critical_trends": ["threat trends affecting business"],
    "industry_context": "sector-specific threat intelligence",
    "attribution": "threat actor information if relevant"
  },
  "risk_assessment": {
    "crown_jewels_exposure": "assessment of critical asset risk",
    "business_process_impact": "operational risk evaluation",
    "regulatory_implications": "compliance and legal considerations"
  },
  "recommendations": {
    "immediate": ["actions required within 48 hours"],
    "short_term": ["actions required within 30 days"],
    "strategic": ["longer-term security investments"]
  },
  "metrics": {
    "threats_processed": 0,
    "high_priority_count": 0,
    "mean_time_to_action": "hours",
    "sla_compliance": "percentage"
  }
}
```

## Executive Communication Standards
- Use business language, not technical jargon
- Quantify risk in financial or operational terms
- Include specific, actionable recommendations
- Provide clear success criteria
- Focus on business enablement, not just protection
```

## Design Principles

### 1. Specificity Over Generality

**Good:**
```
Analyze this Windows vulnerability for impact on Microsoft Active Directory
domain controllers running Windows Server 2019 in a financial services environment.
```

**Bad:**
```
Analyze this security vulnerability for general impact.
```

### 2. Structured Output Enforcement

**Always specify exact JSON schema:**
```json
{
  "required": ["field1", "field2"],
  "properties": {
    "field1": {
      "type": "string",
      "enum": ["value1", "value2"]
    },
    "field2": {
      "type": "number",
      "minimum": 0,
      "maximum": 10
    }
  }
}
```

### 3. Context Integration

**Include organizational context:**
```markdown
## Organizational Context
- Crown Jewels: {crown_jewels}
- Business Sectors: {business_sectors}
- Compliance: {compliance_frameworks}
- Risk Tolerance: {risk_tolerance}
```

### 4. Evidence-Based Reasoning

**Require supporting evidence:**
```markdown
## Reasoning Requirements
- Quote specific evidence from sources
- Reference authoritative cybersecurity frameworks
- Explain decision logic clearly
- Provide confidence levels
```

### 5. Quality Control Integration

**Built-in validation:**
```markdown
## Quality Standards
- Validate all CVE formats before inclusion
- Verify dates are within reasonable ranges
- Ensure admiralty ratings have justification
- Check for required fields completion
```

## Best Practices

### Domain Expertise Integration

**Cybersecurity Knowledge Base:**
```markdown
## Threat Intelligence Context
- MITRE ATT&CK Framework: Reference relevant TTPs
- NIST Cybersecurity Framework: Align with functions
- CIS Controls: Consider implementation priorities
- OWASP Top 10: Web application security focus
```

**Industry-Specific Context:**
```markdown
## Financial Services Context
- PCI DSS compliance requirements
- FFIEC guidance considerations
- High-value transaction security
- Customer data protection priorities

## Healthcare Context
- HIPAA compliance implications
- Patient safety considerations
- Medical device security
- Business continuity requirements
```

### Prompt Modularity

**Reusable Components:**
```markdown
## Standard Admiralty Rating Module
{include: admiralty_rating_guidelines.md}

## Standard CVE Extraction Module
{include: cve_extraction_rules.md}

## Standard Business Context Module
{include: business_context_template.md}
```

### Error Handling Patterns

**Graceful Degradation:**
```markdown
## Error Handling
If unable to determine a required field:
1. Use null for missing numeric values
2. Use "Unknown" for missing string values
3. Include error in processing_notes field
4. Continue processing other fields
5. Never fabricate data
```

## Advanced Techniques

### Chain-of-Thought Reasoning

**For Complex Decisions:**
```markdown
## Reasoning Process
Analyze this threat intelligence step by step:

1. **Source Assessment**: Evaluate source reliability and credibility
   - Check against known reliable sources list
   - Assess publication venue and author credentials
   - Consider potential bias or agenda

2. **Technical Analysis**: Extract and validate technical details
   - Identify and validate CVE references
   - Assess CVSS scores and exploitability
   - Determine affected products and versions

3. **Business Context**: Apply organizational context
   - Map to crown jewels and critical assets
   - Consider business sector specific risks
   - Evaluate compliance implications

4. **Risk Calculation**: Determine priority and routing
   - Calculate composite risk score
   - Apply organizational risk tolerance
   - Determine appropriate response team

5. **Action Recommendation**: Specify concrete next steps
   - Immediate actions required
   - Timeline and resource requirements
   - Success metrics and validation
```

### Few-Shot Learning Examples

**Include representative examples:**
```markdown
## Example 1: High-Severity Windows Vulnerability

**Input:**
RSS item about CVE-2024-12345 affecting Windows Server

**Analysis:**
- Source: Microsoft Security Response Center (Reliability: A)
- CVSS: 9.8 (Critical)
- Exploitation: Active in the wild
- Affected: Windows Server 2019/2022

**Output:**
```json
{
  "routing_decision": "TECHNICAL_ALERT",
  "reasoning": "KEV-listed critical vulnerability affecting Windows servers in production",
  "owner_team": "SOC",
  "sla_hours": 24,
  "priority": "P1"
}
```

## Testing and Validation

### Prompt Testing Framework

**Test Categories:**

**Functional Tests:**
```python
def test_cve_extraction():
    """Test CVE pattern recognition and validation"""
    test_cases = [
        {
            "input": "Critical vulnerability CVE-2024-12345 discovered",
            "expected": ["CVE-2024-12345"]
        },
        {
            "input": "Multiple CVEs: CVE-2024-1111, CVE-2024-2222",
            "expected": ["CVE-2024-1111", "CVE-2024-2222"]
        }
    ]
```

**Quality Tests:**
```python
def test_admiralty_rating_consistency():
    """Test consistent admiralty rating assignment"""
    test_sources = [
        ("https://www.cisa.gov/advisory", "A", 1),
        ("https://unit42.paloaltonetworks.com", "B", 2),
        ("https://random-blog.com", "C", 3)
    ]
```

**Output Validation:**
```python
def test_output_schema_compliance():
    """Test JSON schema compliance"""
    response = agent.process(test_input)
    validate_json_schema(response, agent_schema)
    assert all(required_field in response for required_field in required_fields)
```

### A/B Testing Prompts

**Comparative Evaluation:**
```python
def compare_prompt_versions():
    """Compare effectiveness of different prompt versions"""
    test_cases = load_test_intelligence_items()

    results_v1 = []
    results_v2 = []

    for item in test_cases:
        result_v1 = process_with_prompt_v1(item)
        result_v2 = process_with_prompt_v2(item)

        results_v1.append(evaluate_quality(result_v1))
        results_v2.append(evaluate_quality(result_v2))

    return compare_results(results_v1, results_v2)
```

### Human Evaluation Framework

**Expert Review Process:**
```markdown
## Prompt Quality Evaluation Criteria

**Accuracy (1-5):**
- Technical details correctly extracted
- CVEs properly identified and validated
- Threat severity appropriately assessed

**Relevance (1-5):**
- Business context properly applied
- Organizational priorities reflected
- Industry-specific considerations included

**Completeness (1-5):**
- All required fields populated
- Evidence and reasoning provided
- Follow-up actions specified

**Consistency (1-5):**
- Similar inputs produce similar outputs
- Admiralty ratings applied consistently
- Decision logic follows established criteria
```

## Performance Optimization

### Token Efficiency

**Minimize Token Usage:**
```markdown
# Before (verbose)
You are a highly experienced cybersecurity threat intelligence analyst with extensive knowledge of vulnerability assessment, threat hunting, and risk management who specializes in analyzing RSS feeds...

# After (concise)
You are a cybersecurity analyst specializing in RSS threat intelligence processing.
```

**Use Abbreviations for Repeated Concepts:**
```markdown
## Abbreviations
- TI: Threat Intelligence
- CVE: Common Vulnerabilities and Exposures
- CVSS: Common Vulnerability Scoring System
- KEV: Known Exploited Vulnerabilities
- TTPs: Tactics, Techniques, and Procedures
```

### Caching Strategies

**Template Caching:**
```python
class PromptCache:
    def __init__(self):
        self._template_cache = {}
        self._context_cache = {}

    def get_prompt_template(self, agent_type: str) -> str:
        """Get cached prompt template"""
        if agent_type not in self._template_cache:
            self._template_cache[agent_type] = load_template(agent_type)
        return self._template_cache[agent_type]

    def get_context_variables(self, org_id: str) -> dict:
        """Get cached organization context"""
        cache_key = f"org_context_{org_id}"
        if cache_key not in self._context_cache:
            self._context_cache[cache_key] = load_org_context(org_id)
        return self._context_cache[cache_key]
```

### Streaming Response Optimization

**Progressive Output Processing:**
```python
async def process_intelligence_stream(intelligence_items):
    """Process intelligence items in streaming fashion"""

    prompt_template = get_cached_template("rss_feed")

    async for item in intelligence_items:
        # Build prompt with current item
        prompt = build_prompt(prompt_template, item)

        # Stream processing
        async for chunk in anthropic_client.stream_completion(prompt):
            if is_complete_json(chunk):
                yield parse_intelligence_response(chunk)
```

## Common Patterns

### Conditional Logic Patterns

**Multi-Criteria Decision Making:**
```markdown
## Routing Decision Logic
Evaluate in this order:

IF source_reliability in ['E', 'F'] OR info_credibility >= 5:
    RETURN "DROP"

ELIF kev_listed == true OR epss >= 0.70:
    RETURN "TECHNICAL_ALERT"

ELIF cvss_v3 >= 9.0 AND affects_crown_jewels:
    RETURN "CISO_REPORT"

ELSE:
    RETURN "WATCHLIST"
```

### Data Transformation Patterns

**Normalization Pattern:**
```markdown
## Data Normalization Rules

**CVE Format:**
- Input: "cve-2024-12345" → Output: "CVE-2024-12345"
- Input: "CVE-24-12345" → Output: null (invalid format)

**Date Normalization:**
- Input: "Wed, 13 Sep 2025 10:00:00 GMT" → Output: "2025-09-13T10:00:00Z"
- Input: "2025-09-13" → Output: "2025-09-13T00:00:00Z"

**Severity Mapping:**
- CVSS 9.0-10.0 → "Critical"
- CVSS 7.0-8.9 → "High"
- CVSS 4.0-6.9 → "Medium"
- CVSS 0.1-3.9 → "Low"
```

### Error Recovery Patterns

**Graceful Error Handling:**
```markdown
## Error Recovery Strategies

**Invalid CVE Format:**
```json
{
  "cves": [],
  "processing_notes": "Invalid CVE format detected: 'CVE-24-XXXX'",
  "data_quality_issues": ["invalid_cve_format"]
}
```

**Missing Required Data:**
```json
{
  "cvss_v3": null,
  "processing_notes": "CVSS score not available in source",
  "confidence_level": "Medium"
}
```

**Source Parsing Errors:**
```json
{
  "parsing_status": "partial_success",
  "extracted_fields": ["title", "cves"],
  "failed_fields": ["published_date"],
  "retry_recommended": true
}
```
```

## Troubleshooting

### Common Prompt Issues

**Issue: Inconsistent JSON Output**

*Symptoms:*
- Malformed JSON responses
- Missing required fields
- Unexpected data types

*Solutions:*
```markdown
## JSON Validation Enhancement
Add explicit JSON validation instructions:

CRITICAL: Your response must be valid JSON. Before responding:
1. Verify all required fields are present
2. Check data types match schema
3. Ensure proper JSON syntax
4. Validate against provided schema

Example of valid response structure:
```json
{
  "field1": "string_value",
  "field2": 123,
  "field3": ["array", "values"]
}
```
```

**Issue: Hallucinated CVEs or Data**

*Symptoms:*
- Non-existent CVE numbers
- Fabricated vulnerability details
- Made-up source information

*Solutions:*
```markdown
## Data Fabrication Prevention
Add strict accuracy requirements:

NEVER fabricate or guess data. If information is not explicitly present:
- Use null for missing numeric values
- Use "Unknown" for missing categorical data
- Include uncertainty in processing_notes
- Reference exact source quotes for evidence
- Mark confidence level as "Low" when uncertain
```

**Issue: Poor Admiralty Rating Consistency**

*Symptoms:*
- Same sources get different ratings
- Ratings don't match established criteria
- Missing rating justifications

*Solutions:*
```markdown
## Admiralty Rating Standardization
Include comprehensive source mapping:

## Known Source Reliability Mapping
- cisa.gov, ncsc.gov.uk → A (Official government)
- microsoft.com/security, vendor advisories → A-B
- unit42.paloaltonetworks.com, fireeye.com → B
- bleepingcomputer.com, threatpost.com → C
- reddit.com, unknown blogs → D
- Social media, unverified → E-F

ALWAYS provide justification for rating assignment.
```

### Debug Mode Prompts

**Enhanced Debugging Information:**
```markdown
## Debug Mode Instructions
When debug=true, include additional fields:

```json
{
  "debug_info": {
    "prompt_version": "rss_feed_v2.1",
    "processing_steps": [
      "Extracted 3 CVEs from title and description",
      "Assigned source reliability 'A' based on cisa.gov domain",
      "Applied business context for financial services sector"
    ],
    "decision_factors": {
      "kev_status": true,
      "epss_score": 0.85,
      "asset_exposure": "crown_jewels",
      "routing_trigger": "kev_listed_and_high_epss"
    },
    "confidence_indicators": {
      "source_confidence": 0.95,
      "extraction_confidence": 0.88,
      "routing_confidence": 0.92
    }
  }
}
```
```

### Prompt Validation Tools

**Automated Prompt Testing:**
```python
class PromptValidator:
    def __init__(self):
        self.test_cases = load_test_cases()
        self.schemas = load_schemas()

    def validate_prompt(self, prompt_template, agent_type):
        """Comprehensive prompt validation"""
        results = {
            'schema_compliance': 0,
            'response_quality': 0,
            'consistency_score': 0,
            'error_rate': 0
        }

        for test_case in self.test_cases[agent_type]:
            try:
                # Generate response
                response = generate_response(prompt_template, test_case.input)

                # Validate schema compliance
                if validate_json_schema(response, self.schemas[agent_type]):
                    results['schema_compliance'] += 1

                # Assess quality
                quality_score = assess_response_quality(
                    response, test_case.expected
                )
                results['response_quality'] += quality_score

            except Exception as e:
                results['error_rate'] += 1
                log_error(f"Prompt validation error: {e}")

        # Calculate percentages
        total_tests = len(self.test_cases[agent_type])
        for metric in results:
            results[metric] = (results[metric] / total_tests) * 100

        return results
```

## Custom Development

### Creating New Agent Prompts

**Development Process:**

1. **Define Agent Purpose**
```markdown
## Agent Specification
- **Name**: Custom Threat Hunter Agent
- **Purpose**: Identify APT indicators in threat intelligence
- **Input**: Processed threat intelligence items
- **Output**: APT attribution and hunting recommendations
- **Context**: Advanced persistent threat analysis
```

2. **Design Input/Output Schema**
```json
{
  "input_schema": {
    "type": "object",
    "required": ["intelligence_items"],
    "properties": {
      "intelligence_items": {
        "type": "array",
        "items": {"$ref": "#/definitions/IntelligenceItem"}
      }
    }
  },
  "output_schema": {
    "type": "object",
    "required": ["agent_type", "analysis"],
    "properties": {
      "agent_type": {"const": "threat_hunter"},
      "analysis": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "intelligence_id": {"type": "string"},
            "apt_indicators": {"type": "array"},
            "attribution_confidence": {"type": "number"},
            "hunting_queries": {"type": "array"}
          }
        }
      }
    }
  }
}
```

3. **Build Core Prompt**
```markdown
# APT Threat Hunter Agent

You are an advanced persistent threat (APT) analyst specializing in identifying nation-state and organized criminal threat actor indicators within threat intelligence.

## Core Mission
Analyze threat intelligence for APT indicators and provide actionable threat hunting guidance.

## APT Analysis Framework

### Attribution Indicators
- **TTPs**: MITRE ATT&CK technique patterns
- **Infrastructure**: Command and control patterns
- **Tooling**: Custom malware families and tools
- **Victimology**: Target selection patterns
- **Timeline**: Campaign activity windows

### Known APT Groups Reference
- APT1 (Comment Crew): Chinese PLA Unit 61398
- APT28 (Fancy Bear): Russian GRU Unit 26165
- APT29 (Cozy Bear): Russian SVR
- Lazarus Group: North Korean Reconnaissance General Bureau
- [Include current APT group mappings]

## Processing Instructions

1. **Indicator Extraction**
   - Identify TTPs from threat descriptions
   - Extract infrastructure indicators (IPs, domains, certificates)
   - Catalog malware families and tool usage
   - Note targeting patterns and victim profiles

2. **Attribution Analysis**
   - Match indicators to known APT group profiles
   - Assess confidence levels based on overlap
   - Consider false flag possibilities
   - Account for tool sharing between groups

3. **Hunt Query Generation**
   - Create specific detection queries for SIEMs
   - Include network-based indicators
   - Provide host-based hunting guidance
   - Suggest threat intelligence pivots

## Output Format
[Detailed JSON schema]

## Quality Standards
- Attribution confidence must be justified
- Hunt queries must be actionable
- All indicators must be validated
- Include confidence levels for all assessments
```

4. **Test and Iterate**
```python
def test_custom_prompt():
    """Test custom APT hunter prompt"""
    test_intelligence = load_apt_test_cases()

    for case in test_intelligence:
        response = process_with_prompt(apt_hunter_prompt, case)

        # Validate response structure
        assert validate_schema(response, apt_hunter_schema)

        # Check attribution quality
        if case.expected_apt_group:
            assert response['analysis'][0]['attribution_confidence'] > 0.7

        # Verify hunting queries
        assert len(response['analysis'][0]['hunting_queries']) > 0
```

### Prompt Template System

**Template Inheritance:**
```markdown
# base_agent_template.md
## Common Instructions
{include: common_instructions.md}

## Organizational Context
{include: org_context_template.md}

## Quality Standards
{include: quality_standards.md}

# Specific Agent Template
{inherit: base_agent_template.md}

## Agent-Specific Instructions
[Custom instructions for this agent]

## Custom Output Format
[Agent-specific schema]
```

**Dynamic Context Injection:**
```python
class PromptTemplateEngine:
    def __init__(self):
        self.templates = {}
        self.context_providers = {}

    def render_prompt(self, template_name: str, context: dict) -> str:
        """Render prompt with dynamic context"""
        template = self.load_template(template_name)

        # Inject organizational context
        org_context = self.get_org_context(context.get('org_id'))
        template = template.format(**org_context)

        # Inject threat context
        threat_context = self.get_threat_context()
        template = template.format(**threat_context)

        # Inject dynamic variables
        template = template.format(**context)

        return template

    def get_org_context(self, org_id: str) -> dict:
        """Get organization-specific context"""
        return {
            'crown_jewels': get_crown_jewels(org_id),
            'business_sectors': get_business_sectors(org_id),
            'compliance_frameworks': get_compliance_requirements(org_id)
        }
```

## Version Control

### Prompt Versioning Strategy

**Semantic Versioning for Prompts:**
```
v1.0.0 - Initial production release
v1.1.0 - New feature added (backward compatible)
v1.1.1 - Bug fix (backward compatible)
v2.0.0 - Breaking change (output format changed)
```

**Version Control Structure:**
```
prompts/
├── rss_feed_agent/
│   ├── v1.0.0.md
│   ├── v1.1.0.md
│   ├── v2.0.0.md
│   └── current -> v2.0.0.md
├── orchestrator/
│   ├── v1.0.0.md
│   └── current -> v1.0.0.md
└── schemas/
    ├── rss_feed_v1.json
    └── rss_feed_v2.json
```

### Migration Management

**Prompt Migration Framework:**
```python
class PromptMigrationManager:
    def __init__(self):
        self.migrations = {}

    def register_migration(self, from_version: str, to_version: str):
        """Register a prompt migration"""
        def decorator(migration_func):
            self.migrations[(from_version, to_version)] = migration_func
            return migration_func
        return decorator

    @register_migration('v1.0.0', 'v2.0.0')
    def migrate_rss_agent_v1_to_v2(self, old_response: dict) -> dict:
        """Migrate RSS agent response from v1 to v2 format"""
        new_response = old_response.copy()

        # Add new required fields
        new_response['confidence_metrics'] = {
            'source_confidence': 0.8,
            'extraction_confidence': 0.9
        }

        # Rename fields
        if 'admiralty_rating' in new_response:
            new_response['admiralty_source_reliability'] = new_response.pop('admiralty_rating')

        return new_response
```

### A/B Testing Framework

**Prompt Comparison System:**
```python
class PromptABTester:
    def __init__(self):
        self.test_configs = {}
        self.results = {}

    def setup_test(self, test_name: str, prompt_a: str, prompt_b: str,
                   traffic_split: float = 0.5):
        """Set up A/B test between two prompt versions"""
        self.test_configs[test_name] = {
            'prompt_a': prompt_a,
            'prompt_b': prompt_b,
            'traffic_split': traffic_split,
            'active': True
        }

    def get_prompt_for_request(self, test_name: str, request_id: str) -> str:
        """Determine which prompt to use for this request"""
        if test_name not in self.test_configs:
            return self.test_configs['default']['prompt_a']

        config = self.test_configs[test_name]
        if not config['active']:
            return config['prompt_a']

        # Use consistent hash to assign users to groups
        hash_value = hash(request_id) % 100
        if hash_value < (config['traffic_split'] * 100):
            return config['prompt_a']
        else:
            return config['prompt_b']

    def record_result(self, test_name: str, request_id: str,
                     prompt_version: str, quality_metrics: dict):
        """Record test results for analysis"""
        if test_name not in self.results:
            self.results[test_name] = {'a': [], 'b': []}

        version_key = 'a' if prompt_version == 'prompt_a' else 'b'
        self.results[test_name][version_key].append(quality_metrics)
```

## Integration

### Claude API Integration

**Optimized API Usage:**
```python
class ClaudePromptProcessor:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.rate_limiter = RateLimiter(requests_per_minute=100)

    async def process_intelligence(self, prompt: str,
                                 intelligence_data: dict) -> dict:
        """Process intelligence with Claude API"""

        # Rate limiting
        await self.rate_limiter.acquire()

        # Build full prompt
        full_prompt = self.build_prompt(prompt, intelligence_data)

        try:
            # Make API call
            response = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.1,  # Low temperature for consistency
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )

            # Parse and validate response
            parsed_response = self.parse_response(response.content[0].text)
            self.validate_response_schema(parsed_response)

            return parsed_response

        except anthropic.RateLimitError:
            # Handle rate limiting with exponential backoff
            await asyncio.sleep(2 ** attempt)
            return await self.process_intelligence(prompt, intelligence_data)

        except anthropic.APIError as e:
            # Handle API errors gracefully
            return {
                "error": True,
                "error_type": "api_error",
                "message": str(e),
                "fallback_processing": self.fallback_processing(intelligence_data)
            }

    def build_prompt(self, template: str, data: dict) -> str:
        """Build complete prompt with context injection"""
        return template.format(
            intelligence_data=json.dumps(data, indent=2),
            org_context=self.get_org_context(),
            timestamp=datetime.utcnow().isoformat()
        )
```

### Streaming Response Handling

**Real-time Processing:**
```python
async def stream_intelligence_processing(intelligence_items):
    """Stream process multiple intelligence items"""

    async def process_item(item):
        prompt = build_rss_agent_prompt(item)

        async for chunk in anthropic_client.stream_completion(prompt):
            # Yield partial results as they become available
            if is_parseable_chunk(chunk):
                partial_result = parse_chunk(chunk)
                yield {
                    'item_id': item['id'],
                    'status': 'processing',
                    'partial_data': partial_result
                }

        # Final complete result
        yield {
            'item_id': item['id'],
            'status': 'complete',
            'result': complete_result
        }

    # Process multiple items concurrently
    async for result in asyncio.as_completed([
        process_item(item) for item in intelligence_items
    ]):
        yield result
```

## Examples and Case Studies

### Case Study 1: CISA KEV Processing

**Scenario**: Process CISA Known Exploited Vulnerabilities feed

**Input Intelligence Item:**
```json
{
  "source_type": "rss",
  "source_name": "CISA Known Exploited Vulnerabilities",
  "title": "CISA Adds CVE-2024-12345 to KEV Catalog",
  "description": "CISA has added CVE-2024-12345 affecting Microsoft Exchange Server to the Known Exploited Vulnerabilities catalog. This vulnerability allows remote code execution and is being actively exploited.",
  "link": "https://www.cisa.gov/kev/catalog/CVE-2024-12345"
}
```

**RSS Agent Processing:**
```json
{
  "source_type": "rss",
  "source_name": "CISA Known Exploited Vulnerabilities",
  "source_url": "https://www.cisa.gov/kev/catalog/CVE-2024-12345",
  "title": "CISA Adds CVE-2024-12345 to KEV Catalog",
  "summary": "CISA added CVE-2024-12345 affecting Microsoft Exchange to KEV catalog due to active exploitation",
  "published_utc": "2024-09-13T10:00:00Z",
  "cves": ["CVE-2024-12345"],
  "cvss_v3": null,
  "kev_listed": true,
  "kev_date_added": "2024-09-13",
  "exploit_status": "ITW",
  "affected_products": [
    {
      "vendor": "Microsoft",
      "product": "Exchange Server",
      "versions": ["2019", "2022"]
    }
  ],
  "evidence_excerpt": "is being actively exploited",
  "admiralty_source_reliability": "A",
  "admiralty_info_credibility": 1,
  "admiralty_reason": "Official CISA government advisory",
  "dedupe_key": "sha256_hash_of_title_and_url"
}
```

**Orchestrator Routing Decision:**
```json
{
  "routing_decision": "TECHNICAL_ALERT",
  "reasoning": "KEV-listed vulnerability with active exploitation (ITW) affecting Microsoft Exchange Server, which is a crown jewel system",
  "owner_team": "SOC",
  "sla_hours": 24,
  "priority": "P1",
  "business_impact": "Critical",
  "asset_exposure": "Crown Jewels",
  "recommended_actions": [
    "Immediately patch all Exchange servers",
    "Monitor Exchange logs for exploitation indicators",
    "Implement emergency access controls if patching delayed"
  ]
}
```

### Case Study 2: False Positive Handling

**Scenario**: Handle vendor marketing disguised as security advisory

**Input Intelligence Item:**
```json
{
  "source_type": "rss",
  "source_name": "Vendor Marketing Blog",
  "title": "Revolutionary New Security Feature Protects Against All Threats",
  "description": "Our amazing new product stops all cyber attacks with AI-powered protection. No vulnerabilities can bypass our system!",
  "link": "https://vendor-blog.com/marketing-post"
}
```

**RSS Agent Processing:**
```json
{
  "source_type": "rss",
  "source_name": "Vendor Marketing Blog",
  "source_url": "https://vendor-blog.com/marketing-post",
  "title": "Revolutionary New Security Feature Protects Against All Threats",
  "summary": "Marketing content promoting vendor security product with unrealistic claims",
  "published_utc": "2024-09-13T14:30:00Z",
  "cves": [],
  "cvss_v3": null,
  "kev_listed": null,
  "exploit_status": null,
  "affected_products": [],
  "evidence_excerpt": "amazing new product stops all cyber attacks",
  "admiralty_source_reliability": "D",
  "admiralty_info_credibility": 4,
  "admiralty_reason": "Marketing blog with unrealistic security claims and no technical evidence",
  "dedupe_key": "sha256_hash_of_title_and_url"
}
```

**Orchestrator Routing Decision:**
```json
{
  "routing_decision": "DROP",
  "reasoning": "Marketing content with low source reliability (D) and poor information credibility (4). No actionable threat intelligence present.",
  "owner_team": null,
  "sla_hours": null,
  "priority": null,
  "business_impact": null,
  "asset_exposure": "None"
}
```

### Case Study 3: Executive Reporting

**Scenario**: Generate CISO report from week of threat intelligence

**Input**: Multiple routed intelligence items including critical vulnerabilities

**CISO Report Output:**
```json
{
  "agent_type": "ciso_report",
  "report_period": {
    "week_start": "2024-09-07",
    "week_end": "2024-09-13"
  },
  "executive_summary": {
    "key_threats": [
      "Critical Exchange Server vulnerability actively exploited (CVE-2024-12345)",
      "New ransomware campaign targeting financial sector",
      "Supply chain compromise affecting software vendor in our stack"
    ],
    "business_impact": "High risk to email infrastructure and customer data processing systems",
    "immediate_actions": [
      "Emergency Exchange Server patching within 48 hours",
      "Enhanced monitoring of email traffic and file shares",
      "Vendor security assessment for affected supply chain component"
    ],
    "confidence_level": "High"
  },
  "threat_landscape": {
    "critical_trends": [
      "Increased targeting of email infrastructure in financial services",
      "Shift toward supply chain attacks affecting software vendors",
      "Rise in ransomware groups exploiting recent CVEs"
    ],
    "industry_context": "Financial services seeing 40% increase in email-targeted attacks this quarter",
    "attribution": "APT28 likely behind Exchange exploitation campaign based on TTP analysis"
  },
  "risk_assessment": {
    "crown_jewels_exposure": "High - Exchange Server directly affects email and collaboration systems",
    "business_process_impact": "Critical - Email outage would disrupt customer communications and internal operations",
    "regulatory_implications": "Potential SOX compliance issues if financial reporting systems compromised"
  },
  "recommendations": {
    "immediate": [
      "Deploy Exchange patches across all servers within 48 hours",
      "Activate incident response team for enhanced monitoring"
    ],
    "short_term": [
      "Implement zero-trust email security architecture",
      "Conduct tabletop exercise for email infrastructure compromise",
      "Review and update vendor security assessment process"
    ],
    "strategic": [
      "Invest in advanced email security platform with AI-powered threat detection",
      "Establish supply chain security program with continuous monitoring",
      "Enhance threat intelligence sharing with industry peers"
    ]
  },
  "metrics": {
    "threats_processed": 247,
    "high_priority_count": 8,
    "mean_time_to_action": 4.2,
    "sla_compliance": 94
  }
}
```

---

This comprehensive prompt engineering guide provides the foundation for creating effective, consistent, and high-quality prompts that enable NOMAD to deliver precise, actionable threat intelligence analysis. Regular review and optimization of prompts ensures continued effectiveness as threats and organizational needs evolve.