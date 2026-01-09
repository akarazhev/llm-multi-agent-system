"""
Workflow engine using LangGraph for agent orchestration.

Manages agent execution flow, state management, and conditional routing.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID

from langgraph.graph import StateGraph, END

from src.models.workflow import WorkflowState, WorkflowStatus
from src.agents.base import BaseAgent


class WorkflowEngine:
    """
    Workflow engine for orchestrating agent execution.

    Uses LangGraph to manage state and route between agents.
    """

    def __init__(self):
        """Initialize workflow engine."""
        self.graph: Optional[StateGraph] = None
        self.agents: Dict[str, BaseAgent] = {}
        self._build_graph()

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the workflow engine.

        Args:
            agent: Agent instance to register
        """
        self.agents[agent.agent_name] = agent
        # Rebuild graph when agents are added
        self._build_graph()

    def _build_graph(self) -> None:
        """Build the LangGraph workflow graph."""
        # Define state schema (using WorkflowState)
        # LangGraph will use this to manage state

        # Create graph
        graph = StateGraph(dict)  # Using dict for now, will use WorkflowState later

        # Add nodes for each registered agent
        for agent_name in self.agents.keys():
            graph.add_node(agent_name, self._create_agent_node(agent_name))

        # Define workflow edges
        # This is a simple linear flow for now:
        # business_analyst -> developer -> qa -> devops -> technical_writer
        if "business_analyst" in self.agents:
            graph.set_entry_point("business_analyst")

            if "developer" in self.agents:
                graph.add_edge("business_analyst", "developer")

                if "qa" in self.agents:
                    graph.add_edge("developer", "qa")

                    if "devops" in self.agents:
                        graph.add_edge("qa", "devops")

                        if "technical_writer" in self.agents:
                            graph.add_edge("devops", "technical_writer")
                            graph.add_edge("technical_writer", END)
                        else:
                            graph.add_edge("devops", END)
                    else:
                        if "technical_writer" in self.agents:
                            graph.add_edge("qa", "technical_writer")
                            graph.add_edge("technical_writer", END)
                        else:
                            graph.add_edge("qa", END)
                else:
                    if "devops" in self.agents:
                        graph.add_edge("developer", "devops")
                        if "technical_writer" in self.agents:
                            graph.add_edge("devops", "technical_writer")
                            graph.add_edge("technical_writer", END)
                        else:
                            graph.add_edge("devops", END)
                    else:
                        if "technical_writer" in self.agents:
                            graph.add_edge("developer", "technical_writer")
                            graph.add_edge("technical_writer", END)
                        else:
                            graph.add_edge("developer", END)
            else:
                graph.add_edge("business_analyst", END)

        # Compile graph
        self.graph = graph.compile()

    def _create_agent_node(self, agent_name: str):
        """
        Create a node function for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Node function
        """
        agent = self.agents[agent_name]

        async def agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
            """
            Execute agent and update state.

            Args:
                state: Current workflow state

            Returns:
                Updated state
            """
            # Convert dict to WorkflowState
            workflow_state = WorkflowState(**state)

            # Execute agent
            task = workflow_state.requirements if agent_name == "business_analyst" else f"Process output from previous agents"
            output = await agent.execute(task, workflow_state)

            # Update state with agent output
            state["agent_outputs"][agent_name] = output.content
            state["current_step"] = agent_name
            state["updated_at"] = str(workflow_state.updated_at)

            return state

        return agent_node

    async def execute(self, workflow_state: WorkflowState) -> WorkflowState:
        """
        Execute the workflow.

        Args:
            workflow_state: Initial workflow state

        Returns:
            Final workflow state
        """
        if not self.graph:
            raise RuntimeError("Workflow graph not initialized")

        # Convert WorkflowState to dict for LangGraph
        initial_state = workflow_state.model_dump()

        # Execute graph
        try:
            workflow_state.status = WorkflowStatus.RUNNING
            final_state = await self.graph.ainvoke(initial_state)

            # Convert back to WorkflowState
            workflow_state = WorkflowState(**final_state)
            workflow_state.status = WorkflowStatus.COMPLETED

        except Exception as e:
            workflow_state.status = WorkflowStatus.FAILED
            workflow_state.errors.append(str(e))
            raise

        return workflow_state
