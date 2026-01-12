#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Starting llama.cpp server - requires Python 3.12 environment"

# Start llama.cpp server with Devstral-Small-2 model
llama-server \
  -hf unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL \
  -ngl 99 \
  --threads -1 \
  --ctx-size 16384 \
  --host 127.0.0.1 \
  --port 8080
