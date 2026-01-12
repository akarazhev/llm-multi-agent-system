from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class DeveloperAgent(BaseAgent):
    def __init__(self, agent_id: str, cursor_workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.DEVELOPER, cursor_workspace, config)
        self.programming_languages = config.get("languages", ["python", "javascript", "typescript"]) if config else ["python"]
    
    def get_system_prompt(self) -> str:
        return f"""You are an expert Software Developer agent. Your responsibilities include:
        
        1. Code Implementation: Write clean, maintainable, and efficient code
        2. Architecture Design: Design scalable and robust software architectures
        3. Code Review: Review code for quality, performance, and best practices
        4. Technical Documentation: Document code, APIs, and technical decisions
        5. Debugging: Identify and fix bugs in existing code
        6. Testing: Write unit tests and integration tests
        
        Programming Languages: {', '.join(self.programming_languages)}
        
        When implementing features:
        - Follow SOLID principles and design patterns
        - Write clean, self-documenting code
        - Include proper error handling and logging
        - Add comprehensive tests
        - Consider performance and scalability
        - Follow the project's coding standards
        
        Always provide complete, production-ready code with all necessary imports and dependencies."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing Developer task: {task.description}")
        
        files_to_modify = task.context.get("files", [])
        
        prompt = f"""
{self.get_system_prompt()}

Task: {task.description}

Context:
{self._format_context(task.context)}

Requirements:
{task.context.get('requirements', 'No specific requirements provided')}

Please implement this feature following best practices. Include:
1. Complete implementation with all necessary imports
2. Error handling and logging
3. Unit tests
4. Documentation comments
5. Any configuration changes needed
"""
        
        result = await self.execute_cursor_command(
            prompt,
            files=files_to_modify if files_to_modify else None
        )
        
        if result.get("success"):
            return {
                "status": "completed",
                "implementation": result.get("stdout"),
                "files_modified": files_to_modify,
                "agent_role": self.role.value
            }
        else:
            raise Exception(f"Cursor command failed: {result.get('error', result.get('stderr'))}")
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        lines = []
        for key, value in context.items():
            if key != "files":
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
