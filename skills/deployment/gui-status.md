---
name: gui-status
description: Check NOMAD Web Intake GUI deployment status and health
---

# GUI Status Skill

Check the health and status of the NOMAD Web Intake GUI deployment.

## Workflow

1. Read server IP from Ansible inventory
2. Run status playbook to gather metrics
3. Display formatted status report

```bash
cd deployment/ansible
ansible-playbook playbooks/status.yml
```

## Output Format

```
📊 NOMAD Web GUI Status

Server: nomad-web-gui (1.2.3.4)
URL: http://1.2.3.4:8080

┌─────────────────────────────────────┐
│ Component        │ Status           │
├─────────────────────────────────────┤
│ App Container    │ ✓ Running        │
│ Caddy Container  │ ✓ Running        │
│ API Health       │ ✓ Healthy        │
│ Database         │ ✓ Connected      │
└─────────────────────────────────────┘

Storage:
  Data Size: 12MB
  Disk Free: 18GB (90%)

Reports:
  Total: 24
  This Week: 8

Last Backup: 2026-01-08 03:00 UTC
```

## Health Checks

The skill checks:
- Container status (running/stopped)
- API health endpoint response
- Database connectivity
- Disk usage and capacity
- Report count
- Backup status

## Error States

| State | Meaning | Action |
|-------|---------|--------|
| Container stopped | App crashed | Check logs with /gui-logs |
| API unhealthy | App not responding | Restart with /deploy-gui update |
| Database error | SQLite issue | Check disk space, restore backup |
| High disk usage | Running low on space | Clean old data or resize |
