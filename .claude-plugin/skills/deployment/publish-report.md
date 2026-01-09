---
name: publish-report
description: Publish a threat intelligence report to the Web Intake GUI and generate a share link
argument-hint: "[report-type] [--permanent] [--password <pass>] [--no-pdf]"
---

# Publish Report Skill

Publish a threat intelligence report to the NOMAD Web Intake GUI and optionally generate a shareable link.

## Arguments

| Argument | Description |
|----------|-------------|
| `report-type` | Type of report: `executive-brief`, `technical-alert`, `weekly-summary`, `threats`, `critical`, `cve` |
| `--permanent` | Create a non-expiring share link |
| `--password <pass>` | Require password to view the shared report |
| `--no-pdf` | Disable PDF download on share link |
| `--no-share` | Don't generate a share link |

## Examples

```
/publish-report executive-brief
/publish-report technical-alert --permanent
/publish-report weekly-summary --password SecretPass123
/publish-report threats --no-pdf
```

## Workflow

1. **Generate Report**: Run the appropriate report skill (e.g., `/executive-brief`)
2. **Format for API**: Convert report to JSON payload
3. **Submit to API**: POST to `/api/v1/reports`
4. **Generate Share Link**: POST to `/api/v1/reports/{id}/share`
5. **Return URLs**: Display report URL and share link

## API Integration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NOMAD_WEB_API_TOKEN` | Yes | API authentication token |
| `NOMAD_WEB_GUI_URL` | No | GUI URL (default: from config) |

### Submit Report

```bash
curl -X POST "$NOMAD_WEB_GUI_URL/api/v1/reports" \
  -H "Authorization: Bearer $NOMAD_WEB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "executive-brief",
    "title": "Weekly Threat Intelligence Summary",
    "organization": "Acme Corp",
    "content": {
      "markdown": "# Executive Summary\n\n..."
    },
    "metadata": {
      "period_start": "2026-01-02",
      "period_end": "2026-01-09",
      "threat_count": 45,
      "critical_count": 3
    },
    "classification": "INTERNAL"
  }'
```

### Generate Share Link

```bash
curl -X POST "$NOMAD_WEB_GUI_URL/api/v1/reports/$REPORT_ID/share" \
  -H "Authorization: Bearer $NOMAD_WEB_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "expires_hours": 72,
    "password": null,
    "allow_download": true
  }'
```

## Output Format

```
✓ Report Published Successfully

📄 Executive Threat Intelligence Brief
   ID: rpt_abc123xyz
   Type: executive-brief
   Classification: INTERNAL

🔗 Share Link (expires in 72 hours):
   https://nomad.example.com/s/sh_xyz789abc

📥 Direct PDF Download:
   https://nomad.example.com/s/sh_xyz789abc/pdf

To create additional share links:
   POST /api/v1/reports/rpt_abc123xyz/share
```

## Configuration

Add Web GUI settings to `config/user-preferences.json`:

```json
{
  "web_gui": {
    "enabled": true,
    "base_url": "http://1.2.3.4:8080",
    "api_token": "${NOMAD_WEB_API_TOKEN}",
    "auto_publish": false,
    "default_share_hours": 72
  }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API token | Check `NOMAD_WEB_API_TOKEN` |
| 404 Not Found | GUI not deployed | Run `/deploy-gui provision` |
| Connection refused | Server down | Check `/gui-status` |
| 500 Server Error | Application error | Check `/gui-logs` |
