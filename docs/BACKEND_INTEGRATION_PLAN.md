# Backend Integration Plan

**Version:** 0.1.0  
**Date:** 2026-01-14  
**Status:** Planning Phase

---

## Overview

This document provides a comprehensive plan for integrating the Angular frontend with the existing Python backend (LangGraph-based multi-agent orchestration system).

### Current State

**Frontend (Angular 20):**
- ✅ Project management UI (CRUD, wizard, detail pages)
- ✅ Agent management UI (CRUD, configuration, templates)
- ✅ Workflow management UI (list, detail, creation)
- ✅ Communication tab (agent messages, threads, decisions)
- ✅ Dashboard with statistics
- ⚠️ Currently using mock data

**Backend (Python + LangGraph):**
- ✅ Agent orchestration (BaseAgent, specialized agents)
- ✅ Workflow engine (templates, execution)
- ✅ LLM integration (llama.cpp)
- ✅ File operations (FileWriter)
- ⚠️ No REST API layer
- ⚠️ No database persistence
- ⚠️ No real-time communication

---

## Architecture

### High-Level Integration

```
┌─────────────────────────────────────────────────────────────┐
│                    Angular Frontend                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Projects │  │ Workflows│  │  Agents  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        │    HTTP/REST (CRUD operations)          │
        └─────────────┴─────────────┴─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │   WebSocket (Real-time)   │  ← New!
        └─────────────┬─────────────┘
                      │
┌─────────────────────▼─────────────────────────────────────┐
│                  FastAPI Server (NEW)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐    │
│  │   REST API   │  │  WebSocket   │  │   Auth      │    │
│  │  Controllers │  │   Handler    │  │   Middleware│    │
│  └──────┬───────┘  └──────┬───────┘  └─────────────┘    │
└─────────┼──────────────────┼────────────────────────────┘
          │                  │
┌─────────▼──────────────────▼────────────────────────────┐
│              Business Logic Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Project    │  │   Workflow   │  │   Agent      │  │
│  │   Service    │  │   Service    │  │   Service    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼─────────┐
│                  Data Access Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  PostgreSQL  │  │    Redis     │  │   MinIO/S3   │  │
│  │  (Primary)   │  │  (Cache/RT)  │  │  (Artifacts) │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────────────────────────────────────────────────────────┘
          │
┌─────────▼─────────────────────────────────────────────────┐
│              Existing LangGraph Core                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │AgentOrchest- │  │  Workflow    │  │  BaseAgent   │   │
│  │    rator     │  │   Engine     │  │  + Children  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Foundation (Week 1)

### 1.1 Database Setup

**Goal:** Set up PostgreSQL database with proper schema for all entities.

**Tasks:**

1. **Database Schema Design**
   - Projects table
   - Workflows table
   - Agents table
   - Agent Messages table
   - Decisions table
   - Users table (for auth)

2. **Database Setup Script**
   ```sql
   -- projects table
   CREATE TABLE projects (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     name VARCHAR(255) NOT NULL,
     description TEXT,
     type VARCHAR(50) NOT NULL,
     status VARCHAR(50) NOT NULL,
     repository_url TEXT,
     repository_branch VARCHAR(255),
     jira_project_key VARCHAR(50),
     jira_enabled BOOLEAN DEFAULT false,
     confluence_space_key VARCHAR(50),
     confluence_enabled BOOLEAN DEFAULT false,
     created_by VARCHAR(255) NOT NULL,
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW(),
     metadata JSONB
   );

   -- workflows table
   CREATE TABLE workflows (
     workflow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
     name VARCHAR(255) NOT NULL,
     description TEXT,
     workflow_type VARCHAR(50) NOT NULL,
     status VARCHAR(50) NOT NULL,
     priority VARCHAR(50) NOT NULL,
     requirement TEXT NOT NULL,
     assigned_agents TEXT[],
     steps JSONB,
     artifacts JSONB,
     metrics JSONB,
     errors JSONB,
     tags TEXT[],
     created_by VARCHAR(255) NOT NULL,
     started_at TIMESTAMP,
     completed_at TIMESTAMP,
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW()
   );

   -- agents table
   CREATE TABLE agents (
     agent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     name VARCHAR(255) NOT NULL,
     role VARCHAR(50) NOT NULL,
     status VARCHAR(50) NOT NULL,
     description TEXT,
     model VARCHAR(100) NOT NULL,
     temperature DECIMAL(3,2),
     max_tokens INTEGER,
     system_prompt TEXT,
     capabilities TEXT[],
     project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
     current_task TEXT,
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW(),
     last_active TIMESTAMP,
     metadata JSONB
   );

   -- agent_messages table (for communication)
   CREATE TABLE agent_messages (
     message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     workflow_id UUID REFERENCES workflows(workflow_id) ON DELETE CASCADE,
     agent_id UUID REFERENCES agents(agent_id) ON DELETE SET NULL,
     agent_name VARCHAR(255) NOT NULL,
     agent_role VARCHAR(50) NOT NULL,
     message_type VARCHAR(50) NOT NULL,
     content TEXT NOT NULL,
     addressed_to TEXT[],
     addressed_to_names TEXT[],
     parent_message_id UUID REFERENCES agent_messages(message_id),
     requires_response BOOLEAN DEFAULT false,
     urgency VARCHAR(50) DEFAULT 'medium',
     attachments JSONB,
     is_edited BOOLEAN DEFAULT false,
     edited_at TIMESTAMP,
     created_at TIMESTAMP DEFAULT NOW()
   );

   -- decisions table
   CREATE TABLE decisions (
     decision_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     workflow_id UUID REFERENCES workflows(workflow_id) ON DELETE CASCADE,
     problem TEXT NOT NULL,
     description TEXT,
     variants JSONB NOT NULL,
     chosen_variant_id VARCHAR(100),
     votes JSONB,
     justification TEXT,
     responsible_agents TEXT[],
     discussion_thread_id UUID REFERENCES agent_messages(message_id),
     created_at TIMESTAMP DEFAULT NOW()
   );

   -- users table (for future auth)
   CREATE TABLE users (
     user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     username VARCHAR(100) UNIQUE NOT NULL,
     email VARCHAR(255) UNIQUE NOT NULL,
     full_name VARCHAR(255),
     role VARCHAR(50) DEFAULT 'user',
     is_active BOOLEAN DEFAULT true,
     created_at TIMESTAMP DEFAULT NOW(),
     last_login TIMESTAMP
   );

   -- indexes
   CREATE INDEX idx_workflows_project ON workflows(project_id);
   CREATE INDEX idx_workflows_status ON workflows(status);
   CREATE INDEX idx_agents_role ON agents(role);
   CREATE INDEX idx_agents_project ON agents(project_id);
   CREATE INDEX idx_messages_workflow ON agent_messages(workflow_id);
   CREATE INDEX idx_messages_parent ON agent_messages(parent_message_id);
   ```

3. **SQLAlchemy Models**
   - Create `src/db/models.py` with all ORM models
   - Use Pydantic for validation
   - Match frontend TypeScript interfaces

4. **Alembic Migrations**
   - Set up Alembic for database migrations
   - Create initial migration

**Files to Create:**
- `src/db/__init__.py`
- `src/db/models.py`
- `src/db/database.py` (connection)
- `alembic/versions/001_initial_schema.py`

**Estimated Time:** 2 days

---

### 1.2 FastAPI Server Setup

**Goal:** Create FastAPI application with proper structure.

**Tasks:**

1. **Project Structure**
   ```
   src/
   ├── api/
   │   ├── __init__.py
   │   ├── main.py              # FastAPI app
   │   ├── deps.py              # Dependencies
   │   ├── routers/
   │   │   ├── __init__.py
   │   │   ├── projects.py
   │   │   ├── workflows.py
   │   │   ├── agents.py
   │   │   ├── communication.py
   │   │   └── health.py
   │   └── websocket.py         # WebSocket handler
   ├── services/
   │   ├── __init__.py
   │   ├── project_service.py
   │   ├── workflow_service.py
   │   ├── agent_service.py
   │   └── communication_service.py
   ├── schemas/
   │   ├── __init__.py
   │   ├── project.py           # Pydantic schemas
   │   ├── workflow.py
   │   ├── agent.py
   │   └── communication.py
   └── db/
       ├── __init__.py
       ├── database.py
       └── models.py
   ```

2. **FastAPI App Initialization**
   ```python
   # src/api/main.py
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   from .routers import projects, workflows, agents, communication, health
   from .websocket import router as websocket_router

   app = FastAPI(
       title="LLM Multi-Agent System API",
       version="0.1.0",
       description="REST API for multi-agent orchestration"
   )

   # CORS
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:4200"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

   # Routers
   app.include_router(health.router, prefix="/api/health", tags=["health"])
   app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
   app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
   app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
   app.include_router(communication.router, prefix="/api/communication", tags=["communication"])
   app.include_router(websocket_router, prefix="/ws")

   @app.on_event("startup")
   async def startup():
       # Initialize database connection pool
       pass

   @app.on_event("shutdown")
   async def shutdown():
       # Close database connections
       pass
   ```

3. **Dependencies Setup**
   ```python
   # requirements.txt (add to existing)
   fastapi==0.109.0
   uvicorn[standard]==0.27.0
   sqlalchemy==2.0.25
   asyncpg==0.29.0
   alembic==1.13.1
   python-jose[cryptography]==3.3.0
   passlib[bcrypt]==1.7.4
   python-multipart==0.0.6
   websockets==12.0
   redis==5.0.1
   ```

**Files to Create:**
- `src/api/main.py`
- `src/api/deps.py`
- `requirements-api.txt`

**Estimated Time:** 1 day

---

## Phase 2: REST API Implementation (Week 2)

### 2.1 Projects API

**Endpoints:**

```python
# src/api/routers/projects.py

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ProjectStatus] = None,
    db: Session = Depends(get_db)
):
    """List all projects with optional filters"""
    pass

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project"""
    pass

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Get project by ID"""
    pass

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update project"""
    pass

@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Delete project"""
    pass

