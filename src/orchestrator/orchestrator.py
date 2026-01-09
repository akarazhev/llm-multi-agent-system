"""
Orchestrator service for managing agent workflows.

Coordinates agent execution, manages state, and handles workflow lifecycle.
"""

from typing import Dict, List, Optional
from uuid import UUID, uuid4

from src.models.workflow import WorkflowState, WorkflowStatus
from src.agents.base import BaseAgent
from src.orchestrator.workflow import WorkflowEngine


class Orchestrator:
    """
    Main orchestrator service.

    Manages agent lifecycle, workflow execution, and state persistence.
    """

    def __init__(self):
        """Initialize orchestrator."""
        self.workflow_engine = WorkflowEngine()
        self.agents: Dict[str, BaseAgent] = {}
        self.active_workflows: Dict[str, WorkflowState] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the orchestrator.

        Args:
            agent: Agent instance to register
        """
        self.agents[agent.agent_name] = agent
        self.workflow_engine.register_agent(agent)

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """
        Get a registered agent by name.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(agent_name)

    def list_agents(self) -> List[str]:
        """
        List all registered agent names.

        Returns:
            List of agent names
        """
        return list(self.agents.keys())

    async def start_workflow(
        self,
        requirements: str,
        request_id: Optional[str] = None,
    ) -> WorkflowState:
        """
        Start a new workflow.

        Args:
            requirements: Natural language requirements
            request_id: Optional request ID (generated if not provided)

        Returns:
            Initial workflow state
        """
        if not request_id:
            request_id = f"req-{uuid4().hex[:8]}"

        # Create initial workflow state
        workflow_state = WorkflowState(
            request_id=request_id,
            workflow_id=uuid4(),
            requirements=requirements,
            status=WorkflowStatus.PENDING,
        )

        # Store active workflow
        self.active_workflows[request_id] = workflow_state

        # Execute workflow
        try:
            final_state = await self.workflow_engine.execute(workflow_state)
            self.active_workflows[request_id] = final_state
            return final_state
        except Exception as e:
            workflow_state.status = WorkflowStatus.FAILED
            workflow_state.errors.append(str(e))
            self.active_workflows[request_id] = workflow_state
            raise

    def get_workflow(self, request_id: str) -> Optional[WorkflowState]:
        """
        Get workflow state by request ID.

        Args:
            request_id: Request ID

        Returns:
            Workflow state or None if not found
        """
        return self.active_workflows.get(request_id)

    def list_workflows(self) -> List[WorkflowState]:
        """
        List all active workflows.

        Returns:
            List of workflow states
        """
        return list(self.active_workflows.values())

    async def cancel_workflow(self, request_id: str) -> bool:
        """
        Cancel a running workflow.

        Args:
            request_id: Request ID

        Returns:
            True if cancelled, False if not found
        """
        workflow = self.active_workflows.get(request_id)
        if workflow:
            workflow.status = WorkflowStatus.CANCELLED
            return True
        return False
