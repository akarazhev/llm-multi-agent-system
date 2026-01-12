#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Checking llama.cpp server status - requires Python 3.12 environment"

# Check if llama.cpp server is running
if pgrep -x "llama-server" > /dev/null
then
  echo "Server is running"
  exit 0
else
  echo "Server is not running"
  exit 1
fi