@router.get("/{project_id}/agents", response_model=List[AgentResponse])
async def get_project_agents(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Get all agents assigned to project"""
    pass

@router.get("/{project_id}/workflows", response_model=List[WorkflowResponse])
async def get_project_workflows(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Get all workflows for project"""
    pass
```

**Estimated Time:** 2 days

---

### 2.2 Agents API

**Endpoints:**

```python
# src/api/routers/agents.py

@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    role: Optional[AgentRole] = None,
    status: Optional[AgentStatus] = None,
    project_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all agents with filters"""
    pass

@router.post("/", response_model=AgentResponse, status_code=201)
async def create_agent(
    agent: AgentCreate,
    db: Session = Depends(get_db)
):
    """Create a new agent"""
    # Initialize actual agent in orchestrator
    pass

@router.get("/templates", response_model=List[AgentTemplate])
async def get_agent_templates():
    """Get available agent templates"""
    pass

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get agent by ID"""
    pass

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent: AgentUpdate,
    db: Session = Depends(get_db)
):
    """Update agent configuration"""
    pass

@router.delete("/{agent_id}", status_code=204)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Delete agent"""
    pass

@router.post("/{agent_id}/assign", response_model=AgentResponse)
async def assign_agent_to_project(
    agent_id: str,
    assignment: AgentAssignment,
    db: Session = Depends(get_db)
):
    """Assign agent to a project"""
    pass
```

**Estimated Time:** 2 days

---

### 2.3 Workflows API

**Endpoints:**

```python
# src/api/routers/workflows.py

@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows(
    skip: int = 0,
    limit: int = 100,
    status: Optional[WorkflowStatus] = None,
    workflow_type: Optional[WorkflowType] = None,
    project_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all workflows with filters"""
    pass

