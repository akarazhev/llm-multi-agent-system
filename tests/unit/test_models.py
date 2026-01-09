"""
Unit tests for data models.
"""

import pytest
from uuid import uuid4

from src.models.workflow import WorkflowStatus, WorkflowState, AgentOutput


def test_workflow_state_creation():
    """Test creating a WorkflowState."""
    state = WorkflowState(
        request_id="test-123",
        requirements="Test requirements"
    )
    
    assert state.request_id == "test-123"
    assert state.requirements == "Test requirements"
    assert state.status == WorkflowStatus.PENDING
    assert state.current_step == "initial"
    assert state.agent_outputs == {}
    assert state.shared_context == {}


def test_workflow_state_with_data():
    """Test WorkflowState with populated data."""
    state = WorkflowState(
        request_id="test-456",
        requirements="Build a web app",
        current_step="developer_agent",
        agent_outputs={"business_analyst": {"user_stories": ["Story 1"]}},
        shared_context={"project_name": "Test Project"},
        status=WorkflowStatus.RUNNING
    )
    
    assert state.status == WorkflowStatus.RUNNING
    assert "business_analyst" in state.agent_outputs
    assert state.shared_context["project_name"] == "Test Project"


def test_agent_output_creation():
    """Test creating an AgentOutput."""
    output = AgentOutput(
        agent_name="business_analyst",
        output_type="analysis",
        content={"user_stories": ["Story 1", "Story 2"]}
    )
    
    assert output.agent_name == "business_analyst"
    assert output.output_type == "analysis"
    assert len(output.content["user_stories"]) == 2


