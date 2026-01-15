#!/usr/bin/env sh
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v podman >/dev/null 2>&1; then
  echo "Podman is not installed. Please install Podman first."
  exit 1
fi

cd "$ROOT_DIR"

if podman compose version >/dev/null 2>&1; then
  echo "Starting stack with podman compose..."
  podman compose up -d --build
elif command -v podman-compose >/dev/null 2>&1; then
  echo "Starting stack with podman-compose..."
  podman-compose up -d --build
else
  echo "Podman compose is not available."
  echo "Install the compose plugin or podman-compose."
  echo "Examples:"
  echo "  podman machine init && podman machine start"
  echo "  brew install podman-compose"
  exit 1
fi

echo ""
echo "Services started:"
echo "- Frontend: http://localhost:4200"
echo "- Backend:  http://localhost:8000"
echo "- Keycloak: http://localhost:8081 (admin/admin)"
