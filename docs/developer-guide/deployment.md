# NOMAD Deployment Guide

Comprehensive guide for deploying NOMAD (Notable Object Monitoring And Analysis Director) in various environments from development to production.

## Table of Contents

- [Deployment Overview](#deployment-overview)
- [System Requirements](#system-requirements)
- [Local Development Deployment](#local-development-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Deployment](#production-deployment)
- [Environment Configuration](#environment-configuration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Backup and Recovery](#backup-and-recovery)
- [Scaling Strategies](#scaling-strategies)
- [Security Hardening](#security-hardening)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)
- [Maintenance and Updates](#maintenance-and-updates)

## Deployment Overview

NOMAD supports multiple deployment patterns to accommodate different organizational needs:

### Deployment Options

| Deployment Type | Use Case | Complexity | Scalability |
|----------------|----------|------------|-------------|
| **Local Development** | Development, testing | Low | Single instance |
| **Docker Compose** | Small teams, proof of concept | Medium | Limited scaling |
| **Kubernetes** | Production, enterprise | High | High scalability |
| **Cloud Managed** | Scalable production | Medium | Auto-scaling |
| **Hybrid** | On-premise + cloud | High | Custom scaling |

### Architecture Patterns

**Single-Node Deployment**
```
┌─────────────────────────────────────────┐
│                Server                   │
│  ┌─────────────────────────────────────┐│
│  │            NOMAD Core               ││
│  │  ┌─────────┐ ┌─────────┐ ┌────────┐ ││
│  │  │RSS Agent│ │Orchestr.│ │Reports │ ││
│  │  └─────────┘ └─────────┘ └────────┘ ││
│  └─────────────────────────────────────┘│
│  ┌─────────────────────────────────────┐│
│  │        Storage & Logs               ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

**Multi-Node Deployment**
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Agent Node 1  │  │   Agent Node 2  │  │   Agent Node 3  │
│  ┌─────────────┐│  │  ┌─────────────┐│  │  ┌─────────────┐│
│  │ RSS Agents  ││  │  │Orchestrator ││  │  │Report Agents││
│  └─────────────┘│  │  └─────────────┘│  │  └─────────────┘│
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────────────┐
                    │ Shared Storage  │
                    │   & Database    │
                    └─────────────────┘
```

## System Requirements

### Minimum Requirements

**Development Environment**
- **CPU**: 2 cores, 2.0 GHz
- **Memory**: 4 GB RAM
- **Storage**: 10 GB available space
- **Python**: 3.8 or higher
- **Network**: Internet access for API calls

**Production Environment**
- **CPU**: 4 cores, 2.5 GHz
- **Memory**: 8 GB RAM
- **Storage**: 50 GB available space (with growth capacity)
- **Network**: Stable internet connection, 100 Mbps+
- **OS**: Ubuntu 20.04+, RHEL 8+, or equivalent

### Recommended Requirements

**High-Volume Production**
- **CPU**: 8+ cores, 3.0 GHz
- **Memory**: 16 GB+ RAM
- **Storage**: 200 GB+ SSD with backup
- **Network**: Redundant connections, 1 Gbps+
- **Load Balancer**: For high availability

### Supported Operating Systems

- **Linux**: Ubuntu 20.04+, RHEL 8+, CentOS 8+, Debian 11+
- **macOS**: 11.0+ (development only)
- **Windows**: 10+ with WSL2 (development only)

## Local Development Deployment

### Quick Start

```bash
# Clone repository
git clone https://github.com/your-org/nomad-threat-intel-framework.git
cd nomad-threat-intel-framework

# Create virtual environment
python3 -m venv nomad-env
source nomad-env/bin/activate  # Linux/macOS
# nomad-env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run setup script
python scripts/setup_dev_environment.py

# Test installation
python -c "from config.environment import config; config.validate_api_access()"

# Run first workflow
python nomad_workflow_enhanced.py execute morning_check
```

### Development Environment Script

**scripts/setup_dev_environment.py**
```python
#!/usr/bin/env python3
"""
Development environment setup script
"""
import os
import sys
from pathlib import Path

def setup_development_environment():
    """Set up local development environment"""

    print("🚀 Setting up NOMAD development environment...")

    # Create required directories
    directories = [
        'data/input',
        'data/output',
        'data/cache',
        'logs',
        'config/local',
        'tests/fixtures'
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

    # Set up environment file if it doesn't exist
    env_file = Path('.env')
    env_example = Path('.env.example')

    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env from .env.example")
        print("⚠️  Please edit .env with your API keys")

    # Set development-specific configurations
    dev_config = {
        'NOMAD_ENV': 'development',
        'LOG_LEVEL': 'DEBUG',
        'CACHE_ENABLED': 'true',
        'RATE_LIMITING_ENABLED': 'false'
    }

    # Write development overrides
    with open('.env.dev', 'w') as f:
        for key, value in dev_config.items():
            f.write(f"{key}={value}\n")

    print("✅ Created development configuration")

    # Install pre-commit hooks if available
    if Path('.pre-commit-config.yaml').exists():
        os.system('pre-commit install')
        print("✅ Installed pre-commit hooks")

    print("\n🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Edit .env with your API keys")
    print("2. Run: python -c \"from config.environment import config; config.validate_api_access()\"")
    print("3. Run: python nomad_workflow_enhanced.py list")

if __name__ == "__main__":
    setup_development_environment()
```

### IDE Configuration

**VS Code Settings (.vscode/settings.json)**
```json
{
    "python.defaultInterpreterPath": "./nomad-env/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".coverage": true,
        "htmlcov/": true,
        "nomad-env/": true
    }
}
```

## Docker Deployment

### Single Container Deployment

**Dockerfile**
```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libxml2 \
    libxslt1.1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN groupadd -r nomad && useradd -r -g nomad nomad

# Set up application directory
WORKDIR /app
COPY . .

# Set ownership
RUN chown -R nomad:nomad /app

# Create required directories
RUN mkdir -p data/input data/output data/cache logs \
    && chown -R nomad:nomad data logs

# Switch to non-root user
USER nomad

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV NOMAD_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "from config.environment import config; config.validate_api_access()" || exit 1

# Default command
CMD ["python", "nomad_workflow_enhanced.py", "execute", "morning_check"]
```

### Docker Compose Deployment

**docker-compose.yml**
```yaml
version: '3.8'

services:
  nomad-core:
    build: .
    container_name: nomad-core
    restart: unless-stopped

    environment:
      - NOMAD_ENV=production
      - PYTHONUNBUFFERED=1

    env_file:
      - .env.prod

    volumes:
      # Data persistence
      - nomad-data:/app/data
      - nomad-logs:/app/logs
      - nomad-config:/app/config/local:ro

    # Resource limits
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M

    # Health check
    healthcheck:
      test: ["CMD", "python", "-c", "from config.environment import config; config.validate_api_access()"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

    # Logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

    networks:
      - nomad-network

  nomad-scheduler:
    build: .
    container_name: nomad-scheduler
    restart: unless-stopped

    command: ["python", "scripts/scheduler.py"]

    environment:
      - NOMAD_ENV=production
      - COMPONENT=scheduler

    env_file:
      - .env.prod

    volumes:
      - nomad-data:/app/data
      - nomad-logs:/app/logs
      - nomad-config:/app/config/local:ro

    depends_on:
      nomad-core:
        condition: service_healthy

    networks:
      - nomad-network

  nomad-web:
    build: .
    container_name: nomad-web
    restart: unless-stopped

    command: ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

    ports:
      - "5000:5000"

    environment:
      - NOMAD_ENV=production
      - FLASK_ENV=production

    env_file:
      - .env.prod

    volumes:
      - nomad-data:/app/data:ro
      - nomad-logs:/app/logs:ro

    depends_on:
      nomad-core:
        condition: service_healthy

    networks:
      - nomad-network

  # Optional: Redis for caching and job queuing
  redis:
    image: redis:7-alpine
    container_name: nomad-redis
    restart: unless-stopped

    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

    volumes:
      - redis-data:/data

    networks:
      - nomad-network

  # Optional: Monitoring with Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: nomad-prometheus
    restart: unless-stopped

    ports:
      - "9090:9090"

    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus

    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'

    networks:
      - nomad-network

volumes:
  nomad-data:
  nomad-logs:
  nomad-config:
  redis-data:
  prometheus-data:

networks:
  nomad-network:
    driver: bridge
```

### Docker Deployment Commands

```bash
# Development deployment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale specific services
docker-compose up -d --scale nomad-core=3

# View logs
docker-compose logs -f nomad-core

# Execute commands in container
docker-compose exec nomad-core python nomad_workflow_enhanced.py list

# Health check
docker-compose exec nomad-core python scripts/health_check.py

# Backup data
docker run --rm -v nomad_nomad-data:/data -v $(pwd):/backup \
    busybox tar czf /backup/nomad-backup-$(date +%Y%m%d).tar.gz /data

# Update deployment
docker-compose pull
docker-compose up -d --remove-orphans
```

## Cloud Deployment

### AWS Deployment

#### EC2 Instance Deployment

**CloudFormation Template (infrastructure.yml)**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'NOMAD Threat Intelligence Framework Infrastructure'

Parameters:
  InstanceType:
    Type: String
    Default: t3.medium
    AllowedValues: [t3.small, t3.medium, t3.large, t3.xlarge]

  KeyPairName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: EC2 Key Pair for SSH access

Resources:
  # VPC and Networking
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: NOMAD-VPC

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: NOMAD-PublicSubnet

  PrivateSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      Tags:
        - Key: Name
          Value: NOMAD-PrivateSubnet

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: NOMAD-IGW

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  # Security Groups
  NomadSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for NOMAD application
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0  # Restrict to your IP range
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 5000
          ToPort: 5000
          CidrIp: 10.0.0.0/16  # Internal access only

  # EC2 Instance
  NomadInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c02fb55956c7d316  # Amazon Linux 2 (update as needed)
      InstanceType: !Ref InstanceType
      KeyName: !Ref KeyPairName
      SecurityGroupIds:
        - !Ref NomadSecurityGroup
      SubnetId: !Ref PublicSubnet
      IamInstanceProfile: !Ref NomadInstanceProfile

      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          yum update -y

          # Install Docker
          amazon-linux-extras install docker
          systemctl start docker
          systemctl enable docker
          usermod -a -G docker ec2-user

          # Install Docker Compose
          curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
          chmod +x /usr/local/bin/docker-compose

          # Clone NOMAD repository
          cd /opt
          git clone https://github.com/your-org/nomad-threat-intel-framework.git
          cd nomad-threat-intel-framework

          # Set up environment
          cp .env.example .env.prod

          # Start services
          docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

      Tags:
        - Key: Name
          Value: NOMAD-Instance

  # IAM Role and Instance Profile
  NomadRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy
      Policies:
        - PolicyName: NomadS3Access
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                  - s3:DeleteObject
                Resource: !Sub "${NomadS3Bucket}/*"

  NomadInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref NomadRole

  # S3 Bucket for data storage
  NomadS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "nomad-data-${AWS::StackName}-${AWS::AccountId}"
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

Outputs:
  InstanceIP:
    Description: Public IP address of NOMAD instance
    Value: !GetAtt NomadInstance.PublicIp
    Export:
      Name: !Sub "${AWS::StackName}-InstanceIP"

  S3BucketName:
    Description: S3 bucket for NOMAD data
    Value: !Ref NomadS3Bucket
    Export:
      Name: !Sub "${AWS::StackName}-S3Bucket"
```

#### ECS Deployment

**ECS Task Definition (nomad-task.json)**
```json
{
  "family": "nomad-threat-intel",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/nomadTaskRole",
  "containerDefinitions": [
    {
      "name": "nomad-core",
      "image": "your-account.dkr.ecr.us-east-1.amazonaws.com/nomad:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NOMAD_ENV",
          "value": "production"
        },
        {
          "name": "AWS_DEFAULT_REGION",
          "value": "us-east-1"
        }
      ],
      "secrets": [
        {
          "name": "ANTHROPIC_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:nomad/anthropic-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/nomad-threat-intel",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "python -c \"from config.environment import config; config.validate_api_access()\" || exit 1"
        ],
        "interval": 30,
        "timeout": 10,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

### Kubernetes Deployment

**Kubernetes Manifests (k8s/)**

**namespace.yaml**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nomad-system
  labels:
    name: nomad-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nomad-service-account
  namespace: nomad-system
```

**configmap.yaml**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nomad-config
  namespace: nomad-system
data:
  NOMAD_ENV: "production"
  LOG_LEVEL: "INFO"
  CACHE_ENABLED: "true"
  RATE_LIMITING_ENABLED: "true"
  PYTHONUNBUFFERED: "1"
```

**secret.yaml**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nomad-secrets
  namespace: nomad-system
type: Opaque
data:
  # Base64 encoded values
  anthropic-api-key: <base64-encoded-key>
  virustotal-api-key: <base64-encoded-key>
```

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nomad-core
  namespace: nomad-system
  labels:
    app: nomad-core
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nomad-core
  template:
    metadata:
      labels:
        app: nomad-core
    spec:
      serviceAccountName: nomad-service-account
      containers:
      - name: nomad-core
        image: your-registry/nomad:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
          name: http
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: nomad-secrets
              key: anthropic-api-key
        envFrom:
        - configMapRef:
            name: nomad-config
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        volumeMounts:
        - name: nomad-data
          mountPath: /app/data
        - name: nomad-logs
          mountPath: /app/logs
      volumes:
      - name: nomad-data
        persistentVolumeClaim:
          claimName: nomad-data-pvc
      - name: nomad-logs
        persistentVolumeClaim:
          claimName: nomad-logs-pvc
      restartPolicy: Always
```

**service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nomad-core-service
  namespace: nomad-system
  labels:
    app: nomad-core
spec:
  selector:
    app: nomad-core
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
    name: http
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nomad-ingress
  namespace: nomad-system
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - nomad.your-domain.com
    secretName: nomad-tls
  rules:
  - host: nomad.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nomad-core-service
            port:
              number: 80
```

**pvc.yaml**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nomad-data-pvc
  namespace: nomad-system
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
  storageClassName: gp2
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nomad-logs-pvc
  namespace: nomad-system
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
  storageClassName: gp2
```

**Helm Chart Values (helm/values.yaml)**
```yaml
# Default values for NOMAD
replicaCount: 3

image:
  repository: your-registry/nomad
  pullPolicy: Always
  tag: "latest"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: nomad.your-domain.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: nomad-tls
      hosts:
        - nomad.your-domain.com

resources:
  limits:
    cpu: 500m
    memory: 1Gi
  requests:
    cpu: 250m
    memory: 512Mi

persistence:
  enabled: true
  size: 50Gi
  storageClass: gp2

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

# Environment variables
config:
  nomadEnv: production
  logLevel: INFO
  cacheEnabled: true
  rateLimitingEnabled: true

# Secrets (use external secret operator in production)
secrets:
  anthropicApiKey: ""
  virusTotalApiKey: ""
```

## Production Deployment

### Pre-Deployment Checklist

**Infrastructure Checklist**
- [ ] Server specifications meet requirements
- [ ] Network connectivity and firewall rules configured
- [ ] SSL certificates obtained and configured
- [ ] DNS records configured
- [ ] Load balancer configured (if applicable)
- [ ] Monitoring and alerting set up
- [ ] Backup strategy implemented
- [ ] Security hardening completed

**Application Checklist**
- [ ] Environment variables configured
- [ ] API keys and secrets configured
- [ ] Database initialized (if applicable)
- [ ] Log rotation configured
- [ ] Health checks working
- [ ] Performance testing completed
- [ ] Security testing completed
- [ ] Documentation updated

**Operational Checklist**
- [ ] Deployment procedures documented
- [ ] Rollback procedures tested
- [ ] Monitoring dashboards configured
- [ ] Alert recipients configured
- [ ] Maintenance windows scheduled
- [ ] Team training completed

### Production Environment Configuration

**.env.prod**
```bash
# Environment
NOMAD_ENV=production

# API Keys (use secret management)
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}

# Organization Configuration
ORG_NAME=Your Organization
CROWN_JEWELS=Exchange Server,Active Directory,Database Cluster
BUSINESS_SECTORS=Financial Services,Healthcare

# Performance Configuration
CACHE_ENABLED=true
CACHE_TTL_HOURS=24
RATE_LIMITING_ENABLED=true
MAX_CONCURRENT_AGENTS=5
BATCH_SIZE=50

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_RETENTION_DAYS=90
AUDIT_LOG_ENABLED=true

# Security
ENCRYPTION_ENABLED=true
TLS_VERIFY=true
API_RATE_LIMIT=100
SESSION_TIMEOUT=3600

# Data Storage
DATA_DIR=/var/lib/nomad/data
LOG_DIR=/var/log/nomad
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30

# External Integrations
SIEM_ENDPOINT=${SIEM_ENDPOINT}
WEBHOOK_ENDPOINTS=${WEBHOOK_ENDPOINTS}
SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
```

### Production Deployment Script

**scripts/deploy_production.sh**
```bash
#!/bin/bash
set -euo pipefail

# Production deployment script for NOMAD
echo "🚀 Starting NOMAD production deployment..."

# Configuration
DEPLOY_USER="nomad"
APP_DIR="/opt/nomad"
BACKUP_DIR="/var/backups/nomad"
SERVICE_NAME="nomad"

# Pre-deployment checks
echo "✅ Running pre-deployment checks..."

# Check if running as deployment user
if [[ $EUID -eq 0 ]]; then
   echo "❌ Do not run as root. Use deployment user: $DEPLOY_USER"
   exit 1
fi

# Check disk space
AVAILABLE_SPACE=$(df /opt | tail -1 | awk '{print $4}')
REQUIRED_SPACE=1048576  # 1GB in KB

if [ "$AVAILABLE_SPACE" -lt "$REQUIRED_SPACE" ]; then
    echo "❌ Insufficient disk space. Required: 1GB, Available: $((AVAILABLE_SPACE/1024))MB"
    exit 1
fi

# Check connectivity
echo "🌐 Testing external API connectivity..."
python3 -c "from config.environment import EnvironmentConfig; EnvironmentConfig().validate_api_access()" || {
    echo "❌ API connectivity check failed"
    exit 1
}

# Create backup
echo "💾 Creating backup..."
BACKUP_FILE="$BACKUP_DIR/nomad-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
mkdir -p "$BACKUP_DIR"

if [ -d "$APP_DIR" ]; then
    tar -czf "$BACKUP_FILE" -C "$APP_DIR" . || {
        echo "❌ Backup creation failed"
        exit 1
    }
    echo "✅ Backup created: $BACKUP_FILE"
fi

# Stop services
echo "🛑 Stopping NOMAD services..."
sudo systemctl stop "$SERVICE_NAME" || true

# Deploy application
echo "📦 Deploying application..."

# Create application directory
sudo mkdir -p "$APP_DIR"
sudo chown "$DEPLOY_USER:$DEPLOY_USER" "$APP_DIR"

# Extract or copy application files
if [ -f "nomad-release.tar.gz" ]; then
    tar -xzf nomad-release.tar.gz -C "$APP_DIR"
else
    cp -r . "$APP_DIR/"
fi

# Set permissions
sudo chown -R "$DEPLOY_USER:$DEPLOY_USER" "$APP_DIR"
find "$APP_DIR" -type f -name "*.py" -exec chmod 644 {} \;
find "$APP_DIR" -type f -name "*.sh" -exec chmod 755 {} \;

# Install/update dependencies
echo "📚 Installing dependencies..."
cd "$APP_DIR"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if applicable)
echo "🗃️ Running database setup..."
python scripts/setup_production_db.py

# Update configuration
echo "⚙️ Updating configuration..."

# Validate configuration
python -c "from config.environment import EnvironmentConfig; EnvironmentConfig().validate()" || {
    echo "❌ Configuration validation failed"
    exit 1
}

# Start services
echo "🎬 Starting NOMAD services..."
sudo systemctl daemon-reload
sudo systemctl start "$SERVICE_NAME"
sudo systemctl enable "$SERVICE_NAME"

# Wait for service to start
sleep 10

# Health check
echo "🏥 Running health checks..."
python scripts/health_check.py || {
    echo "❌ Health check failed, rolling back..."

    # Rollback procedure
    sudo systemctl stop "$SERVICE_NAME"

    if [ -f "$BACKUP_FILE" ]; then
        echo "🔄 Rolling back to previous version..."
        rm -rf "$APP_DIR"/*
        tar -xzf "$BACKUP_FILE" -C "$APP_DIR"
        sudo systemctl start "$SERVICE_NAME"
    fi

    exit 1
}

# Run test workflow
echo "🧪 Running test workflow..."
python nomad_workflow_enhanced.py execute morning_check --dry-run || {
    echo "⚠️  Test workflow failed, but deployment continues"
}

echo "🎉 NOMAD production deployment completed successfully!"
echo "📊 Access dashboard at: https://your-domain.com/nomad"
echo "📋 Check logs: sudo journalctl -u $SERVICE_NAME -f"
```

### Systemd Service Configuration

**/etc/systemd/system/nomad.service**
```ini
[Unit]
Description=NOMAD Threat Intelligence Framework
After=network.target
Wants=network.target

[Service]
Type=notify
User=nomad
Group=nomad
WorkingDirectory=/opt/nomad
Environment=PYTHONPATH=/opt/nomad
ExecStart=/opt/nomad/venv/bin/python nomad_workflow_enhanced.py daemon
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=nomad

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/nomad/data /opt/nomad/logs /var/log/nomad

# Resource limits
LimitNOFILE=65536
MemoryLimit=2G

[Install]
WantedBy=multi-user.target
```

## Environment Configuration

### Configuration Management

**config/production.yml**
```yaml
nomad:
  environment: production

  # Performance settings
  performance:
    max_concurrent_agents: 5
    batch_size: 100
    cache_ttl_hours: 24
    request_timeout_seconds: 30

  # Security settings
  security:
    encryption_enabled: true
    tls_verify: true
    rate_limiting_enabled: true
    session_timeout_seconds: 3600

  # Logging settings
  logging:
    level: INFO
    format: json
    file_rotation: daily
    retention_days: 90
    audit_enabled: true

  # External integrations
  integrations:
    siem:
      enabled: true
      endpoint: "${SIEM_ENDPOINT}"
      timeout: 30
      retry_attempts: 3

    slack:
      enabled: true
      webhook_url: "${SLACK_WEBHOOK_URL}"
      channel: "#security-alerts"

    webhooks:
      enabled: true
      endpoints: "${WEBHOOK_ENDPOINTS}"

  # Data management
  data:
    backup_enabled: true
    backup_schedule: "0 2 * * *"  # Daily at 2 AM
    retention_days: 365
    compression_enabled: true

  # Monitoring
  monitoring:
    metrics_enabled: true
    health_check_interval: 30
    prometheus_port: 9090
```

### Secret Management Integration

**config/secrets.py**
```python
import os
import boto3
import hvac
from typing import Dict, Optional

class SecretManager:
    """Manage secrets across different backends"""

    def __init__(self, backend: str = None):
        self.backend = backend or os.getenv('SECRET_BACKEND', 'env')
        self._init_backend()

    def _init_backend(self):
        """Initialize secret management backend"""
        if self.backend == 'aws':
            self.client = boto3.client('secretsmanager')
        elif self.backend == 'vault':
            vault_url = os.getenv('VAULT_URL')
            vault_token = os.getenv('VAULT_TOKEN')
            self.client = hvac.Client(url=vault_url, token=vault_token)
        elif self.backend == 'k8s':
            # Kubernetes secrets are mounted as files
            self.secrets_path = '/var/secrets/nomad'
        else:
            # Environment variables (default)
            self.client = None

    def get_secret(self, secret_name: str) -> Optional[str]:
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

            elif self.backend == 'k8s':
                secret_file = f"{self.secrets_path}/{secret_name}"
                if os.path.exists(secret_file):
                    with open(secret_file, 'r') as f:
                        return f.read().strip()

            else:
                # Environment variables
                return os.getenv(secret_name)

        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None

    def get_all_secrets(self) -> Dict[str, str]:
        """Get all required secrets"""
        secret_names = [
            'ANTHROPIC_API_KEY',
            'VIRUSTOTAL_API_KEY',
            'SHODAN_API_KEY',
            'SIEM_ENDPOINT',
            'SLACK_WEBHOOK_URL'
        ]

        secrets = {}
        for name in secret_names:
            value = self.get_secret(name)
            if value:
                secrets[name] = value

        return secrets
```

## Monitoring and Logging

### Monitoring Setup

**monitoring/prometheus.yml**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "nomad_rules.yml"

scrape_configs:
  - job_name: 'nomad'
    static_configs:
      - targets: ['nomad-core:5000']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

**monitoring/nomad_rules.yml**
```yaml
groups:
  - name: nomad_alerts
    rules:
      # High CPU usage
      - alert: NomadHighCPU
        expr: rate(process_cpu_seconds_total[5m]) * 100 > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "NOMAD high CPU usage"
          description: "NOMAD CPU usage is above 80% for more than 2 minutes"

      # High memory usage
      - alert: NomadHighMemory
        expr: process_resident_memory_bytes / 1024 / 1024 > 1000
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "NOMAD high memory usage"
          description: "NOMAD memory usage is above 1GB"

      # Agent failures
      - alert: NomadAgentFailures
        expr: increase(nomad_agent_errors_total[5m]) > 5
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "NOMAD agent failures detected"
          description: "More than 5 agent failures in the last 5 minutes"

      # API rate limit exceeded
      - alert: NomadRateLimitExceeded
        expr: increase(nomad_api_rate_limit_exceeded_total[1m]) > 0
        for: 0m
        labels:
          severity: warning
        annotations:
          summary: "NOMAD API rate limit exceeded"
          description: "NOMAD has exceeded API rate limits"
```

### Logging Configuration

**logging.conf**
```ini
[loggers]
keys=root,nomad,agents,config,utils

[handlers]
keys=consoleHandler,fileHandler,auditHandler,errorHandler

[formatters]
keys=standardFormatter,jsonFormatter,auditFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_nomad]
level=INFO
handlers=consoleHandler,fileHandler
qualname=nomad
propagate=0

[logger_agents]
level=INFO
handlers=consoleHandler,fileHandler
qualname=agents
propagate=0

[logger_config]
level=INFO
handlers=fileHandler
qualname=config
propagate=0

[logger_utils]
level=INFO
handlers=fileHandler
qualname=utils
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=standardFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=handlers.RotatingFileHandler
level=INFO
formatter=jsonFormatter
args=('/var/log/nomad/nomad.log', 'a', 10485760, 5)

[handler_auditHandler]
class=handlers.TimedRotatingFileHandler
level=INFO
formatter=auditFormatter
args=('/var/log/nomad/audit.log', 'midnight', 1, 90)

[handler_errorHandler]
class=handlers.RotatingFileHandler
level=ERROR
formatter=jsonFormatter
args=('/var/log/nomad/error.log', 'a', 10485760, 5)

[formatter_standardFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

[formatter_jsonFormatter]
format={"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}

[formatter_auditFormatter]
format={"timestamp": "%(asctime)s", "event_type": "audit", "level": "%(levelname)s", "message": "%(message)s"}
```

## Backup and Recovery

### Backup Strategy

**scripts/backup.sh**
```bash
#!/bin/bash
set -euo pipefail

# NOMAD backup script
BACKUP_DIR="/var/backups/nomad"
DATA_DIR="/opt/nomad/data"
LOG_DIR="/var/log/nomad"
CONFIG_DIR="/opt/nomad/config"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate backup filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/nomad_backup_$TIMESTAMP.tar.gz"

echo "🗃️ Starting NOMAD backup..."

# Create compressed backup
tar -czf "$BACKUP_FILE" \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    --exclude="venv" \
    --exclude="*.log.gz" \
    -C /opt nomad/data \
    -C /opt nomad/config \
    -C /var/log nomad

# Verify backup
if [ -f "$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✅ Backup created: $BACKUP_FILE ($BACKUP_SIZE)"
else
    echo "❌ Backup creation failed"
    exit 1
fi

# Upload to cloud storage (optional)
if [ -n "${AWS_S3_BACKUP_BUCKET:-}" ]; then
    echo "☁️ Uploading backup to S3..."
    aws s3 cp "$BACKUP_FILE" "s3://$AWS_S3_BACKUP_BUCKET/nomad-backups/"
fi

# Clean up old backups
echo "🧹 Cleaning up old backups..."
find "$BACKUP_DIR" -name "nomad_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "✅ Backup completed successfully"
```

### Recovery Procedures

**scripts/restore.sh**
```bash
#!/bin/bash
set -euo pipefail

# NOMAD restore script
BACKUP_FILE="$1"
NOMAD_DIR="/opt/nomad"
SERVICE_NAME="nomad"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file>"
    echo "Available backups:"
    ls -la /var/backups/nomad/nomad_backup_*.tar.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "🔄 Starting NOMAD restore from: $BACKUP_FILE"
echo "⚠️  This will stop NOMAD and restore data from backup"
read -p "Continue? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled"
    exit 1
fi

# Stop NOMAD service
echo "🛑 Stopping NOMAD service..."
sudo systemctl stop "$SERVICE_NAME"

# Create backup of current state
CURRENT_BACKUP="/tmp/nomad_pre_restore_$(date +%Y%m%d_%H%M%S).tar.gz"
echo "💾 Creating backup of current state: $CURRENT_BACKUP"
tar -czf "$CURRENT_BACKUP" -C /opt nomad/data -C /var/log nomad

# Restore from backup
echo "📦 Restoring from backup..."
cd /

# Extract backup
tar -xzf "$BACKUP_FILE"

# Set permissions
sudo chown -R nomad:nomad "$NOMAD_DIR/data"
sudo chown -R nomad:nomad "/var/log/nomad"

# Start service
echo "🎬 Starting NOMAD service..."
sudo systemctl start "$SERVICE_NAME"

# Wait for service to start
sleep 10

# Health check
echo "🏥 Running health check..."
if python "$NOMAD_DIR/scripts/health_check.py"; then
    echo "✅ Restore completed successfully"
    echo "🗑️ Current state backup saved to: $CURRENT_BACKUP"
else
    echo "❌ Health check failed after restore"
    echo "🔄 Consider rolling back using: $CURRENT_BACKUP"
    exit 1
fi
```

## Scaling Strategies

### Horizontal Scaling

**Docker Swarm Configuration**
```yaml
# docker-compose.swarm.yml
version: '3.8'

services:
  nomad-core:
    image: your-registry/nomad:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      placement:
        constraints:
          - node.role == worker
      resources:
        limits:
          cpus: '0.5'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 512M
    networks:
      - nomad-overlay

  nomad-scheduler:
    image: your-registry/nomad:latest
    command: ["python", "scripts/scheduler.py"]
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager
    networks:
      - nomad-overlay

  nomad-worker:
    image: your-registry/nomad:latest
    command: ["python", "scripts/worker.py"]
    deploy:
      replicas: 5
      placement:
        constraints:
          - node.role == worker
    networks:
      - nomad-overlay

networks:
  nomad-overlay:
    driver: overlay
    attachable: true
```

### Auto-scaling Configuration

**Kubernetes HPA**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nomad-hpa
  namespace: nomad-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nomad-core
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

## Security Hardening

### System Hardening Script

**scripts/harden_system.sh**
```bash
#!/bin/bash
set -euo pipefail

echo "🔒 Starting system hardening for NOMAD deployment..."

# Update system
apt update && apt upgrade -y

# Install security tools
apt install -y fail2ban ufw aide rkhunter

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 443/tcp
ufw allow 5000/tcp  # NOMAD API (restrict as needed)
ufw --force enable

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

[nomad-api]
enabled = true
port = 5000
logpath = /var/log/nomad/access.log
maxretry = 5
EOF

systemctl enable fail2ban
systemctl restart fail2ban

# Harden SSH
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd

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

# Configure log rotation
cat > /etc/logrotate.d/nomad << EOF
/var/log/nomad/*.log {
    daily
    missingok
    rotate 90
    compress
    delaycompress
    notifempty
    create 0640 nomad nomad
    postrotate
        systemctl reload nomad
    endscript
}
EOF

# Set file permissions
chmod 600 /opt/nomad/.env*
chmod -R 640 /opt/nomad/config/
chown -R nomad:nomad /opt/nomad/

echo "✅ System hardening completed"
```

## CI/CD Pipeline

### GitHub Actions Production Deployment

**.github/workflows/deploy-production.yml**
```yaml
name: Production Deployment

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy'
        required: true
        default: 'latest'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to Container Registry
      uses: docker/login-action@v2
      with:
        registry: your-registry.com
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          your-registry.com/nomad:latest
          your-registry.com/nomad:${{ github.ref_name }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Deploy to production
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.PROD_HOST }}
        username: ${{ secrets.PROD_USER }}
        key: ${{ secrets.PROD_SSH_KEY }}
        script: |
          cd /opt/nomad
          ./scripts/deploy_production.sh

    - name: Run health check
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.PROD_HOST }}
        username: ${{ secrets.PROD_USER }}
        key: ${{ secrets.PROD_SSH_KEY }}
        script: |
          cd /opt/nomad
          python scripts/health_check.py

    - name: Notify team
      if: always()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#deployments'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Troubleshooting

### Common Deployment Issues

**Issue: Service fails to start**
```bash
# Check service status
sudo systemctl status nomad

# Check logs
sudo journalctl -u nomad -f

# Check configuration
python -c "from config.environment import EnvironmentConfig; EnvironmentConfig().validate()"

# Check permissions
ls -la /opt/nomad/
ls -la /var/log/nomad/
```

**Issue: API connectivity problems**
```bash
# Test API access
python -c "from config.environment import config; print(config.validate_api_access())"

# Check network connectivity
curl -v https://api.anthropic.com/v1/health

# Check firewall
sudo ufw status
sudo iptables -L
```

**Issue: High memory usage**
```bash
# Monitor memory usage
top -p $(pgrep -f nomad)
ps aux | grep nomad

# Check for memory leaks
python scripts/memory_profiler.py

# Restart service if needed
sudo systemctl restart nomad
```

**Issue: Database connection problems**
```bash
# Test database connectivity
python -c "from config.database import get_connection; get_connection().test()"

# Check database status
sudo systemctl status postgresql

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### Health Check Script

**scripts/health_check.py**
```python
#!/usr/bin/env python3
"""
Production health check script
"""
import sys
import requests
import time
from datetime import datetime
from config.environment import EnvironmentConfig

def check_api_connectivity():
    """Check external API connectivity"""
    try:
        config = EnvironmentConfig()
        results = config.validate_api_access()

        if not results.get('anthropic', False):
            return False, "Anthropic API not accessible"

        return True, "API connectivity OK"
    except Exception as e:
        return False, f"API check failed: {e}"

def check_local_services():
    """Check local service health"""
    try:
        # Test local API endpoint
        response = requests.get('http://localhost:5000/health', timeout=10)
        if response.status_code == 200:
            return True, "Local services OK"
        else:
            return False, f"Local service returned {response.status_code}"
    except Exception as e:
        return False, f"Local service check failed: {e}"

def check_disk_space():
    """Check available disk space"""
    import shutil

    try:
        # Check data directory space
        total, used, free = shutil.disk_usage('/opt/nomad/data')
        free_gb = free // (1024**3)

        if free_gb < 1:  # Less than 1GB free
            return False, f"Low disk space: {free_gb}GB free"

        return True, f"Disk space OK: {free_gb}GB free"
    except Exception as e:
        return False, f"Disk space check failed: {e}"

def check_log_files():
    """Check log file accessibility"""
    import os

    try:
        log_files = [
            '/var/log/nomad/nomad.log',
            '/var/log/nomad/error.log'
        ]

        for log_file in log_files:
            if not os.path.exists(log_file):
                return False, f"Log file missing: {log_file}"
            if not os.access(log_file, os.W_OK):
                return False, f"Log file not writable: {log_file}"

        return True, "Log files OK"
    except Exception as e:
        return False, f"Log file check failed: {e}"

def main():
    """Run all health checks"""
    print(f"🏥 NOMAD Health Check - {datetime.now()}")
    print("=" * 50)

    checks = [
        ("API Connectivity", check_api_connectivity),
        ("Local Services", check_local_services),
        ("Disk Space", check_disk_space),
        ("Log Files", check_log_files)
    ]

    all_passed = True

    for check_name, check_func in checks:
        try:
            passed, message = check_func()
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{check_name}: {status} - {message}")

            if not passed:
                all_passed = False
        except Exception as e:
            print(f"{check_name}: ❌ ERROR - {e}")
            all_passed = False

    print("=" * 50)

    if all_passed:
        print("🎉 All health checks passed!")
        sys.exit(0)
    else:
        print("💥 One or more health checks failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Maintenance and Updates

### Update Procedure

**scripts/update_nomad.sh**
```bash
#!/bin/bash
set -euo pipefail

# NOMAD update script
NEW_VERSION="$1"
CURRENT_VERSION=$(git describe --tags --abbrev=0)

if [ $# -eq 0 ]; then
    echo "Usage: $0 <version>"
    echo "Current version: $CURRENT_VERSION"
    exit 1
fi

echo "🔄 Updating NOMAD from $CURRENT_VERSION to $NEW_VERSION"

# Pre-update backup
echo "💾 Creating pre-update backup..."
./scripts/backup.sh

# Download and verify new version
echo "📦 Downloading new version..."
wget "https://github.com/your-org/nomad/releases/download/$NEW_VERSION/nomad-$NEW_VERSION.tar.gz"
wget "https://github.com/your-org/nomad/releases/download/$NEW_VERSION/nomad-$NEW_VERSION.tar.gz.sha256"

# Verify checksum
sha256sum -c "nomad-$NEW_VERSION.tar.gz.sha256"

# Stop service
echo "🛑 Stopping NOMAD..."
sudo systemctl stop nomad

# Update application
echo "📥 Installing new version..."
cd /opt
sudo tar -xzf "/tmp/nomad-$NEW_VERSION.tar.gz"
sudo chown -R nomad:nomad nomad/

# Update dependencies
cd /opt/nomad
source venv/bin/activate
pip install -r requirements.txt

# Run migrations (if any)
python scripts/migrate.py

# Update configuration (if needed)
python scripts/update_config.py

# Start service
echo "🎬 Starting NOMAD..."
sudo systemctl start nomad

# Wait and health check
sleep 15
python scripts/health_check.py

echo "✅ Update completed successfully!"
echo "📊 New version: $(git describe --tags --abbrev=0)"
```

### Maintenance Tasks

**Scheduled Maintenance Script**
```bash
#!/bin/bash
# /etc/cron.weekly/nomad-maintenance

set -euo pipefail

echo "🔧 Running weekly NOMAD maintenance..."

# Rotate logs
logrotate -f /etc/logrotate.d/nomad

# Clean up old cache files
find /opt/nomad/data/cache -name "*.cache" -mtime +7 -delete

# Backup data
/opt/nomad/scripts/backup.sh

# Update threat intelligence feeds
python /opt/nomad/scripts/update_feeds.py

# Check for security updates
apt list --upgradable | grep -i security || true

# Generate maintenance report
python /opt/nomad/scripts/maintenance_report.py

echo "✅ Weekly maintenance completed"
```

---

This comprehensive deployment guide provides detailed procedures for deploying NOMAD in various environments, from development to production. Follow the appropriate sections based on your deployment requirements and infrastructure setup.