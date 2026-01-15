import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db_session
from src.api.schemas.demo import DemoProjectResponse
from src.db.models import Agent, AgentMessage, Project, Workflow

router = APIRouter(prefix="/demo", dependencies=[Depends(get_current_user)])


@router.post("/inventory", response_model=DemoProjectResponse)
async def create_inventory_demo(
    session: AsyncSession = Depends(get_db_session),
    user: dict = Depends(get_current_user),
) -> DemoProjectResponse:
    project = await _get_or_create_inventory_project(session, user)
    agents = await _get_or_create_demo_agents(session)
    workflow = await _get_or_create_demo_workflow(session, project, agents, user)
    await _seed_demo_communication(session, workflow, agents)
    return DemoProjectResponse(
        project_id=str(project.id),
        workflow_id=str(workflow.workflow_id),
    )


async def _get_or_create_inventory_project(session: AsyncSession, user: dict) -> Project:
    result = await session.execute(select(Project).where(Project.name == "Inventory Tool"))
    project = result.scalar_one_or_none()
    if project:
        return project

    now = datetime.utcnow()
    project = Project(
        id=uuid.uuid4(),
        name="Inventory Tool",
        description="Inventory Tool for tracking stock, locations, and inbound/outbound operations.",
        icon="📦",
        status="planning",
        type="web_app",
        owner_id=user.get("username") or user.get("sub") or "unknown",
        team_members=[],
        ai_agents=[],
        integrations={
            "git": {
                "platform": "github",
                "url": "https://git.example.com/inventory-tool",
                "branch": "main",
                "connected": True,
            },
            "confluence": {
                "url": "https://confluence.example.com/display/INV",
                "spaceKey": "INV",
                "connected": True,
            },
        },
        tech_stack={
            "languages": ["TypeScript", "Python"],
            "frameworks": ["Angular", "FastAPI"],
            "databases": ["PostgreSQL"],
            "tools": ["Docker"],
        },
        stats={
            "totalWorkflows": 1,
            "activeWorkflows": 0,
            "completedWorkflows": 1,
            "failedWorkflows": 0,
            "teamSize": 1,
            "aiAgentsCount": 5,
            "filesGenerated": 6,
            "linesOfCode": 420,
        },
        created_at=now,
        updated_at=now,
        last_activity=now,
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def _get_or_create_demo_agents(session: AsyncSession) -> list[Agent]:
    roles = [
        ("business_analyst", "Business Analyst"),
        ("developer", "Developer"),
        ("qa_engineer", "QA Engineer"),
        ("devops_engineer", "DevOps Engineer"),
        ("technical_writer", "Technical Writer"),
    ]

    agents: list[Agent] = []
    for role, name in roles:
        result = await session.execute(select(Agent).where(Agent.role == role))
        agent = result.scalar_one_or_none()
        if agent:
            agents.append(agent)
            continue

        agent = Agent(
            agent_id=uuid.uuid4(),
            name=name,
            role=role,
            status="idle",
            description=f"Demo {name} for Inventory Tool.",
            capabilities=["analysis", "planning", "execution"],
            current_task=None,
            completed_tasks=0,
            failed_tasks=0,
            avg_task_duration=None,
            created_at=datetime.utcnow(),
            last_active=None,
            configuration={
                "model": "devstral",
                "temperature": 0.7,
                "max_tokens": 2048,
                "tools_enabled": ["code_execution", "file_operations"],
                "auto_approve": False,
                "max_retries": 3,
            },
            metrics={
                "total_tasks": 0,
                "success_rate": 100,
                "avg_response_time": 12,
                "tokens_used": 0,
                "cost_estimate": 0,
            },
            assigned_projects=[],
        )
        session.add(agent)
        agents.append(agent)

    await session.commit()
    return agents


async def _get_or_create_demo_workflow(
    session: AsyncSession,
    project: Project,
    agents: list[Agent],
    user: dict,
) -> Workflow:
    result = await session.execute(
        select(Workflow)
        .where(Workflow.name == "Inventory Tool MVP")
        .where(Workflow.project_id == project.id)
    )
    workflow = result.scalar_one_or_none()
    if workflow:
        return workflow

    now = datetime.utcnow()
    workflow = Workflow(
        workflow_id=uuid.uuid4(),
        name="Inventory Tool MVP",
        description="Initial MVP for inventory tracking",
        workflow_type="feature_development",
        requirement="Build an inventory MVP with catalog, stock levels, and audit trail.",
        status="completed",
        started_at=now,
        completed_at=now,
        duration=1800,
        current_step=None,
        completed_steps=[
            "requirements",
            "architecture",
            "implementation",
            "testing",
            "devops",
            "documentation",
        ],
        total_steps=6,
        progress_percentage=100,
        files_created=[
            "backend/app/main.py",
            "backend/app/models.py",
            "backend/app/api/items.py",
            "frontend/src/app/items",
            "tests/test_inventory.py",
            "docs/INVENTORY_TOOL.md",
        ],
        errors=[],
        project_id=project.id,
        assigned_agents=[str(agent.agent_id) for agent in agents],
        created_by=user.get("username") or user.get("sub") or "unknown",
        tags=["demo", "inventory", "mvp"],
        priority="medium",
        metrics={
            "total_duration": 1800,
            "agent_time": {agent.role: 300 for agent in agents},
            "files_generated": 6,
            "lines_of_code": 420,
            "tests_created": 4,
            "cost_estimate": 0,
            "success_rate": 100,
        },
        steps=[
            {
                "step_id": "requirements",
                "name": "Requirements",
                "description": "Gather requirements and acceptance criteria.",
                "status": "completed",
                "agent_id": str(agents[0].agent_id),
                "started_at": now.isoformat(),
                "completed_at": now.isoformat(),
                "duration": 300,
                "output": "Inventory MVP requirements finalized.",
                "logs": ["Collected stakeholder inputs."],
                "artifacts": ["docs/requirements.md"],
            },
            {
                "step_id": "architecture",
                "name": "Architecture",
                "description": "Define system architecture and data model.",
                "status": "completed",
                "agent_id": str(agents[1].agent_id),
                "started_at": now.isoformat(),
                "completed_at": now.isoformat(),
                "duration": 300,
                "output": "Architecture diagram and schema drafted.",
                "logs": ["Selected FastAPI + PostgreSQL stack."],
                "artifacts": ["docs/architecture.md"],
            },
            {
                "step_id": "implementation",
                "name": "Implementation",
                "description": "Implement API and UI.",
                "status": "completed",
                "agent_id": str(agents[1].agent_id),
                "started_at": now.isoformat(),
                "completed_at": now.isoformat(),
                "duration": 600,
                "output": "Core endpoints and UI scaffold delivered.",
                "logs": ["Implemented CRUD for items and stock."],
                "artifacts": ["backend/app/api/items.py"],
            },
            {
                "step_id": "testing",
                "name": "Testing",
                "description": "Add tests for critical flows.",
                "status": "completed",
                "agent_id": str(agents[2].agent_id),
                "started_at": now.isoformat(),
                "completed_at": now.isoformat(),
                "duration": 300,
                "output": "Automated tests for inventory flows.",
                "logs": ["Added API tests for stock adjustments."],
                "artifacts": ["tests/test_inventory.py"],
            },
            {
                "step_id": "devops",
                "name": "DevOps",
                "description": "Prepare deployment checklist.",
                "status": "completed",
                "agent_id": str(agents[3].agent_id),
                "started_at": now.isoformat(),
                "completed_at": now.isoformat(),
                "duration": 150,
                "output": "Deployment notes and environment checklist.",
                "logs": ["Prepared Docker runbook."],
                "artifacts": ["docs/deploy.md"],
            },
            {
                "step_id": "documentation",
                "name": "Documentation",
                "description": "Create user and API docs.",
                "status": "completed",
                "agent_id": str(agents[4].agent_id),
                "started_at": now.isoformat(),
                "completed_at": now.isoformat(),
                "duration": 150,
                "output": "Documentation package ready.",
                "logs": ["Created usage guide and API examples."],
                "artifacts": ["docs/INVENTORY_TOOL.md"],
            },
        ],
        artifacts=[
            {
                "artifact_id": str(uuid.uuid4()),
                "type": "documentation",
                "name": "Inventory Tool Overview",
                "path": "docs/INVENTORY_TOOL.md",
                "size": 2048,
                "created_at": now.isoformat(),
                "created_by": str(agents[4].agent_id),
            },
            {
                "artifact_id": str(uuid.uuid4()),
                "type": "code",
                "name": "Inventory API",
                "path": "backend/app/api/items.py",
                "size": 4096,
                "created_at": now.isoformat(),
                "created_by": str(agents[1].agent_id),
            },
        ],
    )
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)
    return workflow


