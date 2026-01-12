#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Stopping llama.cpp server - requires Python 3.12 environment"

# Stop llama.cpp server
pkill -f "llama-server" || {
    echo "No llama-server process found"
}
