# Frontend UI - Quick Guide

The project includes an Angular 20 UI with Material Design for managing agents, projects, and workflows.

## Quick Start (Mock Mode)

```bash
cd frontend-ui
npm install
npm run start:mock
```

Open `http://localhost:4200`.

## Full Stack (Backend + Auth)

```bash
# Infrastructure
docker compose up -d

# Backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn src.api.main:app --reload --port 8000

# Frontend
cd frontend-ui
npm install
npm start
```

Keycloak:
- Admin: `http://localhost:8081` (admin / admin)
- Demo user: `demo / demo`
- Realm display name: **SDLC 2.0** (technical realm: `llm-agents`)

## Documentation

- Full integration details: `docs/FRONTEND_SETUP.md`
- Frontend package docs: `frontend-ui/README.md`
