#!/bin/bash

# Helper script to run Python examples with correct Python command
# Usage: ./scripts/run_example.sh examples/langgraph_feature_development.py

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ Python not found!${NC}"
    echo "Please install Python 3.12: brew install python@3.12"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo -e "${BLUE}Using: $PYTHON_CMD $PYTHON_VERSION${NC}"

if [ "$PYTHON_MAJOR" -ne 3 ] || [ "$PYTHON_MINOR" -ne 12 ]; then
    echo -e "${YELLOW}⚠️  Warning: Python 3.12 is required, you have $PYTHON_VERSION${NC}"
    echo "Install Python 3.12: brew install python@3.12"
fi

# Check if script argument provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}Usage: $0 <script.py>${NC}"
    echo ""
    echo "Available examples:"
    echo "  examples/langgraph_feature_development.py"
    echo "  examples/langgraph_bug_fix.py"
    echo "  examples/langgraph_resume_workflow.py"
    echo "  examples/visualize_workflow.py"
    echo ""
    echo "Example:"
    echo "  $0 examples/langgraph_feature_development.py"
    exit 1
fi

SCRIPT_PATH="$1"

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo -e "${RED}✗ Script not found: $SCRIPT_PATH${NC}"
    exit 1
fi

# Run the script
echo -e "${GREEN}Running: $PYTHON_CMD $SCRIPT_PATH${NC}"
echo ""

$PYTHON_CMD "$SCRIPT_PATH" "${@:2}"
