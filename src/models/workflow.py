"""
Workflow state and data models.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class WorkflowStatus(str, Enum):
    """Workflow execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowState(BaseModel):
    """State of a workflow execution."""

    request_id: str = Field(..., description="Unique request identifier")
    workflow_id: Optional[UUID] = Field(None, description="Workflow UUID")
    requirements: str = Field(..., description="Original requirements text")
    current_step: str = Field(default="initial", description="Current workflow step")
    agent_outputs: Dict[str, Any] = Field(
        default_factory=dict, description="Outputs from each agent"
    )
    shared_context: Dict[str, Any] = Field(
        default_factory=dict, description="Shared context between agents"
    )
    jira_tickets: List[str] = Field(
        default_factory=list, description="Created Jira ticket keys"
    )
    confluence_pages: List[str] = Field(
        default_factory=list, description="Created Confluence page IDs"
    )
    gitlab_repos: List[str] = Field(
        default_factory=list, description="Created GitLab repository URLs"
    )
    status: WorkflowStatus = Field(
        default=WorkflowStatus.PENDING, description="Workflow status"
    )
    errors: List[str] = Field(default_factory=list, description="List of errors")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")

    class Config:
        """Pydantic config."""

        use_enum_values = True


class AgentOutput(BaseModel):
    """Output from an agent execution."""

    agent_name: str = Field(..., description="Name of the agent")
    output_type: str = Field(..., description="Type of output (analysis, code, etc.)")
    content: Dict[str, Any] = Field(..., description="Output content")
    workflow_id: Optional[UUID] = Field(None, description="Associated workflow ID")
    created_at: Optional[str] = Field(None, description="Creation timestamp")


