import asyncio
import uuid
from typing import Dict, Optional

from src.config import load_config
from src.db.database import async_session
from src.db.models import Workflow
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator
from src.api.websocket import manager


class OrchestratorBridge:
    def __init__(self) -> None:
        self._orchestrator: Optional[LangGraphOrchestrator] = None
        self._running: Dict[str, asyncio.Task] = {}

    def _get_orchestrator(self) -> LangGraphOrchestrator:
        if self._orchestrator is None:
            settings = load_config()
            self._orchestrator = LangGraphOrchestrator(
                workspace=settings.workspace,
                config=settings.to_dict(),
                enable_chat_display=False,
            )
        return self._orchestrator

    async def start_workflow(self, workflow_id: str, workflow_type: str, requirement: str) -> None:
        orchestrator = self._get_orchestrator()

        async def _run() -> None:
            await self._update_status(workflow_id, "running")
            try:
                if workflow_type == "bug_fix":
                    await orchestrator.execute_bug_fix(requirement=requirement, bug_description=requirement)
                else:
                    await orchestrator.execute_feature_development(requirement=requirement)
                await self._update_status(workflow_id, "completed")
            except Exception:
                await self._update_status(workflow_id, "failed")

        task = asyncio.create_task(_run())
        self._running[workflow_id] = task

    async def _update_status(self, workflow_id: str, status: str) -> None:
        async with async_session() as session:
            workflow_uuid = uuid.UUID(workflow_id)
            workflow = await session.get(Workflow, workflow_uuid)
            if workflow:
                workflow.status = status
                await session.commit()
        await manager.broadcast(
            workflow_id,
            {
                "event_type": "workflow_status_changed",
                "workflow_id": workflow_id,
                "data": {"status": status},
            },
        )


orchestrator_bridge = OrchestratorBridge()
