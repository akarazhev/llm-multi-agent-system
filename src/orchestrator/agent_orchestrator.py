import asyncio
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from ..agents import (
    BaseAgent,
    AgentRole,
    BusinessAnalystAgent,
    DeveloperAgent,
    QAEngineerAgent,
    DevOpsEngineerAgent,
    TechnicalWriterAgent
)
from ..agents.base_agent import Task, AgentMessage
from ..utils import FileWriter

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    def __init__(self, cursor_workspace: str, config: Optional[Dict[str, Any]] = None):
        self.cursor_workspace = cursor_workspace
        self.config = config or {}
        self.agents: Dict[str, BaseAgent] = {}
        self.task_results: Dict[str, Task] = {}
        self.message_bus: asyncio.Queue = asyncio.Queue()
        self.file_writer = FileWriter(cursor_workspace)
        self._initialize_agents()
    
    def _initialize_agents(self):
        agent_configs = self.config.get("agents", {})
        
        ba_config = agent_configs.get("business_analyst", {}).copy()
        self.agents["ba_001"] = BusinessAnalystAgent(
            agent_id="ba_001",
            cursor_workspace=self.cursor_workspace,
            config=ba_config
        )
        
        dev_config = agent_configs.get("developer", {}).copy()
        self.agents["dev_001"] = DeveloperAgent(
            agent_id="dev_001",
            cursor_workspace=self.cursor_workspace,
            config=dev_config
        )
        
        qa_config = agent_configs.get("qa_engineer", {}).copy()
        self.agents["qa_001"] = QAEngineerAgent(
            agent_id="qa_001",
            cursor_workspace=self.cursor_workspace,
            config=qa_config
        )
        
        devops_config = agent_configs.get("devops_engineer", {}).copy()
        self.agents["devops_001"] = DevOpsEngineerAgent(
            agent_id="devops_001",
            cursor_workspace=self.cursor_workspace,
            config=devops_config
        )
        
        writer_config = agent_configs.get("technical_writer", {}).copy()
        self.agents["writer_001"] = TechnicalWriterAgent(
            agent_id="writer_001",
            cursor_workspace=self.cursor_workspace,
            config=writer_config
        )
        
        logger.info(f"Initialized {len(self.agents)} agents")
    
    def get_agent_by_role(self, role: AgentRole) -> Optional[BaseAgent]:
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        return None
    
    def get_agent_by_id(self, agent_id: str) -> Optional[BaseAgent]:
        return self.agents.get(agent_id)
    
    async def execute_task(self, task: Task, agent_id: str) -> Task:
        agent = self.get_agent_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        logger.info(f"Assigning task {task.task_id} to agent {agent_id}")
        completed_task = await agent.run_task(task)
        self.task_results[task.task_id] = completed_task
        
        return completed_task
    
    async def execute_workflow(self, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = {}
        task_map = {}
        workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        for step in workflow:
            task_id = step["task_id"]
            agent_role = AgentRole(step["agent_role"])
            description = step["description"]
            context = step.get("context", {})
            dependencies = step.get("dependencies", [])
            
            for dep_id in dependencies:
                if dep_id not in task_map:
                    raise ValueError(f"Dependency {dep_id} not found for task {task_id}")
                if dep_id not in results:
                    raise ValueError(f"Dependency {dep_id} not completed for task {task_id}")
            
            task = Task(
                task_id=task_id,
                description=description,
                context=context,
                dependencies=dependencies
            )
            
            agent = self.get_agent_by_role(agent_role)
            if not agent:
                raise ValueError(f"No agent found for role {agent_role}")
            
            task_map[task_id] = task
            completed_task = await self.execute_task(task, agent.agent_id)
            results[task_id] = completed_task
            
            logger.info(f"Completed workflow step: {task_id}")
        
        workflow_result = {
            "workflow_completed": True,
            "workflow_id": workflow_id,
            "total_tasks": len(workflow),
            "results": results,
            "completed_at": datetime.now().isoformat()
        }
        
        # Save workflow results to JSON file
        try:
            self._save_workflow_results(workflow_id, workflow_result, workflow)
        except Exception as e:
            logger.error(f"Failed to save workflow results: {e}")
        
        return workflow_result
    
    def _save_workflow_results(
        self, 
        workflow_id: str, 
        workflow_result: Dict[str, Any],
        workflow: List[Dict[str, Any]]
    ):
        """Save workflow results to JSON file in output directory"""
        output_dir = Path(self.cursor_workspace) / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Prepare serializable data
        serializable_result = {
            "workflow_id": workflow_id,
            "workflow_completed": workflow_result["workflow_completed"],
            "total_tasks": workflow_result["total_tasks"],
            "completed_at": workflow_result["completed_at"],
            "workflow_definition": workflow,
            "tasks": {}
        }
        
        # Convert task results to serializable format
        for task_id, task in workflow_result["results"].items():
            task_data = {
                "task_id": task.task_id,
                "description": task.description,
                "context": task.context,
                "dependencies": task.dependencies,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "error": task.error,
                "result": {}
            }
            
            # Extract key information from result
            if task.result:
                task_data["result"] = {
                    "status": task.result.get("status"),
                    "agent_role": task.result.get("agent_role"),
                    "files_created": task.result.get("files_created", []),
                    "files_modified": task.result.get("files_modified", []),
                }
                
                # Add role-specific result summaries (not full text to keep file size manageable)
                if "implementation" in task.result:
                    task_data["result"]["implementation_length"] = len(task.result["implementation"])
                if "test_suite" in task.result:
                    task_data["result"]["test_suite_length"] = len(task.result["test_suite"])
                if "infrastructure" in task.result:
                    task_data["result"]["infrastructure_length"] = len(task.result["infrastructure"])
                if "documentation" in task.result:
                    task_data["result"]["documentation_length"] = len(task.result["documentation"])
                if "analysis" in task.result:
                    task_data["result"]["analysis_length"] = len(task.result["analysis"])
            
            serializable_result["tasks"][task_id] = task_data
        
        # Determine workflow type from context
        workflow_type = "unknown"
        if workflow and len(workflow) > 0:
            workflow_type = workflow[0].get("context", {}).get("workflow_type", "custom")
        
        # Save to file
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%f')
        filename = f"workflow_{workflow_type}_{timestamp}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_result, f, indent=2, default=str)
        
        logger.info(f"Saved workflow results to: {filepath}")
        
        # Also create a summary file with all created files
        self._save_workflow_summary(workflow_id, serializable_result, output_dir)
    
    def _save_workflow_summary(
        self,
        workflow_id: str,
        workflow_result: Dict[str, Any],
        output_dir: Path
    ):
        """Create a markdown summary of the workflow execution"""
        summary_lines = [
            f"# Workflow Summary: {workflow_id}",
            f"\n**Completed at:** {workflow_result['completed_at']}",
            f"\n**Total tasks:** {workflow_result['total_tasks']}",
            f"\n**Status:** {'✓ Completed' if workflow_result['workflow_completed'] else '✗ Failed'}",
            "\n---\n",
            "\n## Generated Files\n"
        ]
        
        all_files = []
        for task_id, task_data in workflow_result["tasks"].items():
            files_created = task_data.get("result", {}).get("files_created", [])
            if files_created:
                summary_lines.append(f"\n### {task_id}")
                summary_lines.append(f"**Agent:** {task_data.get('result', {}).get('agent_role', 'unknown')}")
                summary_lines.append(f"**Description:** {task_data.get('description', '')}\n")
                for file_path in files_created:
                    summary_lines.append(f"- `{file_path}`")
                    all_files.append(file_path)
                summary_lines.append("")
        
        if not all_files:
            summary_lines.append("\n*No files were generated during this workflow.*\n")
        else:
            summary_lines.append(f"\n---\n\n**Total files created:** {len(all_files)}\n")
        
        summary_lines.append("\n## Task Details\n")
        for task_id, task_data in workflow_result["tasks"].items():
            status = "✓" if not task_data.get("error") else "✗"
            summary_lines.append(f"\n### {status} {task_id}")
            summary_lines.append(f"**Description:** {task_data.get('description', '')}")
            summary_lines.append(f"**Agent:** {task_data.get('result', {}).get('agent_role', 'unknown')}")
            
            if task_data.get("dependencies"):
                summary_lines.append(f"**Dependencies:** {', '.join(task_data['dependencies'])}")
            
            if task_data.get("error"):
                summary_lines.append(f"**Error:** {task_data['error']}")
            
            summary_lines.append("")
        
        # Save summary
        summary_filename = f"workflow_summary_{workflow_id}.md"
        summary_filepath = output_dir / summary_filename
        
        with open(summary_filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary_lines))
        
        logger.info(f"Saved workflow summary to: {summary_filepath}")
    
    async def broadcast_message(self, message: AgentMessage):
        await self.message_bus.put(message)
        
        if message.to_agent:
            target_agent = self.get_agent_by_id(message.to_agent)
            if target_agent:
                await target_agent.send_message(message)
        else:
            for agent in self.agents.values():
                if agent.agent_id != message.from_agent:
                    await agent.send_message(message)
    
    def get_system_status(self) -> Dict[str, Any]:
        agent_statuses = {
            agent_id: agent.get_status()
            for agent_id, agent in self.agents.items()
        }
        
        return {
            "total_agents": len(self.agents),
            "agents": agent_statuses,
            "total_tasks_completed": len(self.task_results),
            "timestamp": datetime.now().isoformat()
        }
    
    async def process_requirement(self, requirement: str) -> Dict[str, Any]:
        logger.info(f"Processing new requirement: {requirement[:100]}...")
        
        workflow = [
            {
                "task_id": "req_analysis",
                "agent_role": "business_analyst",
                "description": "Analyze the requirement and create user stories",
                "context": {
                    "requirement": requirement,
                    "output_format": "user_stories"
                }
            },
            {
                "task_id": "architecture_design",
                "agent_role": "developer",
                "description": "Design the architecture based on requirements",
                "context": {
                    "requirement": requirement,
                    "task_type": "architecture"
                },
                "dependencies": ["req_analysis"]
            },
            {
                "task_id": "implementation",
                "agent_role": "developer",
                "description": "Implement the feature",
                "context": {
                    "requirement": requirement,
                    "task_type": "implementation"
                },
                "dependencies": ["architecture_design"]
            },
            {
                "task_id": "testing",
                "agent_role": "qa_engineer",
                "description": "Create comprehensive test suite",
                "context": {
                    "requirement": requirement,
                    "code_description": "Implementation from previous step"
                },
                "dependencies": ["implementation"]
            },
            {
                "task_id": "infrastructure",
                "agent_role": "devops_engineer",
                "description": "Set up infrastructure and deployment",
                "context": {
                    "requirement": requirement,
                    "deployment_type": "containerized"
                },
                "dependencies": ["implementation"]
            },
            {
                "task_id": "documentation",
                "agent_role": "technical_writer",
                "description": "Create comprehensive documentation",
                "context": {
                    "requirement": requirement,
                    "doc_type": "complete",
                    "audience": "developers and users"
                },
                "dependencies": ["implementation", "testing", "infrastructure"]
            }
        ]
        
        result = await self.execute_workflow(workflow)
        
        return result
