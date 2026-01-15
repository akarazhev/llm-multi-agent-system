from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TechStack(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    languages: List[str]
    frameworks: List[str]
    databases: List[str]
    tools: List[str]


class ProjectStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    totalWorkflows: int
    activeWorkflows: int
    completedWorkflows: int
    failedWorkflows: int
    teamSize: int
    aiAgentsCount: int
    filesGenerated: int
    linesOfCode: int


class GitIntegration(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    platform: str
    url: str
    branch: str
    connected: bool = False
    lastSync: Optional[str] = None


class ConfluenceIntegration(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    url: str
    spaceKey: str
    connected: bool = False
    lastSync: Optional[str] = None


class ProjectIntegrations(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    git: Optional[GitIntegration] = None
    confluence: Optional[ConfluenceIntegration] = None
    jira: Optional[Dict] = None
    slack: Optional[Dict] = None


class Project(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: UUID
    name: str
    description: str
    icon: Optional[str] = None
    status: str
    type: str
    ownerId: str = Field(alias="owner_id")
    teamMembers: List[Dict] = Field(alias="team_members")
    aiAgents: List[str] = Field(alias="ai_agents")
    integrations: ProjectIntegrations
    techStack: TechStack = Field(alias="tech_stack")
    stats: ProjectStats
    createdAt: datetime = Field(alias="created_at")
    updatedAt: datetime = Field(alias="updated_at")
    lastActivity: Optional[datetime] = Field(default=None, alias="last_activity")


class ProjectFormData(BaseModel):
    name: str
    description: str
    icon: Optional[str] = None
    status: str
    type: str
    techStack: TechStack
    integrations: Optional[ProjectIntegrations] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    techStack: Optional[TechStack] = None
    integrations: Optional[ProjectIntegrations] = None


class AssignAgentsRequest(BaseModel):
    agent_ids: List[str]
