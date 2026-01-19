# Notification System Setup Guide

NOMAD v2.1 introduces a multi-channel notification system that can route alerts to Slack, Microsoft Teams, Discord, Email, and PagerDuty based on severity rules.

## Configuration Overview

Configure notifications using the interactive skill:
```
/alert-config
```

Or manually edit `config/user-preferences.json`:

```json
{
  "notifications": {
    "enabled": true,
    "channels": {
      "slack": {
        "webhook_url": "https://hooks.slack.com/services/..."
      },
      "email": {
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_user": "security@example.com",
        "smtp_password": "${SMTP_PASSWORD}",
        "recipients": ["team@example.com"]
      }
    },
    "routing": {
      "critical": ["slack", "pagerduty", "email"],
      "high": ["slack", "email"],
      "medium": ["slack"]
    }
  }
}
```

## Channel Setup

### 1. Slack
1. Go to https://api.slack.com/apps
2. Create a new App -> "Incoming Webhooks"
3. Activate Incoming Webhooks
4. Click "Add New Webhook to Workspace"
5. Copy the Webhook URL

### 2. Microsoft Teams
1. Go to your Teams channel
2. Click "..." -> "Connectors"
3. Search for "Incoming Webhook" and configure
4. Copy the URL provided

### 3. Discord
1. Edit Channel Settings -> Integrations
2. Create Webhook
3. Copy Webhook URL

### 4. PagerDuty
1. Go to Services -> Service Directory
2. Select or create a service
3. Integrations -> Add Integration
4. Choose "Events API v2"
5. Copy the **Routing Key** (not the API key)

### 5. Email (SMTP)
Standard SMTP configuration. For Gmail:
- Use App Passwords if 2FA is enabled
- Host: `smtp.gmail.com`
- Port: `587`
- TLS: `true`

## Routing Rules

You can configure which channels receive which severity levels:

- **Critical**: Immediate action required (PagerDuty, SMS, high-priority Slack)
- **High**: Urgent attention (Slack, Email)
- **Medium**: Review within 24h (Slack digest)
- **Low**: informational only (Logs/Digest)

## Testing

Test your configuration with:
```
/alert-config test [channel]
```
Example: `/alert-config test slack`
