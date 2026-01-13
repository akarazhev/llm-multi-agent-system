#!/bin/bash

# Fix Python Version Script
# Automatically recreates venv with correct Python version

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================="
echo "  Python Version Fix Script"
echo "==================================${NC}"
echo ""

# Get project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Check current Python version if venv exists
if [ -d "venv" ]; then
    echo -e "${BLUE}Checking current venv Python version...${NC}"
    if [ -f "venv/bin/python" ]; then
        CURRENT_VERSION=$(venv/bin/python --version 2>&1 | awk '{print $2}')
        echo "Current venv Python: $CURRENT_VERSION"
        
        # Extract major.minor
        MAJOR=$(echo $CURRENT_VERSION | cut -d. -f1)
        MINOR=$(echo $CURRENT_VERSION | cut -d. -f2)
        
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -eq 12 ]; then
            echo -e "${GREEN}✓ Python 3.12 detected ($CURRENT_VERSION)${NC}"
            echo ""
            echo "Your venv is already using Python 3.12."
            echo "If you're still having issues, try:"
            echo "  pip install --upgrade langgraph langchain-core"
            exit 0
        else
            echo -e "${YELLOW}⚠️  Python $CURRENT_VERSION detected${NC}"
            echo "   Required: Python 3.12"
            echo ""
        fi
    fi
fi

# Find compatible Python version
echo -e "${BLUE}Finding compatible Python version...${NC}"
PYTHON_CMD=""

# Try python3.12 first
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo -e "${GREEN}✓ Found python3.12${NC}"
# Only accept python3.12, nothing else
# Check if default python3 is compatible
elif command -v python3 &> /dev/null; then
    VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    MAJOR=$(echo $VERSION | cut -d. -f1)
    MINOR=$(echo $VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -eq 3 ] && ([ "$MINOR" -eq 11 ] || [ "$MINOR" -eq 12 ]); then
        PYTHON_CMD="python3"
        echo -e "${GREEN}✓ Found compatible python3 ($VERSION)${NC}"
    else
        echo -e "${RED}✗ Default python3 is $VERSION (not compatible)${NC}"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}=================================="
    echo "  Python 3.12 Not Found!"
    echo "==================================${NC}"
    echo ""
    echo "This project requires Python 3.12."
    echo ""
    echo "Install Python 3.12:"
    echo ""
    echo "macOS (Homebrew):"
    echo "  ${GREEN}brew install python@3.12${NC}"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  ${GREEN}sudo apt install python3.12${NC}"
    echo ""
    echo "Or use pyenv:"
    echo "  ${GREEN}pyenv install 3.12.7${NC}"
    echo ""
    exit 1
fi

# Show what we'll do
echo ""
echo -e "${YELLOW}This script will:${NC}"
echo "  1. Deactivate current venv (if active)"
echo "  2. Backup old venv to venv.backup"
echo "  3. Create new venv with $PYTHON_CMD"
echo "  4. Install dependencies"
echo "  5. Verify installation"
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Deactivate if active
if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${BLUE}Deactivating current venv...${NC}"
    deactivate 2>/dev/null || true
fi

# Backup old venv
if [ -d "venv" ]; then
    echo -e "${BLUE}Backing up old venv...${NC}"
    rm -rf venv.backup 2>/dev/null || true
    mv venv venv.backup
    echo -e "${GREEN}✓ Backed up to venv.backup${NC}"
fi

# Create new venv
echo ""
echo -e "${BLUE}Creating new venv with $PYTHON_CMD...${NC}"
$PYTHON_CMD -m venv venv

if [ ! -d "venv" ]; then
    echo -e "${RED}✗ Failed to create venv${NC}"
    
    # Restore backup
    if [ -d "venv.backup" ]; then
        mv venv.backup venv
        echo "Restored old venv"
    fi
    exit 1
fi

echo -e "${GREEN}✓ venv created${NC}"

# Activate new venv
echo ""
echo -e "${BLUE}Activating new venv...${NC}"
source venv/bin/activate

# Verify Python version
NEW_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ venv Python: $NEW_VERSION${NC}"

# Upgrade pip
echo ""
echo -e "${BLUE}Upgrading pip...${NC}"
python -m pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Verify imports
echo ""
echo -e "${BLUE}Verifying installation...${NC}"

python -c "import langgraph; print('✓ LangGraph:', langgraph.__version__)" || {
    echo -e "${RED}✗ LangGraph import failed${NC}"
    exit 1
}

python -c "import langchain_core; print('✓ LangChain Core installed')" || {
    echo -e "${RED}✗ LangChain Core import failed${NC}"
    exit 1
}

python -c "from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator; print('✓ LangGraphOrchestrator imported')" || {
    echo -e "${RED}✗ LangGraphOrchestrator import failed${NC}"
    exit 1
}

# Success
echo ""
echo -e "${GREEN}=================================="
echo "  Fix Complete! ✅"
echo "==================================${NC}"
echo ""
echo "Your venv is now using Python $NEW_VERSION"
echo ""
echo "Next steps:"
echo "  1. Activate venv: ${BLUE}source venv/bin/activate${NC}"
echo "  2. Run example: ${BLUE}python examples/langgraph_feature_development.py${NC}"
echo ""
echo "Old venv backed up to: venv.backup"
echo "You can delete it with: ${BLUE}rm -rf venv.backup${NC}"
echo ""
