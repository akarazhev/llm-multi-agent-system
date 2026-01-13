#!/bin/bash

# llama.cpp Server Health Check Script
# Comprehensive health and status monitoring for llama-server

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
HOST="${LLAMA_HOST:-127.0.0.1}"
PORT="${LLAMA_PORT:-8080}"
API_URL="http://${HOST}:${PORT}"
HEALTH_URL="${API_URL}/health"
MODELS_URL="${API_URL}/v1/models"
LOG_DIR="${PROJECT_ROOT}/logs"
PID_FILE="${LOG_DIR}/llama-server.pid"
VERBOSE="${VERBOSE:-false}"

# Print banner
print_banner() {
    echo -e "${BLUE}=================================="
    echo "  llama.cpp Server Health Check"
    echo "==================================${NC}"
    echo ""
}

# Check if server process is running
check_process() {
    echo -e "${CYAN}[1/6] Checking server process...${NC}"
    
    local pids=$(pgrep -f "llama-server" 2>/dev/null || echo "")
    
    if [ -z "$pids" ]; then
        echo -e "${RED}  ✗ No llama-server process found${NC}"
        echo ""
        echo "Start the server with:"
        echo "  ${BLUE}./scripts/start_llama_server.sh${NC}"
        return 1
    fi
    
    echo -e "${GREEN}  ✓ Server process is running${NC}"
    
    # Show process details
    for pid in $pids; do
        if kill -0 $pid 2>/dev/null; then
            local runtime=$(ps -p $pid -o etime= 2>/dev/null | tr -d ' ' || echo "unknown")
            local mem=$(ps -p $pid -o rss= 2>/dev/null | awk '{print int($1/1024)"MB"}' || echo "unknown")
            local cpu=$(ps -p $pid -o %cpu= 2>/dev/null | tr -d ' ' || echo "unknown")
            echo "    PID: $pid"
            echo "    Runtime: $runtime"
            echo "    Memory: $mem"
            echo "    CPU: ${cpu}%"
        fi
    done
    
    # Check PID file consistency
    if [ -f "$PID_FILE" ]; then
        local stored_pid=$(cat "$PID_FILE")
        if ! echo "$pids" | grep -q "$stored_pid"; then
            echo -e "${YELLOW}    ⚠️  PID file mismatch (stored: $stored_pid)${NC}"
        fi
    else
        echo -e "${YELLOW}    ⚠️  No PID file found${NC}"
    fi
    
    echo ""
    return 0
}

# Check if port is listening
check_port() {
    echo -e "${CYAN}[2/6] Checking network port...${NC}"
    
    if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}  ✗ Port $PORT is not listening${NC}"
        echo ""
        
        # Check if process exists but port not listening
        if pgrep -f "llama-server" > /dev/null 2>&1; then
            echo -e "${YELLOW}  Process is running but not listening on port $PORT${NC}"
            echo "  The server might still be starting up or configured for a different port."
        fi
        
        return 1
    fi
    
    echo -e "${GREEN}  ✓ Port $PORT is listening${NC}"
    
    # Show what's listening
    local listener=$(lsof -i :$PORT -sTCP:LISTEN | tail -n +2)
    echo "    $listener" | while read line; do
        echo "    $line"
    done
    
    echo ""
    return 0
}

# Check HTTP connectivity
check_http() {
    echo -e "${CYAN}[3/6] Checking HTTP connectivity...${NC}"
    
    # Test basic connectivity
    if ! curl -s -f --connect-timeout 5 "${API_URL}/" > /dev/null 2>&1; then
        echo -e "${RED}  ✗ Cannot connect to ${API_URL}${NC}"
        echo ""
        echo "Possible issues:"
        echo "  - Server is still starting up"
        echo "  - Firewall blocking connection"
        echo "  - Wrong host/port configuration"
        return 1
    fi
    
    echo -e "${GREEN}  ✓ HTTP connection successful${NC}"
    
    # Test response time
    local response_time=$(curl -s -w "%{time_total}" -o /dev/null "${API_URL}/health" 2>/dev/null || echo "0")
    echo "    Response time: ${response_time}s"
    
    echo ""
    return 0
}

