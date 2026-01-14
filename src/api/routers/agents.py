import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db_session
from src.api.schemas.agent import Agent as AgentSchema
from src.api.schemas.agent import CreateAgentRequest, UpdateAgentRequest
from src.db.models import Agent

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[AgentSchema])
async def list_agents(session: AsyncSession = Depends(get_db_session)) -> list[AgentSchema]:
    result = await session.execute(select(Agent))
    agents = result.scalars().all()
    return [AgentSchema.model_validate(agent) for agent in agents]


@router.get("/{agent_id}", response_model=AgentSchema)
async def get_agent(agent_id: str, session: AsyncSession = Depends(get_db_session)) -> AgentSchema:
    agent_uuid = uuid.UUID(agent_id)
    result = await session.execute(select(Agent).where(Agent.agent_id == agent_uuid))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return AgentSchema.model_validate(agent)


@router.post("/", response_model=AgentSchema, status_code=status.HTTP_201_CREATED)
async def create_agent(
    request: CreateAgentRequest,
    session: AsyncSession = Depends(get_db_session),
) -> AgentSchema:
    agent = Agent(
        agent_id=uuid.uuid4(),
        name=request.name,
        role=request.role,
        status="idle",
        description=request.description or "",
        capabilities=[],
        current_task=None,
        completed_tasks=0,
        failed_tasks=0,
        avg_task_duration=None,
        created_at=datetime.utcnow(),
        last_active=None,
        configuration=request.configuration.model_dump() if request.configuration else {},
        metrics={
            "total_tasks": 0,
            "success_rate": 0,
            "avg_response_time": 0,
            "tokens_used": 0,
            "cost_estimate": 0,
        },
        assigned_projects=[],
    )
    session.add(agent)
    await session.commit()
    await session.refresh(agent)
    return AgentSchema.model_validate(agent)


@router.put("/{agent_id}", response_model=AgentSchema)
async def update_agent(
    agent_id: str,
    request: UpdateAgentRequest,
    session: AsyncSession = Depends(get_db_session),
) -> AgentSchema:
    agent_uuid = uuid.UUID(agent_id)
    result = await session.execute(select(Agent).where(Agent.agent_id == agent_uuid))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

    if request.name is not None:
        agent.name = request.name
    if request.status is not None:
        agent.status = request.status
    if request.description is not None:
        agent.description = request.description
    if request.configuration is not None:
        agent.configuration = request.configuration.model_dump()

    await session.commit()
    await session.refresh(agent)
    return AgentSchema.model_validate(agent)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: str, session: AsyncSession = Depends(get_db_session)) -> None:
    agent_uuid = uuid.UUID(agent_id)
    result = await session.execute(select(Agent).where(Agent.agent_id == agent_uuid))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    await session.delete(agent)
    await session.commit()
    return None
