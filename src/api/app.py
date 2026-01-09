"""
FastAPI application entry point.

Provides REST API endpoints for the multi-agent system.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from src.config import settings
from src.orchestrator import Orchestrator

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="LLM-based multi-agent system for automated software development",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = Orchestrator()


# Request/Response models
class WorkflowRequest(BaseModel):
    """Request model for starting a workflow."""

    requirements: str
    request_id: Optional[str] = None


class WorkflowResponse(BaseModel):
    """Response model for workflow status."""

    request_id: str
    workflow_id: Optional[str] = None
    status: str
    current_step: Optional[str] = None
    message: str


class AgentInfo(BaseModel):
    """Agent information model."""

    agent_id: str
    agent_name: str
    tools: List[str]


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "agents": "/api/agents",
            "workflows": "/api/workflows",
            "start_workflow": "/api/workflows/start",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "services": {
            "orchestrator": "running",
            "agents_registered": len(orchestrator.list_agents()),
        },
    }


@app.get("/api/agents")
async def list_agents():
    """List all registered agents."""
    agents = orchestrator.list_agents()
    agent_info = []
    for agent_name in agents:
        agent = orchestrator.get_agent(agent_name)
        if agent:
            agent_info.append(agent.get_agent_info())
    return {"agents": agent_info, "count": len(agent_info)}


@app.post("/api/workflows/start", response_model=WorkflowResponse)
async def start_workflow(request: WorkflowRequest):
    """
    Start a new workflow.

    This endpoint accepts requirements and starts the multi-agent workflow.
    """
    if not orchestrator.list_agents():
        raise HTTPException(
            status_code=503,
            detail="No agents registered. Please register agents before starting workflows.",
        )

    try:
        workflow_state = await orchestrator.start_workflow(
            requirements=request.requirements,
            request_id=request.request_id,
        )

        return WorkflowResponse(
            request_id=workflow_state.request_id,
            workflow_id=str(workflow_state.workflow_id) if workflow_state.workflow_id else None,
            status=workflow_state.status.value,
            current_step=workflow_state.current_step,
            message=f"Workflow {workflow_state.status.value}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


@app.get("/api/workflows/{request_id}", response_model=Dict[str, Any])
async def get_workflow(request_id: str):
    """Get workflow status by request ID."""
    workflow = orchestrator.get_workflow(request_id)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow {request_id} not found")

    return workflow.model_dump()


@app.get("/api/workflows")
async def list_workflows():
    """List all active workflows."""
    workflows = orchestrator.list_workflows()
    return {
        "workflows": [w.model_dump() for w in workflows],
        "count": len(workflows),
    }


@app.delete("/api/workflows/{request_id}")
async def cancel_workflow(request_id: str):
    """Cancel a running workflow."""
    cancelled = await orchestrator.cancel_workflow(request_id)
    if not cancelled:
        raise HTTPException(status_code=404, detail=f"Workflow {request_id} not found")

    return {"message": f"Workflow {request_id} cancelled", "request_id": request_id}


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print(f"🚀 {settings.app_name} v{settings.app_version} starting...")
    print(f"📡 API available at http://{settings.api_host}:{settings.api_port}")
    print(f"📚 API documentation at http://{settings.api_host}:{settings.api_port}/docs")
    print("⚠️  No agents registered yet. Use orchestrator.register_agent() to add agents.")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("👋 Shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
