# NOMAD Deployment

Ansible playbooks for deploying NOMAD Web Intake GUI to Hetzner Cloud.

## Prerequisites

1. **Hetzner Cloud Account**
   - Create account at https://console.hetzner.cloud
   - Generate API token in project settings

2. **SSH Key**
   - Upload your SSH public key to Hetzner Console
   - Name it `nomad-deploy` (or update `group_vars/all.yml`)

3. **Ansible**
   ```bash
   pip install ansible
   ansible-galaxy collection install hetzner.hcloud community.docker community.general
   ```

## Environment Setup

```bash
export HETZNER_API_TOKEN="your-hetzner-api-token"
export NOMAD_WEB_API_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export NOMAD_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"

# Optional: Custom domain
export NOMAD_DOMAIN="nomad.example.com"
export LETSENCRYPT_EMAIL="admin@example.com"
```

## Usage

### Provision New Server

```bash
cd ansible
ansible-playbook playbooks/provision.yml
```

This will:
1. Create a Hetzner CX22 server (~€4.50/month)
2. Configure firewall (SSH, HTTP, HTTPS)
3. Install base packages and Docker
4. Update inventory with new server IP

### Deploy Application

```bash
ansible-playbook playbooks/deploy.yml
```

This will:
1. Copy application files to server
2. Build Docker image
3. Start containers with docker-compose
4. Verify health check passes

### Check Status

```bash
ansible-playbook playbooks/status.yml
```

### View Logs

```bash
# All logs
ansible-playbook playbooks/logs.yml

# Last 50 lines of app logs
ansible-playbook playbooks/logs.yml -e "lines=50 service=app"
```

### Backup Data

```bash
ansible-playbook playbooks/backup.yml
```

Backups are saved to `./backups/` locally.

### Destroy Server

```bash
ansible-playbook playbooks/destroy.yml
```

**Warning**: This permanently deletes the server and all data!

## Directory Structure

```
ansible/
├── ansible.cfg              # Ansible configuration
├── inventory/
│   ├── hosts.yml            # Server inventory (auto-managed)
│   └── group_vars/
│       └── all.yml          # Variables
├── playbooks/
│   ├── provision.yml        # Create server
│   ├── deploy.yml           # Deploy app
│   ├── destroy.yml          # Delete server
│   ├── backup.yml           # Backup data
│   ├── logs.yml             # View logs
│   └── status.yml           # Check status
└── templates/
    ├── .env.j2              # Environment file
    ├── docker-compose.prod.yml.j2
    └── Caddyfile.j2         # Reverse proxy config
```

## Claude Code Integration

Use these skills to manage deployment from Claude Code:

| Skill | Description |
|-------|-------------|
| `/deploy-gui provision` | Create new server |
| `/deploy-gui update` | Update deployment |
| `/deploy-gui destroy` | Delete server |
| `/gui-status` | Check health |
| `/gui-logs` | View logs |
| `/publish-report` | Push reports |

## Cost Breakdown

| Resource | Monthly Cost |
|----------|-------------|
| Hetzner CX22 (2 vCPU, 4GB RAM) | ~€4.50 |
| 20GB included storage | Free |
| IPv4 address | Included |
| **Total** | **~€4.50/month** |

## Troubleshooting

### Server won't provision
- Check `HETZNER_API_TOKEN` is valid
- Verify SSH key `nomad-deploy` exists in Hetzner Console
- Check Hetzner account has sufficient credit

### Deployment fails
- Run `ansible-playbook playbooks/status.yml` to check current state
- Check logs with `ansible-playbook playbooks/logs.yml`
- Verify Docker is running on server

### Can't access application
- Check firewall allows ports 80/443
- Verify DNS points to server IP (if using domain)
- Check application health: `curl http://SERVER_IP:8080/health`

### Share links not working
- Verify `NOMAD_WEB_API_TOKEN` matches between client and server
- Check link hasn't expired
- Verify password if protected
