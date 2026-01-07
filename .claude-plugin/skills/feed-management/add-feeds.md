---
name: add-feeds
description: Add industry-specific threat intelligence feed package
argument-hint: "[industry]"
---

You are executing the `/add-feeds` command for NOMAD v2.0. This command adds pre-configured industry-specific threat intelligence feed packages to the user's configuration.

## Command Parameters

- `$ARGUMENTS`: Industry name (healthcare, financial, manufacturing, technology, energy, government)
- If no parameter: Show available industry packages

## Command Execution

1. **Parse Industry Parameter**:
   - If `$ARGUMENTS` provided: Match against available industry templates
   - If no `$ARGUMENTS`: Display list of available industry packages with descriptions
   - Accept variations (e.g., "health", "finance", "tech", "gov")

2. **Load Industry Template**: Read `config/threat-sources-templates.json` and:
   - Find matching industry template
   - Extract feed configuration and crown jewel suggestions
   - Validate all feed URLs are accessible

3. **Check Current Configuration**: Read `config/threat-sources.json` to:
   - Identify already configured feeds
   - Prevent duplicate additions
   - Calculate new feeds to be added

4. **Execute Feed Manager**: Use Task tool to invoke feed-manager agent

## Available Industry Packages

```
🏥 healthcare - Healthcare & Life Sciences
💰 financial - Financial Services & Banking
🏭 manufacturing - Manufacturing & Industrial
💻 technology - Technology & Software Development
⚡ energy - Energy & Utilities
🏛️ government - Government & Public Sector
```

## Response Format

```
✅ INDUSTRY PACKAGE ADDED: [Industry Name]

FEEDS ADDED ([X] new sources):
• [Feed Name]: [Priority Level] - [Description]
• [Feed Name]: [Priority Level] - [Description]

📊 FEED CONFIGURATION UPDATED:
• Total Active Feeds: [X] ([Y] new)
• Industry-Specific Feeds: [X]
• Premium Sources: [X]

💡 CROWN JEWEL SUGGESTIONS:
Consider adding these systems to your crown jewels:
• [Suggested System 1]: [Reason/Description]
• [Suggested System 2]: [Reason/Description]

⚙️ NEXT STEPS:
1. Run `/feed-quality` to validate new feeds
2. Use `/crown-jewel [system]` to see relevant threats
3. Try `/threats` for updated briefing
```

Execute this command now to add industry-specific threat intelligence feeds.
