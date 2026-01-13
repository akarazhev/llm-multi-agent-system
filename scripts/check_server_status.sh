#!/bin/bash

# Quick Server Status Check Script
# Simple, fast check for CI/CD and scripting use

# Exit codes:
# 0 - Server is running and healthy
# 1 - Server is not running
# 2 - Server is running but not healthy

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
HOST="${LLAMA_HOST:-127.0.0.1}"
PORT="${LLAMA_PORT:-8080}"
HEALTH_URL="http://${HOST}:${PORT}/health"
QUIET="${QUIET:-false}"

# Logging function
log() {
    if [ "$QUIET" != "true" ]; then
        echo "$@"
    fi
}

# Check if server process is running
if ! pgrep -f "llama-server" > /dev/null 2>&1; then
    log "Server is not running"
    exit 1
fi

log "Server process is running"

# Check if port is listening
if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    log "Server is running but not listening on port $PORT"
    exit 2
fi

log "Server is listening on port $PORT"

# Check health endpoint
if curl -s -f --connect-timeout 2 --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
    log "Server is healthy"
    exit 0
else
    log "Server is running but health check failed"
    exit 2
fi
