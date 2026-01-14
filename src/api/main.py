from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import load_config
from .routers import agents, communication, health, projects, workflows
from .websocket import router as websocket_router


def create_app() -> FastAPI:
    settings = load_config()
    app = FastAPI(
        title="LLM Multi-Agent System API",
        version="0.1.0",
        description="Demo API for the multi-agent system"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api/health", tags=["health"])
    app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
    app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
    app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
    app.include_router(communication.router, prefix="/api/communication", tags=["communication"])
    app.include_router(websocket_router, prefix="/ws")

    return app


app = create_app()
