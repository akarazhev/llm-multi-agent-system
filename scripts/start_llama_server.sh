#!/bin/bash

# llama.cpp Server Startup Script
# This script starts a local llama.cpp server for the multi-agent system
# with enhanced error handling, validation, and monitoring

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration (can be overridden by environment variables)
# Model quantization options:
#   - Q8_0: Higher quality, larger size (~24GB), better accuracy (default)
#   - UD-Q4_K_XL: Smaller size (~12GB), faster inference, slightly lower quality
# You can set MODEL_QUANTIZATION to switch between quantizations, or set LLAMA_MODEL directly
MODEL_QUANTIZATION="${MODEL_QUANTIZATION:-Q8_0}"
if [ -z "${LLAMA_MODEL:-}" ]; then
    MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:${MODEL_QUANTIZATION}"
else
    MODEL="$LLAMA_MODEL"
fi
HOST="${LLAMA_HOST:-127.0.0.1}"
PORT="${LLAMA_PORT:-8080}"
CTX_SIZE="${LLAMA_CTX_SIZE:-16384}"
GPU_LAYERS="${LLAMA_GPU_LAYERS:-99}"
THREADS="${LLAMA_THREADS:--1}"
LOG_LEVEL="${LLAMA_LOG_LEVEL:-info}"
BATCH_SIZE="${LLAMA_BATCH_SIZE:-512}"
PARALLEL="${LLAMA_PARALLEL:-4}"
LOG_DIR="${PROJECT_ROOT}/logs"
LOG_FILE="${LOG_DIR}/llama-server.log"
PID_FILE="${LOG_DIR}/llama-server.pid"

# Print banner
print_banner() {
    echo -e "${BLUE}=================================="
    echo "  llama.cpp Server Manager"
    echo "==================================${NC}"
}

# Print configuration
print_config() {
    echo ""
    echo -e "${BLUE}Configuration:${NC}"
    echo "  Model:        $MODEL"
    echo "  Host:         $HOST"
    echo "  Port:         $PORT"
    echo "  Context Size: $CTX_SIZE"
    echo "  GPU Layers:   $GPU_LAYERS"
    echo "  Threads:      $THREADS"
    echo "  Batch Size:   $BATCH_SIZE"
    echo "  Parallel:     $PARALLEL"
    echo "  Log Level:    $LOG_LEVEL"
    echo "  Log File:     $LOG_FILE"
    echo ""
}

# Create logs directory if it doesn't exist
create_log_dir() {
    if [ ! -d "$LOG_DIR" ]; then
        echo -e "${YELLOW}Creating logs directory...${NC}"
        mkdir -p "$LOG_DIR"
    fi
}

# Check if llama-server is installed
check_llama_server() {
    if ! command -v llama-server &> /dev/null; then
        echo -e "${RED}❌ Error: llama-server not found!${NC}"
        echo ""
        echo "Installation options:"
        echo ""
        echo "1. macOS (Homebrew):"
        echo "   ${GREEN}brew install llama.cpp${NC}"
        echo ""
        echo "2. Build from source:"
        echo "   ${GREEN}git clone https://github.com/ggerganov/llama.cpp${NC}"
        echo "   ${GREEN}cd llama.cpp${NC}"
        echo "   ${GREEN}make${NC}"
        echo "   ${GREEN}sudo make install${NC}"
        echo ""
        echo "3. Linux (pip):"
        echo "   ${GREEN}pip install llama-cpp-python[server]${NC}"
        echo ""
        exit 1
    fi
    
    # Get llama-server version
    local version=$(llama-server --version 2>/dev/null | head -n 1 || echo "unknown")
    echo -e "${GREEN}✓${NC} llama-server found: $version"
}

