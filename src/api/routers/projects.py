import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db_session
from src.api.schemas.project import AssignAgentsRequest, Project as ProjectSchema, ProjectFormData, ProjectUpdate
from src.db.models import Project

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[ProjectSchema])
async def list_projects(session: AsyncSession = Depends(get_db_session)) -> list[ProjectSchema]:
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return [ProjectSchema.model_validate(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(project_id: str, session: AsyncSession = Depends(get_db_session)) -> ProjectSchema:
    project_uuid = uuid.UUID(project_id)
    result = await session.execute(select(Project).where(Project.id == project_uuid))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return ProjectSchema.model_validate(project)


@router.post("/", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: ProjectFormData,
    session: AsyncSession = Depends(get_db_session),
    user: dict = Depends(get_current_user),
) -> ProjectSchema:
    now = datetime.utcnow()
    project = Project(
        id=uuid.uuid4(),
        name=request.name,
        description=request.description,
        icon=request.icon,
        status=request.status,
        type=request.type,
        owner_id=user.get("username") or user.get("sub") or "unknown",
        team_members=[],
        ai_agents=[],
        integrations={},
        tech_stack=request.techStack.model_dump(),
        stats={
            "totalWorkflows": 0,
            "activeWorkflows": 0,
            "completedWorkflows": 0,
            "failedWorkflows": 0,
            "teamSize": 1,
            "aiAgentsCount": 0,
            "filesGenerated": 0,
            "linesOfCode": 0,
        },
        created_at=now,
        updated_at=now,
        last_activity=None,
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return ProjectSchema.model_validate(project)


@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: str,
    request: ProjectUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> ProjectSchema:
    project_uuid = uuid.UUID(project_id)
    result = await session.execute(select(Project).where(Project.id == project_uuid))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if request.name is not None:
        project.name = request.name
    if request.description is not None:
        project.description = request.description
    if request.icon is not None:
        project.icon = request.icon
    if request.status is not None:
        project.status = request.status
    if request.type is not None:
        project.type = request.type
    if request.techStack is not None:
        project.tech_stack = request.techStack.model_dump()

    project.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(project)
    return ProjectSchema.model_validate(project)


@router.post("/{project_id}/agents", response_model=ProjectSchema)
async def assign_agents(
    project_id: str,
    request: AssignAgentsRequest,
    session: AsyncSession = Depends(get_db_session),
) -> ProjectSchema:
    project_uuid = uuid.UUID(project_id)
    result = await session.execute(select(Project).where(Project.id == project_uuid))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    project.ai_agents = request.agent_ids
    stats = project.stats or {}
    stats["aiAgentsCount"] = len(request.agent_ids)
    project.stats = stats
    project.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(project)
    return ProjectSchema.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str, session: AsyncSession = Depends(get_db_session)) -> None:
    project_uuid = uuid.UUID(project_id)
    result = await session.execute(select(Project).where(Project.id == project_uuid))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    await session.delete(project)
    await session.commit()
    return None
