---
name: help
description: Show NOMAD commands and usage guide
usage: /help [command]
---

You are executing the `/help` command for NOMAD v2.0. This command provides comprehensive documentation of available slash commands and usage guidance.

## Command Parameters

- `$1`: Specific command to get detailed help for
- If no parameter: Show complete command reference

## Response Format

### Complete Command Reference (No Parameters):
```
📖 NOMAD v2.0 COMMAND REFERENCE

THREAT INTELLIGENCE COMMANDS:
/threats                    Latest personalized threat briefing
/critical                   Critical and KEV-listed threats only
/crown-jewel [system]      Threats to specific crown jewel systems
/cve [CVE-ID]              Detailed analysis of specific vulnerability
/trending                  Trending threats and attack vectors

FEED MANAGEMENT COMMANDS:
/add-feeds [industry]      Add industry-specific feed packages
/feed-quality              Feed performance dashboard and recommendations
/import-feeds [file]       Import feeds from OPML/JSON/CSV files

CONFIGURATION COMMANDS:
/setup                     Interactive setup wizard for first-time config
/configure [setting]       Quick configuration updates
/add-crown-jewel [name]    Add critical system to your profile
/update-profile [field]    Update organization profile information

SYSTEM & UTILITY COMMANDS:
/refresh                   Force refresh of threat intelligence data
/status                    Display system health and configuration
/export [format]           Export data and configuration
/help [command]            Show this help or specific command details

REPORTING COMMANDS:
/executive-brief           Generate executive summary report
/technical-alert           Create technical security alert
/weekly-summary            Weekly threat landscape summary

QUICK START:
1. First time? Run: /setup
2. Get threats: /threats
3. Critical only: /critical
4. Add feeds: /add-feeds [your-industry]
5. Check health: /status

EXAMPLES:
/threats                   → Your personalized threat briefing
/critical                  → Show only critical/KEV threats
/crown-jewel "Payment Gateway" → Threats to payment systems
/cve CVE-2024-12345       → Deep dive on specific vulnerability
/add-feeds healthcare     → Add healthcare industry feeds
/configure alerts critical 8.0 → Set critical alert threshold

Need help with a specific command? Use: /help [command-name]
```

### Specific Command Help:
```
📖 DETAILED HELP: /[command-name]

DESCRIPTION:
[Detailed description of what the command does]

USAGE:
/[command] [parameter1] [parameter2]

PARAMETERS:
• [param1]: [Description of parameter]
• [param2]: [Optional parameter description]

EXAMPLES:
/[command] example1       → [What this example does]
/[command] example2       → [What this example does]

RELATED COMMANDS:
• /[related-command]: [Brief description]
• /[another-command]: [Brief description]

For complete command reference: /help
```

## Command Categories

### 🎯 Threat Intelligence
Core commands for accessing and analyzing threat data:
- Real-time threat briefings personalized to your organization
- Critical vulnerability identification and analysis
- Crown jewel system protection
- Trending threat pattern analysis

### 📡 Feed Management
Commands for managing threat intelligence sources:
- Industry-specific feed packages
- Custom feed import capabilities
- Feed performance monitoring
- Quality assurance and optimization

### ⚙️ Configuration
Setup and customization commands:
- Initial system configuration
- Organization profile management
- Crown jewel system identification
- Alert threshold customization

### 🔧 System Operations
Operational and maintenance commands:
- System health monitoring
- Manual data refresh
- Status reporting
- Data export capabilities

### 📊 Reporting
Intelligence reporting and analysis:
- Executive summary generation
- Technical alert creation
- Trend analysis reports
- Custom report formatting

## Usage Tips

**Getting Started:**
1. Run `/setup` for first-time configuration
2. Use `/add-feeds [your-industry]` for relevant sources
3. Execute `/threats` for your first briefing
4. Check `/status` to ensure everything is working

**Daily Operations:**
- `/threats` - Morning threat briefing
- `/critical` - Focus on urgent items
- `/crown-jewel [system]` - Check specific systems
- `/trending` - Weekly pattern analysis

**Maintenance:**
- `/feed-quality` - Monthly source health check
- `/refresh` - When feeds seem stale
- `/status` - Regular system health check
- `/export` - For reporting and backup

**Advanced Usage:**
- Chain commands for comprehensive analysis
- Use parameters to focus on specific areas
- Export data for integration with other tools
- Customize alerts based on your risk tolerance

Execute this command with a specific command name to get detailed help for that command, or without parameters for the complete reference guide.