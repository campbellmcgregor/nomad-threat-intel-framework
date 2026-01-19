---
name: Deployment Skills
description: |
  Use this skill group when the user wants to "deploy the GUI", "provision server", "publish report", "share report", "check gui status", "view gui logs", or mentions Hetzner deployment, web intake GUI, report sharing, or server management.

  This skill group manages the NOMAD Web Intake GUI deployment on Hetzner Cloud (~€4.50/month).
version: 2.1.0
---

# Deployment Skills

This skill group manages the NOMAD Web Intake GUI deployment on Hetzner Cloud.

## Skills

| Skill | Description |
|-------|-------------|
| `/deploy-gui` | Provision, update, or destroy the Hetzner deployment |
| `/gui-status` | Check deployment health and metrics |
| `/gui-logs` | View application logs |
| `/publish-report` | Publish a report to the web GUI |

## Prerequisites

Before using deployment skills, ensure:

1. **Hetzner API Token**: Set `HETZNER_API_TOKEN` environment variable
2. **SSH Key**: Register an SSH key named `nomad-deploy` in Hetzner Console
3. **API Token**: Set `NOMAD_WEB_API_TOKEN` for report authentication

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HETZNER_API_TOKEN` | Yes | Hetzner Cloud API token |
| `NOMAD_WEB_API_TOKEN` | Yes | API token for report submission |
| `NOMAD_SECRET_KEY` | No | Auto-generated if not set |
| `NOMAD_DOMAIN` | No | Custom domain for HTTPS |
| `LETSENCRYPT_EMAIL` | No | Email for Let's Encrypt certificates |

## Trigger Patterns

- "deploy the gui" → `/deploy-gui provision`
- "update the deployment" → `/deploy-gui update`
- "check gui status" → `/gui-status`
- "show gui logs" → `/gui-logs`
- "publish this report" → `/publish-report`
