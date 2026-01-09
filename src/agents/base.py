"""
Base agent class for all specialized agents.

All agents inherit from this base class and implement their specific logic.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from src.models.workflow import AgentOutput, WorkflowState
from src.utils.llm_client import LLMClient, create_llm_client


class BaseAgent(ABC):
    """
    Base class for all agents in the multi-agent system.

    Provides common functionality:
    - LLM integration
    - System prompt management
    - Tool registry
    - Memory/context access
    - Error handling
    """

    def __init__(
        self,
        agent_name: str,
        system_prompt: str,
        llm_provider: str = "openai",
        llm_model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize base agent.

        Args:
            agent_name: Unique name for this agent
            system_prompt: System prompt defining agent's role
            llm_provider: LLM provider ("openai" or "anthropic")
            llm_model: Specific model to use (optional)
            temperature: LLM temperature setting
            max_tokens: Maximum tokens for responses
        """
        self.agent_id = str(uuid4())
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        self.tools: List[Dict[str, Any]] = []
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Initialize LLM client
        self.llm_client: LLMClient = create_llm_client(
            provider=llm_provider,
            model=llm_model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def register_tool(self, tool: Dict[str, Any]) -> None:
        """
        Register a tool for the agent to use.

        Args:
            tool: Tool definition with name, description, and function
        """
        self.tools.append(tool)

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Get all registered tools.

        Returns:
            List of tool definitions
        """
        return self.tools

    async def execute(
        self,
        task: str,
        workflow_state: WorkflowState,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentOutput:
        """
        Execute agent task.

        This is the main entry point for agent execution.
        Subclasses should override _process_task for specific logic.

        Args:
            task: Task description or input
            workflow_state: Current workflow state
            context: Additional context (optional)

        Returns:
            AgentOutput with results
        """
        try:
            # Build prompt with context
            prompt = self._build_prompt(task, workflow_state, context)

            # Process task (can be overridden by subclasses)
            result = await self._process_task(prompt, workflow_state, context)

            # Create agent output
            output = AgentOutput(
                agent_name=self.agent_name,
                output_type=self._get_output_type(),
                content=result,
                workflow_id=workflow_state.workflow_id,
            )

            return output

        except Exception as e:
            # Error handling
            error_output = AgentOutput(
                agent_name=self.agent_name,
                output_type="error",
                content={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "task": task,
                },
                workflow_id=workflow_state.workflow_id,
            )
            return error_output

    @abstractmethod
    async def _process_task(
        self,
        prompt: str,
        workflow_state: WorkflowState,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process the task (to be implemented by subclasses).

        Args:
            prompt: Formatted prompt with context
            workflow_state: Current workflow state
            context: Additional context

        Returns:
            Dictionary with task results
        """
        pass

    @abstractmethod
    def _get_output_type(self) -> str:
        """
        Get the output type for this agent.

        Returns:
            Output type string (e.g., "analysis", "code", "tests")
        """
        pass

    def _build_prompt(
        self,
        task: str,
        workflow_state: WorkflowState,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Build the full prompt with context.

        Args:
            task: Original task
            workflow_state: Workflow state with shared context
            context: Additional context

        Returns:
            Formatted prompt string
        """
        prompt_parts = [f"Task: {task}"]

        # Add shared context
        if workflow_state.shared_context:
            prompt_parts.append("\nShared Context:")
            for key, value in workflow_state.shared_context.items():
                prompt_parts.append(f"  - {key}: {value}")

        # Add agent outputs from previous agents
        if workflow_state.agent_outputs:
            prompt_parts.append("\nPrevious Agent Outputs:")
            for agent_name, output in workflow_state.agent_outputs.items():
                prompt_parts.append(f"  - {agent_name}: {output}")

        # Add additional context
        if context:
            prompt_parts.append("\nAdditional Context:")
            for key, value in context.items():
                prompt_parts.append(f"  - {key}: {value}")

        return "\n".join(prompt_parts)

    async def _call_llm(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Call LLM with prompt.

        Args:
            prompt: User prompt
            temperature: Override default temperature
            max_tokens: Override default max tokens

        Returns:
            LLM response
        """
        return await self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
        )

    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get agent information.

        Returns:
            Dictionary with agent metadata
        """
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "tools": [tool.get("name") for tool in self.tools],
        }
