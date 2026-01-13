#!/bin/bash

# llama.cpp Server Stop Script
# Gracefully stops the local llama.cpp server with proper cleanup

set -e  # Exit on error

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

# Configuration
PORT="${LLAMA_PORT:-8080}"
LOG_DIR="${PROJECT_ROOT}/logs"
PID_FILE="${LOG_DIR}/llama-server.pid"
MAX_WAIT=10  # Maximum seconds to wait for graceful shutdown

# Print banner
print_banner() {
    echo -e "${BLUE}=================================="
    echo "  llama.cpp Server Stop"
    echo "==================================${NC}"
    echo ""
}

# Check if server is running
check_server_running() {
    if ! pgrep -f "llama-server" > /dev/null 2>&1; then
        echo -e "${YELLOW}No llama-server process found${NC}"
        
        # Clean up stale PID file
        if [ -f "$PID_FILE" ]; then
            echo "Cleaning up stale PID file..."
            rm -f "$PID_FILE"
        fi
        
        # Check if port is in use by something else
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  Port $PORT is in use by another process:${NC}"
            lsof -i :$PORT -sTCP:LISTEN
            echo ""
            read -p "Kill this process? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
                echo -e "${GREEN}✓${NC} Process killed"
            fi
        fi
        
        return 1
    fi
    return 0
}

# Get server PIDs
get_server_pids() {
    pgrep -f "llama-server" || echo ""
}

# Stop server gracefully
stop_server_gracefully() {
    local pids=$(get_server_pids)
    
    if [ -z "$pids" ]; then
        return 0
    fi
    
    echo -e "${BLUE}Attempting graceful shutdown...${NC}"
    
    # Try SIGTERM first (graceful shutdown)
    for pid in $pids; do
        if kill -0 $pid 2>/dev/null; then
            echo "Sending SIGTERM to PID $pid..."
            kill -TERM $pid 2>/dev/null || true
        fi
    done
    
    # Wait for processes to exit
    local waited=0
    while [ $waited -lt $MAX_WAIT ]; do
        local remaining_pids=$(get_server_pids)
        if [ -z "$remaining_pids" ]; then
            echo -e "${GREEN}✓${NC} Server stopped gracefully"
            return 0
        fi
        
        echo -n "."
        sleep 1
        waited=$((waited + 1))
    done
    
    echo ""
    echo -e "${YELLOW}⚠️  Graceful shutdown timed out${NC}"
    return 1
}

# Force stop server
force_stop_server() {
    local pids=$(get_server_pids)
    
    if [ -z "$pids" ]; then
        return 0
    fi
    
    echo -e "${YELLOW}Force stopping server...${NC}"
    
    # Send SIGKILL
    for pid in $pids; do
        if kill -0 $pid 2>/dev/null; then
            echo "Sending SIGKILL to PID $pid..."
            kill -9 $pid 2>/dev/null || true
        fi
    done
    
    # Also kill by port
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    
    # Wait a moment
    sleep 1
    
    # Verify all stopped
    if pgrep -f "llama-server" > /dev/null 2>&1; then
        echo -e "${RED}❌ Failed to stop all llama-server processes${NC}"
        echo ""
        echo "Remaining processes:"
        ps aux | grep llama-server | grep -v grep
        return 1
    fi
    
    echo -e "${GREEN}✓${NC} Server force stopped"
    return 0
}

# Clean up resources
cleanup() {
    echo -e "${BLUE}Cleaning up resources...${NC}"
    
    # Remove PID file
    if [ -f "$PID_FILE" ]; then
        rm -f "$PID_FILE"
        echo "  ✓ Removed PID file"
    fi
    
    # Check for zombie processes
    local zombies=$(ps aux | grep -i llama | grep -i defunct | grep -v grep || echo "")
    if [ -n "$zombies" ]; then
        echo -e "${YELLOW}  ⚠️  Found zombie processes (they will clean up automatically):${NC}"
        echo "$zombies"
    fi
    
    # Verify port is free
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}  ⚠️  Port $PORT is still in use${NC}"
    else
        echo "  ✓ Port $PORT is free"
    fi
    
    echo -e "${GREEN}✓${NC} Cleanup complete"
}

# Show server status before stopping
show_status() {
    echo -e "${BLUE}Current server status:${NC}"
    
    # Show running processes
    local pids=$(get_server_pids)
    if [ -n "$pids" ]; then
        echo ""
        echo "Running llama-server processes:"
        for pid in $pids; do
            if kill -0 $pid 2>/dev/null; then
                local runtime=$(ps -p $pid -o etime= | tr -d ' ')
                local mem=$(ps -p $pid -o rss= | awk '{print int($1/1024)"MB"}')
                echo "  PID $pid - Runtime: $runtime, Memory: $mem"
            fi
        done
    fi
    
    # Show port usage
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo ""
        echo "Port $PORT usage:"
        lsof -i :$PORT -sTCP:LISTEN | tail -n +2 | while read line; do
            echo "  $line"
        done
    fi
    
    # Check PID file
    if [ -f "$PID_FILE" ]; then
        local stored_pid=$(cat "$PID_FILE")
        echo ""
        echo "PID file exists: $stored_pid"
        if ! kill -0 $stored_pid 2>/dev/null; then
            echo -e "  ${YELLOW}(stale - process not running)${NC}"
        fi
    fi
    
    echo ""
}

# Print success message
print_success() {
    echo ""
    echo -e "${GREEN}=================================="
    echo "  Server Stopped Successfully! ✓"
    echo "==================================${NC}"
    echo ""
    echo "To start the server again:"
    echo "  ${BLUE}./scripts/start_llama_server.sh${NC}"
    echo ""
}

# Main execution
main() {
    print_banner
    
    if ! check_server_running; then
        echo ""
        echo "Server is not running."
        exit 0
    fi
    
    show_status
    
    # Try graceful shutdown first
    if stop_server_gracefully; then
        cleanup
        print_success
        exit 0
    fi
    
    # If graceful shutdown failed, ask user
    echo ""
    read -p "Graceful shutdown failed. Force stop? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if force_stop_server; then
            cleanup
            print_success
            exit 0
        else
            echo -e "${RED}Failed to stop server${NC}"
            exit 1
        fi
    else
        echo "Server left running"
        exit 1
    fi
}

# Handle Ctrl+C gracefully
trap 'echo ""; echo "Interrupted"; exit 130' INT

# Run main function
main
