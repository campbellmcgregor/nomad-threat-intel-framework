# NOMAD Web Intake GUI - Implementation Plan

## Overview

A Docker-based web application for viewing and sharing NOMAD threat intelligence reports, deployed to Hetzner Cloud via Ansible and fully manageable from Claude Code.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend | Python FastAPI | Lightweight, async, OpenAPI docs |
| Frontend | Alpine.js + Tailwind | No build step, ~15KB |
| Database | SQLite | Zero config, file-based |
| PDF Export | WeasyPrint | Python-native HTML-to-PDF |
| Deployment | Ansible + Hetzner | Cost-effective, Claude Code manageable |
| Auth Model | **Link-only access** | Reports not browsable without share link |

## Security Model: Link-Only Access

```
┌─────────────────────────────────────────────────────────────────┐
│                     Access Control Model                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PUBLIC (no auth):                                              │
│  └── GET /shared/{token}  → View report with valid share link  │
│  └── GET /health          → Health check                       │
│                                                                 │
│  API TOKEN (required):                                          │
│  └── POST /api/v1/reports       → Push new report              │
│  └── GET  /api/v1/reports       → List all reports             │
│  └── GET  /api/v1/reports/{id}  → Get specific report          │
│  └── POST /api/v1/reports/{id}/share → Generate share link     │
│  └── DELETE /api/v1/reports/{id}     → Delete report           │
│                                                                 │
│  Share links are the ONLY way to view reports without API key  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Points:**
- No public report listing - must have API token or share link
- Share links can be time-limited (default 72h) or permanent
- Share links can optionally require a password
- Claude Code manages report lifecycle via API token

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         User's Machine                               │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Claude Code                                                   │  │
│  │  ├── /publish-report  → Push reports to web GUI               │  │
│  │  ├── /deploy-gui      → Provision/update Hetzner server       │  │
│  │  ├── /gui-status      → Check deployment health               │  │
│  │  └── /gui-logs        → View server logs                      │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│                              │ Ansible over SSH                      │
│                              ▼                                       │
└──────────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTPS
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Hetzner Cloud (CX22)                            │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Docker Host (Ubuntu 24.04)                                    │  │
│  │  ├── nomad-web-gui container                                   │  │
│  │  │   ├── FastAPI backend (:8080)                               │  │
│  │  │   ├── SQLite database                                       │  │
│  │  │   └── Report storage volume                                 │  │
│  │  ├── caddy container (reverse proxy + auto HTTPS)              │  │
│  │  └── watchtower container (optional auto-updates)              │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
nomad-threat-intel-framework/
├── web-intake-gui/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Settings management
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── reports.py          # Report CRUD endpoints
│   │   │   ├── sharing.py          # Share link endpoints
│   │   │   └── health.py           # Health checks
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── report.py           # Pydantic models
│   │   │   ├── share.py            # Share token models
│   │   │   └── database.py         # SQLAlchemy models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── report_service.py   # Report business logic
│   │   │   ├── share_service.py    # Share link logic
│   │   │   └── pdf_service.py      # PDF generation
│   │   ├── static/
│   │   │   ├── index.html          # Landing/login page
│   │   │   ├── shared.html         # Shared report viewer
│   │   │   ├── css/
│   │   │   │   └── styles.css
│   │   │   └── js/
│   │   │       ├── app.js
│   │   │       └── report-viewer.js
│   │   └── templates/
│   │       └── pdf/
│   │           └── report.html     # PDF template
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── deployment/
│   ├── ansible/
│   │   ├── ansible.cfg
│   │   ├── inventory/
│   │   │   ├── hosts.yml           # Hetzner server inventory
│   │   │   └── group_vars/
│   │   │       └── all.yml         # Common variables
│   │   ├── playbooks/
│   │   │   ├── provision.yml       # Create Hetzner server
│   │   │   ├── deploy.yml          # Deploy/update application
│   │   │   ├── destroy.yml         # Tear down server
│   │   │   ├── backup.yml          # Backup data
│   │   │   └── logs.yml            # Fetch logs
│   │   ├── roles/
│   │   │   ├── common/             # Base server setup
│   │   │   ├── docker/             # Docker installation
│   │   │   ├── caddy/              # Reverse proxy + TLS
│   │   │   └── nomad-gui/          # Application deployment
│   │   └── templates/
│   │       ├── docker-compose.prod.yml.j2
│   │       ├── Caddyfile.j2
│   │       └── .env.j2
│   └── README.md
│
└── .claude-plugin/
    └── skills/
        └── deployment/             # NEW skill group
            ├── SKILL.md
            ├── deploy-gui.md
            ├── gui-status.md
            ├── gui-logs.md
            └── publish-report.md
```

## API Specification

### Authentication

```
Authorization: Bearer <API_TOKEN>
```

API token is set via environment variable and required for all `/api/v1/*` endpoints.

### Endpoints

#### Submit Report (Claude Code → Web GUI)

