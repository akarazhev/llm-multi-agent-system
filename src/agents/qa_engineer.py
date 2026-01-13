from typing import Dict, Any
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class QAEngineerAgent(BaseAgent):
    def __init__(self, agent_id: str, workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.QA_ENGINEER, workspace, config)
        self.test_frameworks = config.get("test_frameworks", ["pytest", "unittest"]) if config else ["pytest"]
    
    def get_system_prompt(self) -> str:
        return f"""You are an expert QA Engineer agent. Your responsibilities include:
        
        1. Test Planning: Create comprehensive test plans and test strategies
        2. Test Case Design: Write detailed test cases covering all scenarios
        3. Automated Testing: Develop automated test scripts and frameworks
        4. Quality Assurance: Ensure code quality and adherence to standards
        5. Bug Reporting: Document bugs with clear reproduction steps
        6. Performance Testing: Test application performance and scalability
        
        Test Frameworks: {', '.join(self.test_frameworks)}
        
        When creating tests:
        - Cover happy path, edge cases, and error scenarios
        - Write clear, maintainable test code
        - Use appropriate assertions and test data
        - Include integration and end-to-end tests
        - Document test coverage and gaps
        - Follow testing best practices (AAA pattern, etc.)
        
        Provide comprehensive test suites that ensure code reliability."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing QA task: {task.description}")
        
        files_to_test = task.context.get("files", [])
        
        prompt = f"""
{self.get_system_prompt()}

Task: {task.description}

Context:
{self._format_context(task.context)}

Code to Test:
{task.context.get('code_description', 'See related files')}

Please create comprehensive tests including:
1. Unit tests for all functions/methods
2. Integration tests for component interactions
3. Edge case and error scenario tests
4. Test data fixtures
5. Test documentation
6. Coverage analysis recommendations

IMPORTANT: Format your test code using markdown code blocks with filenames:
```python:tests/test_feature.py
# Your test code here
```

Or specify files explicitly:
File: tests/test_feature.py
# Your test code here
"""
        
        result = await self.execute_llm_task(
            prompt,
            files=files_to_test if files_to_test else None
        )
        
        if result.get("success"):
            test_text = result.get("stdout", "")
            
            # Write test files from the LLM response
            created_files = []
            try:
                created_files = self.file_writer.write_code_blocks(
                    test_text,
                    task.task_id,
                    self.role.value
                )
                
                logger.info(f"[{self.agent_id}] Created {len(created_files)} test files")
            except Exception as e:
                logger.warning(f"[{self.agent_id}] Failed to write test files: {e}")
            
            return {
                "status": "completed",
                "test_suite": test_text,
                "files_created": created_files,
                "files_tested": files_to_test,
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
