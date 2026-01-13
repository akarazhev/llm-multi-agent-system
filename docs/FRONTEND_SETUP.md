# Frontend UI Integration

## Overview

The LLM Multi-Agent System now includes a modern Angular 20 frontend with Material Design.

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

### 1. Install Frontend Dependencies

```bash
cd frontend-ui
npm install
```

### 2. Start Frontend (Development)

```bash
npm start
# Runs on http://localhost:4200
```

### 3. Start Backend

```bash
# From project root
python main.py
# Backend runs on http://localhost:8000
```

### 4. Access Application

Open browser: `http://localhost:4200`

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

## Backend Integration Required

To connect the frontend to the backend, you need to:

### 1. Add FastAPI Backend

Create `backend_api.py`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator
from src.config.settings import load_config

app = FastAPI(title="LLM Multi-Agent API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = load_config()
orchestrator = LangGraphOrchestrator(
    workspace=config.workspace,
    config=config.to_dict()
)

@app.get("/api/agents")
async def get_agents():
    """Get all agents status"""
    agents = []
    for agent_id, agent in orchestrator.agents.items():
        agents.append(agent.get_status())
    return agents

@app.get("/api/workflows")
async def get_workflows():
    """Get all workflows"""
    # Load from output directory
    import json
    from pathlib import Path
    
    workflows = []
    output_dir = Path(config.output_directory)
    
    for file in output_dir.glob("langgraph_*.json"):
        with open(file, 'r') as f:
            workflow = json.load(f)
            workflows.append(workflow)
    
    return workflows

@app.post("/api/workflows")
async def create_workflow(request: dict):
    """Create new workflow"""
    result = await orchestrator.execute_feature_development(
        requirement=request["requirement"],
        context=request.get("context", {})
    )
    return result

# Add more endpoints...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. Run Backend API

```bash
# Install FastAPI and Uvicorn
pip install fastapi uvicorn

# Run backend
python backend_api.py
```

### 3. Test Connection

```bash
# Test from terminal
curl http://localhost:8000/api/agents

# Or open in browser
http://localhost:8000/docs
```

## Development Workflow

### 1. Frontend Development

```bash
cd frontend-ui
npm start
# Auto-reload on file changes
```

### 2. Backend Development

```bash
# Terminal 1: Backend
python backend_api.py

# Terminal 2: Frontend
cd frontend-ui
npm start
```

### 3. Full Stack Testing

1. Start backend: `python backend_api.py`
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

1. **Real-time Updates**
   - Add WebSocket support
   - Live workflow progress
   - Agent status updates

2. **Authentication**
   - Add Keycloak integration
   - User management
   - Role-based access

3. **Advanced Features**
   - Workflow templates
   - Agent configuration UI
   - Workflow scheduling

## Resources

- Frontend code: `/frontend-ui`
- Backend API: `/backend_api.py` (to be created)
- Documentation: `/docs/FRONTEND_SETUP.md`
- Examples: `/frontend-ui/README.md`

---

**Status**: ✅ Frontend Ready - Backend Integration Required

For questions or issues, see `/frontend-ui/README.md` or `/docs/TROUBLESHOOTING.md`.