```http
POST /api/v1/reports
Authorization: Bearer <token>
Content-Type: application/json

{
  "report_type": "executive-brief",
  "title": "Weekly Threat Intelligence Summary",
  "generated_at": "2026-01-09T15:30:00Z",
  "organization": "Acme Corp",
  "content": {
    "markdown": "# Executive Summary\n\n...",
    "raw_data": { ... }
  },
  "metadata": {
    "period_start": "2026-01-02",
    "period_end": "2026-01-09",
    "threat_count": 45,
    "critical_count": 3,
    "crown_jewels_affected": ["Web Servers", "Databases"]
  },
  "classification": "INTERNAL"
}

Response 201:
{
  "id": "rpt_abc123xyz",
  "created_at": "2026-01-09T15:30:05Z"
}
```

#### Generate Share Link

```http
POST /api/v1/reports/{report_id}/share
Authorization: Bearer <token>

{
  "expires_hours": 72,        // null for permanent
  "password": null,           // optional
  "allow_download": true      // PDF download
}

Response 201:
{
  "share_token": "sh_xyz789abc",
  "share_url": "https://nomad.example.com/s/sh_xyz789abc",
  "expires_at": "2026-01-12T15:30:00Z"
}
```

#### View Shared Report (Public)

```http
GET /s/{share_token}
→ Returns HTML page with rendered report

GET /s/{share_token}/pdf
→ Returns PDF download (if allowed)

GET /s/{share_token}?password=secret
→ For password-protected shares
```

## Hetzner Deployment via Ansible

### Prerequisites

1. Hetzner Cloud account with API token
2. SSH key registered in Hetzner
3. Domain name (optional, for custom domain)

### Configuration

```yaml
# deployment/ansible/inventory/group_vars/all.yml

hetzner:
  api_token: "{{ lookup('env', 'HETZNER_API_TOKEN') }}"
  server_type: cx22          # 2 vCPU, 4GB RAM, ~€4.5/mo
  location: fsn1             # Falkenstein, Germany
  image: ubuntu-24.04
  ssh_key_name: nomad-deploy

app:
  domain: nomad.example.com  # or use IP
  api_token: "{{ lookup('env', 'NOMAD_WEB_API_TOKEN') }}"
  secret_key: "{{ lookup('env', 'NOMAD_SECRET_KEY') }}"

backup:
  enabled: true
  retention_days: 30
  destination: ./backups/
```

### Playbooks

#### Provision Server

```yaml
# deployment/ansible/playbooks/provision.yml
- name: Provision Hetzner server for NOMAD Web GUI
  hosts: localhost
  tasks:
    - name: Create server
      hetzner.hcloud.server:
        api_token: "{{ hetzner.api_token }}"
        name: nomad-web-gui
        server_type: "{{ hetzner.server_type }}"
        image: "{{ hetzner.image }}"
        location: "{{ hetzner.location }}"
        ssh_keys:
          - "{{ hetzner.ssh_key_name }}"
        state: present
      register: server

    - name: Add to inventory
      add_host:
        name: "{{ server.hcloud_server.ipv4_address }}"
        groups: nomad_servers

    - name: Create firewall
      hetzner.hcloud.firewall:
        api_token: "{{ hetzner.api_token }}"
        name: nomad-web-gui-fw
        rules:
          - direction: in
            protocol: tcp
            port: "22"
            source_ips: ["0.0.0.0/0"]
          - direction: in
            protocol: tcp
            port: "80"
            source_ips: ["0.0.0.0/0"]
          - direction: in
            protocol: tcp
            port: "443"
            source_ips: ["0.0.0.0/0"]
```

#### Deploy Application

```yaml
# deployment/ansible/playbooks/deploy.yml
- name: Deploy NOMAD Web GUI
  hosts: nomad_servers
  become: yes
  roles:
    - common
    - docker
    - caddy
    - nomad-gui
```

## Claude Code Skills

### /deploy-gui

Provision or update the Hetzner deployment.

```markdown
---
name: deploy-gui
description: Deploy or update the NOMAD Web Intake GUI on Hetzner
argument-hint: "[provision|update|destroy]"
---

# Deploy GUI Skill

## Actions
- `provision` - Create new Hetzner server and deploy
- `update` - Update existing deployment with latest code
- `destroy` - Tear down the server (with confirmation)

## Usage
User: /deploy-gui provision
→ Runs ansible playbook to create server and deploy app

User: /deploy-gui update
→ Pulls latest image and restarts containers
```

### /publish-report

Push a report to the web GUI and get a share link.

```markdown
---
name: publish-report
description: Publish a threat report to the web GUI and generate share link
argument-hint: "[report-type] [--permanent] [--password]"
---

# Publish Report Skill

## Workflow
1. Generate report using existing skill (e.g., /executive-brief)
2. POST report to web GUI API
3. Generate share link
4. Return shareable URL to user

## Options
- `--permanent` - Create non-expiring share link
- `--password <pass>` - Require password to view
- `--no-pdf` - Disable PDF download

## Example Output
✓ Report published successfully

📄 Executive Threat Intelligence Brief
   ID: rpt_abc123xyz

🔗 Share Link (expires in 72 hours):
   https://nomad.example.com/s/sh_xyz789abc

📥 Direct PDF: https://nomad.example.com/s/sh_xyz789abc/pdf
```

