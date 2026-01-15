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

echo "Waiting for Keycloak..."
attempt=0
until podman exec llm_agents_keycloak /opt/keycloak/bin/kcadm.sh config credentials \
  --server http://localhost:8081 \
  --realm master \
  --user admin \
  --password admin >/dev/null 2>&1; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 15 ]; then
    echo "Keycloak is not ready. Skipping demo user setup."
    break
  fi
  sleep 4
done

if [ "$attempt" -lt 15 ]; then
  if ! podman exec llm_agents_keycloak /opt/keycloak/bin/kcadm.sh get users \
    -r llm-agents -q username=demo | tr -d '\n' | grep -q '"username":"demo"'; then
    echo "Creating demo user..."
    podman exec llm_agents_keycloak /opt/keycloak/bin/kcadm.sh create users \
      -r llm-agents \
      -s username=demo \
      -s enabled=true >/dev/null

    podman exec llm_agents_keycloak /opt/keycloak/bin/kcadm.sh set-password \
      -r llm-agents \
      --username demo \
      --new-password demo >/dev/null
  else
    echo "Demo user already exists."
  fi
fi

echo ""
echo "Services started:"
echo "- Frontend: http://localhost:4200"
echo "- Backend:  http://localhost:8000"
echo "- Keycloak: http://localhost:8081 (admin/admin)"
