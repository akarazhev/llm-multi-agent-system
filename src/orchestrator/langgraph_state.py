"""
LangGraph State Definitions for Multi-Agent Workflows

This module defines the state structure used by LangGraph to manage
multi-agent workflows with state persistence and conditional routing.
"""

from typing import TypedDict, Annotated, Optional, List, Dict, Any
from typing_extensions import NotRequired
import operator
from datetime import datetime


class MultiAgentState(TypedDict):
    """
    State definition for multi-agent workflows.
    
    Uses Annotated types with operator.add to automatically merge
    results from multiple agents into lists.
    """
    # Input
    requirement: str
    workflow_type: str
    workflow_id: str
    context: NotRequired[Dict[str, Any]]
    
    # Agent outputs (using operator.add for automatic list merging)
    business_analysis: NotRequired[Annotated[List[Dict[str, Any]], operator.add]]
    architecture: NotRequired[Annotated[List[Dict[str, Any]], operator.add]]
    implementation: NotRequired[Annotated[List[Dict[str, Any]], operator.add]]
    tests: NotRequired[Annotated[List[Dict[str, Any]], operator.add]]
    infrastructure: NotRequired[Annotated[List[Dict[str, Any]], operator.add]]
    documentation: NotRequired[Annotated[List[Dict[str, Any]], operator.add]]
    
    # Workflow metadata
    errors: Annotated[List[Dict[str, Any]], operator.add]
    files_created: Annotated[List[str], operator.add]
    current_step: str
    completed_steps: Annotated[List[str], operator.add]
    
    # Status tracking
    status: str  # 'running', 'completed', 'failed', 'paused'
    started_at: NotRequired[str]
    completed_at: NotRequired[str]
    
    # Human-in-the-loop
    requires_approval: NotRequired[bool]
    approved: NotRequired[bool]
    approval_notes: NotRequired[str]


class BugFixState(TypedDict):
    """State definition for bug fix workflows"""
    requirement: str
    bug_description: str
    workflow_type: str
    workflow_id: str
    
    # Agent outputs
    bug_analysis: NotRequired[Dict[str, Any]]
    bug_fix: NotRequired[Dict[str, Any]]
    regression_tests: NotRequired[Dict[str, Any]]
    release_notes: NotRequired[Dict[str, Any]]
    
    # Metadata
    errors: Annotated[List[Dict[str, Any]], operator.add]
    files_created: Annotated[List[str], operator.add]
    current_step: str
    completed_steps: Annotated[List[str], operator.add]
    status: str


class InfrastructureState(TypedDict):
    """State definition for infrastructure workflows"""
    requirement: str
    infrastructure_type: str
    workflow_type: str
    workflow_id: str
    
    # Agent outputs
    infrastructure_design: NotRequired[Dict[str, Any]]
    infrastructure_implementation: NotRequired[Dict[str, Any]]
    infrastructure_tests: NotRequired[Dict[str, Any]]
    infrastructure_docs: NotRequired[Dict[str, Any]]
    
    # Metadata
    errors: Annotated[List[Dict[str, Any]], operator.add]
    files_created: Annotated[List[str], operator.add]
    current_step: str
    completed_steps: Annotated[List[str], operator.add]
    status: str


class AnalysisState(TypedDict):
    """State definition for analysis workflows"""
    requirement: str
    analysis_type: str
    workflow_type: str
    workflow_id: str
    
    # Agent outputs
    requirements_gathering: NotRequired[Dict[str, Any]]
    technical_feasibility: NotRequired[Dict[str, Any]]
    infrastructure_assessment: NotRequired[Dict[str, Any]]
    final_analysis: NotRequired[Dict[str, Any]]
    
    # Metadata
    errors: Annotated[List[Dict[str, Any]], operator.add]
    files_created: Annotated[List[str], operator.add]
    current_step: str
    completed_steps: Annotated[List[str], operator.add]
    status: str


def create_initial_state(
    requirement: str,
    workflow_type: str,
    workflow_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> MultiAgentState:
    """
    Create initial state for a multi-agent workflow.
    
    Args:
        requirement: The user requirement/task description
        workflow_type: Type of workflow (feature_development, bug_fix, etc.)
        workflow_id: Optional workflow ID (generated if not provided)
        context: Optional additional context
    
    Returns:
        Initial state dictionary
    """
    if workflow_id is None:
        workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return {
        "requirement": requirement,
        "workflow_type": workflow_type,
        "workflow_id": workflow_id,
        "context": context or {},
        "errors": [],
        "files_created": [],
        "current_step": "start",
        "completed_steps": [],
        "status": "running",
        "started_at": datetime.now().isoformat(),
    }


def create_bug_fix_state(
    requirement: str,
    bug_description: str,
    workflow_id: Optional[str] = None
) -> BugFixState:
    """Create initial state for bug fix workflow"""
    if workflow_id is None:
        workflow_id = f"bugfix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return {
        "requirement": requirement,
        "bug_description": bug_description,
        "workflow_type": "bug_fix",
        "workflow_id": workflow_id,
        "errors": [],
        "files_created": [],
        "current_step": "start",
        "completed_steps": [],
        "status": "running",
    }


def create_infrastructure_state(
    requirement: str,
    infrastructure_type: str,
    workflow_id: Optional[str] = None
) -> InfrastructureState:
    """Create initial state for infrastructure workflow"""
    if workflow_id is None:
        workflow_id = f"infra_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return {
        "requirement": requirement,
        "infrastructure_type": infrastructure_type,
        "workflow_type": "infrastructure",
        "workflow_id": workflow_id,
        "errors": [],
        "files_created": [],
        "current_step": "start",
        "completed_steps": [],
        "status": "running",
    }


def create_analysis_state(
    requirement: str,
    analysis_type: str,
    workflow_id: Optional[str] = None
) -> AnalysisState:
    """Create initial state for analysis workflow"""
    if workflow_id is None:
        workflow_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return {
        "requirement": requirement,
        "analysis_type": analysis_type,
        "workflow_type": "analysis",
        "workflow_id": workflow_id,
        "errors": [],
        "files_created": [],
        "current_step": "start",
        "completed_steps": [],
        "status": "running",
    }
