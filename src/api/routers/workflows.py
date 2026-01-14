import asyncio
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db_session
from src.api.schemas.workflow import Workflow as WorkflowSchema
from src.api.schemas.workflow import WorkflowCreateRequest, WorkflowStatus, WorkflowUpdateRequest
from src.db.models import Workflow
from src.services.orchestrator_bridge import orchestrator_bridge

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[WorkflowSchema])
async def list_workflows(session: AsyncSession = Depends(get_db_session)) -> list[WorkflowSchema]:
    result = await session.execute(select(Workflow))
    workflows = result.scalars().all()
    return [WorkflowSchema.model_validate(workflow) for workflow in workflows]


@router.get("/{workflow_id}", response_model=WorkflowSchema)
async def get_workflow(workflow_id: str, session: AsyncSession = Depends(get_db_session)) -> WorkflowSchema:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(select(Workflow).where(Workflow.workflow_id == workflow_uuid))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return WorkflowSchema.model_validate(workflow)


@router.post("/", response_model=WorkflowSchema, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    request: WorkflowCreateRequest,
    session: AsyncSession = Depends(get_db_session),
    user: dict = Depends(get_current_user),
) -> WorkflowSchema:
    now = datetime.utcnow()
    workflow = Workflow(
        workflow_id=uuid.uuid4(),
        name=request.name,
        description=request.description or "",
        workflow_type=request.workflow_type.value,
        requirement=request.requirement,
        status=WorkflowStatus.PENDING.value,
        started_at=now,
        completed_at=None,
        duration=None,
        current_step=None,
        completed_steps=[],
        total_steps=0,
        progress_percentage=0,
        files_created=[],
        errors=[],
        project_id=request.project_id,
        assigned_agents=request.assigned_agents or [],
        created_by=user.get("username") or user.get("sub") or "unknown",
        tags=request.tags or [],
        priority=(request.priority.value if request.priority else "medium"),
        metrics={
            "total_duration": 0,
            "agent_time": {},
            "files_generated": 0,
            "lines_of_code": 0,
            "tests_created": 0,
            "cost_estimate": 0,
            "success_rate": 0,
        },
        steps=[],
        artifacts=[],
    )
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)
    asyncio.create_task(
        orchestrator_bridge.start_workflow(
            workflow_id=str(workflow.workflow_id),
            workflow_type=workflow.workflow_type,
            requirement=workflow.requirement,
        )
    )
    return WorkflowSchema.model_validate(workflow)


@router.put("/{workflow_id}", response_model=WorkflowSchema)
async def update_workflow(
    workflow_id: str,
    request: WorkflowUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> WorkflowSchema:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(select(Workflow).where(Workflow.workflow_id == workflow_uuid))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    if request.name is not None:
        workflow.name = request.name
    if request.description is not None:
        workflow.description = request.description
    if request.status is not None:
        workflow.status = request.status.value
    if request.priority is not None:
        workflow.priority = request.priority.value
    if request.tags is not None:
        workflow.tags = request.tags

    await session.commit()
    await session.refresh(workflow)
    return WorkflowSchema.model_validate(workflow)


@router.post("/{workflow_id}/cancel", response_model=WorkflowSchema)
async def cancel_workflow(workflow_id: str, session: AsyncSession = Depends(get_db_session)) -> WorkflowSchema:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(select(Workflow).where(Workflow.workflow_id == workflow_uuid))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    workflow.status = WorkflowStatus.CANCELLED.value
    workflow.completed_at = datetime.utcnow()
    await session.commit()
    await session.refresh(workflow)
    return WorkflowSchema.model_validate(workflow)


@router.post("/{workflow_id}/resume", response_model=WorkflowSchema)
async def resume_workflow(workflow_id: str, session: AsyncSession = Depends(get_db_session)) -> WorkflowSchema:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(select(Workflow).where(Workflow.workflow_id == workflow_uuid))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    workflow.status = WorkflowStatus.RUNNING.value
    await session.commit()
    await session.refresh(workflow)
    return WorkflowSchema.model_validate(workflow)


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(workflow_id: str, session: AsyncSession = Depends(get_db_session)) -> None:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(select(Workflow).where(Workflow.workflow_id == workflow_uuid))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    await session.delete(workflow)
    await session.commit()
    return None
