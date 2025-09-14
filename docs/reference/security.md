# NOMAD Security Guide

Comprehensive security guide for deploying and operating NOMAD in production environments.

## Table of Contents

- [Security Overview](#security-overview)
- [API Key Management](#api-key-management)
- [Data Protection](#data-protection)
- [Network Security](#network-security)
- [Input Validation](#input-validation)
- [Audit and Logging](#audit-and-logging)
- [Production Deployment Security](#production-deployment-security)
- [Compliance Considerations](#compliance-considerations)
- [Incident Response](#incident-response)
- [Security Configuration](#security-configuration)
- [Threat Model](#threat-model)
- [Security Monitoring](#security-monitoring)

## Security Overview

NOMAD processes sensitive threat intelligence data and integrates with external APIs, making security a critical concern. This guide covers security best practices for development, deployment, and operations.

### Security Principles

- **Defense in Depth**: Multiple security layers
- **Least Privilege**: Minimal required permissions
- **Zero Trust**: Verify every interaction
- **Data Classification**: Appropriate protection levels
- **Audit Everything**: Complete activity logging

### Threat Landscape

NOMAD faces these primary security threats:
- API key compromise and misuse
- Data injection and manipulation attacks
- Unauthorized access to sensitive intelligence
- Man-in-the-middle attacks on external API calls
- Data exfiltration and insider threats

## API Key Management

### Secure Storage

**Environment Variables Only**
```bash
# .env file (never commit to version control)
ANTHROPIC_API_KEY=sk-ant-api03-xxx
VIRUSTOTAL_API_KEY=xxx
SHODAN_API_KEY=xxx
```

**File Permissions**
```bash
# Set restrictive permissions on configuration files
chmod 600 .env
chmod 700 config/
```

**Secret Management Systems**
```python
# Production: Use dedicated secret management
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# config/environment.py
class SecureConfig:
    def __init__(self):
        if os.getenv('ENVIRONMENT') == 'production':
            self.anthropic_key = get_secret('nomad/anthropic-api-key')
        else:
            self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
```

### API Key Rotation

**Automated Rotation Strategy**
```python
class APIKeyManager:
    def __init__(self):
        self.rotation_interval = timedelta(days=30)
        self.warning_threshold = timedelta(days=7)

    def check_key_expiry(self):
        """Check if API keys need rotation"""
        for service, last_rotation in self.key_rotations.items():
            time_since_rotation = datetime.now() - last_rotation
            if time_since_rotation >= self.rotation_interval:
                self.logger.warning(f"API key for {service} requires rotation")
                self.notify_rotation_required(service)

    def rotate_key(self, service: str):
        """Rotate API key for specified service"""
        # Implementation depends on service provider
        pass
```

### Key Validation

**Startup Validation**
```python
class APIValidator:
    def validate_all_keys(self):
        """Validate all API keys at startup"""
        results = {}

        # Anthropic API
        results['anthropic'] = self._validate_anthropic_key()

        # Other APIs
        results['virustotal'] = self._validate_virustotal_key()

        return results

    def _validate_anthropic_key(self):
        """Test Anthropic API key validity"""
        try:
            client = anthropic.Anthropic(api_key=self.config.anthropic_key)
            # Make a minimal test request
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return {"valid": True, "quota_remaining": response.usage}
        except Exception as e:
            return {"valid": False, "error": str(e)}
```

## Data Protection

### Data Classification

**Intelligence Data Classification**
```python
class DataClassification:
    CLASSIFICATIONS = {
        'PUBLIC': {
            'description': 'Publicly available threat intelligence',
            'storage': 'any',
            'transmission': 'any',
            'retention': '5 years'
        },
        'INTERNAL': {
            'description': 'Organization-specific threat context',
            'storage': 'encrypted',
            'transmission': 'TLS 1.3+',
            'retention': '3 years'
        },
        'CONFIDENTIAL': {
            'description': 'Sensitive threat intelligence, asset mapping',
            'storage': 'encrypted + access control',
            'transmission': 'mutual TLS',
            'retention': '1 year'
        },
        'RESTRICTED': {
            'description': 'Highly sensitive organizational security data',
            'storage': 'encrypted + HSM',
            'transmission': 'encrypted + signed',
            'retention': '6 months'
        }
    }
```

### Encryption at Rest

**File-Based Encryption**
```python
from cryptography.fernet import Fernet
import os

class SecureStorage:
    def __init__(self):
        # Use environment-specific encryption key
        key = os.getenv('NOMAD_ENCRYPTION_KEY')
        if not key:
            key = Fernet.generate_key()
            self.logger.warning("Generated new encryption key - store securely!")

        self.fernet = Fernet(key.encode() if isinstance(key, str) else key)

    def save_encrypted(self, data: dict, filepath: str):
        """Save data with encryption"""
        json_data = json.dumps(data).encode()
        encrypted_data = self.fernet.encrypt(json_data)

        with open(filepath, 'wb') as f:
            f.write(encrypted_data)

        # Set secure file permissions
        os.chmod(filepath, 0o600)

    def load_encrypted(self, filepath: str) -> dict:
        """Load and decrypt data"""
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = self.fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
```

### Encryption in Transit

**Secure HTTP Client**
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl

class SecureHTTPAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        # Force TLS 1.3
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

class SecureAPIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.mount('https://', SecureHTTPAdapter())

        # Security headers
        self.session.headers.update({
            'User-Agent': 'NOMAD-ThreatIntel/1.0',
            'Accept': 'application/json',
            'Cache-Control': 'no-cache'
        })

        # Timeouts and retries
        self.session.timeout = 30

    def secure_get(self, url: str, **kwargs):
        """Make secure GET request"""
        # Validate URL
        if not url.startswith('https://'):
            raise ValueError("Only HTTPS URLs allowed")

        return self.session.get(url, **kwargs)
```

### Data Sanitization

**Input Sanitization**
```python
import re
from html import escape
from urllib.parse import urlparse

class DataSanitizer:
    def __init__(self):
        # Patterns for known injection attempts
        self.sql_injection_patterns = [
            r"(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b)",
            r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
            r"(\';|\"\;|\/\*|\*\/)"
        ]

        self.xss_patterns = [
            r"<script.*?>.*?</script>",
            r"javascript:",
            r"on\w+\s*="
        ]

    def sanitize_intelligence_item(self, item: dict) -> dict:
        """Sanitize intelligence item data"""
        sanitized = {}

        for key, value in item.items():
            if isinstance(value, str):
                sanitized[key] = self._sanitize_string(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_string(v) if isinstance(v, str) else v for v in value]
            else:
                sanitized[key] = value

        return sanitized

    def _sanitize_string(self, text: str) -> str:
        """Sanitize string input"""
        # Remove potential SQL injection
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                self.logger.warning(f"Potential SQL injection detected: {text[:100]}")
                text = re.sub(pattern, "[FILTERED]", text, flags=re.IGNORECASE)

        # Remove potential XSS
        for pattern in self.xss_patterns:
            text = re.sub(pattern, "[FILTERED]", text, flags=re.IGNORECASE)

        # HTML escape
        text = escape(text)

        return text

    def validate_url(self, url: str) -> bool:
        """Validate URL format and scheme"""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ['http', 'https'] and parsed.netloc
        except Exception:
            return False
```

## Network Security

### Firewall Configuration

**Ingress Rules**
```bash
# Only allow necessary inbound connections
# Management SSH (restrict to admin IPs)
sudo ufw allow from 10.0.0.0/8 to any port 22

# HTTPS (if web interface is added)
sudo ufw allow 443/tcp

# Block all other inbound
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

**Egress Filtering**
```python
# config/allowed_domains.py
ALLOWED_DOMAINS = {
    'anthropic.com',          # Claude API
    'api.anthropic.com',
    'feeds.feedburner.com',   # RSS feeds
    'nvd.nist.gov',          # CVE data
    'cve.mitre.org',
    'www.cisa.gov',          # CISA feeds
    # Add other legitimate threat intel sources
}

class NetworkPolicy:
    def validate_outbound_request(self, url: str) -> bool:
        """Validate outbound requests against allowlist"""
        domain = urlparse(url).netloc

        # Check against allowed domains
        for allowed in self.ALLOWED_DOMAINS:
            if domain.endswith(allowed):
                return True

        self.logger.warning(f"Blocked outbound request to: {domain}")
        return False
```

### TLS Configuration

**Strict TLS Settings**
```python
import ssl

class TLSConfig:
    @staticmethod
    def get_secure_context():
        """Get secure SSL context"""
        context = ssl.create_default_context()

        # Require TLS 1.3
        context.minimum_version = ssl.TLSVersion.TLSv1_3

        # Strict certificate validation
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Disable insecure protocols
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.options |= ssl.OP_NO_TLSv1_2

        return context
```

### Rate Limiting

**API Rate Limiting**
```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.limits = {
            'anthropic': {'requests': 100, 'window': 60},  # 100 req/min
            'default': {'requests': 60, 'window': 60}       # 60 req/min
        }

    def check_rate_limit(self, service: str, identifier: str = 'default') -> bool:
        """Check if request is within rate limits"""
        key = f"{service}:{identifier}"
        now = time.time()

        # Get service limits
        limits = self.limits.get(service, self.limits['default'])
        window = limits['window']
        max_requests = limits['requests']

        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < window
        ]

        # Check if under limit
        if len(self.requests[key]) >= max_requests:
            return False

        # Record this request
        self.requests[key].append(now)
        return True

    def get_retry_after(self, service: str, identifier: str = 'default') -> int:
        """Get seconds to wait before next request"""
        key = f"{service}:{identifier}"
        if not self.requests[key]:
            return 0

        limits = self.limits.get(service, self.limits['default'])
        oldest_request = min(self.requests[key])
        return max(0, int(limits['window'] - (time.time() - oldest_request)))
```

## Input Validation

### Schema Validation

**Strict Input Validation**
```python
import jsonschema
from typing import Dict, Any

class InputValidator:
    def __init__(self):
        # Load schemas
        self.intelligence_schema = self._load_intelligence_schema()
        self.config_schema = self._load_config_schema()

    def validate_intelligence_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize intelligence item"""
        try:
            # Schema validation
            jsonschema.validate(item, self.intelligence_schema)

            # Custom business logic validation
            self._validate_cve_format(item.get('cves', []))
            self._validate_timestamp(item.get('published_utc'))
            self._validate_admiralty_rating(item.get('admiralty_source_reliability'))

            # Sanitize strings
            sanitized = self._sanitize_strings(item)

            return sanitized

        except jsonschema.ValidationError as e:
            raise ValueError(f"Schema validation failed: {e.message}")
        except Exception as e:
            raise ValueError(f"Validation failed: {str(e)}")

    def _validate_cve_format(self, cves: list):
        """Validate CVE format"""
        cve_pattern = re.compile(r'^CVE-\d{4}-\d{4,7}$')
        for cve in cves:
            if not cve_pattern.match(cve):
                raise ValueError(f"Invalid CVE format: {cve}")

    def _validate_timestamp(self, timestamp: str):
        """Validate ISO timestamp"""
        if timestamp:
            try:
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError(f"Invalid timestamp format: {timestamp}")

    def _validate_admiralty_rating(self, rating: str):
        """Validate Admiralty rating"""
        if rating and rating not in ['A', 'B', 'C', 'D', 'E', 'F']:
            raise ValueError(f"Invalid Admiralty rating: {rating}")
```

### Command Injection Prevention

**Safe Command Execution**
```python
import shlex
import subprocess
from pathlib import Path

class SafeCommandExecutor:
    ALLOWED_COMMANDS = {
        'git': ['/usr/bin/git'],
        'python': ['/usr/bin/python3', '/usr/local/bin/python3']
    }

    def execute_safe_command(self, command: str, cwd: str = None) -> str:
        """Safely execute system commands"""
        # Parse command
        try:
            args = shlex.split(command)
        except ValueError:
            raise ValueError("Invalid command syntax")

        # Validate command
        if not args:
            raise ValueError("Empty command")

        cmd_name = Path(args[0]).name
        if cmd_name not in self.ALLOWED_COMMANDS:
            raise ValueError(f"Command not allowed: {cmd_name}")

        # Use full path
        full_cmd_paths = self.ALLOWED_COMMANDS[cmd_name]
        args[0] = next(path for path in full_cmd_paths if Path(path).exists())

        # Validate working directory
        if cwd and not Path(cwd).is_dir():
            raise ValueError("Invalid working directory")

        # Execute with restrictions
        try:
            result = subprocess.run(
                args,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30,
                check=True
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            raise RuntimeError("Command timed out")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}")
```

## Audit and Logging

### Security Audit Logging

**Comprehensive Audit Trail**
```python
import logging
import json
from datetime import datetime
from typing import Dict, Any

class SecurityAuditLogger:
    def __init__(self):
        # Create security-specific logger
        self.audit_logger = logging.getLogger('nomad.security.audit')
        self.audit_logger.setLevel(logging.INFO)

        # File handler for audit logs
        audit_handler = logging.FileHandler('/var/log/nomad/security_audit.log')
        audit_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        self.audit_logger.addHandler(audit_handler)

        # SIEM handler (if configured)
        if os.getenv('SIEM_ENDPOINT'):
            siem_handler = SIEMHandler(os.getenv('SIEM_ENDPOINT'))
            self.audit_logger.addHandler(siem_handler)

    def log_api_access(self, service: str, endpoint: str, user_id: str = None,
                      success: bool = True, error: str = None):
        """Log API access attempts"""
        event = {
            'event_type': 'api_access',
            'timestamp': datetime.utcnow().isoformat(),
            'service': service,
            'endpoint': endpoint,
            'user_id': user_id or 'system',
            'success': success,
            'error': error,
            'source_ip': self._get_source_ip()
        }
        self.audit_logger.info(json.dumps(event))

    def log_data_access(self, operation: str, data_type: str,
                       classification: str, success: bool = True):
        """Log data access events"""
        event = {
            'event_type': 'data_access',
            'timestamp': datetime.utcnow().isoformat(),
            'operation': operation,  # read, write, delete
            'data_type': data_type,  # intelligence, config, logs
            'classification': classification,  # public, internal, confidential
            'success': success,
            'user_id': self._get_current_user(),
            'process_id': os.getpid()
        }
        self.audit_logger.info(json.dumps(event))

    def log_config_change(self, component: str, setting: str,
                         old_value: str, new_value: str):
        """Log configuration changes"""
        event = {
            'event_type': 'config_change',
            'timestamp': datetime.utcnow().isoformat(),
            'component': component,
            'setting': setting,
            'old_value': self._redact_sensitive(old_value),
            'new_value': self._redact_sensitive(new_value),
            'user_id': self._get_current_user()
        }
        self.audit_logger.info(json.dumps(event))

    def log_security_event(self, event_type: str, severity: str,
                          description: str, details: Dict[str, Any] = None):
        """Log security-relevant events"""
        event = {
            'event_type': 'security_event',
            'timestamp': datetime.utcnow().isoformat(),
            'security_event_type': event_type,
            'severity': severity,  # low, medium, high, critical
            'description': description,
            'details': details or {},
            'source_ip': self._get_source_ip(),
            'user_agent': self._get_user_agent()
        }
        self.audit_logger.warning(json.dumps(event))
```

### Log Protection

**Secure Log Management**
```python
class SecureLogManager:
    def __init__(self):
        self.log_dir = Path('/var/log/nomad')
        self.log_dir.mkdir(mode=0o750, parents=True, exist_ok=True)

        # Log rotation settings
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        self.backup_count = 10

    def setup_secure_logging(self):
        """Configure secure logging"""
        # Main application log
        main_handler = RotatingFileHandler(
            self.log_dir / 'nomad.log',
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )

        # Security audit log
        audit_handler = RotatingFileHandler(
            self.log_dir / 'security_audit.log',
            maxBytes=self.max_file_size,
            backupCount=self.backup_count * 2  # Keep more audit logs
        )

        # Error log
        error_handler = RotatingFileHandler(
            self.log_dir / 'error.log',
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        error_handler.setLevel(logging.ERROR)

        # Set secure permissions on log files
        for handler in [main_handler, audit_handler, error_handler]:
            if hasattr(handler, 'stream') and hasattr(handler.stream, 'name'):
                os.chmod(handler.stream.name, 0o640)

    def sanitize_log_entry(self, message: str) -> str:
        """Remove sensitive data from log entries"""
        # Redact API keys
        message = re.sub(r'sk-ant-api03-[A-Za-z0-9-_]{95}', '[REDACTED-API-KEY]', message)

        # Redact other sensitive patterns
        patterns = [
            (r'password["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'password=[REDACTED]'),
            (r'token["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'token=[REDACTED]'),
            (r'key["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'key=[REDACTED]')
        ]

        for pattern, replacement in patterns:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)

        return message
```

## Production Deployment Security

### Container Security

**Docker Security Configuration**
```dockerfile
# Use minimal base image
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r nomad && useradd -r -g nomad nomad

# Set secure working directory
WORKDIR /app
RUN chown nomad:nomad /app

# Install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=nomad:nomad . .

# Switch to non-root user
USER nomad

# Use specific Python executable
ENTRYPOINT ["/usr/local/bin/python", "-m", "nomad"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "from config.environment import config; config.validate_api_access()" || exit 1
```

**Docker Compose Security**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  nomad:
    build: .
    restart: unless-stopped

    # Security options
    security_opt:
      - no-new-privileges:true

    # Read-only root filesystem
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp

    # Resource limits
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M

    # Network security
    networks:
      - nomad-internal

    # Environment
    environment:
      - ENVIRONMENT=production
    env_file:
      - .env.prod

    # Volumes
    volumes:
      - ./data:/app/data:ro
      - ./logs:/app/logs:rw
      - ./config:/app/config:ro

networks:
  nomad-internal:
    driver: bridge
    internal: true
```

### System Hardening

**OS Security Configuration**
```bash
#!/bin/bash
# system-hardening.sh

# Update system
apt update && apt upgrade -y

# Install security tools
apt install -y fail2ban ufw aide rkhunter

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow from 10.0.0.0/8 to any port 22
ufw --force enable

# Harden SSH
cat >> /etc/ssh/sshd_config << EOF
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 0
X11Forwarding no
EOF

systemctl restart sshd

# Configure fail2ban
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
EOF

systemctl enable fail2ban
systemctl start fail2ban

# Set up intrusion detection
aide --init
mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Create daily security check
cat > /etc/cron.daily/security-check << 'EOF'
#!/bin/bash
/usr/bin/aide --check
/usr/bin/rkhunter --check --skip-keypress
EOF
chmod +x /etc/cron.daily/security-check
```

### Secret Management

**Production Secret Management**
```python
# config/secrets.py
import boto3
import hvac
from typing import Dict, Any

class SecretManager:
    def __init__(self, backend: str = 'env'):
        self.backend = backend
        self._init_backend()

    def _init_backend(self):
        """Initialize secret management backend"""
        if self.backend == 'aws':
            self.client = boto3.client('secretsmanager')
        elif self.backend == 'vault':
            self.client = hvac.Client(url=os.getenv('VAULT_URL'))
            self.client.token = os.getenv('VAULT_TOKEN')
        elif self.backend == 'env':
            self.client = None

    def get_secret(self, secret_name: str) -> str:
        """Retrieve secret by name"""
        try:
            if self.backend == 'aws':
                response = self.client.get_secret_value(SecretId=secret_name)
                return response['SecretString']

            elif self.backend == 'vault':
                response = self.client.secrets.kv.v2.read_secret_version(
                    path=secret_name
                )
                return response['data']['data']['value']

            elif self.backend == 'env':
                value = os.getenv(secret_name)
                if not value:
                    raise ValueError(f"Environment variable {secret_name} not found")
                return value

        except Exception as e:
            self.logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            raise

    def get_all_secrets(self) -> Dict[str, str]:
        """Get all required secrets"""
        secrets = {}
        required_secrets = [
            'ANTHROPIC_API_KEY',
            'NOMAD_ENCRYPTION_KEY',
            'VIRUSTOTAL_API_KEY',
            'SHODAN_API_KEY'
        ]

        for secret_name in required_secrets:
            try:
                secrets[secret_name] = self.get_secret(secret_name)
            except Exception as e:
                self.logger.warning(f"Optional secret {secret_name} not available: {e}")

        return secrets
```

## Compliance Considerations

### Data Retention

**Retention Policy Implementation**
```python
class DataRetentionManager:
    def __init__(self):
        self.retention_policies = {
            'intelligence_raw': timedelta(days=365),      # 1 year
            'intelligence_processed': timedelta(days=730), # 2 years
            'audit_logs': timedelta(days=2555),           # 7 years
            'error_logs': timedelta(days=90),             # 3 months
            'cache_data': timedelta(hours=24)             # 24 hours
        }

    def cleanup_expired_data(self):
        """Remove data past retention period"""
        for data_type, retention_period in self.retention_policies.items():
            cutoff_date = datetime.now() - retention_period
            self._cleanup_data_type(data_type, cutoff_date)

    def _cleanup_data_type(self, data_type: str, cutoff_date: datetime):
        """Clean up specific data type"""
        if data_type == 'intelligence_raw':
            self._cleanup_intelligence_files(cutoff_date, 'raw')
        elif data_type == 'audit_logs':
            self._cleanup_log_files('security_audit.log', cutoff_date)
        # ... handle other data types
```

### Privacy Protection

**PII Detection and Handling**
```python
import re
from typing import List, Dict

class PIIProtection:
    def __init__(self):
        # PII detection patterns
        self.pii_patterns = {
            'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            'credit_card': re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'ip_internal': re.compile(r'\b(10\.|172\.1[6-9]\.|172\.2[0-9]\.|172\.3[0-1]\.|192\.168\.)\d{1,3}\.\d{1,3}\b'),
            'phone': re.compile(r'\b\d{3}-\d{3}-\d{4}\b')
        }

    def scan_for_pii(self, text: str) -> List[Dict[str, str]]:
        """Scan text for PII"""
        findings = []

        for pii_type, pattern in self.pii_patterns.items():
            matches = pattern.findall(text)
            for match in matches:
                findings.append({
                    'type': pii_type,
                    'value': match,
                    'severity': self._get_pii_severity(pii_type)
                })

        return findings

    def redact_pii(self, text: str) -> str:
        """Redact PII from text"""
        redacted_text = text

        for pii_type, pattern in self.pii_patterns.items():
            if pii_type == 'email':
                # Keep domain for threat intel context
                redacted_text = pattern.sub(r'[REDACTED-EMAIL]@\2', redacted_text)
            elif pii_type == 'ip_internal':
                # Critical to redact internal IPs
                redacted_text = pattern.sub('[REDACTED-INTERNAL-IP]', redacted_text)
            else:
                redacted_text = pattern.sub(f'[REDACTED-{pii_type.upper()}]', redacted_text)

        return redacted_text
```

## Incident Response

### Security Incident Detection

**Automated Incident Detection**
```python
class SecurityIncidentDetector:
    def __init__(self):
        self.alert_thresholds = {
            'failed_api_calls': {'count': 10, 'window': 300},  # 10 failures in 5 min
            'unusual_data_access': {'count': 100, 'window': 3600},  # 100 accesses in 1 hour
            'config_changes': {'count': 5, 'window': 900}     # 5 changes in 15 min
        }

        self.incident_handlers = {
            'api_compromise': self._handle_api_compromise,
            'data_breach': self._handle_data_breach,
            'config_tampering': self._handle_config_tampering
        }

    def detect_incidents(self):
        """Check for security incidents"""
        current_time = time.time()

        # Check API failures
        api_failures = self._get_recent_events('api_failure', 300)
        if len(api_failures) >= self.alert_thresholds['failed_api_calls']['count']:
            self._trigger_incident('api_compromise', {
                'failure_count': len(api_failures),
                'timeframe': '5 minutes',
                'last_failures': api_failures[-5:]
            })

        # Check data access patterns
        data_accesses = self._get_recent_events('data_access', 3600)
        if len(data_accesses) >= self.alert_thresholds['unusual_data_access']['count']:
            self._trigger_incident('data_breach', {
                'access_count': len(data_accesses),
                'timeframe': '1 hour',
                'accessed_types': list(set(event['data_type'] for event in data_accesses))
            })

    def _trigger_incident(self, incident_type: str, details: dict):
        """Trigger security incident response"""
        incident_id = self._generate_incident_id()

        # Log incident
        self.logger.critical(f"Security incident detected: {incident_type} - {incident_id}")

        # Execute incident handler
        if incident_type in self.incident_handlers:
            self.incident_handlers[incident_type](incident_id, details)

        # Notify security team
        self._notify_security_team(incident_type, incident_id, details)

    def _handle_api_compromise(self, incident_id: str, details: dict):
        """Handle suspected API key compromise"""
        # Temporarily disable API access
        self._disable_api_access()

        # Rotate API keys
        self._initiate_key_rotation()

        # Block suspicious IPs
        self._update_firewall_rules(details.get('source_ips', []))
```

### Incident Response Playbook

**Automated Response Actions**
```python
class IncidentResponsePlaybook:
    def __init__(self):
        self.playbooks = {
            'api_compromise': self._api_compromise_playbook,
            'data_breach': self._data_breach_playbook,
            'malware_detection': self._malware_playbook
        }

    def execute_playbook(self, incident_type: str, incident_data: dict):
        """Execute incident response playbook"""
        if incident_type in self.playbooks:
            return self.playbooks[incident_type](incident_data)

    def _api_compromise_playbook(self, incident_data: dict):
        """API compromise response"""
        steps = [
            {'action': 'isolate_system', 'priority': 1},
            {'action': 'rotate_api_keys', 'priority': 1},
            {'action': 'audit_recent_api_calls', 'priority': 2},
            {'action': 'notify_stakeholders', 'priority': 2},
            {'action': 'update_security_controls', 'priority': 3}
        ]

        for step in sorted(steps, key=lambda x: x['priority']):
            self._execute_response_step(step['action'], incident_data)

    def _execute_response_step(self, action: str, incident_data: dict):
        """Execute individual response step"""
        try:
            if action == 'isolate_system':
                self._isolate_system()
            elif action == 'rotate_api_keys':
                self._rotate_all_api_keys()
            elif action == 'audit_recent_api_calls':
                self._audit_api_calls(incident_data)
            # ... other actions

            self.logger.info(f"Incident response step completed: {action}")

        except Exception as e:
            self.logger.error(f"Incident response step failed: {action} - {e}")
```

## Security Configuration

### Security Configuration Template

**Production Security Config**
```yaml
# config/security.yml
security:
  # Encryption settings
  encryption:
    algorithm: "AES-256-GCM"
    key_rotation_days: 90

  # API security
  api_security:
    rate_limiting:
      anthropic: 100  # requests per minute
      external_apis: 60
    timeout_seconds: 30
    retry_attempts: 3

  # Network security
  network:
    allowed_domains:
      - "api.anthropic.com"
      - "nvd.nist.gov"
      - "feeds.feedburner.com"
    tls_version: "1.3"
    certificate_validation: true

  # Data protection
  data_protection:
    classification_required: true
    pii_scanning: true
    retention_days:
      public: 1825      # 5 years
      internal: 1095    # 3 years
      confidential: 365 # 1 year

  # Audit settings
  audit:
    log_all_api_calls: true
    log_data_access: true
    log_config_changes: true
    siem_integration: true

  # Incident response
  incident_response:
    auto_isolation: false
    notification_channels:
      - email
      - slack
    escalation_minutes: 15
```

### Runtime Security Validation

**Security Check Framework**
```python
class SecurityValidator:
    def __init__(self):
        self.checks = [
            self._check_api_keys,
            self._check_file_permissions,
            self._check_network_config,
            self._check_encryption_status,
            self._check_audit_logging
        ]

    def run_security_checks(self) -> Dict[str, Any]:
        """Run all security validation checks"""
        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_status': 'pass',
            'checks': {}
        }

        for check in self.checks:
            try:
                check_name = check.__name__.replace('_check_', '')
                check_result = check()
                results['checks'][check_name] = check_result

                if not check_result['status']:
                    results['overall_status'] = 'fail'

            except Exception as e:
                results['checks'][check_name] = {
                    'status': False,
                    'error': str(e)
                }
                results['overall_status'] = 'error'

        return results

    def _check_api_keys(self) -> Dict[str, Any]:
        """Validate API key security"""
        result = {'status': True, 'issues': []}

        # Check if keys are in environment (not hardcoded)
        if 'sk-ant-' in open(__file__).read():
            result['status'] = False
            result['issues'].append('API key found in source code')

        # Check key format
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key and not api_key.startswith('sk-ant-'):
            result['status'] = False
            result['issues'].append('Invalid API key format')

        return result

    def _check_file_permissions(self) -> Dict[str, Any]:
        """Check file and directory permissions"""
        result = {'status': True, 'issues': []}

        sensitive_files = ['.env', 'config/', 'data/']

        for file_path in sensitive_files:
            if os.path.exists(file_path):
                stat_info = os.stat(file_path)
                permissions = oct(stat_info.st_mode)[-3:]

                if file_path.endswith('.env') and permissions != '600':
                    result['status'] = False
                    result['issues'].append(f'{file_path} has insecure permissions: {permissions}')

        return result
```

## Threat Model

### NOMAD Threat Model

**Asset Identification**
```python
THREAT_MODEL = {
    'assets': {
        'high_value': [
            'API keys (Anthropic, external services)',
            'Threat intelligence data (confidential)',
            'Organization security context',
            'System credentials and certificates'
        ],
        'medium_value': [
            'Processed intelligence reports',
            'Configuration files',
            'Audit logs and security events'
        ],
        'low_value': [
            'Public threat intelligence',
            'Application logs',
            'Temporary cache files'
        ]
    },

    'threat_actors': [
        {
            'name': 'External Attackers',
            'motivation': 'Data theft, system compromise',
            'capabilities': 'High technical skills, persistent',
            'attack_vectors': ['Network intrusion', 'API exploitation', 'Social engineering']
        },
        {
            'name': 'Malicious Insiders',
            'motivation': 'Data theft, sabotage',
            'capabilities': 'System access, insider knowledge',
            'attack_vectors': ['Data exfiltration', 'Configuration tampering', 'Credential misuse']
        },
        {
            'name': 'Nation State Actors',
            'motivation': 'Intelligence gathering, disruption',
            'capabilities': 'Advanced persistent threat techniques',
            'attack_vectors': ['Supply chain compromise', 'Zero-day exploits', 'Long-term persistence']
        }
    ],

    'attack_scenarios': [
        {
            'name': 'API Key Compromise',
            'likelihood': 'Medium',
            'impact': 'High',
            'description': 'Attacker gains access to Claude API keys',
            'mitigations': ['Key rotation', 'Usage monitoring', 'Rate limiting']
        },
        {
            'name': 'Data Poisoning',
            'likelihood': 'Medium',
            'impact': 'Medium',
            'description': 'Malicious RSS feeds inject false intelligence',
            'mitigations': ['Source validation', 'Content filtering', 'Admiralty ratings']
        },
        {
            'name': 'System Compromise',
            'likelihood': 'Low',
            'impact': 'High',
            'description': 'Full system compromise via exploitation',
            'mitigations': ['System hardening', 'Access controls', 'Monitoring']
        }
    ]
}
```

## Security Monitoring

### Real-Time Security Monitoring

**Security Monitoring Dashboard**
```python
class SecurityMonitor:
    def __init__(self):
        self.metrics = {
            'api_calls': Counter(),
            'failed_authentications': Counter(),
            'suspicious_activities': Counter(),
            'data_access_events': Counter()
        }

        self.alerts = {
            'api_rate_exceeded': {'threshold': 1000, 'window': 3600},
            'failed_auth_spike': {'threshold': 10, 'window': 300},
            'unusual_data_access': {'threshold': 500, 'window': 3600}
        }

    def monitor_api_usage(self):
        """Monitor API usage patterns"""
        current_hour = datetime.now().hour
        hourly_calls = self.metrics['api_calls'].get(current_hour, 0)

        if hourly_calls > self.alerts['api_rate_exceeded']['threshold']:
            self._trigger_alert('api_rate_exceeded', {
                'calls': hourly_calls,
                'threshold': self.alerts['api_rate_exceeded']['threshold'],
                'hour': current_hour
            })

    def generate_security_report(self) -> Dict[str, Any]:
        """Generate security status report"""
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'healthy',
            'metrics': {
                'total_api_calls': sum(self.metrics['api_calls'].values()),
                'failed_authentications': sum(self.metrics['failed_authentications'].values()),
                'security_events': sum(self.metrics['suspicious_activities'].values())
            },
            'alerts': self._get_active_alerts(),
            'recommendations': self._generate_security_recommendations()
        }

        return report

    def _generate_security_recommendations(self) -> List[str]:
        """Generate security recommendations based on current state"""
        recommendations = []

        # Check API key age
        if self._api_key_age() > timedelta(days=90):
            recommendations.append("Rotate API keys (>90 days old)")

        # Check for failed authentication patterns
        recent_failures = sum(self.metrics['failed_authentications'].values())
        if recent_failures > 50:
            recommendations.append("Investigate authentication failures")

        # Check log file sizes
        if self._get_log_size() > 1024 * 1024 * 100:  # 100MB
            recommendations.append("Archive or rotate log files")

        return recommendations
```

---

## Security Checklist

### Pre-Production Security Checklist

- [ ] **API Key Management**
  - [ ] API keys stored in environment variables or secret manager
  - [ ] No API keys in source code or configuration files
  - [ ] Key rotation schedule established
  - [ ] Key usage monitoring enabled

- [ ] **Data Protection**
  - [ ] Encryption at rest configured
  - [ ] TLS 1.3 enforced for all communications
  - [ ] Data classification implemented
  - [ ] PII detection and redaction enabled

- [ ] **Network Security**
  - [ ] Firewall rules configured (deny by default)
  - [ ] Egress filtering enabled
  - [ ] Rate limiting implemented
  - [ ] DDoS protection in place

- [ ] **System Hardening**
  - [ ] OS security updates applied
  - [ ] Unnecessary services disabled
  - [ ] File permissions configured securely
  - [ ] Non-root user for application execution

- [ ] **Audit and Monitoring**
  - [ ] Security audit logging enabled
  - [ ] SIEM integration configured
  - [ ] Real-time alerting set up
  - [ ] Log retention policy implemented

- [ ] **Incident Response**
  - [ ] Incident response playbooks created
  - [ ] Automated response capabilities tested
  - [ ] Contact lists and escalation procedures defined
  - [ ] Backup and recovery procedures validated

- [ ] **Compliance**
  - [ ] Data retention policies implemented
  - [ ] Privacy protection measures enabled
  - [ ] Regulatory requirements addressed
  - [ ] Security documentation completed

---

This comprehensive security guide provides the foundation for securely deploying and operating NOMAD in production environments. Regular security reviews and updates to these practices are essential to maintain strong security posture as threats evolve.