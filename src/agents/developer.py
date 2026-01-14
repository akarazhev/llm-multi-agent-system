from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class DeveloperAgent(BaseAgent):
    def __init__(self, agent_id: str, workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.DEVELOPER, workspace, config)
        self.programming_languages = config.get("languages", ["python", "javascript", "typescript"]) if config else ["python"]
    
    def get_system_prompt(self) -> str:
        return f"""You are an expert Software Developer AI agent with deep expertise in software engineering best practices.

ROLE & RESPONSIBILITIES:
1. Code Implementation - Write clean, maintainable, production-ready code
2. Architecture Design - Design scalable, robust, and fault-tolerant systems
3. Code Quality - Ensure code follows industry best practices and design patterns
4. Testing - Write comprehensive unit, integration, and end-to-end tests
5. Debugging - Identify root causes and implement robust fixes
6. Documentation - Document code with clear comments and technical specifications

TECHNICAL EXPERTISE:
- Programming Languages: {', '.join(self.programming_languages)}
- Design Patterns: SOLID, DRY, KISS, Factory, Strategy, Observer, Dependency Injection
- Testing Frameworks: pytest, unittest, jest, mocha
- Version Control: Git best practices, semantic versioning

IMPLEMENTATION STANDARDS:
✓ Write production-ready code with proper error handling
✓ Include comprehensive logging with appropriate log levels
✓ Add input validation and sanitization
✓ Implement proper exception handling with specific error types
✓ Follow language-specific style guides (PEP 8, ESLint, etc.)
✓ Add type hints/annotations for better code maintainability
✓ Include docstrings/JSDoc for all public functions and classes
✓ Consider security implications (SQL injection, XSS, CSRF protection)
✓ Optimize for performance and scalability
✓ Make code testable with dependency injection where appropriate

OUTPUT FORMAT:
- Always format code in markdown code blocks with file paths
- Include all necessary imports and dependencies
- Provide complete, runnable implementations (no pseudocode)
- Add configuration files if needed (requirements.txt, package.json, etc.)

Remember: Your code will be deployed to production. Prioritize reliability, security, and maintainability."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing Developer task: {task.description}")
        
        files_to_modify = task.context.get("files", [])
        
        # Note: System prompt is now properly passed separately to execute_llm_task
        # This ensures it's used correctly in the LLM API call as a system message
        prompt = f"""Task: {task.description}

Context:
{self._format_context(task.context)}

Requirements:
{task.context.get('requirement', task.context.get('requirements', 'No specific requirements provided'))}

Please implement this feature following best practices. Include:
1. Complete implementation with all necessary imports
2. Error handling and logging
3. Unit tests
4. Documentation comments
5. Any configuration changes needed

IMPORTANT: Format your code output using markdown code blocks with filenames:
```python:path/to/file.py
# Your code here
```

Or specify files explicitly:
File: path/to/file.py
# Your code here
"""
        
        result = await self.execute_llm_task(
            prompt,
            files=files_to_modify if files_to_modify else None
        )
        
        if result.get("success"):
            implementation_text = result.get("stdout", "")
            
            # Write files from the LLM response
            created_files = []
            try:
                # Parse and write code blocks (handles both File: format and code blocks)
                created_files = self.file_writer.write_code_blocks(
                    implementation_text,
                    task.task_id,
                    self.role.value
                )
                
                logger.info(f"[{self.agent_id}] Created {len(created_files)} files")
            except Exception as e:
                logger.warning(f"[{self.agent_id}] Failed to write files: {e}")
            
            return {
                "status": "completed",
                "implementation": implementation_text,
                "files_created": created_files,
                "files_modified": files_to_modify,
                "agent_role": self.role.value
            }
        else:
            raise Exception(f"LLM task failed: {result.get('error', result.get('stderr'))}")
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        lines = []
        for key, value in context.items():
            if key != "files":
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
