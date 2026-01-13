#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Create Python virtual environment in project root using Python 3.12
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12 not found!"
    echo "Install with: brew install python@3.12"
    exit 1
fi

echo "Creating virtual environment with python3.12..."
python3.12 -m venv "$PROJECT_ROOT/.venv" || {
    echo "Failed to create virtual environment"
    exit 1
}

# Detect Windows Git Bash environment
if [[ "$OSTYPE" == "msys"* ]]; then
    # Windows (Git Bash)
    ACTIVATE_CMD="$PROJECT_ROOT/.venv/Scripts/activate"
else
    # Linux/macOS
    ACTIVATE_CMD="$PROJECT_ROOT/.venv/bin/activate"
fi

# Activate environment
source "$PROJECT_ROOT/.venv/bin/activate" || {
    echo "Failed to activate virtual environment"
    exit 1
}

export PATH="$PROJECT_ROOT/.venv/bin:$PATH"

# Install the package in editable mode
pip install --force-reinstall -e . || {
    echo "Failed to install business_analyst_agent package"
    exit 1
}

# Verify installation
pip show business_analyst_agent || {
    echo "Package installation verification failed"
    exit 1
}

# Set execute permissions for scripts (skip on Windows)
if [[ "$OSTYPE" != "msys"* ]]; then
    chmod +x "$SCRIPT_DIR"/*.sh || {
        echo "Failed to set execute permissions"
        exit 1
    }
fi

echo "Environment setup complete. Activate with:"
echo "source '$PROJECT_ROOT/.venv/bin/activate'"
echo "To run the agent: ba-agent"