# Check if port is available
check_port() {
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Warning: Port $PORT is already in use!${NC}"
        echo ""
        
        # Show process using the port
        local process_info=$(lsof -i :$PORT -sTCP:LISTEN | tail -n +2)
        echo "Process using port $PORT:"
        echo "$process_info"
        echo ""
        
        # Check if it's our llama-server
        if echo "$process_info" | grep -q "llama-server"; then
            echo -e "${BLUE}A llama-server is already running on port $PORT.${NC}"
            echo ""
            read -p "Do you want to restart it? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                stop_existing_server
            else
                echo "Use './scripts/check_llama_server.sh' to check server status"
                exit 0
            fi
        else
            read -p "Kill existing process and start llama-server? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
                echo -e "${GREEN}✓${NC} Killed existing process"
                sleep 2
            else
                echo "Exiting..."
                exit 1
            fi
        fi
    else
        echo -e "${GREEN}✓${NC} Port $PORT is available"
    fi
}

# Stop existing llama-server
stop_existing_server() {
    echo -e "${YELLOW}Stopping existing llama-server...${NC}"
    
    # Try graceful shutdown first
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            kill -TERM "$pid" 2>/dev/null || true
            sleep 2
        fi
        rm -f "$PID_FILE"
    fi
    
    # Force kill if still running
    pkill -9 -f "llama-server.*--port $PORT" 2>/dev/null || true
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    
    sleep 2
    echo -e "${GREEN}✓${NC} Existing server stopped"
}

# Validate configuration
validate_config() {
    echo -e "${BLUE}Validating configuration...${NC}"
    
    # Validate port number
    if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1024 ] || [ "$PORT" -gt 65535 ]; then
        echo -e "${YELLOW}⚠️  Warning: Port $PORT may be invalid. Valid range: 1024-65535${NC}"
    fi
    
    # Validate context size
    if ! [[ "$CTX_SIZE" =~ ^[0-9]+$ ]] || [ "$CTX_SIZE" -lt 512 ]; then
        echo -e "${YELLOW}⚠️  Warning: Context size $CTX_SIZE may be too small. Recommended: 4096+${NC}"
    fi
    
    # Validate GPU layers
    if ! [[ "$GPU_LAYERS" =~ ^-?[0-9]+$ ]]; then
        echo -e "${YELLOW}⚠️  Warning: Invalid GPU layers value: $GPU_LAYERS${NC}"
    fi
    
    echo -e "${GREEN}✓${NC} Configuration validated"
}

# Check system resources
check_system_resources() {
    echo -e "${BLUE}Checking system resources...${NC}"
    
    # Check available memory
    if command -v free &> /dev/null; then
        local available_mem=$(free -g | awk '/^Mem:/{print $7}')
        echo "  Available Memory: ${available_mem}GB"
        if [ "$available_mem" -lt 8 ]; then
            echo -e "  ${YELLOW}⚠️  Low memory warning: Less than 8GB available${NC}"
        fi
    elif command -v vm_stat &> /dev/null; then
        # macOS
        local free_pages=$(vm_stat | awk '/Pages free/{print $3}' | tr -d '.')
        local page_size=$(vm_stat | awk '/page size of/{print $8}')
        local free_gb=$((free_pages * page_size / 1024 / 1024 / 1024))
        echo "  Available Memory: ~${free_gb}GB"
    fi
    
    # Check CPU cores
    if command -v nproc &> /dev/null; then
        local cpu_cores=$(nproc)
        echo "  CPU Cores: $cpu_cores"
    elif command -v sysctl &> /dev/null; then
        # macOS
        local cpu_cores=$(sysctl -n hw.ncpu)
        echo "  CPU Cores: $cpu_cores"
    fi
    
    # Check disk space
    local disk_space=$(df -h "$PROJECT_ROOT" | awk 'NR==2{print $4}')
    echo "  Disk Space: $disk_space available"
    
    echo -e "${GREEN}✓${NC} System resources checked"
}

