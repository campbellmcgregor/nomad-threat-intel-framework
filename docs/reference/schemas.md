# NOMAD Schema Reference

Complete reference for all data schemas used in the NOMAD Threat Intelligence Framework.

## Table of Contents

- [Schema Overview](#schema-overview)
- [Core Intelligence Schema](#core-intelligence-schema)
- [Agent Output Schemas](#agent-output-schemas)
- [Configuration Schemas](#configuration-schemas)
- [Validation and Examples](#validation-and-examples)

## Schema Overview

NOMAD uses standardized JSON schemas to ensure data consistency across all agents and workflows. All schemas follow these principles:

- **Consistent Structure**: Common fields across all intelligence items
- **Required vs Optional**: Clear distinction between mandatory and optional fields
- **Type Safety**: Strict data types for validation
- **Extensibility**: Support for additional fields without breaking compatibility
- **Null Handling**: Explicit handling of unknown/unavailable data

### Schema Versioning

Current schema version: **v1.0**

Schema versions follow semantic versioning:
- **Major version**: Breaking changes requiring migration
- **Minor version**: New fields or non-breaking changes
- **Patch version**: Bug fixes or clarifications

## Core Intelligence Schema

### Standard Intelligence Item

The fundamental data structure for all threat intelligence in NOMAD:

```json
{
  "schema_version": "1.0",
  "source_type": "rss|vendor|cert|api|manual",
  "source_name": "string",
  "source_url": "https://example.com/threat-report",
  "title": "string (max 200 chars)",
  "summary": "string (max 500 chars, ≤60 words preferred)",
  "published_utc": "2025-09-13T10:00:00Z",
  "collected_at_utc": "2025-09-13T10:05:00Z",
  "cves": ["CVE-YYYY-XXXX"],
  "cvss_v3": null|float (0.0-10.0),
  "cvss_v4": null|float (0.0-10.0),
  "epss": null|float (0.0-1.0),
  "kev_listed": true|false|null,
  "kev_date_added": "2025-09-13"|null,
  "exploit_status": "ITW|PoC|None"|null,
  "affected_products": [
    {
      "vendor": "string",
      "product": "string",
      "versions": ["string"],
      "cpe": "cpe:2.3:a:vendor:product:version"
    }
  ],
  "threat_actors": ["string"],
  "mitre_techniques": [
    {
      "technique_id": "T1055",
      "technique_name": "Process Injection",
      "tactic": "Defense Evasion"
    }
  ],
  "iocs": [
    {
      "type": "ip|domain|url|hash|email",
      "value": "string",
      "context": "string",
      "confidence": "high|medium|low"
    }
  ],
  "evidence_excerpt": "string (max 300 chars)",
  "admiralty_source_reliability": "A|B|C|D|E|F",
  "admiralty_info_credibility": 1|2|3|4|5|6,
  "admiralty_reason": "string",
  "tags": ["string"],
  "language": "en|es|fr|de|zh|ja|ru",
  "tlp_marking": "WHITE|GREEN|AMBER|RED",
  "confidence": "high|medium|low",
  "dedupe_key": "string (SHA256 hash)",
  "created_at": "2025-09-13T10:00:00Z",
  "updated_at": "2025-09-13T10:00:00Z"
}
```

### Field Descriptions

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `source_type` | string | Type of intelligence source |
| `source_name` | string | Human-readable source name |
| `source_url` | string | URL of original source |
| `title` | string | Intelligence item title |
| `published_utc` | string | ISO 8601 UTC timestamp |
| `dedupe_key` | string | Unique identifier for deduplication |

#### Vulnerability Fields

| Field | Type | Description |
|-------|------|-------------|
| `cves` | array | List of CVE identifiers |
| `cvss_v3` | number\|null | CVSS v3.x base score (0.0-10.0) |
| `cvss_v4` | number\|null | CVSS v4.0 base score (0.0-10.0) |
| `epss` | number\|null | EPSS probability score (0.0-1.0) |
| `kev_listed` | boolean\|null | Whether CVE is in CISA KEV catalog |
| `kev_date_added` | string\|null | Date added to KEV (YYYY-MM-DD) |
| `exploit_status` | string\|null | Exploitation status |

#### Threat Intelligence Fields

| Field | Type | Description |
|-------|------|-------------|
| `threat_actors` | array | Associated threat actor names |
| `mitre_techniques` | array | MITRE ATT&CK technique mappings |
| `iocs` | array | Indicators of compromise |
| `affected_products` | array | Software/hardware affected |

#### Quality Assessment

| Field | Type | Description |
|-------|------|-------------|
| `admiralty_source_reliability` | string | NATO Admiralty source rating |
| `admiralty_info_credibility` | integer | NATO Admiralty information rating |
| `admiralty_reason` | string | Justification for ratings |
| `confidence` | string | Overall confidence level |
| `tlp_marking` | string | Traffic Light Protocol marking |

### Admiralty Code Reference

#### Source Reliability (A-F)
- **A**: Completely reliable (official sources, verified)
- **B**: Usually reliable (established sources, minimal doubt)
- **C**: Fairly reliable (some doubt about source)
- **D**: Not usually reliable (significant doubt)
- **E**: Unreliable (lack of competence)
- **F**: Reliability cannot be judged

#### Information Credibility (1-6)
- **1**: Confirmed (confirmed by other sources)
- **2**: Probably true (logical, consistent)
- **3**: Possibly true (reasonably consistent)
- **4**: Doubtful (possible but inconsistent)
- **5**: Improbable (inconsistent with established facts)
- **6**: Truth cannot be judged

## Agent Output Schemas

### RSS Feed Agent Output

```json
{
  "schema_version": "1.0",
  "agent_type": "rss",
  "agent_version": "1.0.0",
  "collected_at_utc": "2025-09-13T10:00:00Z",
  "execution_time_seconds": 45.2,
  "config": {
    "since": "2025-09-06T10:00:00Z",
    "until": "2025-09-13T10:00:00Z",
    "priority": "high",
    "source_type": "vendor"
  },
  "metrics": {
    "feeds_processed": 25,
    "feeds_failed": 1,
    "total_entries": 150,
    "filtered_entries": 45,
    "unique_items": 42,
    "cves_found": 18
  },
  "intelligence": [
    // Array of Standard Intelligence Items
  ],
  "errors": [
    {
      "feed_name": "Broken Feed",
      "feed_url": "https://broken.example.com/feed.xml",
      "error_type": "timeout",
      "error_message": "Connection timeout after 30 seconds",
      "timestamp": "2025-09-13T10:02:30Z"
    }
  ],
  "warnings": [
    {
      "message": "Feed returned no new items",
      "feed_name": "Empty Feed",
      "timestamp": "2025-09-13T10:01:15Z"
    }
  ]
}
```

### Orchestrator Agent Output

```json
{
  "schema_version": "1.0",
  "agent_type": "orchestrator",
  "agent_version": "1.0.0",
  "processed_at_utc": "2025-09-13T10:30:00Z",
  "execution_time_seconds": 15.8,
  "input_items": 42,
  "routing_decisions": [
    {
      "item_id": "dedupe_key_hash",
      "title": "Critical VMware vCenter Vulnerability",
      "route": "TECHNICAL_ALERT|CISO_REPORT|WATCHLIST|DROP",
      "route_reason": "KEV-listed vulnerability with HIGH asset exposure",
      "owner_team": "SOC|Vuln Mgmt|IT Ops",
      "priority": "critical|high|medium|low",
      "sla_hours": 24,
      "sla_due_utc": "2025-09-14T10:30:00Z",
      "asset_exposure": "HIGH|MEDIUM|LOW|NONE",
      "business_impact": "HIGH|MEDIUM|LOW",
      "automation_eligible": true,
      "escalation_required": false,
      "created_at": "2025-09-13T10:30:00Z"
    }
  ],
  "routing_summary": {
    "TECHNICAL_ALERT": 8,
    "CISO_REPORT": 3,
    "WATCHLIST": 25,
    "DROP": 6
  },
  "sla_summary": {
    "critical": 2,
    "high": 6,
    "medium": 15,
    "low": 19
  },
  "context": {
    "org_name": "Acme Corporation",
    "crown_jewels": ["Exchange", "Active Directory"],
    "business_sectors": ["Financial Services"]
  }
}
```

### CISO Report Agent Output

```json
{
  "schema_version": "1.0",
  "agent_type": "ciso_report",
  "agent_version": "1.0.0",
  "generated_at_utc": "2025-09-13T11:00:00Z",
  "report_period": {
    "week_start": "2025-09-07",
    "week_end": "2025-09-13"
  },
  "executive_summary": {
    "headline": "3 critical vulnerabilities patched, 2 ITW campaigns contained; identity system exposure eliminated",
    "threat_level": "ELEVATED|NORMAL|LOW",
    "key_actions_taken": 5,
    "sla_compliance": "92%"
  },
  "top_risks": [
    {
      "risk_id": "RISK-2025-001",
      "item": "Microsoft Exchange Server – CVE-2025-2847",
      "why_it_matters": "Internet-facing email infrastructure vulnerable to remote code execution",
      "status": "RESOLVED|IN_PROGRESS|ACCEPTED|MITIGATED",
      "business_impact": "HIGH|MEDIUM|LOW",
      "affected_systems": ["Exchange Server", "Email Infrastructure"],
      "resolution_date": "2025-09-13T08:00:00Z"
    }
  ],
  "decisions_made": [
    {
      "decision_id": "DEC-2025-001",
      "decision_type": "EMERGENCY_PATCH|RISK_ACCEPTANCE|COMPENSATING_CONTROLS",
      "decision": "Emergency patching authorized",
      "rationale": "Exchange CVE-2025-2847 - active exploitation detected",
      "impact": "18-hour maintenance window, all mail servers patched",
      "decision_date": "2025-09-12T14:00:00Z",
      "decision_maker": "CISO",
      "status": "IMPLEMENTED"
    }
  ],
  "metrics": {
    "alerts_created": 12,
    "alerts_closed": 9,
    "mean_time_to_acknowledge_hours": 2.5,
    "mean_time_to_resolve_hours": 26.0,
    "sla_compliance_rate": 0.92,
    "patch_deployment_rate": 0.85,
    "false_positive_rate": 0.05,
    "watchlist_items": 15,
    "kev_vulnerabilities_addressed": 3
  },
  "threat_landscape": {
    "active_campaigns": [
      {
        "campaign_name": "APT29 CloudHopper 2.0",
        "threat_actor": "APT29 (Cozy Bear)",
        "target_sectors": ["Cloud Services", "MSPs"],
        "impact_to_org": "LOW - monitoring MSP security clauses",
        "first_observed": "2025-09-10",
        "techniques": ["T1566.001", "T1078"]
      }
    ],
    "trending_vulnerabilities": [
      "Exchange Server RCE",
      "VMware vCenter Auth Bypass",
      "Cisco ASA Firewall Bypass"
    ],
    "emerging_threats": [
      "Supply chain attacks on CI/CD pipelines",
      "AI-powered social engineering"
    ]
  },
  "recommendations": [
    "Complete VMware vCenter patching by EOD Friday",
    "Validate Jenkins CI/CD security hardening post-patch",
    "Conduct tabletop exercise for supply chain scenarios"
  ],
  "appendix": {
    "data_sources": 25,
    "intelligence_items_processed": 150,
    "report_confidence": "HIGH",
    "next_report_due": "2025-09-20"
  }
}
```

### Technical Alert Agent Output

```json
{
  "schema_version": "1.0",
  "agent_type": "technical_alert",
  "agent_version": "1.0.0",
  "generated_at_utc": "2025-09-13T10:45:00Z",
  "alerts": [
    {
      "alert_id": "ALERT-2025-0913-001",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "title": "Critical VMware vCenter Authentication Bypass",
      "description": "CVE-2025-1234 allows remote authentication bypass in VMware vCenter Server",
      "affected_systems": [
        {
          "system_name": "VMware vCenter",
          "system_type": "Infrastructure Management",
          "exposure": "Internal Network",
          "criticality": "HIGH",
          "patch_available": true,
          "patch_url": "https://example.com/patch"
        }
      ],
      "threat_details": {
        "cves": ["CVE-2025-1234"],
        "cvss_v3": 9.8,
        "epss": 0.85,
        "kev_listed": true,
        "exploit_status": "ITW",
        "first_seen": "2025-09-10T00:00:00Z",
        "threat_actors": ["APT28", "Unknown"]
      },
      "remediation": {
        "immediate_actions": [
          "Apply vendor patch within 24 hours",
          "Monitor authentication logs for anomalies",
          "Enable additional authentication logging"
        ],
        "patch_info": {
          "vendor": "VMware",
          "patch_id": "VMSA-2025-0001",
          "patch_url": "https://vmware.com/security/advisories/VMSA-2025-0001.html",
          "testing_required": true,
          "estimated_downtime": "2 hours"
        },
        "workarounds": [
          "Implement network segmentation",
          "Enable MFA for all administrative accounts"
        ]
      },
      "business_context": {
        "asset_exposure": "MEDIUM",
        "business_impact": "HIGH",
        "compliance_impact": ["SOX", "PCI-DSS"],
        "affected_business_units": ["IT Operations", "Development"]
      },
      "sla_info": {
        "assigned_team": "IT Ops",
        "priority": "P1",
        "sla_hours": 24,
        "due_date": "2025-09-14T10:45:00Z",
        "escalation_contacts": ["it-ops-manager@company.com"]
      },
      "tracking": {
        "ticket_id": "INC-2025-001234",
        "status": "NEW|ASSIGNED|IN_PROGRESS|RESOLVED|CLOSED",
        "assigned_to": "john.smith@company.com",
        "created_at": "2025-09-13T10:45:00Z",
        "updated_at": "2025-09-13T10:45:00Z"
      }
    }
  ],
  "alert_summary": {
    "total_alerts": 8,
    "critical": 2,
    "high": 3,
    "medium": 2,
    "low": 1,
    "kev_related": 3,
    "patches_available": 7
  }
}
```

## Configuration Schemas

### RSS Feeds Configuration

```yaml
# config/rss_feeds.yaml schema
feeds:
  metadata:
    version: "1.0"
    last_updated: "2025-09-13T10:00:00Z"
    total_feeds: 50

  feeds:
    - name: "string (required)"
      url: "https://example.com/feed.xml (required)"
      source_type: "cert|vendor|research|news|database (required)"
      priority: "high|medium|low (required)"
      enabled: true|false

      # Feed-specific settings
      update_frequency: "hourly|daily|weekly"
      timeout_seconds: 30
      max_items: 100

      # Authentication (if required)
      auth_type: "none|basic|token|oauth"
      username: "string"
      password: "string"
      api_key: "string"

      # Processing options
      parser: "default|custom_parser_name"
      extract_iocs: true|false
      language: "en|es|fr|de"

      # Quality settings
      min_confidence: "high|medium|low"
      admiralty_override:
        source_reliability: "A|B|C|D|E|F"
        default_credibility: 1-6

      # Filtering
      keywords_include: ["keyword1", "keyword2"]
      keywords_exclude: ["spam", "test"]
      cve_required: true|false

      # Metadata
      description: "string"
      contact_email: "admin@example.com"
      added_date: "2025-09-13"
      tags: ["government", "vendor", "critical-infrastructure"]
```

### Workflow Configuration

```yaml
# config/claude_agent_config.yaml schema
workflows:
  workflow_name:
    name: "Human Readable Name (required)"
    description: "Detailed description (required)"
    version: "1.0"

    # Scheduling
    schedule: "cron_expression"
    timezone: "America/New_York"
    enabled: true|false

    # Execution settings
    timeout_minutes: 60
    max_retries: 3
    retry_on_failure: true|false
    continue_on_agent_failure: true|false

    # Dependencies
    requires: ["other_workflow_name"]
    conflicts_with: ["conflicting_workflow"]

    # Steps
    steps:
      - name: "step_name"
        agent: "agent_name (required)"
        config:
          parameter_name: "value"

        # Step-level settings
        timeout_minutes: 30
        retry_count: 2
        required: true|false

        # Conditional execution
        condition: "expression"
        skip_if: "expression"

      # Parallel execution
      - parallel:
          - agent: "agent1"
          - agent: "agent2"
        max_concurrent: 5
        wait_for_completion: true

      # Conditional execution
      - conditional:
          - condition: "route == TECHNICAL_ALERT"
            agent: "technical_alert"
          - condition: "route == CISO_REPORT"
            agent: "ciso_report"

    # Notifications
    notifications:
      on_success: ["email@company.com"]
      on_failure: ["oncall@company.com"]
      on_timeout: ["admin@company.com"]

    # Outputs
    outputs:
      save_intermediate: true|false
      archive_after_days: 30
      notification_channels: ["slack", "email", "webhook"]
```

## Validation and Examples

### JSON Schema Validation

NOMAD includes JSON Schema files for validation:

```bash
# Validate intelligence item
python -c "
import json
import jsonschema
from pathlib import Path

# Load schema
with open('schema/intelligence-item.json', 'r') as f:
    schema = json.load(f)

# Load data
with open('data/output/rss_feed_result.json', 'r') as f:
    data = json.load(f)

# Validate each intelligence item
for item in data.get('intelligence', []):
    try:
        jsonschema.validate(item, schema)
        print(f'✓ {item[\"title\"][:50]}... is valid')
    except jsonschema.ValidationError as e:
        print(f'❌ Validation error: {e.message}')
"
```

### Example Data Files

#### Sample Intelligence Item

```json
{
  "source_type": "rss",
  "source_name": "CISA Known Exploited Vulnerabilities",
  "source_url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
  "title": "VMware vCenter Server Authentication Bypass Vulnerability",
  "summary": "VMware vCenter Server contains an authentication bypass vulnerability that allows remote attackers to gain administrative access.",
  "published_utc": "2025-09-13T10:00:00Z",
  "collected_at_utc": "2025-09-13T10:05:00Z",
  "cves": ["CVE-2025-1234"],
  "cvss_v3": 9.8,
  "cvss_v4": null,
  "epss": 0.85,
  "kev_listed": true,
  "kev_date_added": "2025-09-13",
  "exploit_status": "ITW",
  "affected_products": [
    {
      "vendor": "VMware",
      "product": "vCenter Server",
      "versions": ["7.0", "8.0"],
      "cpe": "cpe:2.3:a:vmware:vcenter_server:*:*:*:*:*:*:*:*"
    }
  ],
  "threat_actors": ["Unknown"],
  "mitre_techniques": [
    {
      "technique_id": "T1078",
      "technique_name": "Valid Accounts",
      "tactic": "Initial Access"
    }
  ],
  "iocs": [],
  "evidence_excerpt": "VMware has released security updates to address authentication bypass vulnerability...",
  "admiralty_source_reliability": "A",
  "admiralty_info_credibility": 2,
  "admiralty_reason": "Official government CERT advisory with vendor confirmation",
  "tags": ["authentication", "bypass", "vmware", "critical-infrastructure"],
  "language": "en",
  "tlp_marking": "WHITE",
  "confidence": "high",
  "dedupe_key": "sha256_hash_of_title_and_url",
  "created_at": "2025-09-13T10:00:00Z",
  "updated_at": "2025-09-13T10:00:00Z"
}
```

### Schema Evolution

When updating schemas:

1. **Backward Compatibility**: New fields should be optional
2. **Migration Scripts**: Provide scripts for breaking changes
3. **Deprecation Notice**: Mark old fields as deprecated before removal
4. **Version Documentation**: Document changes in schema changelog

### Common Validation Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Missing required field | Agent didn't set required field | Update agent to set all required fields |
| Invalid date format | Wrong timestamp format | Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ` |
| Invalid CVE format | Malformed CVE identifier | Use pattern: `CVE-YYYY-NNNNN` |
| Invalid CVSS score | Score outside 0.0-10.0 range | Validate CVSS scores before assignment |
| Invalid Admiralty code | Wrong reliability/credibility values | Use valid A-F for reliability, 1-6 for credibility |

---

These schemas ensure data consistency and quality throughout the NOMAD framework. Always validate data against these schemas before processing to maintain system integrity.