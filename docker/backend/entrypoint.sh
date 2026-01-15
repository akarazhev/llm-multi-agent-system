#!/usr/bin/env sh
set -e

export AGENT_CONFIG_PATH="/app/config.docker.yaml"

alembic upgrade head

uvicorn src.api.main:app --host 0.0.0.0 --port 8000
