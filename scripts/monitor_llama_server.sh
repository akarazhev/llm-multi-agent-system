#!/bin/bash

# llama.cpp Server Monitoring Script
# Continuous monitoring with auto-restart capabilities

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
HOST="${LLAMA_HOST:-127.0.0.1}"
PORT="${LLAMA_PORT:-8080}"
CHECK_INTERVAL="${MONITOR_INTERVAL:-30}"  # Seconds between checks
AUTO_RESTART="${MONITOR_AUTO_RESTART:-false}"
MAX_RESTART_ATTEMPTS="${MONITOR_MAX_RESTARTS:-3}"
RESTART_COOLDOWN="${MONITOR_RESTART_COOLDOWN:-60}"  # Seconds to wait between restart attempts
LOG_DIR="${PROJECT_ROOT}/logs"
MONITOR_LOG="${LOG_DIR}/monitor.log"

# State tracking
RESTART_COUNT=0
LAST_RESTART_TIME=0
CONSECUTIVE_FAILURES=0
MAX_CONSECUTIVE_FAILURES=3

# Initialize
RUNNING=true
START_TIME=$(date +%s)

# Print banner
print_banner() {
    clear
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  llama.cpp Server Monitor"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "  Target:       http://${HOST}:${PORT}"
    echo "  Interval:     ${CHECK_INTERVAL}s"
    echo "  Auto-restart: ${AUTO_RESTART}"
    echo ""
    echo -e "${CYAN}Press Ctrl+C to stop monitoring${NC}"
    echo ""
}

# Log message
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$MONITOR_LOG"
}

# Get uptime
get_uptime() {
    local current_time=$(date +%s)
    local uptime=$((current_time - START_TIME))
    local hours=$((uptime / 3600))
    local minutes=$(((uptime % 3600) / 60))
    local seconds=$((uptime % 60))
    printf "%02d:%02d:%02d" $hours $minutes $seconds
}

# Check server health
check_health() {
    local health_url="http://${HOST}:${PORT}/health"
    
    # Check if process is running
    if ! pgrep -f "llama-server" > /dev/null 2>&1; then
        return 1
    fi
    
    # Check if port is listening
    if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 2
    fi
    
    # Check HTTP health endpoint
    if ! curl -s -f --connect-timeout 2 --max-time 5 "$health_url" > /dev/null 2>&1; then
        return 3
    fi
    
    return 0
}

# Get server metrics
get_metrics() {
    local pids=$(pgrep -f "llama-server" 2>/dev/null || echo "")
    
    if [ -z "$pids" ]; then
        echo "Process: Not running"
        return
    fi
    
    for pid in $pids; do
        if kill -0 $pid 2>/dev/null; then
            local mem=$(ps -p $pid -o rss= 2>/dev/null | awk '{print int($1/1024)}' || echo "0")
            local cpu=$(ps -p $pid -o %cpu= 2>/dev/null | tr -d ' ' || echo "0")
            local runtime=$(ps -p $pid -o etime= 2>/dev/null | tr -d ' ' || echo "unknown")
            
            echo "  PID:     $pid"
            echo "  Runtime: $runtime"
            echo "  Memory:  ${mem}MB"
            echo "  CPU:     ${cpu}%"
        fi
    done
}

# Test inference
test_inference() {
    local api_url="http://${HOST}:${PORT}/v1/chat/completions"
    local test_request='{
        "model": "devstral",
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 5
    }'
    
    local start=$(date +%s%3N)
    local response=$(curl -s -f --max-time 30 \
        -H "Content-Type: application/json" \
        -d "$test_request" \
        "$api_url" 2>/dev/null || echo "")
    local end=$(date +%s%3N)
    local latency=$((end - start))
    
    if [ -n "$response" ] && ! echo "$response" | grep -q '"error"'; then
        echo "  Latency: ${latency}ms"
        return 0
    else
        echo "  Latency: FAILED"
        return 1
    fi
}

