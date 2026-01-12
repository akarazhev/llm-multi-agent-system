#!/bin/bash

# Check if llama.cpp server is running and healthy

HOST="${LLAMA_HOST:-127.0.0.1}"
PORT="${LLAMA_PORT:-8080}"
API_URL="http://${HOST}:${PORT}/v1/models"

echo "Checking llama.cpp server at ${HOST}:${PORT}..."
echo ""

# Check if port is listening
if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "❌ Server is NOT running on port $PORT"
    echo ""
    echo "Start the server with:"
    echo "  ./scripts/start_llama_server.sh"
    exit 1
fi

echo "✓ Server is listening on port $PORT"

# Check API health
if curl -s -f "$API_URL" > /dev/null 2>&1; then
    echo "✓ API is responding"
    echo ""
    echo "Server Status: 🟢 HEALTHY"
    echo ""
    
    # Get model info
    echo "Available Models:"
    curl -s "$API_URL" | python3 -m json.tool 2>/dev/null || echo "  (Unable to parse model info)"
    
    exit 0
else
    echo "⚠️  Server is running but API not responding"
    echo ""
    echo "Server Status: 🟡 STARTING (wait a moment and try again)"
    exit 1
fi
