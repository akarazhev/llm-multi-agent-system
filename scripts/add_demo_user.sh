#!/usr/bin/env sh
set -e

# Script to add a demo user to Keycloak running in Podman
# Based on start_podman.sh Keycloak configuration

KEYCLOAK_CONTAINER="llm_agents_keycloak"
KEYCLOAK_REALM="llm-agents"
KEYCLOAK_SERVER="http://localhost:8081"
KEYCLOAK_ADMIN_USER="admin"
KEYCLOAK_ADMIN_PASSWORD="admin"
DEMO_USERNAME="demo"
DEMO_PASSWORD="demo"

echo "Checking if Keycloak container is running..."
if ! podman ps --format "{{.Names}}" | grep -q "^${KEYCLOAK_CONTAINER}$"; then
  echo "Error: Keycloak container '${KEYCLOAK_CONTAINER}' is not running."
  echo "Please start the Podman stack first using: ./scripts/start_podman.sh"
  exit 1
fi

echo "Waiting for Keycloak to be ready..."
attempt=0
until podman exec "${KEYCLOAK_CONTAINER}" /opt/keycloak/bin/kcadm.sh config credentials \
  --server "${KEYCLOAK_SERVER}" \
  --realm master \
  --user "${KEYCLOAK_ADMIN_USER}" \
  --password "${KEYCLOAK_ADMIN_PASSWORD}" >/dev/null 2>&1; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 30 ]; then
    echo "Error: Keycloak is not ready after 30 attempts."
    echo "Please check the Keycloak container logs:"
    echo "  podman logs ${KEYCLOAK_CONTAINER}"
    exit 1
  fi
  echo "Waiting for Keycloak... (attempt $attempt/30)"
  sleep 2
done

echo "Keycloak is ready!"

# Check if realm exists, create if not
echo "Checking if realm '${KEYCLOAK_REALM}' exists..."
if ! podman exec "${KEYCLOAK_CONTAINER}" /opt/keycloak/bin/kcadm.sh get realms/"${KEYCLOAK_REALM}" >/dev/null 2>&1; then
  echo "Realm '${KEYCLOAK_REALM}' does not exist. Creating..."
  podman exec "${KEYCLOAK_CONTAINER}" /opt/keycloak/bin/kcadm.sh create realms \
    -s realm="${KEYCLOAK_REALM}" \
    -s enabled=true
  echo "Realm '${KEYCLOAK_REALM}' created successfully!"
else
  echo "Realm '${KEYCLOAK_REALM}' already exists."
fi

# Check if demo user already exists
echo "Checking if demo user exists..."
if podman exec "${KEYCLOAK_CONTAINER}" /opt/keycloak/bin/kcadm.sh get users \
  -r "${KEYCLOAK_REALM}" -q username="${DEMO_USERNAME}" | tr -d '\n' | grep -q "\"username\":\"${DEMO_USERNAME}\""; then
  echo "Demo user already exists. Resetting password..."
  
  # Reset password for existing user
  podman exec "${KEYCLOAK_CONTAINER}" /opt/keycloak/bin/kcadm.sh set-password \
    -r "${KEYCLOAK_REALM}" \
    --username "${DEMO_USERNAME}" \
    --new-password "${DEMO_PASSWORD}"
  
  echo "Password reset successfully!"
else
  echo "Creating demo user..."
  
  # Create new user
  podman exec "${KEYCLOAK_CONTAINER}" /opt/keycloak/bin/kcadm.sh create users \
    -r "${KEYCLOAK_REALM}" \
    -s username="${DEMO_USERNAME}" \
    -s enabled=true
  
  # Set password
  podman exec "${KEYCLOAK_CONTAINER}" /opt/keycloak/bin/kcadm.sh set-password \
    -r "${KEYCLOAK_REALM}" \
    --username "${DEMO_USERNAME}" \
    --new-password "${DEMO_PASSWORD}"
  
  echo "Demo user created successfully!"
fi

echo ""
echo "========================================="
echo "Demo User Credentials:"
echo "  Username: ${DEMO_USERNAME}"
echo "  Password: ${DEMO_PASSWORD}"
echo "========================================="
echo ""
echo "You can now log in at: http://localhost:4200"
echo "Keycloak admin console: http://localhost:8081 (${KEYCLOAK_ADMIN_USER}/${KEYCLOAK_ADMIN_PASSWORD})"