async def _seed_demo_communication(
    session: AsyncSession,
    workflow: Workflow,
    agents: list[Agent],
) -> None:
    result = await session.execute(
        select(AgentMessage).where(AgentMessage.workflow_id == workflow.workflow_id)
    )
    if result.scalars().first():
        return

    now = datetime.utcnow()
    ba = agents[0]
    dev = agents[1]
    qa = agents[2]

    root_question = AgentMessage(
        message_id=uuid.uuid4(),
        workflow_id=workflow.workflow_id,
        agent_id=ba.agent_id,
        agent_name=ba.name,
        agent_role=ba.role,
        message_type="question",
        content="Do we need batch adjustments in the MVP?",
        addressed_to=[str(dev.agent_id)],
        addressed_to_names=[dev.name],
        parent_message_id=None,
        requires_response=True,
        urgency="medium",
        attachments=[],
        is_edited=False,
        edited_at=None,
        created_at=now,
    )
    root_proposal = AgentMessage(
        message_id=uuid.uuid4(),
        workflow_id=workflow.workflow_id,
        agent_id=dev.agent_id,
        agent_name=dev.name,
        agent_role=dev.role,
        message_type="proposal",
        content="Suggest we focus on single-item adjustments for MVP and add batch later.",
        addressed_to=[str(ba.agent_id)],
        addressed_to_names=[ba.name],
        parent_message_id=None,
        requires_response=True,
        urgency="low",
        attachments=[],
        is_edited=False,
        edited_at=None,
        created_at=now,
    )
    reply_answer = AgentMessage(
        message_id=uuid.uuid4(),
        workflow_id=workflow.workflow_id,
        agent_id=ba.agent_id,
        agent_name=ba.name,
        agent_role=ba.role,
        message_type="answer",
        content="Agree. Single-item adjustments only for MVP.",
        addressed_to=[str(dev.agent_id)],
        addressed_to_names=[dev.name],
        parent_message_id=root_question.message_id,
        requires_response=False,
        urgency="low",
        attachments=[],
        is_edited=False,
        edited_at=None,
        created_at=now,
    )
    reply_decision = AgentMessage(
        message_id=uuid.uuid4(),
        workflow_id=workflow.workflow_id,
        agent_id=qa.agent_id,
        agent_name=qa.name,
        agent_role=qa.role,
        message_type="decision",
        content="Decision recorded: MVP excludes batch adjustments.",
        addressed_to=[str(ba.agent_id), str(dev.agent_id)],
        addressed_to_names=[ba.name, dev.name],
        parent_message_id=root_proposal.message_id,
        requires_response=False,
        urgency="low",
        attachments=[],
        is_edited=False,
        edited_at=None,
        created_at=now,
    )

    session.add_all([root_question, root_proposal, reply_answer, reply_decision])
    await session.commit()
