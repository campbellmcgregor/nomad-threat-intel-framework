---
name: Feed Management Skills
description: |
  Use this skill group when the user wants to "add feeds", "import OPML", "check feed quality", "refresh data", "manage sources", "import feeds", or mentions feed configuration, RSS sources, or threat data sources.

  This skill group manages threat intelligence feed subscriptions, imports, quality monitoring, and data refresh operations.
version: 2.1.0
---

# Feed Management Skills

This skill group manages threat intelligence feeds for NOMAD v2.0.

## Available Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `/add-feeds` | Add industry-specific feed packages | `[industry]` |
| `/feed-quality` | Feed performance dashboard | None |
| `/import-feeds` | Import feeds from OPML/JSON/CSV | `[file]` |
| `/refresh` | Force intelligence refresh | None |

## Agent Integration

These commands coordinate with NOMAD agents:
- **feed-manager**: Manages feed subscriptions and imports
- **feed-quality-monitor**: Tracks feed health and performance
- **threat-collector**: Fetches data from configured feeds

## Available Industry Packages

- **healthcare** - Healthcare & Life Sciences feeds
- **financial** - Financial Services & Banking feeds
- **manufacturing** - Manufacturing & Industrial feeds
- **technology** - Technology & Software Development feeds
- **energy** - Energy & Utilities feeds
- **government** - Government & Public Sector feeds

## Trigger Patterns

These commands are auto-suggested when users:
- Mention feeds ("add feeds", "import feeds", "feed quality")
- Ask about data sources ("RSS", "OPML", "threat sources")
- Request data refresh ("refresh", "update data", "stale data")
- Mention industry packages ("healthcare feeds", "financial sources")
