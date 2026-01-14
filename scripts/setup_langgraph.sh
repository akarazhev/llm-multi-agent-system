#!/bin/bash

# Setup LangGraph Integration
# This script installs LangGraph dependencies and verifies the installation

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================="
echo "  LangGraph Integration Setup"
echo "==================================${NC}"
echo ""

# Check if virtual environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Warning: No virtual environment detected${NC}"
    echo ""
    echo "Create virtual environment with Python 3.12:"
    echo "  ${BLUE}python3.12 -m venv venv${NC}"
    echo "  ${BLUE}source venv/bin/activate${NC}  # Linux/macOS"
    echo "  ${BLUE}venv\\Scripts\\activate${NC}      # Windows"
    echo ""
    echo "If python3.12 is not installed:"
    echo "  ${BLUE}brew install python@3.12${NC}  # macOS"
    echo ""
    read -p "Continue without virtual environment? (y/N): " -n 1 -r
    echo
    if [[! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${BLUE}Installing LangGraph dependencies...${NC}"
echo ""

# Inside venv, use python and pip (not python3/pip3)
if [[ -n "$VIRTUAL_ENV" ]]; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
    echo "Using: $PYTHON_CMD (inside venv)"
else
    # Outside venv, check for python3.12
    if command -v python3.12 &> /dev/null; then
        PYTHON_CMD="python3.12"
        PIP_CMD="pip3.12"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    else
        echo -e "${RED}✗ Python not found!${NC}"
        echo "Please install Python 3.12: brew install python@3.12"
        exit 1
    fi
    echo "Using: $PYTHON_CMD ($(${PYTHON_CMD} --version))"
fi
echo ""

# Install dependencies
$PIP_CMD install --upgrade pip
$PIP_CMD install -r requirements.txt

echo ""
echo -e "${GREEN}✓${NC} Dependencies installed"
echo ""

# Verify installation
echo -e "${BLUE}Verifying installation...${NC}"
echo ""

$PYTHON_CMD -c "import langgraph; print('✓ LangGraph:', langgraph.__version__)" || {
    echo -e "${RED}✗ LangGraph import failed${NC}"
    exit 1
}

$PYTHON_CMD -c "import langchain_core; print('✓ LangChain Core installed')" || {
    echo -e "${RED}✗ LangChain Core import failed${NC}"
    exit 1
}

$PYTHON_CMD -c "import aiosqlite; print('✓ aiosqlite installed')" || {
    echo -e "${RED}✗ aiosqlite import failed${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}✓${NC} All dependencies verified"
echo ""

# Test import
echo -e "${BLUE}Testing LangGraph orchestrator import...${NC}"
echo ""

$PYTHON_CMD -c "from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator; print('✓ LangGraphOrchestrator imported successfully')" || {
    echo -e "${RED}✗ LangGraphOrchestrator import failed${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}=================================="
echo "  Setup Complete! 🎉"
echo "==================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Run example workflows:"
echo "   ${BLUE}${PYTHON_CMD} examples/langgraph_feature_development.py${NC}"
echo ""
echo "2. Read the documentation:"
echo "   ${BLUE}docs/LANGGRAPH_INTEGRATION.md${NC}"
echo ""
echo "3. Try the visualization:"
echo "   ${BLUE}${PYTHON_CMD} examples/visualize_workflow.py${NC}"
echo ""
echo "Key features enabled:"
echo "  ⚡ Parallel execution (30-40% faster)"
echo "  💾 State persistence (resume workflows)"
echo "  🔀 Conditional routing"
echo "  📊 Workflow visualization"
echo ""
