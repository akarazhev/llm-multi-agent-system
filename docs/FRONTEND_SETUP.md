# Frontend UI Integration

## Overview

The LLM Multi-Agent System now includes a modern Angular 20 frontend with Material Design.

## Table of Contents

- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [API Integration](#api-integration)
- [Backend Integration](#backend-integration)
- [Development Workflow](#development-workflow)
- [Production Deployment](#production-deployment)
- [Styling Guide](#styling-guide)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)
- [Resources](#resources)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Angular Frontend                    │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │  Dashboard   │  │  Workflows   │  │   Agents   ││
│  └──────────────┘  └──────────────┘  └────────────┘│
│                         │                            │
│              ┌──────────▼──────────┐                 │
│              │   HTTP Services     │                 │
│              └──────────┬──────────┘                 │
└────────────────────────┼──────────────────────────────┘
                         │
                         │ REST API
                         │
┌────────────────────────▼──────────────────────────────┐
│              Python FastAPI Backend                    │
│  ┌──────────────────────────────────────────────────┐ │
│  │         LangGraph Orchestrator                   │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

## Quick Start

### Option A: Full Stack via Docker Compose (Recommended)

```bash
docker compose up -d --build
```

Access:
- Frontend: `http://localhost:4200`
- Backend: `http://localhost:8000`
- Keycloak Admin: `http://localhost:8081` (admin / admin)
- Demo user: `demo / demo`

Notes:
- If port `4200` is busy, stop local `npm start` or change the compose port mapping.
- Realm display name is **SDLC 2.0** (technical realm stays `llm-agents`).

### Option B: Local Frontend + Local Backend

```bash
# 1) Start infrastructure
docker compose up -d

# 2) Frontend
cd frontend-ui
npm install
npm start

# 3) Backend (inside venv)
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn src.api.main:app --reload --port 8000
```

## Features

### Dashboard
- Real-time agent status
- Workflow statistics
- Recent workflows overview
- Quick actions

### Workflows
- Create new workflows
- View all workflows
- Monitor progress
- Cancel/Resume workflows

### Workflow Detail
- Detailed progress tracking
- Step-by-step visualization
- Files created
- Error logs

### Agents
- All 5 AI agents overview
- Current status
- Completed tasks count
- Agent descriptions

## Technology Stack

- **Angular 20** - Latest framework version
- **TypeScript 5.9** - Type-safe development
- **Angular Material 20** - Material Design components
- **RxJS 7.8** - Reactive programming
- **SCSS** - Advanced styling

## API Integration

### Endpoints

The frontend connects to these backend endpoints:

```typescript
// Agents
GET    /api/agents              // Get all agents
GET    /api/agents/{id}         // Get agent details
GET    /api/agents/{id}/status  // Get agent status

// Workflows
GET    /api/workflows           // Get all workflows
GET    /api/workflows/{id}      // Get workflow details
POST   /api/workflows           // Create workflow
POST   /api/workflows/{id}/cancel  // Cancel workflow
POST   /api/workflows/{id}/resume  // Resume workflow
GET    /api/workflows/{id}/results // Get results
```

### Request/Response Models

```typescript
// Agent
interface Agent {
  agent_id: string;
  role: AgentRole;
  status: AgentStatus;
  current_task?: string;
  completed_tasks: number;
}

// Workflow
interface Workflow {
  workflow_id: string;
  workflow_type: WorkflowType;
  requirement: string;
  status: WorkflowStatus;
  started_at: string;
  completed_at?: string;
  completed_steps: string[];
  files_created: string[];
  errors: WorkflowError[];
}
```

## Backend Integration

The production integration uses FastAPI with PostgreSQL persistence and Keycloak authentication.

### 1. Start Backend API

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn src.api.main:app --reload --port 8000
```

### 2. API Endpoints

```txt
GET    /api/agents
GET    /api/agents/{id}
POST   /api/agents
PUT    /api/agents/{id}
DELETE /api/agents/{id}

GET    /api/workflows
GET    /api/workflows/{id}
POST   /api/workflows
PUT    /api/workflows/{id}
POST   /api/workflows/{id}/cancel
POST   /api/workflows/{id}/resume
DELETE /api/workflows/{id}

GET    /api/projects
GET    /api/projects/{id}
POST   /api/projects
PUT    /api/projects/{id}
POST   /api/projects/{id}/agents
DELETE /api/projects/{id}

GET    /api/communication/{workflowId}/messages
GET    /api/communication/{workflowId}/threads
GET    /api/communication/{workflowId}/stats
```

### 3. Authentication (Keycloak)

Frontend configuration:

```typescript
export const environment = {
  authEnabled: true,
  keycloak: {
    url: 'http://localhost:8081',
    realm: 'llm-agents',
    clientId: 'llm-agent-ui'
  }
};
```

Admin and demo access:
- Admin: `http://localhost:8081` (admin / admin)
- Demo user: `demo / demo`
- Realm display name: **SDLC 2.0** (technical realm: `llm-agents`)

Backend configuration:

```yaml
keycloak:
  server_url: "http://localhost:8081"
  realm: "llm-agents"
  client_id: "llm-agent-ui"
  audience: "llm-agent-api"
```

WebSocket connection format:

```
ws://localhost:8000/ws/workflows/{workflowId}?token={accessToken}
```

## Development Workflow

### 1. Frontend Development

```bash
cd frontend-ui
npm start
# Auto-reload on file changes
```

### Settings (LLM Configuration)

Open **Settings** from the gear icon in the top-right. Values are stored in the backend and used by the orchestrator.

Fields:
- LLM Base URL
- API Key (optional)
- Model
- Timeout

### 2. Backend Development

```bash
# Terminal 1: Backend
uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend-ui
npm start
```

### 3. Full Stack Testing

1. Start backend: `uvicorn src.api.main:app --reload --port 8000`
2. Start frontend: `cd frontend-ui && npm start`
3. Open browser: `http://localhost:4200`
4. Test all features

## Production Deployment

### Build Frontend

```bash
cd frontend-ui
npm run build:prod
# Output: dist/llm-agent-ui/
```

### Serve from FastAPI

```python
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="frontend-ui/dist/llm-agent-ui", html=True), name="static")
```

### Docker Deployment

```dockerfile
# Multi-stage build
FROM node:20 AS frontend
WORKDIR /app/frontend-ui
COPY frontend-ui/package*.json ./
RUN npm install
COPY frontend-ui/ ./
RUN npm run build:prod

FROM python:3.12
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY --from=frontend /app/frontend-ui/dist/llm-agent-ui ./static
COPY . .
CMD ["python", "backend_api.py"]
```

## Styling Guide

### Theme Colors

From SPP project:
- Primary: `#3061D5` (Santander Blue)
- Secondary: `#F17B2C` (Orange)
- Surface: Material Design 3 surfaces

### Custom Styles

All styles use Material Design variables:

```scss
@use './style/material-variables' as vars;

.custom-component {
  background-color: vars.$surface-container;
  color: vars.$text-primary;
  border: vars.$border-primary;
}
```

## Troubleshooting

### CORS Errors

Add frontend origin to FastAPI CORS:

```python
allow_origins=["http://localhost:4200", "http://localhost:4300"]
```

### API Connection Failed

1. Check backend is running: `curl http://localhost:8000/api/agents`
2. Check CORS configuration
3. Check environment.ts has correct API URL

### Build Errors

```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Clear Angular cache
rm -rf .angular/cache
```

## Next Steps

1. **Role-Based Access**
   - Add realm roles and map to UI permissions
   - Restrict admin-only actions

2. **Seed Data**
   - Provide demo projects/agents/workflows
   - Add script for repeatable demo data

3. **Advanced Features**
   - Workflow templates
   - Agent configuration UI
   - Workflow scheduling

## Resources

- Frontend code: `/frontend-ui`
- Backend API: `/src/api/main.py`
- Documentation: `/docs/FRONTEND_SETUP.md`
- Examples: `/frontend-ui/README.md`

---

**Status**: ✅ Full stack integration available (FastAPI + Postgres + Keycloak)

For questions or issues, see `/frontend-ui/README.md` or `/docs/TROUBLESHOOTING.md`.