@router.post("/", response_model=WorkflowResponse, status_code=201)
async def create_workflow(
    workflow: WorkflowCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and start a new workflow"""
    # Start workflow execution in background
    background_tasks.add_task(execute_workflow_task, workflow.workflow_id)
    pass

@router.get("/templates", response_model=List[WorkflowTemplate])
async def get_workflow_templates():
    """Get available workflow templates"""
    pass

@router.get("/{workflow_id}", response_model=WorkflowDetailResponse)
async def get_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """Get workflow details"""
    pass

@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: str,
    workflow: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """Update workflow"""
    pass

@router.post("/{workflow_id}/cancel", response_model=WorkflowResponse)
async def cancel_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """Cancel running workflow"""
    # Signal orchestrator to stop
    pass

@router.post("/{workflow_id}/resume", response_model=WorkflowResponse)
async def resume_workflow(
    workflow_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Resume failed/cancelled workflow"""
    pass

@router.delete("/{workflow_id}", status_code=204)
async def delete_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """Delete workflow"""
    pass
```

**Estimated Time:** 3 days

---

### 2.4 Communication API

**Endpoints:**

```python
# src/api/routers/communication.py

@router.get("/{workflow_id}/messages", response_model=List[AgentMessageResponse])
async def get_workflow_messages(
    workflow_id: str,
    message_type: Optional[MessageType] = None,
    agent_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all messages for a workflow"""
    pass

@router.post("/{workflow_id}/messages", response_model=AgentMessageResponse, status_code=201)
async def create_message(
    workflow_id: str,
    message: AgentMessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new message (for manual intervention)"""
    pass

@router.get("/{workflow_id}/threads", response_model=List[MessageThread])
async def get_workflow_threads(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """Get message threads for a workflow"""
    pass

@router.get("/{workflow_id}/decisions", response_model=List[AgentDecision])
async def get_workflow_decisions(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """Get all decisions made in workflow"""
    pass

@router.get("/{workflow_id}/stats", response_model=CommunicationStats)
async def get_communication_stats(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """Get communication statistics"""
    pass
```

**Estimated Time:** 2 days

---

## Phase 3: Real-Time Communication (Week 3)

### 3.1 WebSocket Implementation

**Goal:** Implement WebSocket for real-time updates.

**Features:**
- Workflow status updates
- Agent status changes
- New messages notifications
- Progress updates

**Implementation:**

```python
# src/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, workflow_id: str):
        await websocket.accept()
        if workflow_id not in self.active_connections:
            self.active_connections[workflow_id] = set()
        self.active_connections[workflow_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, workflow_id: str):
        if workflow_id in self.active_connections:
            self.active_connections[workflow_id].discard(websocket)
    
    async def broadcast_to_workflow(self, workflow_id: str, message: dict):
        if workflow_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[workflow_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.add(connection)
            
            # Clean up disconnected clients
            for conn in disconnected:
                self.active_connections[workflow_id].discard(conn)

manager = ConnectionManager()

@router.websocket("/workflows/{workflow_id}")
async def workflow_websocket(websocket: WebSocket, workflow_id: str):
    await manager.connect(websocket, workflow_id)
    try:
        while True:
            # Keep connection alive, listen for client messages
            data = await websocket.receive_text()
            # Handle client messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, workflow_id)
```

**Event Types:**

```python
# Event types to send via WebSocket
class WSEventType(str, Enum):
    WORKFLOW_STATUS_CHANGED = "workflow_status_changed"
    WORKFLOW_PROGRESS_UPDATE = "workflow_progress_update"
    AGENT_STATUS_CHANGED = "agent_status_changed"
    NEW_MESSAGE = "new_message"
    NEW_DECISION = "new_decision"
    STEP_STARTED = "step_started"
    STEP_COMPLETED = "step_completed"
    ERROR_OCCURRED = "error_occurred"

# Example event payload
{
    "event_type": "workflow_progress_update",
    "workflow_id": "workflow_001",
    "data": {
        "progress_percentage": 45,
        "current_step": "Step 3: Testing",
        "completed_steps": 2,
        "total_steps": 5
    },
    "timestamp": "2026-01-14T10:30:00Z"
}
```

**Estimated Time:** 2 days

---

### 3.2 Frontend WebSocket Service

**Angular Service:**

```typescript
// src/app/shared/services/websocket.service.ts
import { Injectable, signal } from '@angular/core';
import { Subject, Observable } from 'rxjs';

export interface WSMessage {
  event_type: string;
  workflow_id: string;
  data: any;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket?: WebSocket;
  private messageSubject = new Subject<WSMessage>();
  
  public messages$ = this.messageSubject.asObservable();
  public connectionStatus = signal<'connected' | 'disconnected' | 'connecting'>('disconnected');

  connectToWorkflow(workflowId: string): void {
    if (this.socket) {
      this.socket.close();
    }

    this.connectionStatus.set('connecting');
    this.socket = new WebSocket(`ws://localhost:8000/ws/workflows/${workflowId}`);

    this.socket.onopen = () => {
      this.connectionStatus.set('connected');
      console.log(`Connected to workflow ${workflowId}`);
    };

    this.socket.onmessage = (event) => {
      const message: WSMessage = JSON.parse(event.data);
      this.messageSubject.next(message);
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.socket.onclose = () => {
      this.connectionStatus.set('disconnected');
      console.log('WebSocket disconnected');
    };
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = undefined;
    }
  }

  ngOnDestroy(): void {
    this.disconnect();
  }
}
```

**Usage in Components:**

```typescript
// workflow-detail.component.ts
export class WorkflowDetailComponent implements OnInit, OnDestroy {
  private readonly wsService = inject(WebSocketService);
  private wsSubscription?: Subscription;

  ngOnInit(): void {
    const workflowId = this.route.snapshot.params['id'];
    
    // Connect to WebSocket
    this.wsService.connectToWorkflow(workflowId);
    
    // Subscribe to messages
    this.wsSubscription = this.wsService.messages$.subscribe(message => {
      this.handleWebSocketMessage(message);
    });
  }

  private handleWebSocketMessage(message: WSMessage): void {
    switch (message.event_type) {
      case 'workflow_progress_update':
        this.updateWorkflowProgress(message.data);
        break;
      case 'new_message':
        this.addNewMessage(message.data);
        break;
      // ... handle other events
    }
  }

  ngOnDestroy(): void {
    this.wsSubscription?.unsubscribe();
    this.wsService.disconnect();
  }
}
```

**Estimated Time:** 1 day

---

## Phase 4: LangGraph Integration (Week 4)

### 4.1 Orchestrator Bridge

**Goal:** Bridge between FastAPI and existing LangGraph orchestrator.

**Implementation:**

```python
# src/services/orchestrator_bridge.py
from typing import Dict, Any, Optional
import asyncio
from ..orchestrator import AgentOrchestrator
from ..db.database import get_db
from ..db.models import Workflow, Agent, AgentMessage
from ..api.websocket import manager

class OrchestratorBridge:
    """Bridge between API layer and LangGraph orchestrator"""
    
    def __init__(self):
        self.orchestrators: Dict[str, AgentOrchestrator] = {}
        self.running_workflows: Dict[str, asyncio.Task] = {}
    
    def get_orchestrator(self, project_id: str) -> AgentOrchestrator:
        """Get or create orchestrator for project"""
        if project_id not in self.orchestrators:
            self.orchestrators[project_id] = AgentOrchestrator(
                workspace=f"./projects/{project_id}",
                config={}
            )
        return self.orchestrators[project_id]
    
    async def start_workflow(
        self,
        workflow_id: str,
        project_id: str,
        workflow_type: str,
        requirement: str,
        assigned_agents: list[str],
        config: Dict[str, Any]
    ):
        """Start workflow execution"""
        orchestrator = self.get_orchestrator(project_id)
        
        # Create task for workflow execution
        task = asyncio.create_task(
            self._execute_workflow(
                orchestrator,
                workflow_id,
                workflow_type,
                requirement,
                assigned_agents,
                config
            )
        )
        
        self.running_workflows[workflow_id] = task
        return task
    
    async def _execute_workflow(
        self,
        orchestrator: AgentOrchestrator,
        workflow_id: str,
        workflow_type: str,
        requirement: str,
        assigned_agents: list[str],
        config: Dict[str, Any]
    ):
        """Execute workflow and emit events"""
        try:
            # Update workflow status: running
            await self._update_workflow_status(workflow_id, "running")
            await manager.broadcast_to_workflow(
                workflow_id,
                {
                    "event_type": "workflow_status_changed",
                    "workflow_id": workflow_id,
                    "data": {"status": "running"}
                }
            )
            
            # Execute workflow steps
            result = await orchestrator.execute_workflow(
                workflow_type=workflow_type,
                requirement=requirement,
                assigned_agents=assigned_agents,
                on_progress=lambda progress: self._on_progress(workflow_id, progress),
                on_message=lambda message: self._on_agent_message(workflow_id, message),
                on_decision=lambda decision: self._on_decision(workflow_id, decision)
            )
            
            # Update workflow status: completed
            await self._update_workflow_status(workflow_id, "completed", result)
            await manager.broadcast_to_workflow(
                workflow_id,
                {
                    "event_type": "workflow_status_changed",
                    "workflow_id": workflow_id,
                    "data": {"status": "completed", "result": result}
                }
            )
            
        except Exception as e:
            # Handle errors
            await self._update_workflow_status(workflow_id, "failed", error=str(e))
            await manager.broadcast_to_workflow(
                workflow_id,
                {
                    "event_type": "error_occurred",
                    "workflow_id": workflow_id,
                    "data": {"error": str(e)}
                }
            )
    
    async def _on_progress(self, workflow_id: str, progress: Dict):
        """Handle progress updates"""
        # Save to DB
        # Broadcast via WebSocket
        await manager.broadcast_to_workflow(
            workflow_id,
            {
                "event_type": "workflow_progress_update",
                "workflow_id": workflow_id,
                "data": progress
            }
        )
    
    async def _on_agent_message(self, workflow_id: str, message: Dict):
        """Handle agent messages"""
        # Save message to DB
        db = next(get_db())
        db_message = AgentMessage(**message, workflow_id=workflow_id)
        db.add(db_message)
        db.commit()
        
        # Broadcast via WebSocket
        await manager.broadcast_to_workflow(
            workflow_id,
            {
                "event_type": "new_message",
                "workflow_id": workflow_id,
                "data": message
            }
        )
    
    async def _on_decision(self, workflow_id: str, decision: Dict):
        """Handle agent decisions"""
        # Save decision to DB
        # Broadcast via WebSocket
        await manager.broadcast_to_workflow(
            workflow_id,
            {
                "event_type": "new_decision",
                "workflow_id": workflow_id,
                "data": decision
            }
        )
    
    async def cancel_workflow(self, workflow_id: str):
        """Cancel running workflow"""
        if workflow_id in self.running_workflows:
            task = self.running_workflows[workflow_id]
            task.cancel()
            await self._update_workflow_status(workflow_id, "cancelled")

# Global instance
orchestrator_bridge = OrchestratorBridge()
```

**Estimated Time:** 3 days

---

### 4.2 Agent Communication Logger

**Goal:** Capture and log all agent communication.

```python
# src/services/communication_logger.py
from typing import Dict, Any
from ..db.database import get_db
from ..db.models import AgentMessage, Decision
from ..api.websocket import manager
import uuid
from datetime import datetime

class CommunicationLogger:
    """Logger for agent communication"""
    
    async def log_message(
        self,
        workflow_id: str,
        agent_id: str,
        agent_name: str,
        agent_role: str,
        message_type: str,
        content: str,
        addressed_to: list[str] = None,
        parent_message_id: str = None,
        requires_response: bool = False,
        urgency: str = "medium",
        attachments: list = None
    ) -> str:
        """Log an agent message"""
        db = next(get_db())
        
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            agent_id=agent_id,
            agent_name=agent_name,
            agent_role=agent_role,
            message_type=message_type,
            content=content,
            addressed_to=addressed_to or [],
            parent_message_id=parent_message_id,
            requires_response=requires_response,
            urgency=urgency,
            attachments=attachments or [],
            created_at=datetime.utcnow()
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        # Broadcast via WebSocket
        await manager.broadcast_to_workflow(
            workflow_id,
            {
                "event_type": "new_message",
                "workflow_id": workflow_id,
                "data": message.to_dict()
            }
        )
        
        return message.message_id
    
    async def log_decision(
        self,
        workflow_id: str,
        problem: str,
        description: str,
        variants: list[Dict],
        chosen_variant_id: str,
        votes: Dict[str, str],
        justification: str,
        responsible_agents: list[str]
    ) -> str:
        """Log an agent decision"""
        db = next(get_db())
        
        decision = Decision(
            decision_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            problem=problem,
            description=description,
            variants=variants,
            chosen_variant_id=chosen_variant_id,
            votes=votes,
            justification=justification,
            responsible_agents=responsible_agents,
            created_at=datetime.utcnow()
        )
        
        db.add(decision)
        db.commit()
        db.refresh(decision)
        
        # Broadcast via WebSocket
        await manager.broadcast_to_workflow(
            workflow_id,
            {
                "event_type": "new_decision",
                "workflow_id": workflow_id,
                "data": decision.to_dict()
            }
        )
        
        return decision.decision_id

communication_logger = CommunicationLogger()
```

**Estimated Time:** 2 days

---

## Phase 5: External Integrations (Week 5)

### 5.1 Jira Integration

**Goal:** Auto-create Jira issues from workflows.

```python
# src/integrations/jira_client.py
from jira import JIRA
from typing import Dict, Any, Optional
import os

class JiraIntegration:
    def __init__(self):
        self.client = JIRA(
            server=os.getenv("JIRA_URL"),
            basic_auth=(
                os.getenv("JIRA_USERNAME"),
                os.getenv("JIRA_API_TOKEN")
            )
        )
    
    async def create_epic_from_workflow(
        self,
        project_key: str,
        workflow: Dict[str, Any]
    ) -> str:
        """Create epic for workflow"""
        epic = self.client.create_issue(
            project=project_key,
            summary=workflow["name"],
            description=workflow["description"],
            issuetype={"name": "Epic"},
            customfield_10011=workflow["name"]  # Epic name field
        )
        return epic.key
    
    async def create_story_from_step(
        self,
        project_key: str,
        epic_key: str,
        step: Dict[str, Any]
    ) -> str:
        """Create story for workflow step"""
        story = self.client.create_issue(
            project=project_key,
            summary=step["name"],
            description=step["description"],
            issuetype={"name": "Story"},
            customfield_10014=epic_key  # Epic link field
        )
        return story.key
    
    async def add_comment_from_message(
        self,
        issue_key: str,
        message: Dict[str, Any]
    ):
        """Add comment to issue from agent message"""
        comment_body = f"[{message['agent_name']}] {message['content']}"
        self.client.add_comment(issue_key, comment_body)

jira_integration = JiraIntegration()
```

**Estimated Time:** 2 days

---

### 5.2 Confluence Integration

**Goal:** Auto-generate documentation in Confluence.

```python
# src/integrations/confluence_client.py
from atlassian import Confluence
import os

class ConfluenceIntegration:
    def __init__(self):
        self.client = Confluence(
            url=os.getenv("CONFLUENCE_URL"),
            username=os.getenv("CONFLUENCE_USERNAME"),
            password=os.getenv("CONFLUENCE_API_TOKEN")
        )
    
    async def create_workflow_documentation(
        self,
        space_key: str,
        workflow: Dict[str, Any],
        messages: list[Dict[str, Any]],
        decisions: list[Dict[str, Any]]
    ) -> str:
        """Create documentation page for workflow"""
        
        # Build page content
        content = self._build_workflow_page_content(
            workflow, messages, decisions
        )
        
        page = self.client.create_page(
            space=space_key,
            title=f"Workflow: {workflow['name']}",
            body=content,
            parent_id=None
        )
        
        return page["id"]
    
    def _build_workflow_page_content(
        self,
        workflow: Dict,
        messages: list[Dict],
        decisions: list[Dict]
    ) -> str:
        """Build HTML/Storage format for Confluence"""
        # Format: Confluence Storage Format
        html = f"""
        <h1>{workflow['name']}</h1>
        <h2>Overview</h2>
        <p>{workflow['description']}</p>
        
        <h2>Requirements</h2>
        <p>{workflow['requirement']}</p>
        
        <h2>Agent Communication</h2>
        <ul>
        """
        
        for msg in messages:
            html += f"<li><strong>{msg['agent_name']}</strong>: {msg['content']}</li>"
        
        html += "</ul>"
        
        if decisions:
            html += "<h2>Decisions</h2><ul>"
            for decision in decisions:
                html += f"<li><strong>{decision['problem']}</strong>: {decision['justification']}</li>"
            html += "</ul>"
        
        return html

confluence_integration = ConfluenceIntegration()
```

**Estimated Time:** 2 days

---

## Phase 6: Frontend Integration (Week 6)

### 6.1 Update Frontend Services

**Remove mock data, use real API:**

```typescript
// src/app/shared/services/workflow.service.ts
import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { Workflow, WorkflowCreateRequest, WorkflowTemplate } from '../../core/interfaces/workflow.interface';

@Injectable({
  providedIn: 'root'
})
export class WorkflowService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/api';
  
  private readonly workflowsSource = signal<Workflow[]>([]);
  private readonly loadingSource = signal<boolean>(false);
  
  readonly workflows = this.workflowsSource.asReadonly();
  readonly loading = this.loadingSource.asReadonly();

  loadWorkflows(): void {
    this.loadingSource.set(true);
    this.http.get<Workflow[]>(`${this.apiUrl}/workflows`)
      .pipe(tap(() => this.loadingSource.set(false)))
      .subscribe(workflows => {
        this.workflowsSource.set(workflows);
      });
  }

  createWorkflow(request: WorkflowCreateRequest): Observable<Workflow> {
    return this.http.post<Workflow>(`${this.apiUrl}/workflows`, request)
      .pipe(tap(workflow => {
        this.workflowsSource.update(workflows => [...workflows, workflow]);
      }));
  }

  getWorkflowById(id: string): Observable<Workflow> {
    return this.http.get<Workflow>(`${this.apiUrl}/workflows/${id}`);
  }

  // ... other methods
}
```

**Estimated Time:** 2 days

---

### 6.2 Environment Configuration

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  wsUrl: 'ws://localhost:8000/ws',
  enableMockData: false
};

// src/environments/environment.prod.ts
export const environment = {
  production: true,
  apiUrl: '/api',  // Nginx proxy
  wsUrl: 'wss://yourdomain.com/ws',
  enableMockData: false
};
```

**Estimated Time:** 0.5 days

---

## Testing Strategy

### Unit Tests
- **Backend:** pytest for all services and routers
- **Frontend:** Jasmine/Karma for Angular components

### Integration Tests
- Test API endpoints with database
- Test WebSocket connections
- Test orchestrator bridge

### E2E Tests
- Playwright for full user flows
- Test workflow creation → execution → completion
- Test real-time updates

**Estimated Time:** 1 week (ongoing)

---

## Deployment

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: llm_agents
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: .
    command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/llm_agents
      REDIS_URL: redis://redis:6379

  frontend:
    build: ./frontend-ui
    ports:
      - "4200:4200"
    volumes:
      - ./frontend-ui:/app
    command: npm run start

  llama-server:
    image: ghcr.io/ggerganov/llama.cpp:server
    command: --model /models/devstral.gguf --host 0.0.0.0 --port 8080
    volumes:
      - ./models:/models
    ports:
      - "8080:8080"

volumes:
  postgres_data:
```

---

## Timeline Summary

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| 1 | Database Setup | 2 days | ⏳ Pending |
| 1 | FastAPI Server | 1 day | ⏳ Pending |
| 2 | Projects API | 2 days | ⏳ Pending |
| 2 | Agents API | 2 days | ⏳ Pending |
| 2 | Workflows API | 3 days | ⏳ Pending |
| 2 | Communication API | 2 days | ⏳ Pending |
| 3 | WebSocket Backend | 2 days | ⏳ Pending |
| 3 | WebSocket Frontend | 1 day | ⏳ Pending |
| 4 | Orchestrator Bridge | 3 days | ⏳ Pending |
| 4 | Communication Logger | 2 days | ⏳ Pending |
| 5 | Jira Integration | 2 days | ⏳ Pending |
| 5 | Confluence Integration | 2 days | ⏳ Pending |
| 6 | Frontend Services Update | 2 days | ⏳ Pending |
| 6 | Environment Config | 0.5 days | ⏳ Pending |
| - | Testing (ongoing) | 1 week | ⏳ Pending |

**Total Estimated Time:** 6 weeks

---

## Priority Order (What to Start Tomorrow)

### Day 1 (Tomorrow):
1. ✅ **Database Schema** - Most critical, blocks everything else
2. ✅ **FastAPI Setup** - Basic server structure

### Day 2-3:
3. ✅ **Projects API** - Simple CRUD to test full stack
4. ✅ **Basic Frontend Service** - Connect one endpoint

### Day 4-5:
5. ✅ **Workflows API** - Core functionality
6. ✅ **WebSocket Basic** - Real-time foundation

### Week 2:
7. ✅ **Agents API**
8. ✅ **Communication API**
9. ✅ **Orchestrator Bridge**

### Week 3+:
10. ✅ **External Integrations** (Jira, Confluence)
11. ✅ **Complete Frontend Integration**
12. ✅ **Testing & Polish**

---

## Questions to Answer Tomorrow

1. **Database Choice Confirmation:**
   - PostgreSQL confirmed? Or consider alternatives?
   - Hosting: Local, Docker, managed service?

2. **Authentication:**
   - Do we need user authentication now or later?
   - OAuth, JWT, or simple API keys for MVP?

3. **File Storage:**
   - Where to store generated artifacts?
   - Local filesystem, S3/MinIO, or database BLOB?

4. **Existing Code:**
   - Keep current Python orchestrator as-is?
   - Refactor needed before API layer?

5. **External Integrations:**
   - Jira/Confluence credentials ready?
   - Which instances (Cloud/Server)?

---

## Success Criteria

✅ **Phase 1 Complete When:**
- Database is set up and migrated
- FastAPI server runs successfully
- Can create/read one entity (e.g., Project)

✅ **Phase 2 Complete When:**
- All CRUD endpoints working
- Frontend can fetch and display real data
- No more mock data in use

✅ **Phase 3 Complete When:**
- WebSocket broadcasts workflow updates
- Frontend receives and displays real-time updates
- Connection is stable

✅ **Phase 4 Complete When:**
- Workflows execute via API
- Agent communication is logged
- Real-time events flow to frontend

✅ **Phase 5 Complete When:**
- Jira epics/stories auto-created
- Confluence pages auto-generated
- External systems sync correctly

✅ **Full Integration Complete When:**
- End-to-end workflow: Create project → Run workflow → See results
- Real-time communication visible
- External integrations working
- Production-ready deployment

---

**Next Step:** Review this plan tomorrow morning and start with Phase 1 (Database Setup)! 🚀
