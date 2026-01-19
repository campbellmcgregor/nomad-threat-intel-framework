---
name: Configuration Skills
description: |
  Use this skill group when the user wants to "setup NOMAD", "configure settings", "add crown jewels", "update profile", "change preferences", or mentions organization configuration, setup wizard, or profile management.

  This skill group manages NOMAD configuration including initial setup, organization profiles, crown jewel systems, and preference management.
version: 2.1.0
---

# Configuration Skills

This skill group manages NOMAD v2.0 configuration.

## Available Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `/setup` | Interactive setup wizard | None |
| `/configure` | Quick configuration updates | `[setting]` |
| `/add-crown-jewel` | Add critical system | `[name]` |
| `/update-profile` | Update organization info | `[field]` |

## Agent Integration

These commands coordinate with NOMAD agents:
- **setup-wizard**: Guides initial configuration and modifications
- **query-handler**: Routes configuration requests

## Configuration Files

- `config/user-preferences.json` - Organization profile
- `config/setup-state.json` - Setup progress tracking
- `config/threat-sources.json` - Feed configuration

## Trigger Patterns

These commands are auto-suggested when users:
- Mention setup ("setup", "configure", "get started")
- Ask about crown jewels ("add system", "protect", "critical asset")
- Want to update profile ("change industry", "update organization")
- Need configuration help ("preferences", "settings")