# Start llama-server
start_server() {
    echo ""
    echo -e "${GREEN}🚀 Starting llama-server...${NC}"
    echo ""
    
    # Rotate log file if it's too large (> 100MB)
    if [ -f "$LOG_FILE" ]; then
        local log_size=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
        if [ "$log_size" -gt 104857600 ]; then
            echo "Rotating large log file..."
            mv "$LOG_FILE" "${LOG_FILE}.old"
        fi
    fi
    
    # Build llama-server command
    local cmd="llama-server"
    cmd="$cmd -hf \"$MODEL\""
    cmd="$cmd -ngl $GPU_LAYERS"
    cmd="$cmd --threads $THREADS"
    cmd="$cmd --ctx-size $CTX_SIZE"
    cmd="$cmd --batch-size $BATCH_SIZE"
    cmd="$cmd --parallel $PARALLEL"
    cmd="$cmd --host $HOST"
    cmd="$cmd --port $PORT"
    # Note: --log-level is not supported in all versions of llama-server
    
    # Add Metal support for Apple Silicon
    if [[ "$(uname)" == "Darwin" ]] && [[ "$(uname -m)" == "arm64" ]]; then
        echo -e "${BLUE}Detected Apple Silicon - enabling Metal acceleration${NC}"
    fi
    
    # Start server in background and capture PID
    echo "Starting server with command:"
    echo "  $cmd"
    echo ""
    echo "Logs will be written to: $LOG_FILE"
    echo ""
    
    # Start server
    nohup sh -c "$cmd" > "$LOG_FILE" 2>&1 &
    local pid=$!
    echo $pid > "$PID_FILE"
    
    echo -e "${GREEN}✓${NC} Server started with PID: $pid"
    echo ""
    
    # Wait for server to start
    echo "Waiting for server to start..."
    local max_wait=30
    local waited=0
    local api_url="http://${HOST}:${PORT}/health"
    
    while [ $waited -lt $max_wait ]; do
        if curl -s -f "$api_url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} Server is ready!"
            echo ""
            return 0
        fi
        
        # Check if process is still running
        if ! kill -0 $pid 2>/dev/null; then
            echo -e "${RED}❌ Server process died unexpectedly!${NC}"
            echo ""
            echo "Last 20 lines of log:"
            tail -n 20 "$LOG_FILE"
            exit 1
        fi
        
        echo -n "."
        sleep 1
        waited=$((waited + 1))
    done
    
    echo ""
    echo -e "${YELLOW}⚠️  Server started but health check timed out${NC}"
    echo "This might be normal if the model is still loading."
    echo ""
    echo "Check status with: ./scripts/check_llama_server.sh"
    echo "View logs with: tail -f $LOG_FILE"
    return 0
}

# Print success message
print_success() {
    echo -e "${GREEN}=================================="
    echo "  Server Started Successfully! 🎉"
    echo "==================================${NC}"
    echo ""
    echo "Server Details:"
    echo "  URL:      http://${HOST}:${PORT}"
    echo "  API:      http://${HOST}:${PORT}/v1"
    echo "  Health:   http://${HOST}:${PORT}/health"
    echo "  Docs:     http://${HOST}:${PORT}/docs"
    echo ""
    echo "Management Commands:"
    echo "  Check Status:  ${BLUE}./scripts/check_llama_server.sh${NC}"
    echo "  Stop Server:   ${BLUE}./scripts/stop_llama_server.sh${NC}"
    echo "  View Logs:     ${BLUE}tail -f $LOG_FILE${NC}"
    echo ""
    echo "Environment Configuration:"
    echo "  Add to your .env file:"
    echo "  ${BLUE}OPENAI_API_BASE=http://${HOST}:${PORT}/v1${NC}"
    echo "  ${BLUE}OPENAI_API_KEY=not-needed${NC}"
    echo "  ${BLUE}OPENAI_API_MODEL=devstral${NC}"
    echo ""
}

# Main execution
main() {
    print_banner
    print_config
    create_log_dir
    check_llama_server
    validate_config
    check_system_resources
    check_port
    start_server
    print_success
}

# Run main function
main