### /gui-status

Check deployment health and metrics.

```markdown
---
name: gui-status
description: Check NOMAD Web GUI deployment status and health
---

## Output
- Server status (running/stopped)
- Container health
- Disk usage
- Recent report count
- SSL certificate expiry
```

### /gui-logs

Fetch recent logs from the deployment.

```markdown
---
name: gui-logs
description: View recent logs from the NOMAD Web GUI deployment
argument-hint: "[lines] [--service]"
---

## Options
- `lines` - Number of log lines (default: 100)
- `--service` - Filter by service (app|caddy|all)
```

## UI Mockups

### Shared Report View (`/s/{token}`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ┌─────┐  NOMAD Threat Intelligence            [Download PDF] 📥    │
│  │ 🛡️  │  Shared Report                                            │
│  └─────┘                                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📈 EXECUTIVE THREAT INTELLIGENCE BRIEF                            │
│  ─────────────────────────────────────────────────────────────────  │
│  Organization: Acme Corp                                            │
│  Period: Jan 2-9, 2026                                              │
│  Classification: INTERNAL                                           │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════    │
│                                                                     │
│  EXECUTIVE SUMMARY                                                  │
│                                                                     │
│  The threat landscape this week shows increased targeting of        │
│  web application infrastructure...                                  │
│                                                                     │
│  ┌────────────────────────────┐  ┌────────────────────────────┐    │
│  │ Threat Severity            │  │ Crown Jewel Impact         │    │
│  │ ┌────────────────────────┐ │  │ ┌────────────────────────┐ │    │
│  │ │     [Pie Chart]        │ │  │ │     [Bar Chart]        │ │    │
│  │ │  Critical: 3           │ │  │ │  Web Servers: 5        │ │    │
│  │ │  High: 12              │ │  │ │  Databases: 3          │ │    │
│  │ │  Medium: 30            │ │  │ │  Auth: 2               │ │    │
│  │ └────────────────────────┘ │  │ └────────────────────────┘ │    │
│  └────────────────────────────┘  └────────────────────────────┘    │
│                                                                     │
│  KEY THREATS                                                        │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  🔴 CVE-2026-12345 - Critical RCE in Exchange Server               │
│     CVSS: 9.8 | EPSS: 0.85 | KEV: Yes                              │
│     Affected: Web Application Servers                               │
│                                                                     │
│  ...                                                                │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  This link expires: Jan 12, 2026 at 3:30 PM                        │
│  Powered by NOMAD Threat Intelligence Framework                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Password Protected View

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                    🔒 Password Required                             │
│                                                                     │
│         This report is protected. Enter password to view.          │
│                                                                     │
│                   ┌─────────────────────────┐                       │
│                   │ ••••••••                │                       │
│                   └─────────────────────────┘                       │
│                         [View Report]                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 1: Core Application
- [ ] FastAPI backend with report CRUD
- [ ] SQLite database setup
- [ ] Share link generation with expiry
- [ ] Basic HTML viewer for shared reports
- [ ] Docker containerization

### Phase 2: PDF Export
- [ ] WeasyPrint integration
- [ ] PDF report template
- [ ] Chart rendering for PDF
- [ ] Download endpoint

### Phase 3: Ansible Deployment
- [ ] Hetzner provisioning playbook
- [ ] Docker deployment role
- [ ] Caddy reverse proxy with auto-TLS
- [ ] Firewall configuration

### Phase 4: Claude Code Integration
- [ ] `/publish-report` skill
- [ ] `/deploy-gui` skill
- [ ] `/gui-status` skill
- [ ] `/gui-logs` skill
- [ ] Update user-preferences.json schema

### Phase 5: Polish
- [ ] Error handling and validation
- [ ] Rate limiting
- [ ] Backup playbook
- [ ] Documentation

## Cost Estimate

| Resource | Monthly Cost |
|----------|-------------|
| Hetzner CX22 (2 vCPU, 4GB) | ~€4.50 |
| 20GB Volume (optional) | ~€1.00 |
| **Total** | **~€5.50/month** |

## Environment Variables

```bash
# Required
HETZNER_API_TOKEN=        # Hetzner Cloud API token
NOMAD_WEB_API_TOKEN=      # API token for report submission
NOMAD_SECRET_KEY=         # JWT signing key

# Optional
NOMAD_DOMAIN=             # Custom domain (default: IP address)
SHARE_EXPIRY_HOURS=72     # Default share link expiry
BACKUP_ENABLED=true       # Enable automated backups
```

## Next Steps

1. Review and approve this plan
2. Begin Phase 1 implementation
3. Set up Hetzner account and API token
4. Configure domain (optional)
