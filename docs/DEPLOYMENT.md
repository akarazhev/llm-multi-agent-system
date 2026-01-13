# Deployment Guide

Production deployment guide for the LLM Multi-Agent System.

## Table of Contents

1. [Overview](#overview)
2. [Deployment Architectures](#deployment-architectures)
3. [Prerequisites](#prerequisites)
4. [Local Production Setup](#local-production-setup)
5. [Server Deployment](#server-deployment)
6. [Containerization](#containerization)
7. [Process Management](#process-management)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Backup & Recovery](#backup--recovery)
10. [Security Hardening](#security-hardening)
11. [Performance Tuning](#performance-tuning)

## Overview

The LLM Multi-Agent System can be deployed in various configurations depending on your requirements:

- **Single Workstation**: Development and small-scale use
- **Dedicated Server**: Production workloads
- **Containerized**: Docker-based deployment
- **High Availability**: Distributed setup (future)

## Deployment Architectures

### Architecture 1: Single Workstation

```
┌────────────────────────────────────────┐
│         Local Workstation              │
│  ┌──────────────────────────────────┐ │
│  │  Multi-Agent System              │ │
│  │  - Python application            │ │
│  │  - Config & logs                 │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  llama-server                    │ │
│  │  - Local LLM inference           │ │
│  │  - Port 8080                     │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  File System                     │ │
│  │  - Generated outputs             │ │
│  │  - Logs                          │ │
│  └──────────────────────────────────┘ │
└────────────────────────────────────────┘
```

**Use Case**: Development, personal use, small projects

### Architecture 2: Dedicated Server

```
┌────────────────────────────────────────┐
│        Production Server               │
│  ┌──────────────────────────────────┐ │
│  │  systemd Services                │ │
│  │  - agent-system.service          │ │
│  │  - llama-server.service          │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  Application                     │ │
│  │  - Virtual environment           │ │
│  │  - Configuration                 │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  Monitoring                      │ │
│  │  - System metrics                │ │
│  │  - Log aggregation               │ │
│  │  - Alerts                        │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  Backups                         │ │
│  │  - Automated backups             │ │
│  │  - Off-site storage              │ │
│  └──────────────────────────────────┘ │
└────────────────────────────────────────┘
```

**Use Case**: Production workloads, team use, continuous operation

### Architecture 3: Containerized

```
┌────────────────────────────────────────┐
│         Docker Host                    │
│  ┌──────────────────────────────────┐ │
│  │  agent-system container          │ │
│  │  - Python app                    │ │
│  │  - Volume mounts                 │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  llama-server container          │ │
│  │  - Model volume                  │ │
│  │  - GPU passthrough               │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  Docker Volumes                  │ │
│  │  - Config                        │ │
│  │  - Logs                          │ │
│  │  - Output                        │ │
│  │  - Models                        │ │
│  └──────────────────────────────────┘ │
└────────────────────────────────────────┘
```

**Use Case**: Reproducible deployments, cloud hosting, CI/CD

## Prerequisites

### Hardware Requirements

#### Minimum
- **CPU**: 8 cores
- **RAM**: 16GB
- **Storage**: 100GB SSD
- **Network**: 100 Mbps (for downloads)

#### Recommended
- **CPU**: 16+ cores or Apple Silicon M1/M2/M3
- **RAM**: 32GB+
- **GPU**: NVIDIA GPU with 16GB+ VRAM or Apple Silicon
- **Storage**: 250GB+ NVMe SSD
- **Network**: 1 Gbps

#### Production
- **CPU**: 24+ cores or high-end GPU
- **RAM**: 64GB+
- **GPU**: NVIDIA A100, H100, or Apple M2 Ultra
- **Storage**: 500GB+ NVMe SSD in RAID
- **Network**: 10 Gbps
- **Redundancy**: Dual power supplies, RAID storage

### Software Requirements

- **OS**: Ubuntu 22.04 LTS, macOS 12+, or Windows 11
- **Python**: 3.12
- **llama.cpp**: Latest version
- **Git**: For deployment
- **systemd**: For process management (Linux)

## Local Production Setup

### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y  # Ubuntu
# brew update && brew upgrade  # macOS

# Install build essentials
sudo apt install build-essential git python3.11 python3.11-venv -y

# Create dedicated user
sudo useradd -r -s /bin/bash -d /opt/agent-system agent-system
sudo mkdir -p /opt/agent-system
sudo chown agent-system:agent-system /opt/agent-system
```

### 2. Application Installation

```bash
# Switch to agent-system user
sudo su - agent-system

# Clone repository
cd /opt/agent-system
git clone https://github.com/yourusername/llm-multi-agent-system.git app
cd app

# Create virtual environment with Python 3.12
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
mkdir -p logs output models
```

### 3. Configuration

```bash
# Copy configuration templates
cp .env.example .env
cp config.yaml config.prod.yaml

# Edit production configuration
nano .env
```

Production `.env`:
```bash
# Production LLM Server
OPENAI_API_BASE=http://127.0.0.1:8080/v1
OPENAI_API_KEY=production-key-not-needed
OPENAI_API_MODEL=devstral

# Workspace
CURSOR_WORKSPACE=/opt/agent-system/app

# Configuration
AGENT_CONFIG_PATH=/opt/agent-system/app/config.prod.yaml
```

Production `config.prod.yaml`:
```yaml
cursor_workspace: "/opt/agent-system/app"
output_directory: "/opt/agent-system/app/output"

log_level: "INFO"
log_file: "/opt/agent-system/app/logs/agent_system.log"

cursor_timeout: 600
task_timeout: 1200
max_concurrent_agents: 5
task_retry_attempts: 3

enable_message_bus: true
enable_task_persistence: true

agents:
  business_analyst:
    enabled: true
  developer:
    enabled: true
  qa_engineer:
    enabled: true
  devops_engineer:
    enabled: true
  technical_writer:
    enabled: true
```

### 4. Install llama.cpp

```bash
# Install llama.cpp
cd /opt/agent-system
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build with GPU support (NVIDIA)
make LLAMA_CUDA=1

# Or for Apple Silicon
make

# Add to PATH
echo 'export PATH="/opt/agent-system/llama.cpp:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 5. Download Model

```bash
# Create models directory
mkdir -p /opt/agent-system/models

# Download model (example)
cd /opt/agent-system/models
wget https://huggingface.co/unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF/resolve/main/Devstral-Small-2-24B-Instruct-2512.Q4_K_M.gguf

# Or use llama.cpp download
llama-cli -hf unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL -m /opt/agent-system/models/
```

## Server Deployment

### systemd Service Configuration

#### 1. llama-server Service

Create `/etc/systemd/system/llama-server.service`:

```ini
[Unit]
Description=llama-server for Multi-Agent System
After=network.target

[Service]
Type=simple
User=agent-system
Group=agent-system
WorkingDirectory=/opt/agent-system/llama.cpp
Environment="PATH=/opt/agent-system/llama.cpp:/usr/local/bin:/usr/bin:/bin"
Environment="LLAMA_GPU_LAYERS=99"
Environment="LLAMA_CTX_SIZE=16384"
ExecStart=/opt/agent-system/llama.cpp/llama-server \
    -m /opt/agent-system/models/Devstral-Small-2-24B-Instruct-2512.Q4_K_M.gguf \
    -ngl 99 \
    --ctx-size 16384 \
    --host 127.0.0.1 \
    --port 8080 \
    --threads 8
Restart=always
RestartSec=10
StandardOutput=append:/opt/agent-system/logs/llama-server.log
StandardError=append:/opt/agent-system/logs/llama-server-error.log

[Install]
WantedBy=multi-user.target
```

#### 2. Agent System Service

Create `/etc/systemd/system/agent-system.service`:

```ini
[Unit]
Description=LLM Multi-Agent System
After=network.target llama-server.service
Requires=llama-server.service

[Service]
Type=simple
User=agent-system
Group=agent-system
WorkingDirectory=/opt/agent-system/app
Environment="PATH=/opt/agent-system/app/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/opt/agent-system/app/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=append:/opt/agent-system/app/logs/system.log
StandardError=append:/opt/agent-system/app/logs/system-error.log

[Install]
WantedBy=multi-user.target
```

#### 3. Enable and Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable llama-server.service
sudo systemctl enable agent-system.service

# Start services
sudo systemctl start llama-server.service
sudo systemctl start agent-system.service

# Check status
sudo systemctl status llama-server.service
sudo systemctl status agent-system.service

# View logs
sudo journalctl -u llama-server.service -f
sudo journalctl -u agent-system.service -f
```

## Containerization

### Docker Setup

#### 1. Dockerfile for llama-server

Create `docker/llama-server/Dockerfile`:

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone and build llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && \
    make

# Download model (or mount as volume)
RUN mkdir -p /models

EXPOSE 8080

CMD ["/app/llama.cpp/llama-server", \
     "-m", "/models/model.gguf", \
     "-ngl", "99", \
     "--ctx-size", "16384", \
     "--host", "0.0.0.0", \
     "--port", "8080"]
```

#### 2. Dockerfile for Agent System

Create `docker/agent-system/Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY examples/ ./examples/
COPY config.yaml .
COPY main.py .

# Create necessary directories
RUN mkdir -p logs output generated

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OPENAI_API_BASE=http://llama-server:8080/v1
ENV OPENAI_API_KEY=not-needed
ENV OPENAI_API_MODEL=devstral

CMD ["python", "main.py"]
```

#### 3. docker-compose.yml

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  llama-server:
    build:
      context: .
      dockerfile: docker/llama-server/Dockerfile
    container_name: llama-server
    volumes:
      - ./models:/models:ro
      - llama-logs:/app/logs
    ports:
      - "8080:8080"
    environment:
      - LLAMA_GPU_LAYERS=99
      - LLAMA_CTX_SIZE=16384
    restart: unless-stopped
    # For GPU support
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  agent-system:
    build:
      context: .
      dockerfile: docker/agent-system/Dockerfile
    container_name: agent-system
    depends_on:
      - llama-server
    volumes:
      - ./config.yaml:/app/config.yaml:ro
      - ./output:/app/output
      - ./logs:/app/logs
      - ./.env:/app/.env:ro
    environment:
      - OPENAI_API_BASE=http://llama-server:8080/v1
      - OPENAI_API_KEY=not-needed
      - OPENAI_API_MODEL=devstral
    restart: unless-stopped

volumes:
  llama-logs:
  agent-logs:
  agent-output:
```

#### 4. Deploy with Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Update and restart
docker-compose pull
docker-compose up -d --build
```

## Process Management

### Supervisor (Alternative to systemd)

Create `/etc/supervisor/conf.d/agent-system.conf`:

```ini
[program:llama-server]
command=/opt/agent-system/llama.cpp/llama-server -m /opt/agent-system/models/model.gguf -ngl 99 --ctx-size 16384 --host 127.0.0.1 --port 8080
directory=/opt/agent-system/llama.cpp
user=agent-system
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/agent-system/logs/llama-server.log

[program:agent-system]
command=/opt/agent-system/app/venv/bin/python main.py
directory=/opt/agent-system/app
user=agent-system
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/agent-system/app/logs/system.log
```

Commands:
```bash
# Reload configuration
sudo supervisorctl reread
sudo supervisorctl update

# Control services
sudo supervisorctl start llama-server
sudo supervisorctl start agent-system
sudo supervisorctl status
sudo supervisorctl restart all
```

## Monitoring & Maintenance

### Health Checks

Create `/opt/agent-system/scripts/health-check.sh`:

```bash
#!/bin/bash

# Check llama-server
if ! curl -sf http://127.0.0.1:8080/health > /dev/null; then
    echo "ERROR: llama-server is not responding"
    exit 1
fi

# Check agent-system process
if ! pgrep -f "python main.py" > /dev/null; then
    echo "ERROR: agent-system is not running"
    exit 1
fi

# Check disk space
DISK_USAGE=$(df /opt/agent-system | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "WARNING: Disk usage is at ${DISK_USAGE}%"
fi

echo "OK: All systems operational"
exit 0
```

Make executable:
```bash
chmod +x /opt/agent-system/scripts/health-check.sh
```

### Monitoring Script

Create `/opt/agent-system/scripts/monitor.sh`:

```bash
#!/bin/bash

LOG_FILE="/opt/agent-system/logs/monitor.log"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # CPU Usage
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d% -f1)
    
    # Memory Usage
    MEM=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
    
    # Disk Usage
    DISK=$(df /opt/agent-system | tail -1 | awk '{print $5}')
    
    # Log metrics
    echo "$TIMESTAMP - CPU: ${CPU}% | MEM: ${MEM}% | DISK: $DISK" >> "$LOG_FILE"
    
    sleep 300  # 5 minutes
done
```

### Log Rotation

Create `/etc/logrotate.d/agent-system`:

```
/opt/agent-system/app/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 agent-system agent-system
}

/opt/agent-system/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 agent-system agent-system
}
```

## Backup & Recovery

### Backup Script

Create `/opt/agent-system/scripts/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backup/agent-system"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup application
tar -czf "$BACKUP_FILE" \
    --exclude='venv' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    /opt/agent-system/app \
    /opt/agent-system/models

# Remove old backups (keep last 30 days)
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE"
```

### Automated Backups

Add to crontab:
```bash
# Daily backup at 2 AM
0 2 * * * /opt/agent-system/scripts/backup.sh

# Weekly full backup to external storage
0 3 * * 0 rsync -av /backup/agent-system/ remote-server:/backups/agent-system/
```

### Recovery Procedure

```bash
# Stop services
sudo systemctl stop agent-system.service
sudo systemctl stop llama-server.service

# Restore backup
cd /opt
sudo tar -xzf /backup/agent-system/backup_TIMESTAMP.tar.gz

# Fix permissions
sudo chown -R agent-system:agent-system /opt/agent-system

# Start services
sudo systemctl start llama-server.service
sudo systemctl start agent-system.service
```

## Security Hardening

### 1. File Permissions

```bash
# Set strict permissions
sudo chown -R agent-system:agent-system /opt/agent-system
sudo chmod 750 /opt/agent-system/app
sudo chmod 640 /opt/agent-system/app/.env
sudo chmod 640 /opt/agent-system/app/config.prod.yaml
```

### 2. Firewall Configuration

```bash
# Allow SSH only
sudo ufw allow ssh
sudo ufw enable

# llama-server is bound to localhost only (no firewall rule needed)
```

### 3. SELinux/AppArmor

```bash
# Ubuntu with AppArmor
sudo aa-enforce /opt/agent-system/app/main.py
```

### 4. Network Isolation

Ensure llama-server binds to localhost only:
```bash
# In llama-server command
--host 127.0.0.1  # NOT 0.0.0.0
```

## Performance Tuning

### 1. System Limits

Edit `/etc/security/limits.conf`:
```
agent-system soft nofile 65536
agent-system hard nofile 65536
agent-system soft nproc 32768
agent-system hard nproc 32768
```

### 2. GPU Optimization

```bash
# NVIDIA
export CUDA_VISIBLE_DEVICES=0
export LLAMA_GPU_LAYERS=99

# Apple Silicon
export LLAMA_METAL=1
export LLAMA_GPU_LAYERS=99
```

### 3. Memory Settings

```yaml
# config.prod.yaml
cursor_timeout: 600
task_timeout: 1200
max_concurrent_agents: 3  # Reduce for lower memory usage
```

### 4. Model Selection

```bash
# For faster inference, use smaller quantization
# Q4_K_M - Good balance
# Q4_K_S - Smaller, faster
# Q8_0 - Larger, better quality
```

## Maintenance Checklist

### Daily
- [ ] Check service status
- [ ] Review error logs
- [ ] Monitor disk space
- [ ] Verify backups completed

### Weekly
- [ ] Review performance metrics
- [ ] Check for system updates
- [ ] Clean old output files
- [ ] Rotate logs manually if needed

### Monthly
- [ ] Update dependencies
- [ ] Test backup recovery
- [ ] Review security logs
- [ ] Update documentation

### Quarterly
- [ ] System security audit
- [ ] Performance benchmarking
- [ ] Capacity planning
- [ ] Disaster recovery test

## Troubleshooting Production Issues

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## Additional Resources

- [Architecture](ARCHITECTURE.md) - System design
- [Configuration](../config.yaml) - Configuration reference
- [Monitoring](MONITORING.md) - Monitoring setup
- [Security](SECURITY.md) - Security best practices

---

For production support, contact your system administrator or consult the project documentation.
