import asyncio
import logging
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

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    def __init__(self, cursor_workspace: str, config: Optional[Dict[str, Any]] = None):
        self.cursor_workspace = cursor_workspace
        self.config = config or {}
        self.agents: Dict[str, BaseAgent] = {}
        self.task_results: Dict[str, Task] = {}
        self.message_bus: asyncio.Queue = asyncio.Queue()
        self._initialize_agents()
    
    def _initialize_agents(self):
        agent_configs = self.config.get("agents", {})
        
        ba_config = agent_configs.get("business_analyst", {}).copy()
        ba_config['cursor_cli_path'] = self.config.get('cursor_cli_path', 'cursor')
        self.agents["ba_001"] = BusinessAnalystAgent(
            agent_id="ba_001",
            cursor_workspace=self.cursor_workspace,
            config=ba_config
        )
        
        dev_config = agent_configs.get("developer", {}).copy()
        dev_config['cursor_cli_path'] = self.config.get('cursor_cli_path', 'cursor')
        self.agents["dev_001"] = DeveloperAgent(
            agent_id="dev_001",
            cursor_workspace=self.cursor_workspace,
            config=dev_config
        )
        
        qa_config = agent_configs.get("qa_engineer", {}).copy()
        qa_config['cursor_cli_path'] = self.config.get('cursor_cli_path', 'cursor')
        self.agents["qa_001"] = QAEngineerAgent(
            agent_id="qa_001",
            cursor_workspace=self.cursor_workspace,
            config=qa_config
        )
        
        devops_config = agent_configs.get("devops_engineer", {}).copy()
        devops_config['cursor_cli_path'] = self.config.get('cursor_cli_path', 'cursor')
        self.agents["devops_001"] = DevOpsEngineerAgent(
            agent_id="devops_001",
            cursor_workspace=self.cursor_workspace,
            config=devops_config
        )
        
        writer_config = agent_configs.get("technical_writer", {}).copy()
        writer_config['cursor_cli_path'] = self.config.get('cursor_cli_path', 'cursor')
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
        
        return {
            "workflow_completed": True,
            "total_tasks": len(workflow),
            "results": results,
            "completed_at": datetime.now().isoformat()
        }
    
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
