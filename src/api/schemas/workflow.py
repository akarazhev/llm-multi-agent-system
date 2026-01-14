from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class WorkflowType(str, Enum):
    FEATURE_DEVELOPMENT = "feature_development"
    BUG_FIX = "bug_fix"
    INFRASTRUCTURE = "infrastructure"
    DOCUMENTATION = "documentation"
    ANALYSIS = "analysis"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    REFACTORING = "refactoring"


class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowError(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    step: str
    error: str
    message: str
    stack_trace: Optional[str] = None
    timestamp: str
    severity: str


class WorkflowStep(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    step_id: str
    name: str
    description: str
    status: StepStatus
    agent_id: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration: Optional[int] = None
    output: Optional[str] = None
    logs: List[str]
    artifacts: List[str]


class WorkflowMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_duration: int
    agent_time: Dict[str, int]
    files_generated: int
    lines_of_code: int
    tests_created: int
    cost_estimate: float
    success_rate: float


class WorkflowArtifact(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    artifact_id: str
    type: str
    name: str
    path: str
    size: int
    created_at: str
    created_by: str


class Workflow(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    workflow_id: str
    name: str
    description: str
    workflow_type: WorkflowType
    requirement: str
    status: WorkflowStatus
    started_at: str
    completed_at: Optional[str] = None
    duration: Optional[int] = None
    current_step: Optional[str] = None
    completed_steps: List[str]
    total_steps: int
    progress_percentage: int
    files_created: List[str]
    errors: List[WorkflowError]
    project_id: Optional[str] = None
    assigned_agents: List[str]
    created_by: str
    tags: List[str]
    priority: WorkflowPriority
    metrics: WorkflowMetrics
    steps: List[WorkflowStep]
    artifacts: List[WorkflowArtifact]


class WorkflowCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    requirement: str
    workflow_type: WorkflowType
    project_id: Optional[str] = None
    assigned_agents: Optional[List[str]] = None
    priority: Optional[WorkflowPriority] = None
    tags: Optional[List[str]] = None
    context: Optional[Dict[str, object]] = None


class WorkflowUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[WorkflowStatus] = None
    priority: Optional[WorkflowPriority] = None
    tags: Optional[List[str]] = None
