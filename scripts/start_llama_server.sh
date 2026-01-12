#!/bin/bash

# llama.cpp Server Startup Script
# This script starts a local llama.cpp server for the multi-agent system

set -e  # Exit on error

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration (can be overridden by environment variables)
MODEL="${LLAMA_MODEL:-unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL}"
HOST="${LLAMA_HOST:-127.0.0.1}"
PORT="${LLAMA_PORT:-8080}"
CTX_SIZE="${LLAMA_CTX_SIZE:-16384}"
GPU_LAYERS="${LLAMA_GPU_LAYERS:-99}"
THREADS="${LLAMA_THREADS:--1}"
LOG_LEVEL="${LLAMA_LOG_LEVEL:-info}"

echo "=================================="
echo "Starting llama.cpp Server"
echo "=================================="
echo "Model: $MODEL"
echo "Host: $HOST"
echo "Port: $PORT"
echo "Context Size: $CTX_SIZE"
echo "GPU Layers: $GPU_LAYERS"
echo "Threads: $THREADS"
echo "Log Level: $LOG_LEVEL"
echo "=================================="
echo ""

# Check if llama-server is installed
if ! command -v llama-server &> /dev/null; then
    echo "❌ Error: llama-server not found!"
    echo ""
    echo "Please install llama.cpp:"
    echo "  brew install llama.cpp"
    echo ""
    echo "Or build from source:"
    echo "  git clone https://github.com/ggerganov/llama.cpp"
    echo "  cd llama.cpp"
    echo "  make"
    exit 1
fi

# Check if port is already in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Warning: Port $PORT is already in use!"
    echo ""
    read -p "Kill existing process and restart? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
        echo "✓ Killed existing process"
        sleep 2
    else
        echo "Exiting..."
        exit 1
    fi
fi

echo "🚀 Starting llama-server..."
echo ""

# Start llama.cpp server
llama-server \
  -hf "$MODEL" \
  -ngl "$GPU_LAYERS" \
  --threads "$THREADS" \
  --ctx-size "$CTX_SIZE" \
  --host "$HOST" \
  --port "$PORT" \
  --log-level "$LOG_LEVEL" \
  --log-disable \
  2>&1 | tee "$PROJECT_ROOT/logs/llama-server.log"
