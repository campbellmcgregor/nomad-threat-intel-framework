---
name: Reporting Skills
description: |
  Use this skill group when the user wants to "generate a report", "executive summary", "technical alert", "weekly briefing", or mentions reporting, leadership briefings, SOC alerts, or documentation.

  This skill group generates formatted threat intelligence reports for different audiences including executives, technical teams, and compliance purposes.
version: 2.1.0
---

# Reporting Skills

This skill group generates threat intelligence reports for NOMAD v2.0.

## Available Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `/executive-brief` | Leadership summary report | `[timeframe]` |
| `/technical-alert` | SOC/IT alert format | `[threat-id]` |
| `/weekly-summary` | Weekly threat landscape | None |

## Agent Integration

These commands coordinate with NOMAD agents:
- **threat-synthesizer**: Generates personalized reports
- **intelligence-processor**: Provides enriched data
- **truth-verifier**: Validates confidence scores

## Report Types

- **Executive Brief**: Business-focused for leadership
- **Technical Alert**: Detailed for SOC/IT teams
- **Weekly Summary**: Comprehensive weekly analysis

## Trigger Patterns

These commands are auto-suggested when users:
- Ask for reports ("report", "summary", "briefing")
- Mention leadership ("executive", "CEO", "board")
- Need technical documentation ("alert", "SOC", "incident")
- Request periodic summaries ("weekly", "monthly")
