from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AgentConfiguration(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    model: str
    temperature: float
    max_tokens: int
    tools_enabled: List[str]
    auto_approve: bool
    max_retries: int
    system_prompt: Optional[str] = None


class AgentMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_tasks: int
    success_rate: float
    avg_response_time: float
    tokens_used: int
    cost_estimate: float


class Agent(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    agent_id: UUID
    name: str
    role: str
    status: str
    description: str
    capabilities: List[str]
    current_task: Optional[str] = None
    completed_tasks: int
    failed_tasks: int
    avg_task_duration: Optional[float] = None
    created_at: datetime
    last_active: Optional[datetime] = None
    configuration: AgentConfiguration
    metrics: AgentMetrics
    assigned_projects: Optional[List[str]] = None


class CreateAgentRequest(BaseModel):
    name: str
    role: str
    description: Optional[str] = None
    configuration: Optional[AgentConfiguration] = None
    template_id: Optional[str] = None


class UpdateAgentRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[AgentConfiguration] = None