# Check API health endpoint
check_health() {
    echo -e "${CYAN}[4/6] Checking API health...${NC}"
    
    local health_response=$(curl -s -f --max-time 5 "$HEALTH_URL" 2>/dev/null || echo "")
    
    if [ -z "$health_response" ]; then
        echo -e "${RED}  ✗ Health endpoint not responding${NC}"
        echo ""
        echo "The server process is running but the API is not ready."
        echo "This is normal if the model is still loading."
        echo ""
        echo "Wait a moment and try again, or check logs:"
        echo "  ${BLUE}tail -f ${LOG_DIR}/llama-server.log${NC}"
        return 1
    fi
    
    echo -e "${GREEN}  ✓ Health endpoint responding${NC}"
    
    if [ "$VERBOSE" = "true" ]; then
        echo "    Response: $health_response"
    fi
    
    echo ""
    return 0
}

# Check models endpoint
check_models() {
    echo -e "${CYAN}[5/6] Checking available models...${NC}"
    
    local models_response=$(curl -s -f --max-time 5 "$MODELS_URL" 2>/dev/null || echo "")
    
    if [ -z "$models_response" ]; then
        echo -e "${YELLOW}  ⚠️  Models endpoint not responding${NC}"
        echo "    This might be normal depending on server configuration"
        echo ""
        return 0
    fi
    
    echo -e "${GREEN}  ✓ Models endpoint responding${NC}"
    
    # Parse and display models (if jq is available)
    if command -v jq &> /dev/null; then
        local model_count=$(echo "$models_response" | jq '.data | length' 2>/dev/null || echo "0")
        echo "    Available models: $model_count"
        
        if [ "$VERBOSE" = "true" ] && [ "$model_count" -gt 0 ]; then
            echo "$models_response" | jq -r '.data[].id' 2>/dev/null | while read model; do
                echo "      - $model"
            done
        fi
    else
        # Fallback: pretty print JSON with python
        if command -v python3 &> /dev/null; then
            echo "$models_response" | python3 -m json.tool 2>/dev/null | head -n 15 | sed 's/^/    /'
        else
            echo "    (Install jq or python3 for formatted output)"
        fi
    fi
    
    echo ""
    return 0
}

# Test inference endpoint
check_inference() {
    echo -e "${CYAN}[6/6] Testing inference endpoint...${NC}"
    
    local test_request='{
        "model": "devstral",
        "messages": [{"role": "user", "content": "Say hello"}],
        "max_tokens": 10,
        "temperature": 0.1
    }'
    
    local start_time=$(date +%s)
    local inference_response=$(curl -s -f --max-time 30 \
        -H "Content-Type: application/json" \
        -d "$test_request" \
        "${API_URL}/v1/chat/completions" 2>/dev/null || echo "")
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    if [ -z "$inference_response" ]; then
        echo -e "${YELLOW}  ⚠️  Inference endpoint not responding${NC}"
        echo "    This might indicate:"
        echo "      - Model is still loading"
        echo "      - Insufficient system resources"
        echo "      - Configuration issues"
        echo ""
        return 0
    fi
    
    # Check for error in response
    if echo "$inference_response" | grep -q '"error"'; then
        echo -e "${YELLOW}  ⚠️  Inference endpoint returned an error${NC}"
        if [ "$VERBOSE" = "true" ]; then
            echo "$inference_response" | python3 -m json.tool 2>/dev/null | sed 's/^/    /'
        fi
        echo ""
        return 0
    fi
    
    echo -e "${GREEN}  ✓ Inference endpoint working${NC}"
    echo "    Response time: ${duration}s"
    
    if [ "$VERBOSE" = "true" ] && command -v jq &> /dev/null; then
        local content=$(echo "$inference_response" | jq -r '.choices[0].message.content' 2>/dev/null || echo "")
        if [ -n "$content" ]; then
            echo "    Response: $content"
        fi
        
        local usage=$(echo "$inference_response" | jq '.usage' 2>/dev/null || echo "")
        if [ "$usage" != "null" ] && [ -n "$usage" ]; then
            echo "    Token usage: $usage"
        fi
    fi
    
    echo ""
    return 0
}

# Check system resources
check_resources() {
    echo -e "${CYAN}System Resources:${NC}"
    
    # Memory usage
    if command -v free &> /dev/null; then
        echo "  Memory:"
        free -h | grep -E "Mem:|Swap:" | sed 's/^/    /'
    elif command -v vm_stat &> /dev/null; then
        # macOS
        local free_pages=$(vm_stat | awk '/Pages free/{print $3}' | tr -d '.')
        local active_pages=$(vm_stat | awk '/Pages active/{print $3}' | tr -d '.')
        local page_size=$(vm_stat | awk '/page size of/{print $8}')
        local free_gb=$((free_pages * page_size / 1024 / 1024 / 1024))
        local used_gb=$((active_pages * page_size / 1024 / 1024 / 1024))
        echo "  Memory: ~${used_gb}GB used, ~${free_gb}GB free"
    fi
    
    # Disk usage
    local disk_usage=$(df -h "$PROJECT_ROOT" | awk 'NR==2{print $5 " used, " $4 " available"}')
    echo "  Disk: $disk_usage"
    
    # CPU load
    if command -v uptime &> /dev/null; then
        local load=$(uptime | awk -F'load average:' '{print $2}')
        echo "  Load average:$load"
    fi
    
    echo ""
}

