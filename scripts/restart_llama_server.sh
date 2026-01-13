#!/bin/bash

# llama.cpp Server Restart Script
# Safely restart the llama-server with health verification

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Configuration
MAX_WAIT=60  # Maximum seconds to wait for server to be ready

# Print banner
print_banner() {
    echo -e "${BLUE}=================================="
    echo "  llama.cpp Server Restart"
    echo "==================================${NC}"
    echo ""
}

# Check if stop script exists
check_scripts() {
    if [ ! -f "$SCRIPT_DIR/stop_llama_server.sh" ]; then
        echo -e "${RED}Error: stop_llama_server.sh not found${NC}"
        exit 1
    fi
    
    if [ ! -f "$SCRIPT_DIR/start_llama_server.sh" ]; then
        echo -e "${RED}Error: start_llama_server.sh not found${NC}"
        exit 1
    fi
}

# Stop existing server
stop_server() {
    echo -e "${YELLOW}Stopping existing server...${NC}"
    echo ""
    
    if "$SCRIPT_DIR/stop_llama_server.sh"; then
        echo -e "${GREEN}✓${NC} Server stopped"
    else
        echo -e "${YELLOW}⚠️  Stop script exited with errors, continuing...${NC}"
    fi
    
    # Give it a moment to fully shut down
    sleep 2
    echo ""
}

# Start server
start_server() {
    echo -e "${YELLOW}Starting server...${NC}"
    echo ""
    
    if "$SCRIPT_DIR/start_llama_server.sh"; then
        echo -e "${GREEN}✓${NC} Server start script completed"
    else
        echo -e "${RED}✗ Failed to start server${NC}"
        exit 1
    fi
    
    echo ""
}

# Wait for server to be healthy
wait_for_health() {
    echo -e "${YELLOW}Waiting for server to be ready...${NC}"
    
    local waited=0
    while [ $waited -lt $MAX_WAIT ]; do
        # Use check_server_status.sh if available
        if [ -f "$SCRIPT_DIR/check_server_status.sh" ]; then
            if QUIET=true "$SCRIPT_DIR/check_server_status.sh" 2>/dev/null; then
                echo -e "${GREEN}✓${NC} Server is ready!"
                return 0
            fi
        else
            # Fallback: check if llama-server process exists
            if pgrep -f "llama-server" > /dev/null 2>&1; then
                echo -e "${GREEN}✓${NC} Server process is running"
                return 0
            fi
        fi
        
        echo -n "."
        sleep 2
        waited=$((waited + 2))
    done
    
    echo ""
    echo -e "${YELLOW}⚠️  Server health check timed out${NC}"
    echo ""
    echo "The server might still be starting up."
    echo "Check status with: ./scripts/check_llama_server.sh"
    return 1
}

# Print success message
print_success() {
    echo ""
    echo -e "${GREEN}=================================="
    echo "  Server Restarted Successfully! ✓"
    echo "==================================${NC}"
    echo ""
    echo "Check status:"
    echo "  ${BLUE}./scripts/check_llama_server.sh${NC}"
    echo ""
}

# Main execution
main() {
    print_banner
    check_scripts
    stop_server
    start_server
    
    if wait_for_health; then
        print_success
        exit 0
    else
        echo "Restart completed but health check failed"
        exit 1
    fi
}

# Handle Ctrl+C gracefully
trap 'echo ""; echo "Interrupted"; exit 130' INT

# Run main function
main
