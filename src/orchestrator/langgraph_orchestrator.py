"""
LangGraph Multi-Agent Orchestrator

This module provides a LangGraph-based orchestration layer for multi-agent workflows.
It wraps existing agent implementations and provides state persistence, parallel execution,
conditional routing, and workflow visualization.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime
from pathlib import Path
import json

from langgraph.graph import StateGraph, END, START
from langgraph.types import Send
from langgraph.checkpoint.memory import MemorySaver

# Try to import AsyncSqliteSaver for persistent checkpointing (optional)
try:
    # Try newer import path first (langgraph >= 0.2.0)
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
except ImportError:
    try:
        # Fall back to older import path
        from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver
    except ImportError:
        # Use in-memory checkpointing as fallback
        # Note: This doesn't persist across restarts but enables all checkpoint features
        AsyncSqliteSaver = None
        logger = logging.getLogger(__name__)
        logger.info("Using MemorySaver for checkpointing (in-memory, not persistent)")

from ..agents import (
    BaseAgent,
    AgentRole,
    BusinessAnalystAgent,
    DeveloperAgent,
    QAEngineerAgent,
    DevOpsEngineerAgent,
    TechnicalWriterAgent,
)
from ..agents.base_agent import Task
from .langgraph_state import (
    MultiAgentState,
    BugFixState,
    InfrastructureState,
    AnalysisState,
    create_initial_state,
    create_bug_fix_state,
    create_infrastructure_state,
    create_analysis_state,
)

logger = logging.getLogger(__name__)


class LangGraphOrchestrator:
    """
    LangGraph-based orchestrator for multi-agent workflows.
    
    Features:
    - State persistence with SQLite checkpointing
    - Parallel agent execution
    - Conditional routing based on agent outputs
    - Human-in-the-loop capability
    - Workflow visualization
    - Time-travel debugging
    """
    
    def __init__(
        self,
        workspace: str,
        config: Optional[Dict[str, Any]] = None,
        checkpoint_db: Optional[str] = None
    ):
        self.workspace = workspace
        self.config = config or {}
        self.checkpoint_db = checkpoint_db or str(Path(workspace) / "checkpoints.db")
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_agents()
        
        # Compiled graphs cache
        self._compiled_graphs: Dict[str, Any] = {}
    
    def _initialize_agents(self):
        """Initialize all agent instances"""
        agent_configs = self.config.get("agents", {})
        
        # Business Analyst
        ba_config = agent_configs.get("business_analyst", {}).copy()
        self.agents["business_analyst"] = BusinessAnalystAgent(
            agent_id="ba_001",
            workspace=self.workspace,
            config=ba_config
        )
        
        # Developer
        dev_config = agent_configs.get("developer", {}).copy()
        self.agents["developer"] = DeveloperAgent(
            agent_id="dev_001",
            workspace=self.workspace,
            config=dev_config
        )
        
        # QA Engineer
        qa_config = agent_configs.get("qa_engineer", {}).copy()
        self.agents["qa_engineer"] = QAEngineerAgent(
            agent_id="qa_001",
            workspace=self.workspace,
            config=qa_config
        )
        
        # DevOps Engineer
        devops_config = agent_configs.get("devops_engineer", {}).copy()
        self.agents["devops_engineer"] = DevOpsEngineerAgent(
            agent_id="devops_001",
            workspace=self.workspace,
            config=devops_config
        )
        
        # Technical Writer
        writer_config = agent_configs.get("technical_writer", {}).copy()
        self.agents["technical_writer"] = TechnicalWriterAgent(
            agent_id="writer_001",
            workspace=self.workspace,
            config=writer_config
        )
        
        logger.info(f"Initialized {len(self.agents)} agents for LangGraph orchestration")
    
    # ==================== Agent Node Functions ====================
    
    async def business_analyst_node(self, state: MultiAgentState) -> Dict[str, Any]:
        """Business Analyst Agent Node"""
        logger.info(f"[{state['workflow_id']}] Executing Business Analyst node")
        
        try:
            agent = self.agents["business_analyst"]
            
            task = Task(
                task_id=f"ba_{datetime.now().timestamp()}",
                description="Analyze requirements and create user stories",
                context={
                    "requirement": state["requirement"],
                    "workflow_type": state["workflow_type"],
                    "task_type": "requirements_analysis",
                }
            )
            
            completed_task = await agent.run_task(task)
            
            if completed_task.error:
                return {
                    "errors": [{
                        "step": "business_analyst",
                        "error": completed_task.error,
                        "timestamp": datetime.now().isoformat()
                    }],
                    "current_step": "business_analyst",
                    "completed_steps": ["business_analyst"],
                    "status": "failed"
                }
            
            return {
                "business_analysis": [completed_task.result] if completed_task.result else [],
                "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                "current_step": "business_analyst",
                "completed_steps": ["business_analyst"],
            }
            
        except Exception as e:
            logger.error(f"Error in business_analyst_node: {e}", exc_info=True)
            return {
                "errors": [{
                    "step": "business_analyst",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }],
                "current_step": "business_analyst",
                "completed_steps": ["business_analyst"],
                "status": "failed"
            }
    
    async def developer_design_node(self, state: MultiAgentState) -> Dict[str, Any]:
        """Developer Agent - Architecture Design Node"""
        logger.info(f"[{state['workflow_id']}] Executing Developer Design node")
        
        try:
            agent = self.agents["developer"]
            
            # Get business analysis from previous step
            business_analysis = state.get("business_analysis", [])
            
            task = Task(
                task_id=f"dev_design_{datetime.now().timestamp()}",
                description="Design system architecture based on requirements",
                context={
                    "requirement": state["requirement"],
                    "workflow_type": state["workflow_type"],
                    "task_type": "architecture_design",
                    "business_analysis": business_analysis[-1] if business_analysis else {},
                }
            )
            
            completed_task = await agent.run_task(task)
            
            if completed_task.error:
                return {
                    "errors": [{
                        "step": "architecture_design",
                        "error": completed_task.error,
                        "timestamp": datetime.now().isoformat()
                    }],
                    "current_step": "architecture_design",
                    "completed_steps": ["architecture_design"],
                    "status": "failed"
                }
            
            return {
                "architecture": [completed_task.result] if completed_task.result else [],
                "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                "current_step": "architecture_design",
                "completed_steps": ["architecture_design"],
            }
            
        except Exception as e:
            logger.error(f"Error in developer_design_node: {e}", exc_info=True)
            return {
                "errors": [{
                    "step": "architecture_design",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }],
                "current_step": "architecture_design",
                "completed_steps": ["architecture_design"],
                "status": "failed"
            }
    
    async def developer_implementation_node(self, state: MultiAgentState) -> Dict[str, Any]:
        """Developer Agent - Implementation Node"""
        logger.info(f"[{state['workflow_id']}] Executing Developer Implementation node")
        
        try:
            agent = self.agents["developer"]
            
            architecture = state.get("architecture", [])
            
            task = Task(
                task_id=f"dev_impl_{datetime.now().timestamp()}",
                description="Implement the feature based on architecture design",
                context={
                    "requirement": state["requirement"],
                    "workflow_type": state["workflow_type"],
                    "task_type": "implementation",
                    "architecture": architecture[-1] if architecture else {},
                }
            )
            
            completed_task = await agent.run_task(task)
            
            if completed_task.error:
                return {
                    "errors": [{
                        "step": "implementation",
                        "error": completed_task.error,
                        "timestamp": datetime.now().isoformat()
                    }],
                    "current_step": "implementation",
                    "completed_steps": ["implementation"],
                    "status": "failed"
                }
            
            return {
                "implementation": [completed_task.result] if completed_task.result else [],
                "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                "current_step": "implementation",
                "completed_steps": ["implementation"],
            }
            
        except Exception as e:
            logger.error(f"Error in developer_implementation_node: {e}", exc_info=True)
            return {
                "errors": [{
                    "step": "implementation",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }],
                "current_step": "implementation",
                "completed_steps": ["implementation"],
                "status": "failed"
            }
    
    async def qa_engineer_node(self, state: MultiAgentState) -> Dict[str, Any]:
        """QA Engineer Agent Node"""
        logger.info(f"[{state['workflow_id']}] Executing QA Engineer node")
        
        try:
            agent = self.agents["qa_engineer"]
            
            implementation = state.get("implementation", [])
            
            task = Task(
                task_id=f"qa_{datetime.now().timestamp()}",
                description="Create comprehensive test suite",
                context={
                    "requirement": state["requirement"],
                    "workflow_type": state["workflow_type"],
                    "task_type": "testing",
                    "implementation": implementation[-1] if implementation else {},
                }
            )
            
            completed_task = await agent.run_task(task)
            
            if completed_task.error:
                return {
                    "errors": [{
                        "step": "qa_testing",
                        "error": completed_task.error,
                        "timestamp": datetime.now().isoformat()
                    }],
                    "completed_steps": ["qa_testing"],
                }
            
            return {
                "tests": [completed_task.result] if completed_task.result else [],
                "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                "completed_steps": ["qa_testing"],
            }
            
        except Exception as e:
            logger.error(f"Error in qa_engineer_node: {e}", exc_info=True)
            return {
                "errors": [{
                    "step": "qa_testing",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }],
                "completed_steps": ["qa_testing"],
            }
    
    async def devops_engineer_node(self, state: MultiAgentState) -> Dict[str, Any]:
        """DevOps Engineer Agent Node"""
        logger.info(f"[{state['workflow_id']}] Executing DevOps Engineer node")
        
        try:
            agent = self.agents["devops_engineer"]
            
            implementation = state.get("implementation", [])
            
            task = Task(
                task_id=f"devops_{datetime.now().timestamp()}",
                description="Set up deployment infrastructure",
                context={
                    "requirement": state["requirement"],
                    "workflow_type": state["workflow_type"],
                    "task_type": "deployment",
                    "implementation": implementation[-1] if implementation else {},
                }
            )
            
            completed_task = await agent.run_task(task)
            
            if completed_task.error:
                return {
                    "errors": [{
                        "step": "infrastructure",
                        "error": completed_task.error,
                        "timestamp": datetime.now().isoformat()
                    }],
                    "completed_steps": ["infrastructure"],
                }
            
            return {
                "infrastructure": [completed_task.result] if completed_task.result else [],
                "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                "completed_steps": ["infrastructure"],
            }
            
        except Exception as e:
            logger.error(f"Error in devops_engineer_node: {e}", exc_info=True)
            return {
                "errors": [{
                    "step": "infrastructure",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }],
                "completed_steps": ["infrastructure"],
            }
    
    async def technical_writer_node(self, state: MultiAgentState) -> Dict[str, Any]:
        """Technical Writer Agent Node"""
        logger.info(f"[{state['workflow_id']}] Executing Technical Writer node")
        
        try:
            agent = self.agents["technical_writer"]
            
            implementation = state.get("implementation", [])
            tests = state.get("tests", [])
            infrastructure = state.get("infrastructure", [])
            
            task = Task(
                task_id=f"writer_{datetime.now().timestamp()}",
                description="Create comprehensive documentation",
                context={
                    "requirement": state["requirement"],
                    "workflow_type": state["workflow_type"],
                    "task_type": "documentation",
                    "implementation": implementation[-1] if implementation else {},
                    "tests": tests[-1] if tests else {},
                    "infrastructure": infrastructure[-1] if infrastructure else {},
                }
            )
            
            completed_task = await agent.run_task(task)
            
            if completed_task.error:
                return {
                    "errors": [{
                        "step": "documentation",
                        "error": completed_task.error,
                        "timestamp": datetime.now().isoformat()
                    }],
                    "current_step": "documentation",
                    "completed_steps": ["documentation"],
                    "status": "completed"
                }
            
            return {
                "documentation": [completed_task.result] if completed_task.result else [],
                "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                "current_step": "documentation",
                "completed_steps": ["documentation"],
                "status": "completed",
                "completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in technical_writer_node: {e}", exc_info=True)
            return {
                "errors": [{
                    "step": "documentation",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }],
                "current_step": "documentation",
                "completed_steps": ["documentation"],
                "status": "completed",
                "completed_at": datetime.now().isoformat()
            }
    
    # ==================== Conditional Routing ====================
    
    def should_continue_after_implementation(
        self, state: MultiAgentState
    ) -> List[Send] | Literal[END]:
        """
        Conditional routing after implementation.
        Decides whether to proceed with parallel QA/DevOps or stop on failure.
        Returns Send objects for parallel execution or END to stop.
        """
        errors = state.get("errors", [])
        
        # Check if implementation step had errors
        impl_errors = [e for e in errors if e.get("step") == "implementation"]
        
        if impl_errors:
            logger.warning(f"Implementation failed, stopping workflow")
            return END
        
        # Check implementation status
        implementation = state.get("implementation", [])
        if implementation:
            impl_status = implementation[-1].get("status")
            if impl_status == "failed":
                logger.warning(f"Implementation marked as failed")
                return END
        
        logger.info(f"Implementation successful, proceeding with parallel QA/DevOps")
        # Return Send objects for parallel execution
        return [
            Send("qa_testing", state),
            Send("infrastructure", state)
        ]
    
    def route_after_parallel(
        self, state: MultiAgentState
    ) -> Literal["documentation", "failed"]:
        """
        Route after parallel QA and DevOps execution.
        Proceeds to documentation if both completed successfully.
        """
        errors = state.get("errors", [])
        completed_steps = state.get("completed_steps", [])
        
        # Check if both QA and DevOps completed
        has_qa = "qa_testing" in completed_steps
        has_devops = "infrastructure" in completed_steps
        
        if not (has_qa and has_devops):
            logger.warning(f"Not all parallel tasks completed")
            return "failed"
        
        # Check for critical errors
        critical_errors = [e for e in errors if e.get("step") in ["qa_testing", "infrastructure"]]
        
        if critical_errors:
            logger.warning(f"Critical errors in parallel execution")
            return "failed"
        
        logger.info(f"Parallel execution successful, proceeding to documentation")
        return "documentation"
    
    # ==================== Workflow Graph Builders ====================
    
    async def build_feature_development_graph(self) -> Any:
        """
        Build the Feature Development workflow graph with parallel execution.
        
        Workflow:
        1. Business Analyst → Requirements Analysis
        2. Developer → Architecture Design
        3. Developer → Implementation
        4. [PARALLEL] QA Engineer → Testing + DevOps Engineer → Infrastructure
        5. Technical Writer → Documentation
        """
        # Create checkpointer (use MemorySaver if AsyncSqliteSaver not available)
        if AsyncSqliteSaver is None:
            checkpointer = MemorySaver()
            logger.info("Using MemorySaver for checkpointing (in-memory, not persisted across restarts)")
        else:
            checkpointer = await AsyncSqliteSaver.from_conn_string(self.checkpoint_db).__aenter__()
        
        try:
            # Create graph
            workflow = StateGraph(MultiAgentState)
            
            # Add nodes
            workflow.add_node("business_analyst", self.business_analyst_node)
            workflow.add_node("architecture_design", self.developer_design_node)
            workflow.add_node("implementation", self.developer_implementation_node)
            workflow.add_node("qa_testing", self.qa_engineer_node)
            workflow.add_node("infrastructure", self.devops_engineer_node)
            workflow.add_node("documentation", self.technical_writer_node)
            
            # Define edges
            workflow.set_entry_point("business_analyst")
            workflow.add_edge("business_analyst", "architecture_design")
            workflow.add_edge("architecture_design", "implementation")
            
            # Conditional routing after implementation with parallel execution
            # The routing function returns Send objects for parallel execution
            workflow.add_conditional_edges(
                "implementation",
                self.should_continue_after_implementation
            )
            
            # Both QA and Infrastructure must complete before documentation
            workflow.add_edge("qa_testing", "documentation")
            workflow.add_edge("infrastructure", "documentation")
            workflow.add_edge("documentation", END)
            
            # Compile with checkpointing
            return workflow.compile(checkpointer=checkpointer)
        finally:
            # Clean up checkpointer if it was created
            if checkpointer is not None and AsyncSqliteSaver is not None:
                try:
                    await checkpointer.__aexit__(None, None, None)
                except:
                    pass
    
    async def build_bug_fix_graph(self) -> Any:
        """Build Bug Fix workflow graph"""
        if AsyncSqliteSaver is None:
            checkpointer = MemorySaver()
            logger.info("Using MemorySaver for checkpointing (in-memory, not persisted across restarts)")
        else:
            checkpointer = await AsyncSqliteSaver.from_conn_string(self.checkpoint_db).__aenter__()
        
        try:
            workflow = StateGraph(BugFixState)
            
            # For bug fix, we'll need simpler node implementations
            # Using the same agents but different task types
            
            async def bug_analysis_node(state: BugFixState) -> Dict[str, Any]:
                agent = self.agents["qa_engineer"]
                task = Task(
                    task_id=f"bug_analysis_{datetime.now().timestamp()}",
                    description="Analyze and reproduce the bug",
                    context={
                        "requirement": state["requirement"],
                        "bug_description": state["bug_description"],
                        "task_type": "bug_analysis",
                    }
                )
                completed_task = await agent.run_task(task)
                return {
                    "bug_analysis": completed_task.result or {},
                    "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                    "current_step": "bug_analysis",
                    "completed_steps": ["bug_analysis"],
                }
            
            async def bug_fix_node(state: BugFixState) -> Dict[str, Any]:
                agent = self.agents["developer"]
                task = Task(
                    task_id=f"bug_fix_{datetime.now().timestamp()}",
                    description="Fix the bug",
                    context={
                        "requirement": state["requirement"],
                        "bug_analysis": state.get("bug_analysis", {}),
                        "task_type": "bug_fix",
                    }
                )
                completed_task = await agent.run_task(task)
                return {
                    "bug_fix": completed_task.result or {},
                    "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                    "current_step": "bug_fix",
                    "completed_steps": ["bug_fix"],
                }
            
            async def regression_testing_node(state: BugFixState) -> Dict[str, Any]:
                agent = self.agents["qa_engineer"]
                task = Task(
                    task_id=f"regression_{datetime.now().timestamp()}",
                    description="Run regression tests",
                    context={
                        "requirement": state["requirement"],
                        "bug_fix": state.get("bug_fix", {}),
                        "task_type": "regression_testing",
                    }
                )
                completed_task = await agent.run_task(task)
                return {
                    "regression_tests": completed_task.result or {},
                    "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                    "current_step": "regression_testing",
                    "completed_steps": ["regression_testing"],
                }
            
            async def release_notes_node(state: BugFixState) -> Dict[str, Any]:
                agent = self.agents["technical_writer"]
                task = Task(
                    task_id=f"release_notes_{datetime.now().timestamp()}",
                    description="Update release notes",
                    context={
                        "requirement": state["requirement"],
                        "bug_fix": state.get("bug_fix", {}),
                        "task_type": "release_notes",
                    }
                )
                completed_task = await agent.run_task(task)
                return {
                    "release_notes": completed_task.result or {},
                    "files_created": completed_task.result.get("files_created", []) if completed_task.result else [],
                    "current_step": "release_notes",
                    "completed_steps": ["release_notes"],
                    "status": "completed"
                }
            
            workflow.add_node("bug_analysis", bug_analysis_node)
            workflow.add_node("bug_fix", bug_fix_node)
            workflow.add_node("regression_testing", regression_testing_node)
            workflow.add_node("release_notes", release_notes_node)
            
            workflow.set_entry_point("bug_analysis")
            workflow.add_edge("bug_analysis", "bug_fix")
            workflow.add_edge("bug_fix", "regression_testing")
            workflow.add_edge("regression_testing", "release_notes")
            workflow.add_edge("release_notes", END)
            
            return workflow.compile(checkpointer=checkpointer)
        finally:
            if checkpointer is not None and AsyncSqliteSaver is not None:
                try:
                    await checkpointer.__aexit__(None, None, None)
                except:
                    pass
    
    # ==================== Execution Methods ====================
    
    async def execute_feature_development(
        self,
        requirement: str,
        context: Optional[Dict[str, Any]] = None,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute feature development workflow with LangGraph.
        
        Args:
            requirement: User requirement description
            context: Optional additional context
            thread_id: Optional thread ID for resuming workflows
        
        Returns:
            Final workflow state
        """
        # Create initial state
        initial_state = create_initial_state(
            requirement=requirement,
            workflow_type="feature_development",
            context=context
        )
        
        workflow_id = initial_state["workflow_id"]
        logger.info(f"Starting feature development workflow: {workflow_id}")
        
        # Build graph
        app = await self.build_feature_development_graph()
        
        # Configure execution
        config = {
            "configurable": {
                "thread_id": thread_id or workflow_id
            }
        }
        
        try:
            # Execute workflow with streaming for progress updates
            final_state = None
            async for event in app.astream(initial_state, config):
                # Log progress
                for node_name, node_state in event.items():
                    logger.info(f"[{workflow_id}] Completed node: {node_name}")
                    if "current_step" in node_state:
                        logger.info(f"[{workflow_id}] Current step: {node_state['current_step']}")
                final_state = event
            
            # Save results
            await self._save_workflow_results(workflow_id, final_state)
            
            return final_state
            
        except Exception as e:
            logger.error(f"Error executing workflow {workflow_id}: {e}", exc_info=True)
            raise
    
    async def execute_bug_fix(
        self,
        requirement: str,
        bug_description: str,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute bug fix workflow"""
        initial_state = create_bug_fix_state(
            requirement=requirement,
            bug_description=bug_description
        )
        
        workflow_id = initial_state["workflow_id"]
        logger.info(f"Starting bug fix workflow: {workflow_id}")
        
        app = await self.build_bug_fix_graph()
        
        config = {
            "configurable": {
                "thread_id": thread_id or workflow_id
            }
        }
        
        try:
            final_state = None
            async for event in app.astream(initial_state, config):
                logger.info(f"[{workflow_id}] Progress: {event}")
                final_state = event
            
            await self._save_workflow_results(workflow_id, final_state)
            return final_state
            
        except Exception as e:
            logger.error(f"Error executing bug fix workflow {workflow_id}: {e}", exc_info=True)
            raise
    
    async def _save_workflow_results(
        self,
        workflow_id: str,
        final_state: Dict[str, Any]
    ):
        """Save workflow results to JSON file"""
        output_dir = Path(self.workspace) / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get the last state from the event stream
        # The final_state is a dict with node_name: state
        actual_state = list(final_state.values())[0] if final_state else {}
        
        result = {
            "workflow_id": workflow_id,
            "workflow_type": actual_state.get("workflow_type", "unknown"),
            "status": actual_state.get("status", "completed"),
            "requirement": actual_state.get("requirement", ""),
            "completed_steps": actual_state.get("completed_steps", []),
            "files_created": actual_state.get("files_created", []),
            "errors": actual_state.get("errors", []),
            "started_at": actual_state.get("started_at", ""),
            "completed_at": actual_state.get("completed_at", datetime.now().isoformat()),
        }
        
        filename = f"langgraph_{workflow_id}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        logger.info(f"Saved workflow results to: {filepath}")
