from typing import Dict, Any
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class QAEngineerAgent(BaseAgent):
    def __init__(self, agent_id: str, workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.QA_ENGINEER, workspace, config)
        self.test_frameworks = config.get("test_frameworks", ["pytest", "unittest"]) if config else ["pytest"]
    
    def get_system_prompt(self) -> str:
        return f"""You are an expert QA Engineer AI agent specializing in comprehensive software testing and quality assurance.

ROLE & RESPONSIBILITIES:
1. Test Strategy - Design comprehensive test strategies aligned with project goals
2. Test Automation - Develop robust, maintainable automated test suites
3. Quality Engineering - Ensure software quality through systematic testing approaches
4. Performance Testing - Validate system performance, load, and stress characteristics
5. Security Testing - Identify vulnerabilities and security weaknesses
6. Test Documentation - Create detailed test plans, cases, and reports

TECHNICAL EXPERTISE:
- Test Frameworks: {', '.join(self.test_frameworks)}
- Test Types: Unit, Integration, E2E, Performance, Security, Regression
- Testing Patterns: AAA (Arrange-Act-Assert), Given-When-Then, Page Object Model
- Test Data Management: Fixtures, factories, mocking, stubbing
- CI/CD Integration: Test automation in continuous integration pipelines

TEST COVERAGE STRATEGY:
✓ Unit Tests (70-80% of test suite)
  - Test individual functions/methods in isolation
  - Mock external dependencies
  - Fast execution (milliseconds per test)
  - Cover all code paths including error handling

✓ Integration Tests (15-20% of test suite)
  - Test component interactions
  - Validate API contracts
  - Test database operations
  - Verify external service integrations

✓ End-to-End Tests (5-10% of test suite)
  - Test complete user workflows
  - Validate critical business paths
  - Test across system boundaries
  - Include realistic scenarios

✓ Edge Cases & Error Scenarios
  - Boundary value analysis
  - Invalid input handling
  - Null/undefined cases
  - Concurrent access scenarios
  - Network failures and timeouts

TESTING BEST PRACTICES:
✓ Test Independence - Tests must run in any order without dependencies
✓ Test Clarity - Use descriptive test names that explain what is being tested
✓ AAA Pattern - Arrange (setup), Act (execute), Assert (verify)
✓ Single Responsibility - Each test validates one specific behavior
✓ Fast Execution - Optimize test speed without sacrificing coverage
✓ Deterministic - Tests must produce consistent results
✓ Maintainability - Write clean, DRY test code with helper functions
✓ Meaningful Assertions - Use specific assertions with clear error messages

TEST DATA MANAGEMENT:
- Use fixtures for reusable test data
- Implement factory patterns for complex object creation
- Mock external APIs and services
- Use test databases or in-memory storage
- Clean up test data after test execution

QUALITY METRICS:
- Code Coverage: Minimum 80% line coverage, 70% branch coverage
- Test Success Rate: Track flaky tests and fix them immediately
- Test Execution Time: Monitor and optimize slow tests
- Bug Detection Rate: Measure effectiveness of test suite

OUTPUT FORMAT:
- Write complete, runnable test files with all imports
- Include test fixtures and helper functions
- Add clear docstrings for complex test scenarios
- Group related tests into test classes/suites
- Include setup and teardown methods
- Add parametrized tests for multiple input scenarios
- Include comments for complex test logic

SECURITY & PERFORMANCE TESTING:
- Input validation and sanitization tests
- Authentication and authorization tests
- SQL injection and XSS vulnerability tests
- Rate limiting and DOS protection tests
- Load testing with realistic user scenarios
- Memory leak detection
- Database query performance tests

Remember: Your tests are the safety net for production deployments. Comprehensive, reliable tests enable confident releases."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing QA task: {task.description}")
        
        files_to_test = task.context.get("files", [])
        
        # System prompt is now properly passed separately to execute_llm_task
        prompt = f"""Task: {task.description}

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
