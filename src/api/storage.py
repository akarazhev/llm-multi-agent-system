import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .schemas.agent import Agent, AgentConfiguration, AgentMetrics, CreateAgentRequest
from .schemas.project import Project, ProjectFormData, ProjectStats, TechStack
from .schemas.workflow import (
    Workflow,
    WorkflowCreateRequest,
    WorkflowMetrics,
    WorkflowPriority,
    WorkflowStatus,
    WorkflowStep,
    WorkflowType,
    StepStatus,
)


class InMemoryStore:
    def __init__(self) -> None:
        self.agents: Dict[str, Agent] = {}
        self.projects: Dict[str, Project] = {}
        self.workflows: Dict[str, Workflow] = {}

    def seed(self) -> None:
        now = datetime.utcnow()

        agent_configs = [
            ("Business Analyst", "business_analyst"),
            ("Developer", "developer"),
            ("QA Engineer", "qa_engineer"),
            ("DevOps Engineer", "devops_engineer"),
            ("Technical Writer", "technical_writer"),
        ]

        for name, role in agent_configs:
            agent_id = str(uuid.uuid4())
            self.agents[agent_id] = Agent(
                agent_id=agent_id,
                name=name,
                role=role,
                status="idle",
                description=f"{name} agent",
                capabilities=["requirements", "planning"],
                completed_tasks=0,
                failed_tasks=0,
                created_at=now.isoformat(),
                configuration=AgentConfiguration(
                    model="devstral",
                    temperature=0.5,
                    max_tokens=2048,
                    tools_enabled=[],
                    auto_approve=False,
                    max_retries=3,
                ),
                metrics=AgentMetrics(
                    total_tasks=0,
                    success_rate=0,
                    avg_response_time=0,
                    tokens_used=0,
                    cost_estimate=0,
                ),
                assigned_projects=[],
            )

        project_id = str(uuid.uuid4())
        self.projects[project_id] = Project(
            id=project_id,
            name="LLM Demo Project",
            description="Demo project for the presentation",
            icon="📁",
            status="active",
            type="web_app",
            ownerId="user_demo",
            teamMembers=[],
            aiAgents=list(self.agents.keys()),
            integrations={},
            techStack=TechStack(
                languages=["TypeScript", "Python"],
                frameworks=["Angular", "FastAPI"],
                databases=["PostgreSQL"],
                tools=["Docker"],
            ),
            stats=ProjectStats(
                totalWorkflows=2,
                activeWorkflows=1,
                completedWorkflows=1,
                failedWorkflows=0,
                teamSize=1,
                aiAgentsCount=len(self.agents),
                filesGenerated=0,
                linesOfCode=0,
            ),
            createdAt=now.isoformat(),
            updatedAt=now.isoformat(),
        )

        workflows = [
            ("Feature Development", "feature_development", WorkflowStatus.RUNNING),
            ("Bug Fix Sprint", "bug_fix", WorkflowStatus.COMPLETED),
        ]

        for index, (name, workflow_type, status) in enumerate(workflows, start=1):
            workflow_id = str(uuid.uuid4())
            started_at = now - timedelta(minutes=30 * index)
            completed_at = None
            if status == WorkflowStatus.COMPLETED:
                completed_at = (started_at + timedelta(minutes=25)).isoformat()

            steps = [
                WorkflowStep(
                    step_id=str(uuid.uuid4()),
                    name="Requirements",
                    description="Analyze requirements",
                    status=StepStatus.COMPLETED if status != WorkflowStatus.RUNNING else StepStatus.IN_PROGRESS,
                    logs=[],
                    artifacts=[],
                ),
                WorkflowStep(
                    step_id=str(uuid.uuid4()),
                    name="Implementation",
                    description="Implement solution",
                    status=StepStatus.PENDING if status == WorkflowStatus.RUNNING else StepStatus.COMPLETED,
                    logs=[],
                    artifacts=[],
                ),
            ]

            workflow = Workflow(
                workflow_id=workflow_id,
                name=name,
                description=f"{name} workflow",
                workflow_type=WorkflowType(workflow_type),
                requirement="Demo requirement",
                status=status,
                started_at=started_at.isoformat(),
                completed_at=completed_at,
                completed_steps=[step.name for step in steps if step.status == StepStatus.COMPLETED],
                total_steps=len(steps),
                progress_percentage=50 if status == WorkflowStatus.RUNNING else 100,
                files_created=[],
                errors=[],
                project_id=project_id,
                assigned_agents=list(self.agents.keys()),
                created_by="user_demo",
                tags=["demo"],
                priority=WorkflowPriority.MEDIUM,
                metrics=WorkflowMetrics(
                    total_duration=0,
                    agent_time={},
                    files_generated=0,
                    lines_of_code=0,
                    tests_created=0,
                    cost_estimate=0,
                    success_rate=100 if status == WorkflowStatus.COMPLETED else 0,
                ),
                steps=steps,
                artifacts=[],
            )
            self.workflows[workflow_id] = workflow

    def list_agents(self) -> List[Agent]:
        return list(self.agents.values())

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def create_agent(self, request: CreateAgentRequest) -> Agent:
        agent_id = str(uuid.uuid4())
        agent = Agent(
            agent_id=agent_id,
            name=request.name,
            role=request.role,
            status="idle",
            description=request.description or "",
            capabilities=[],
            completed_tasks=0,
            failed_tasks=0,
            created_at=datetime.utcnow().isoformat(),
            configuration=AgentConfiguration(
                model=request.configuration.model if request.configuration else "devstral",
                temperature=request.configuration.temperature if request.configuration else 0.5,
                max_tokens=request.configuration.max_tokens if request.configuration else 2048,
                tools_enabled=request.configuration.tools_enabled if request.configuration else [],
                auto_approve=request.configuration.auto_approve if request.configuration else False,
                max_retries=request.configuration.max_retries if request.configuration else 3,
                system_prompt=request.configuration.system_prompt if request.configuration else None,
            ),
            metrics=AgentMetrics(
                total_tasks=0,
                success_rate=0,
                avg_response_time=0,
                tokens_used=0,
                cost_estimate=0,
            ),
            assigned_projects=[],
        )
        self.agents[agent_id] = agent
        return agent

    def delete_agent(self, agent_id: str) -> bool:
        return self.agents.pop(agent_id, None) is not None

    def list_projects(self) -> List[Project]:
        return list(self.projects.values())

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def create_project(self, data: ProjectFormData) -> Project:
        project_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        project = Project(
            id=project_id,
            name=data.name,
            description=data.description,
            icon=data.icon,
            status=data.status,
            type=data.type,
            ownerId="user_demo",
            teamMembers=[],
            aiAgents=[],
            integrations={},
            techStack=data.techStack,
            stats=ProjectStats(
                totalWorkflows=0,
                activeWorkflows=0,
                completedWorkflows=0,
                failedWorkflows=0,
                teamSize=1,
                aiAgentsCount=0,
                filesGenerated=0,
                linesOfCode=0,
            ),
            createdAt=now,
            updatedAt=now,
        )
        self.projects[project_id] = project
        return project

    def update_project(self, project_id: str, data: ProjectFormData) -> Optional[Project]:
        existing = self.projects.get(project_id)
        if not existing:
            return None
        updated = existing.model_copy(update={
            "name": data.name,
            "description": data.description,
            "icon": data.icon,
            "status": data.status,
            "type": data.type,
            "techStack": data.techStack,
            "updatedAt": datetime.utcnow().isoformat(),
        })
        self.projects[project_id] = updated
        return updated

    def delete_project(self, project_id: str) -> bool:
        return self.projects.pop(project_id, None) is not None

    def assign_agents(self, project_id: str, agent_ids: List[str]) -> Optional[Project]:
        project = self.projects.get(project_id)
        if not project:
            return None
        updated_stats = project.stats.model_copy(update={
            "aiAgentsCount": len(agent_ids)
        })
        updated = project.model_copy(update={
            "aiAgents": agent_ids,
            "stats": updated_stats,
            "updatedAt": datetime.utcnow().isoformat()
        })
        self.projects[project_id] = updated
        return updated

    def list_workflows(self) -> List[Workflow]:
        return list(self.workflows.values())

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        return self.workflows.get(workflow_id)

    def create_workflow(self, request: WorkflowCreateRequest) -> Workflow:
        workflow_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        workflow = Workflow(
            workflow_id=workflow_id,
            name=request.name,
            description=request.description or "",
            workflow_type=request.workflow_type,
            requirement=request.requirement,
            status=WorkflowStatus.PENDING,
            started_at=now,
            completed_steps=[],
            total_steps=6,
            progress_percentage=0,
            files_created=[],
            errors=[],
            project_id=request.project_id,
            assigned_agents=request.assigned_agents or [],
            created_by="user_demo",
            tags=request.tags or [],
            priority=request.priority or WorkflowPriority.MEDIUM,
            metrics=WorkflowMetrics(
                total_duration=0,
                agent_time={},
                files_generated=0,
                lines_of_code=0,
                tests_created=0,
                cost_estimate=0,
                success_rate=0,
            ),
            steps=[],
            artifacts=[],
        )
        self.workflows[workflow_id] = workflow
        return workflow

    def update_workflow_status(self, workflow_id: str, status: WorkflowStatus) -> Optional[Workflow]:
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        updated = workflow.model_copy(update={
            "status": status,
            "completed_at": datetime.utcnow().isoformat() if status == WorkflowStatus.CANCELLED else workflow.completed_at,
        })
        self.workflows[workflow_id] = updated
        return updated


STORE = InMemoryStore()
STORE.seed()
