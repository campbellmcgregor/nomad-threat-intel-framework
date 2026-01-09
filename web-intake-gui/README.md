# NOMAD Web Intake GUI

A Docker-based web application for viewing and sharing NOMAD threat intelligence reports.

## Features

- **Link-only access**: Reports are only viewable via share links (no public browsing)
- **PDF export**: Download reports as professionally formatted PDFs
- **Password protection**: Optional password protection for sensitive reports
- **Expiring links**: Share links can auto-expire after a configurable period
- **API-first**: Full REST API for integration with Claude Code

## Quick Start

### Local Development

```bash
# Create environment file
cp .env.example .env
# Edit .env and set NOMAD_WEB_API_TOKEN

# Build and run
docker-compose up --build

# Access at http://localhost:8080
```

### Production Deployment

See `deployment/ansible/` for Hetzner Cloud deployment with Ansible.

## API Endpoints

### Authentication

All `/api/v1/*` endpoints require Bearer token authentication:

```
Authorization: Bearer <NOMAD_WEB_API_TOKEN>
```

### Submit Report

```bash
curl -X POST http://localhost:8080/api/v1/reports \
  -H "Authorization: Bearer $NOMAD_WEB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "executive-brief",
    "title": "Weekly Threat Summary",
    "organization": "Acme Corp",
    "content": {
      "markdown": "# Summary\n\nYour report content..."
    },
    "classification": "INTERNAL"
  }'
```

### Generate Share Link

```bash
curl -X POST http://localhost:8080/api/v1/reports/rpt_xxx/share \
  -H "Authorization: Bearer $NOMAD_WEB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "expires_hours": 72,
    "allow_download": true
  }'
```

### View Shared Report

```
GET /s/{share_token}           # View report
GET /s/{share_token}/pdf       # Download PDF
GET /s/{share_token}?password=xxx  # Password-protected
```

## Report Types

| Type | Description |
|------|-------------|
| `executive-brief` | High-level summary for leadership |
| `technical-alert` | Detailed technical analysis for SOC |
| `weekly-summary` | Weekly threat landscape overview |
| `threats` | Current threat intelligence |
| `cve-analysis` | Deep dive on specific CVE |
| `critical` | Critical/urgent alerts |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NOMAD_WEB_API_TOKEN` | Yes | - | API authentication token |
| `NOMAD_SECRET_KEY` | No | Auto-generated | JWT signing key |
| `SHARE_EXPIRY_HOURS` | No | 72 | Default share link expiry |
| `DEBUG` | No | false | Enable debug mode |

## Architecture

```
┌─────────────────────────────────────────┐
│           FastAPI Application           │
├─────────────────────────────────────────┤
│  /api/v1/reports    - Report CRUD       │
│  /api/v1/.../share  - Share management  │
│  /s/{token}         - Public viewing    │
│  /health            - Health checks     │
├─────────────────────────────────────────┤
│         SQLite Database                 │
│  - Reports metadata                     │
│  - Share tokens & expiry                │
└─────────────────────────────────────────┘
```

## Security

- API endpoints require Bearer token authentication
- Share tokens are cryptographically random (24+ bytes)
- Passwords are hashed with bcrypt
- HTML content is sanitized to prevent XSS
- No report browsing without valid share link

## License

Part of the NOMAD Threat Intelligence Framework.
