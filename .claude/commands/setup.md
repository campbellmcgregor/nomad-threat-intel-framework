---
name: setup
description: Interactive setup wizard for NOMAD configuration
---

You are executing the `/setup` command for NOMAD v2.0. This command provides an interactive setup wizard to configure the threat intelligence framework for first-time use or major reconfiguration.

## Command Execution

1. **Check Current Configuration**: Read existing configuration files:
   - `config/user-preferences.json` (if exists)
   - `config/threat-sources.json` (if exists)
   - Determine if this is initial setup or reconfiguration

2. **Guided Setup Process**: Use Task tool to invoke setup-wizard agent for:
   - Organization profile configuration
   - Industry-specific settings
   - Crown jewel system identification
   - Feed source selection
   - Alert threshold customization

3. **Configuration Validation**: Ensure all required fields are populated and valid
4. **Initial Data Collection**: Trigger first threat intelligence collection

## Response Format

### Initial Setup:
```
🚀 NOMAD SETUP WIZARD

Welcome to NOMAD v2.0! Let's configure your threat intelligence framework.

SETUP PROGRESS: [▓▓▓░░░░] Step 1 of 5

ORGANIZATION PROFILE:
We'll start by setting up your organization profile. This helps NOMAD prioritize threats relevant to your environment.

Organization Name: [Waiting for input]
Industry Sector: [Technology/Healthcare/Financial/Manufacturing/Energy/Government/Other]
Business Focus: [What does your organization do?]

Example: "Acme Financial" in "Financial" sector focusing on "Online Banking and Payment Processing"

Once you provide these details, we'll continue with:
2. Crown Jewel Systems (your most critical assets)
3. Feed Source Selection (30+ premium sources available)
4. Alert Configuration (thresholds and preferences)
5. Initial Intelligence Collection

Please provide your organization details to continue.
```

### Reconfiguration Mode:
```
🔧 NOMAD RECONFIGURATION

Current Configuration Detected:
• Organization: [Current Name]
• Industry: [Current Industry]
• Crown Jewels: [X] systems configured
• Feed Sources: [X] active feeds
• Last Updated: [Date]

RECONFIGURATION OPTIONS:
1. Update organization profile
2. Modify crown jewel systems
3. Change feed sources
4. Adjust alert thresholds
5. Reset to defaults (fresh start)
6. Export current configuration

Which would you like to modify? [1-6]
```

### Setup Completion:
```
✅ NOMAD SETUP COMPLETE!

CONFIGURATION SUMMARY:
• Organization: [Name] ([Industry])
• Crown Jewels: [X] critical systems identified
• Feed Sources: [X] premium feeds configured
• Quality Score: [X]/100 (feed health)
• Alert Thresholds: Customized for your environment

NEXT STEPS:
1. Run `/threats` to see your first personalized briefing
2. Try `/critical` for immediate action items
3. Use `/feed-quality` to validate your sources
4. Check `/help` for all available commands

🎯 Your threat intelligence framework is ready! NOMAD will now provide threats tailored to [Organization] with focus on [Industry] sector threats affecting your crown jewel systems.

Setup completed in [X] seconds. Welcome to intelligent threat monitoring!
```

## Setup Wizard Integration

The setup command integrates with the setup-wizard agent to provide:
- Interactive questionnaire for organization profiling
- Intelligent industry template selection
- Crown jewel system recommendations
- Feed source optimization for user's environment
- Threshold tuning based on organization size and risk tolerance

Execute this command now to begin or modify NOMAD configuration with guided assistance.