# Check log file
check_logs() {
    echo -e "${CYAN}Recent Logs:${NC}"
    
    local log_file="${LOG_DIR}/llama-server.log"
    
    if [ ! -f "$log_file" ]; then
        echo -e "${YELLOW}  No log file found${NC}"
        return
    fi
    
    local log_size=$(stat -f%z "$log_file" 2>/dev/null || stat -c%s "$log_file" 2>/dev/null || echo 0)
    local log_size_mb=$((log_size / 1024 / 1024))
    echo "  Log file: $log_file (${log_size_mb}MB)"
    
    # Show last few lines
    echo "  Last 5 lines:"
    tail -n 5 "$log_file" 2>/dev/null | sed 's/^/    /' || echo "    (unable to read log)"
    
    # Check for errors in recent logs
    local error_count=$(tail -n 100 "$log_file" 2>/dev/null | grep -i "error\|fail\|exception" | wc -l | tr -d ' ')
    if [ "$error_count" -gt 0 ]; then
        echo -e "${YELLOW}  ⚠️  Found $error_count error(s) in recent logs${NC}"
    fi
    
    echo ""
}

# Print overall status
print_status() {
    local all_passed=true
    
    echo -e "${BLUE}=================================="
    echo "  Overall Server Status"
    echo "==================================${NC}"
    echo ""
    
    # Run all checks
    local process_ok=false
    local port_ok=false
    local http_ok=false
    local health_ok=false
    local models_ok=false
    
    check_process && process_ok=true
    check_port && port_ok=true
    check_http && http_ok=true
    check_health && health_ok=true
    check_models && models_ok=true
    check_inference  # Optional
    
    # Summary
    echo -e "${BLUE}=================================="
    echo "  Summary"
    echo "==================================${NC}"
    echo ""
    
    if $process_ok && $port_ok && $http_ok && $health_ok; then
        echo -e "${GREEN}✓ Server Status: HEALTHY 🟢${NC}"
        echo ""
        echo "The llama-server is running and ready to accept requests."
        echo ""
        echo "Connection Details:"
        echo "  API Base: http://${HOST}:${PORT}/v1"
        echo "  Health:   http://${HOST}:${PORT}/health"
        echo "  Models:   http://${HOST}:${PORT}/v1/models"
        echo ""
        echo "Test with curl:"
        echo "  ${BLUE}curl http://${HOST}:${PORT}/health${NC}"
        echo ""
        check_resources
        check_logs
        return 0
    elif $process_ok && $port_ok; then
        echo -e "${YELLOW}⚠️  Server Status: STARTING 🟡${NC}"
        echo ""
        echo "The server is running but not fully ready."
        echo "This is normal if the model is still loading."
        echo ""
        echo "Wait a moment and check again:"
        echo "  ${BLUE}./scripts/check_llama_server.sh${NC}"
        echo ""
        check_logs
        return 1
    elif $process_ok; then
        echo -e "${YELLOW}⚠️  Server Status: DEGRADED 🟠${NC}"
        echo ""
        echo "The server process is running but has connection issues."
        echo ""
        check_resources
        check_logs
        return 1
    else
        echo -e "${RED}✗ Server Status: NOT RUNNING 🔴${NC}"
        echo ""
        echo "The llama-server is not running."
        echo ""
        echo "Start the server with:"
        echo "  ${BLUE}./scripts/start_llama_server.sh${NC}"
        echo ""
        return 1
    fi
}

# Main execution
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                print_banner
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  -v, --verbose    Show detailed output"
                echo "  -h, --help       Show this help message"
                echo ""
                echo "Environment variables:"
                echo "  LLAMA_HOST      Server host (default: 127.0.0.1)"
                echo "  LLAMA_PORT      Server port (default: 8080)"
                echo ""
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Use -h for help"
                exit 1
                ;;
        esac
    done
    
    print_banner
    print_status
}

# Run main function
main "$@"