# Restart server
restart_server() {
    local current_time=$(date +%s)
    local time_since_restart=$((current_time - LAST_RESTART_TIME))
    
    # Check if we're in cooldown period
    if [ "$LAST_RESTART_TIME" -ne 0 ] && [ "$time_since_restart" -lt "$RESTART_COOLDOWN" ]; then
        log_message "⚠️  In restart cooldown period (${time_since_restart}s/${RESTART_COOLDOWN}s)"
        return 1
    fi
    
    # Check restart count
    if [ "$RESTART_COUNT" -ge "$MAX_RESTART_ATTEMPTS" ]; then
        log_message "❌ Maximum restart attempts reached ($MAX_RESTART_ATTEMPTS)"
        return 1
    fi
    
    log_message "🔄 Attempting to restart server (attempt $((RESTART_COUNT + 1))/$MAX_RESTART_ATTEMPTS)..."
    
    # Try to restart
    if [ -f "$SCRIPT_DIR/restart_llama_server.sh" ]; then
        if "$SCRIPT_DIR/restart_llama_server.sh" >> "$MONITOR_LOG" 2>&1; then
            RESTART_COUNT=$((RESTART_COUNT + 1))
            LAST_RESTART_TIME=$(date +%s)
            CONSECUTIVE_FAILURES=0
            log_message "✓ Server restarted successfully"
            return 0
        else
            log_message "✗ Failed to restart server"
            return 1
        fi
    else
        log_message "✗ Restart script not found"
        return 1
    fi
}

# Handle server failure
handle_failure() {
    local failure_type="$1"
    
    CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
    
    log_message "❌ Health check failed: $failure_type (consecutive: $CONSECUTIVE_FAILURES)"
    
    if [ "$AUTO_RESTART" = "true" ] && [ "$CONSECUTIVE_FAILURES" -ge "$MAX_CONSECUTIVE_FAILURES" ]; then
        log_message "⚠️  Threshold reached, attempting auto-restart..."
        if restart_server; then
            sleep 10  # Give server time to start
        fi
    fi
}

# Display status
display_status() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local uptime=$(get_uptime)
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}Status Check at $timestamp${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Run health check
    check_health
    local health_status=$?
    
    if [ $health_status -eq 0 ]; then
        echo -e "${GREEN}✓ Server Status: HEALTHY${NC}"
        CONSECUTIVE_FAILURES=0
        echo ""
        echo "Server Metrics:"
        get_metrics
        echo ""
        echo "Performance:"
        test_inference
    else
        case $health_status in
            1)
                echo -e "${RED}✗ Server Status: PROCESS NOT RUNNING${NC}"
                handle_failure "process_dead"
                ;;
            2)
                echo -e "${YELLOW}⚠️  Server Status: PORT NOT LISTENING${NC}"
                handle_failure "port_not_listening"
                ;;
            3)
                echo -e "${YELLOW}⚠️  Server Status: HEALTH CHECK FAILED${NC}"
                handle_failure "health_check_failed"
                ;;
        esac
    fi
    
    echo ""
    echo "Monitor Statistics:"
    echo "  Uptime:       $uptime"
    echo "  Restarts:     $RESTART_COUNT/$MAX_RESTART_ATTEMPTS"
    echo "  Failures:     $CONSECUTIVE_FAILURES/$MAX_CONSECUTIVE_FAILURES"
    echo ""
    echo -e "${CYAN}Next check in ${CHECK_INTERVAL}s...${NC}"
    echo ""
}

# Cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping monitor...${NC}"
    log_message "Monitor stopped"
    echo ""
    echo "Monitor Statistics:"
    echo "  Total uptime: $(get_uptime)"
    echo "  Total restarts: $RESTART_COUNT"
    echo ""
    exit 0
}

# Main monitoring loop
monitor_loop() {
    while $RUNNING; do
        display_status
        sleep "$CHECK_INTERVAL"
        
        # Clear screen for next iteration
        if $RUNNING; then
            clear
            print_banner
        fi
    done
}

# Main execution
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -i|--interval)
                CHECK_INTERVAL="$2"
                shift 2
                ;;
            -a|--auto-restart)
                AUTO_RESTART=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  -i, --interval SECONDS    Check interval (default: 30)"
                echo "  -a, --auto-restart        Enable auto-restart on failure"
                echo "  -h, --help                Show this help message"
                echo ""
                echo "Environment variables:"
                echo "  LLAMA_HOST                     Server host (default: 127.0.0.1)"
                echo "  LLAMA_PORT                     Server port (default: 8080)"
                echo "  MONITOR_INTERVAL               Check interval in seconds"
                echo "  MONITOR_AUTO_RESTART           Enable auto-restart (true/false)"
                echo "  MONITOR_MAX_RESTARTS           Max restart attempts (default: 3)"
                echo "  MONITOR_RESTART_COOLDOWN       Seconds between restarts (default: 60)"
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
    
    # Create log directory
    mkdir -p "$LOG_DIR"
    
    # Setup signal handlers
    trap cleanup INT TERM
    
    # Start monitoring
    log_message "Monitor started (interval: ${CHECK_INTERVAL}s, auto-restart: $AUTO_RESTART)"
    print_banner
    monitor_loop
}

# Run main function
main "$@"
