#!/usr/bin/env sh
set -e

# Script to populate demo projects in Podman environment
# This script copies the populate script into the backend container and runs it

CONTAINER_NAME="llm_agents_backend"
SCRIPT_NAME="populate_demo_projects.py"

echo "="*80
echo "Populating Demo Projects in Podman Container"
echo "="*80
echo

# Check if container is running
if ! podman ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Container '${CONTAINER_NAME}' is not running!"
    echo "   Please start the containers first:"
    echo "   ./scripts/start_podman.sh"
    exit 1
fi

echo "✓ Container '${CONTAINER_NAME}' is running"
echo

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
POPULATE_SCRIPT="${SCRIPT_DIR}/${SCRIPT_NAME}"

# Check if the populate script exists
if [ ! -f "${POPULATE_SCRIPT}" ]; then
    echo "❌ Populate script not found: ${POPULATE_SCRIPT}"
    exit 1
fi

echo "Copying script to container..."
podman cp "${POPULATE_SCRIPT}" "${CONTAINER_NAME}:/app/${SCRIPT_NAME}"

echo "Running populate script in container..."
echo

# Run the script in the container
# The container uses config.docker.yaml which has the correct database URL
podman exec -it "${CONTAINER_NAME}" python /app/${SCRIPT_NAME} "$@"

echo
echo "Cleaning up..."
podman exec "${CONTAINER_NAME}" rm -f /app/${SCRIPT_NAME}

echo
echo "="*80
echo "✓ Done! Demo projects should now be available in the UI."
echo "="*80
