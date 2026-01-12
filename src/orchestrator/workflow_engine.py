import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from ..agents.base_agent import Task, AgentRole

logger = logging.getLogger(__name__)


class WorkflowType(Enum):
    FEATURE_DEVELOPMENT = "feature_development"
    BUG_FIX = "bug_fix"
    INFRASTRUCTURE = "infrastructure"
    DOCUMENTATION = "documentation"
    ANALYSIS = "analysis"


class WorkflowEngine:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.workflow_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[WorkflowType, List[Dict[str, Any]]]:
        return {
            WorkflowType.FEATURE_DEVELOPMENT: [
                {
                    "step": 1,
                    "agent_role": "business_analyst",
                    "task_type": "requirements_analysis",
                    "description": "Analyze requirements and create user stories"
                },
                {
                    "step": 2,
                    "agent_role": "developer",
                    "task_type": "architecture_design",
                    "description": "Design system architecture",
                    "depends_on": [1]
                },
                {
                    "step": 3,
                    "agent_role": "developer",
                    "task_type": "implementation",
                    "description": "Implement the feature",
                    "depends_on": [2]
                },
                {
                    "step": 4,
                    "agent_role": "qa_engineer",
                    "task_type": "testing",
                    "description": "Create and execute test suite",
                    "depends_on": [3]
                },
                {
                    "step": 5,
                    "agent_role": "devops_engineer",
                    "task_type": "deployment",
                    "description": "Set up deployment infrastructure",
                    "depends_on": [3]
                },
                {
                    "step": 6,
                    "agent_role": "technical_writer",
                    "task_type": "documentation",
                    "description": "Create comprehensive documentation",
                    "depends_on": [3, 4, 5]
                }
            ],
            WorkflowType.BUG_FIX: [
                {
                    "step": 1,
                    "agent_role": "qa_engineer",
                    "task_type": "bug_analysis",
                    "description": "Analyze and reproduce the bug"
                },
                {
                    "step": 2,
                    "agent_role": "developer",
                    "task_type": "bug_fix",
                    "description": "Fix the bug",
                    "depends_on": [1]
                },
                {
                    "step": 3,
                    "agent_role": "qa_engineer",
                    "task_type": "regression_testing",
                    "description": "Verify fix and run regression tests",
                    "depends_on": [2]
                },
                {
                    "step": 4,
                    "agent_role": "technical_writer",
                    "task_type": "release_notes",
                    "description": "Update release notes",
                    "depends_on": [3]
                }
            ],
            WorkflowType.INFRASTRUCTURE: [
                {
                    "step": 1,
                    "agent_role": "devops_engineer",
                    "task_type": "infrastructure_design",
                    "description": "Design infrastructure architecture"
                },
                {
                    "step": 2,
                    "agent_role": "devops_engineer",
                    "task_type": "infrastructure_implementation",
                    "description": "Implement infrastructure as code",
                    "depends_on": [1]
                },
                {
                    "step": 3,
                    "agent_role": "qa_engineer",
                    "task_type": "infrastructure_testing",
                    "description": "Test infrastructure setup",
                    "depends_on": [2]
                },
                {
                    "step": 4,
                    "agent_role": "technical_writer",
                    "task_type": "infrastructure_documentation",
                    "description": "Document infrastructure setup and operations",
                    "depends_on": [2, 3]
                }
            ],
            WorkflowType.DOCUMENTATION: [
                {
                    "step": 1,
                    "agent_role": "business_analyst",
                    "task_type": "documentation_requirements",
                    "description": "Gather documentation requirements"
                },
                {
                    "step": 2,
                    "agent_role": "technical_writer",
                    "task_type": "documentation_creation",
                    "description": "Create comprehensive documentation",
                    "depends_on": [1]
                },
                {
                    "step": 3,
                    "agent_role": "developer",
                    "task_type": "technical_review",
                    "description": "Review technical accuracy",
                    "depends_on": [2]
                }
            ],
            WorkflowType.ANALYSIS: [
                {
                    "step": 1,
                    "agent_role": "business_analyst",
                    "task_type": "requirements_gathering",
                    "description": "Gather and analyze requirements"
                },
                {
                    "step": 2,
                    "agent_role": "developer",
                    "task_type": "technical_feasibility",
                    "description": "Assess technical feasibility",
                    "depends_on": [1]
                },
                {
                    "step": 3,
                    "agent_role": "devops_engineer",
                    "task_type": "infrastructure_assessment",
                    "description": "Assess infrastructure requirements",
                    "depends_on": [1]
                },
                {
                    "step": 4,
                    "agent_role": "business_analyst",
                    "task_type": "final_analysis",
                    "description": "Compile final analysis report",
                    "depends_on": [2, 3]
                }
            ]
        }
    
    def create_workflow(
        self,
        workflow_type: WorkflowType,
        requirement: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        template = self.workflow_templates.get(workflow_type)
        if not template:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        workflow = []
        step_to_task_id = {}
        
        for step_config in template:
            step_num = step_config["step"]
            task_id = f"{workflow_type.value}_{step_num}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            dependencies = []
            if "depends_on" in step_config:
                dependencies = [
                    step_to_task_id[dep_step]
                    for dep_step in step_config["depends_on"]
                ]
            
            task_context = context.copy() if context else {}
            task_context.update({
                "requirement": requirement,
                "workflow_type": workflow_type.value,
                "task_type": step_config["task_type"]
            })
            
            workflow.append({
                "task_id": task_id,
                "agent_role": step_config["agent_role"],
                "description": step_config["description"],
                "context": task_context,
                "dependencies": dependencies,
                "step": step_num
            })
            
            step_to_task_id[step_num] = task_id
        
        logger.info(f"Created workflow of type {workflow_type.value} with {len(workflow)} steps")
        return workflow
    
    async def execute_workflow(
        self,
        workflow_type: WorkflowType,
        requirement: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        workflow = self.create_workflow(workflow_type, requirement, context)
        result = await self.orchestrator.execute_workflow(workflow)
        
        return {
            "workflow_type": workflow_type.value,
            "requirement": requirement,
            "result": result
        }
    
    def get_workflow_template(self, workflow_type: WorkflowType) -> List[Dict[str, Any]]:
        return self.workflow_templates.get(workflow_type, [])
    
    def list_workflow_types(self) -> List[str]:
        return [wf_type.value for wf_type in WorkflowType]
