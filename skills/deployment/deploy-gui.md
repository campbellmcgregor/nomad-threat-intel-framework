---
name: deploy-gui
description: Provision, update, or destroy the NOMAD Web Intake GUI on Hetzner Cloud
argument-hint: "[provision|update|destroy|status]"
---

# Deploy GUI Skill

Manage the NOMAD Web Intake GUI deployment on Hetzner Cloud using Ansible.

## Actions

| Action | Description |
|--------|-------------|
| `provision` | Create a new Hetzner server and deploy the application |
| `update` | Update existing deployment with latest code |
| `destroy` | Tear down the server (requires confirmation) |
| `status` | Check deployment status (alias for /gui-status) |

## Prerequisites

1. **Hetzner API Token**: Export `HETZNER_API_TOKEN`
2. **SSH Key**: Create an SSH key named `nomad-deploy` in Hetzner Console
3. **Ansible**: Install with `pip install ansible hcloud`

## Workflow

### Provision (First-time deployment)

1. Check environment variables are set
2. Install Ansible dependencies if needed
3. Run provision playbook to create Hetzner server
4. Run deploy playbook to install application
5. Return the application URL

```bash
cd deployment/ansible
ansible-galaxy collection install hetzner.hcloud community.docker community.general
ansible-playbook playbooks/provision.yml
ansible-playbook playbooks/deploy.yml
```

### Update (Existing deployment)

1. Verify server exists in inventory
2. Sync latest application code
3. Rebuild Docker image
4. Restart containers
5. Verify health check passes

```bash
cd deployment/ansible
ansible-playbook playbooks/deploy.yml
```

### Destroy

1. Confirm destruction with user
2. Backup data if requested
3. Run destroy playbook
4. Remove from inventory

```bash
cd deployment/ansible
ansible-playbook playbooks/destroy.yml
```

## Output Format

```
✓ NOMAD Web GUI Deployment

Action: provision
Status: Success

Server Details:
  Name: nomad-web-gui
  IP: 1.2.3.4
  Type: cx22 (2 vCPU, 4GB RAM)
  Location: fsn1

Application URL: http://1.2.3.4:8080
API Endpoint: http://1.2.3.4:8080/api/v1/reports

Next Steps:
  1. Set NOMAD_WEB_API_TOKEN in your environment
  2. Use /publish-report to publish threat intelligence reports
  3. Share reports using the generated links
```

## Cost Estimate

| Resource | Monthly Cost |
|----------|-------------|
| Hetzner CX22 | ~€4.50 |
| Optional Volume | ~€1.00 |
| **Total** | **~€5.50/month** |

## Error Handling

- If Hetzner API token is missing, prompt user to set it
- If SSH key doesn't exist, provide instructions to create one
- If server already exists during provision, offer to update instead
- If deployment fails, show logs and suggest fixes
