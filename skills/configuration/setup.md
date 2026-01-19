---
name: setup
description: Interactive setup wizard for NOMAD configuration
---

You are executing the `/setup` command for NOMAD v2.0. This command provides an interactive setup wizard to configure the threat intelligence framework for first-time use or major reconfiguration.

## Command Execution

1. **Check Current Configuration**: Read existing configuration files:
   - `config/user-preferences.json` (if exists)
   - `config/setup-state.json` (if exists)
   - Determine if this is initial setup or reconfiguration

2. **Guided Setup Process**: Use Task tool to invoke setup-wizard agent for:
   - Organization profile configuration
   - Industry-specific settings
   - Crown jewel system identification
   - Feed source selection
   - Alert threshold customization

3. **Configuration Validation**: Ensure all required fields are populated
4. **Initial Data Collection**: Trigger first threat intelligence collection

## Response Format

### Initial Setup:
```
🚀 NOMAD SETUP WIZARD

Welcome to NOMAD v2.0! Let's configure your threat intelligence framework.

SETUP PROGRESS: [▓▓▓░░░░] Step 1 of 5

We'll walk through:
1. Organization Profile (your company details)
2. Crown Jewel Systems (your most critical assets)
3. Feed Source Selection (30+ premium sources available)
4. Alert Configuration (thresholds and preferences)
5. Initial Intelligence Collection

This takes about 2-3 minutes and dramatically improves the quality of your threat intelligence.

Ready to get started?
```

### Reconfiguration Mode:
```
🔧 NOMAD RECONFIGURATION

Current Configuration Detected:
• Organization: [Current Name]
• Industry: [Current Industry]
• Crown Jewels: [X] systems configured
• Feed Sources: [X] active feeds

RECONFIGURATION OPTIONS:
1. Update organization profile
2. Modify crown jewel systems
3. Change feed sources
4. Adjust alert thresholds
5. Reset to defaults (fresh start)
6. Export current configuration

Which would you like to modify?
```

### Setup Completion:
```
✅ NOMAD SETUP COMPLETE!

CONFIGURATION SUMMARY:
• Organization: [Name] ([Industry])
• Crown Jewels: [X] critical systems identified
• Feed Sources: [X] premium feeds configured
• Alert Thresholds: Customized for your environment

NEXT STEPS:
1. Run `/threats` for your first personalized briefing
2. Try `/critical` for immediate action items
3. Use `/feed-quality` to validate your sources

🎯 Your threat intelligence framework is ready!
```

Execute this command now to begin or modify NOMAD configuration.
