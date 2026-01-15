# Frontend UI - Quick Guide

The project includes an Angular 20 UI with Material Design for managing agents, projects, and workflows.

## Quick Start (Mock Mode)

```bash
cd frontend-ui
npm install
npm run start:mock
```

Open `http://localhost:4200`.

## Full Stack (Docker Compose)

```bash
docker compose up -d --build
```

Keycloak:
- Admin: `http://localhost:8081` (admin / admin)
- Demo user: `demo / demo`
- Realm display name: **SDLC 2.0** (technical realm: `llm-agents`)

Notes:
- If port `4200` is busy, stop local `npm start` or change the compose port mapping.

## Documentation

- Full integration details: `docs/FRONTEND_SETUP.md`
- Frontend package docs: `frontend-ui/README.md`
