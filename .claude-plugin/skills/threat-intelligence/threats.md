---
name: threats
description: Show latest personalized threat intelligence briefing
---

You are executing the `/threats` command for NOMAD v2.0. This command provides the user with their personalized threat intelligence briefing based on their organization profile and crown jewels.

## Command Execution

1. **Read User Context**: Load user preferences from `config/user-preferences.json` to understand their:
   - Industry and business sectors
   - Crown jewels (critical systems)
   - Asset exposure types
   - Threat preferences and alert thresholds
   - Verification settings

2. **Check Threat Cache**: Examine `data/threats-cache.json` to:
   - Verify data freshness (last updated timestamp)
   - Get total threat count and priority distribution
   - Access processed threat intelligence

3. **Execute Query Handler**: Use the Task tool to invoke the query-handler agent with the request "Show me latest threats" including full user context

4. **Generate Briefing**: The system should provide a personalized briefing showing:
   - Critical/High/Medium threat counts
   - Specific threats affecting user's crown jewels
   - Business impact context for their industry
   - Verification confidence scores
   - Immediate actions required
   - Follow-up suggestions

## Expected Response Format

The response should be formatted as an executive-style briefing with:
- Clear threat priority indicators (🔴 Critical, 🟠 High, 🟡 Medium)
- Verification status icons (✅ ⚠️ ❓)
- Crown jewel impact analysis
- Actionable remediation steps
- Reference to original threat sources

## Data Freshness

If threat data is stale (>6 hours old), automatically trigger a refresh by coordinating the threat-collector and intelligence-processor agents before generating the briefing.

Execute this command now by coordinating the appropriate NOMAD agents to deliver a comprehensive, personalized threat intelligence briefing.
