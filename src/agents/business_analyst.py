from typing import Dict, Any
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class BusinessAnalystAgent(BaseAgent):
    def __init__(self, agent_id: str, cursor_workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.BUSINESS_ANALYST, cursor_workspace, config)
    
    def get_system_prompt(self) -> str:
        return """You are an expert Business Analyst agent. Your responsibilities include:
        
        1. Requirements Analysis: Gather, analyze, and document business requirements
        2. User Story Creation: Write clear, actionable user stories with acceptance criteria
        3. Stakeholder Communication: Translate technical concepts to business language
        4. Process Documentation: Document business processes and workflows
        5. Jira Management: Create and organize Jira tickets with proper structure
        6. Gap Analysis: Identify gaps between current state and desired outcomes
        
        When analyzing requirements:
        - Ask clarifying questions to understand the business context
        - Break down complex requirements into manageable user stories
        - Define clear acceptance criteria for each requirement
        - Identify dependencies and potential risks
        - Prioritize requirements based on business value
        
        Output your analysis in a structured format with clear sections."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing BA task: {task.description}")
        
        prompt = f"""
{self.get_system_prompt()}

Task: {task.description}

Context:
{self._format_context(task.context)}

Please analyze this requirement and provide:
1. Detailed requirements breakdown
2. User stories with acceptance criteria
3. Business value assessment
4. Dependencies and risks
5. Jira ticket structure recommendations
"""
        
        result = await self.execute_cursor_command(prompt)
        
        if result.get("success"):
            return {
                "status": "completed",
                "analysis": result.get("stdout"),
                "agent_role": self.role.value
            }
        else:
            raise Exception(f"Cursor command failed: {result.get('error', result.get('stderr'))}")
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        lines = []
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)
