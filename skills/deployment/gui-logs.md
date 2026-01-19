---
name: gui-logs
description: View recent logs from the NOMAD Web Intake GUI deployment
argument-hint: "[lines] [--service app|caddy]"
---

# GUI Logs Skill

Fetch and display logs from the NOMAD Web Intake GUI deployment.

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `lines` | 100 | Number of log lines to fetch |
| `--service` | all | Filter by service: `app`, `caddy`, or `all` |

## Examples

```
/gui-logs              # Last 100 lines from all services
/gui-logs 50           # Last 50 lines
/gui-logs --service app    # Only application logs
/gui-logs 200 --service caddy  # Last 200 Caddy logs
```

## Workflow

```bash
cd deployment/ansible
ansible-playbook playbooks/logs.yml -e "lines=100 service=all"
```

## Output Format

```
📋 NOMAD Web GUI Logs

Server: nomad-web-gui (1.2.3.4)
Lines: 100 | Service: all

═══ Application Logs ═══
2026-01-09 10:15:23 INFO     Started server on 0.0.0.0:8080
2026-01-09 10:15:24 INFO     Database initialized
2026-01-09 10:16:01 INFO     POST /api/v1/reports 201 - 45ms
2026-01-09 10:16:02 INFO     POST /api/v1/reports/rpt_abc/share 201 - 12ms
2026-01-09 10:18:15 INFO     GET /s/sh_xyz 200 - 8ms
...

═══ Caddy Logs ═══
2026-01-09 10:15:20 {"level":"info","msg":"serving initial configuration"}
2026-01-09 10:16:01 {"level":"info","msg":"handled request","status":201}
...
```

## Log Filtering

Common patterns to look for:
- `ERROR` - Application errors
- `401` - Authentication failures
- `404` - Not found errors
- `POST /api/v1/reports` - Report submissions
- `GET /s/` - Shared report views
