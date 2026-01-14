# Contributing to LLM Multi-Agent System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Project Structure](#project-structure)
5. [Development Workflow](#development-workflow)
6. [Coding Standards](#coding-standards)
7. [Testing](#testing)
8. [Documentation](#documentation)
9. [Submitting Changes](#submitting-changes)
10. [Review Process](#review-process)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for everyone. We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

- Python 3.12
- Git
- llama.cpp with llama-server
- Familiarity with async Python
- Basic understanding of LLMs

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/llm-multi-agent-system.git
cd llm-multi-agent-system

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/llm-multi-agent-system.git
```

## Development Setup

### 1. Create Development Environment

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 2. Install Development Tools

```bash
# Code formatting
pip install black isort

# Linting
pip install flake8 pylint mypy

# Testing
pip install pytest pytest-cov pytest-asyncio

# Pre-commit hooks
pip install pre-commit
pre-commit install
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env

# Ensure llama-server is running
# Ensure your local LLM server is running on port 8080
```

### 4. Verify Setup

```bash
# Run tests
pytest tests/ -v

# Check code style
black --check src/ tests/
flake8 src/ tests/

# Run type checker
mypy src/
```

## Project Structure

```
llm-multi-agent-system/
├── src/                    # Source code
│   ├── agents/            # Agent implementations
│   │   ├── base_agent.py
│   │   ├── developer.py
│   │   └── ...
│   ├── orchestrator/      # Orchestration logic
│   │   ├── agent_orchestrator.py
│   │   ├── workflow_engine.py
│   │   └── task_manager.py
│   ├── config/            # Configuration
│   │   └── settings.py
│   └── utils/             # Utilities
│       └── file_writer.py
├── tests/                 # Test suite
│   ├── test_agent.py
│   ├── test_orchestrator.py
│   └── ...
├── examples/              # Example scripts
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── main.py               # Entry point
```

### Key Components

- **BaseAgent**: Abstract base class for all agents
- **AgentOrchestrator**: Central coordinator
- **WorkflowEngine**: Workflow management
- **TaskManager**: Task queue and dependencies
- **FileWriter**: Parse and write LLM outputs

## Development Workflow

### 1. Create a Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 2. Make Changes

```bash
# Edit files
# Write tests
# Update documentation

# Check your changes
git status
git diff
```

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agent.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### 4. Format Code

```bash
# Format with black
black src/ tests/ examples/

# Sort imports
isort src/ tests/ examples/

# Check with flake8
flake8 src/ tests/

# Type check
mypy src/
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: description of changes"

# Follow commit message guidelines (see below)
```

### Commit Message Guidelines

Format:
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat: add support for custom workflow templates

Implemented WorkflowEngine.load_custom_template() to allow
users to define their own workflow templates from YAML files.

Closes #123
```

```
fix: resolve file writer duplicate handling

Fixed issue where FileWriter would create duplicate files
when LLM returned multiple code blocks with same filename.

Fixes #456
```

## Coding Standards

### Python Style Guide

Follow PEP 8 with these additions:

**Formatting:**
- Use Black for code formatting (line length: 88)
- Use isort for import sorting
- Use type hints for all functions

**Naming Conventions:**
```python
# Classes: PascalCase
class DeveloperAgent:
    pass

# Functions/methods: snake_case
def execute_workflow():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Private: leading underscore
def _internal_helper():
    pass
```

**Type Hints:**
```python
from typing import Dict, List, Optional, Any

async def execute_task(
    task: Task,
    agent_id: str,
    timeout: Optional[int] = None
) -> Dict[str, Any]:
    ...
```

**Docstrings:**
```python
def process_workflow(workflow: List[Dict]) -> Dict[str, Any]:
    """
    Process a workflow with multiple tasks.
    
    Args:
        workflow: List of workflow step dictionaries
        
    Returns:
        Dict containing workflow results and metadata
        
    Raises:
        ValueError: If workflow is invalid
        RuntimeError: If execution fails
        
    Example:
        >>> result = process_workflow(workflow)
        >>> print(result['total_tasks'])
    """
    pass
```

### Async Best Practices

```python
# Use async/await consistently
async def process_task(self, task: Task) -> Dict:
    result = await self.execute_llm_task(prompt)
    return result

# Handle errors properly
try:
    result = await agent.run_task(task)
except asyncio.TimeoutError:
    logger.error("Task timed out")
    raise
except Exception as e:
    logger.error(f"Task failed: {e}", exc_info=True)
    raise

# Use asyncio.gather for parallel operations
results = await asyncio.gather(
    agent1.run_task(task1),
    agent2.run_task(task2),
    return_exceptions=True
)
```

### Error Handling

```python
# Specific exceptions
class AgentError(Exception):
    """Base exception for agent errors"""
    pass

class TaskTimeoutError(AgentError):
    """Task execution timeout"""
    pass

# Proper logging
import logging
logger = logging.getLogger(__name__)

try:
    result = await execute_task(task)
except TaskTimeoutError as e:
    logger.error(f"Task {task.task_id} timed out: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

### Logging

```python
import logging

# Use module-level logger
logger = logging.getLogger(__name__)

# Log levels
logger.debug(f"Debug information: {details}")
logger.info(f"[{agent_id}] Task started")
logger.warning(f"Potential issue: {warning}")
logger.error(f"Error occurred: {error}", exc_info=True)

# Include context
logger.info(
    f"[{self.agent_id}] Task {task.task_id} completed in {duration}s"
)
```

## Testing

### Writing Tests

```python
import pytest
from src.agents import DeveloperAgent
from src.agents.base_agent import Task

class TestDeveloperAgent:
    """Test suite for DeveloperAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create agent fixture"""
        return DeveloperAgent(
            agent_id="test_dev",
            workspace=".",
            config={"languages": ["python"]}
        )
    
    @pytest.fixture
    def task(self):
        """Create task fixture"""
        return Task(
            task_id="test_task",
            description="Test task",
            context={"requirement": "Test"}
        )
    
    def test_agent_initialization(self, agent):
        """Test agent initializes correctly"""
        assert agent.agent_id == "test_dev"
        assert agent.role.value == "developer"
    
    @pytest.mark.asyncio
    async def test_task_execution(self, agent, task):
        """Test task execution"""
        result = await agent.run_task(task)
        assert result.completed_at is not None
        assert result.error is None
```

### Test Coverage

Aim for:
- **Unit tests**: 80%+ coverage
- **Integration tests**: Critical paths
- **Edge cases**: Error conditions, timeouts, etc.

Run coverage:
```bash
pytest tests/ --cov=src --cov-report=term --cov-report=html
```

### Test Organization

```
tests/
├── unit/                  # Unit tests
│   ├── test_agent.py
│   ├── test_orchestrator.py
│   └── test_utils.py
├── integration/           # Integration tests
│   ├── test_workflow.py
│   └── test_end_to_end.py
├── fixtures/              # Test fixtures
│   └── sample_data.py
└── conftest.py           # Pytest configuration
```

## Documentation

### Code Documentation

- Add docstrings to all public functions, classes, and methods
- Include type hints
- Provide usage examples
- Document exceptions

### README and Guides

When changing functionality:
1. Update relevant documentation in `docs/`
2. Update examples if affected
3. Update README.md if needed
4. Add entry to CHANGELOG.md

### Documentation Style

- Use Markdown for all documentation
- Include code examples
- Keep it concise and clear
- Add diagrams where helpful

## Submitting Changes

### Pre-submission Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts with main
- [ ] CHANGELOG.md updated

### Creating a Pull Request

1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out PR template

3. **PR Description:**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [x] New feature
   - [ ] Documentation update
   
   ## Changes Made
   - Added X functionality
   - Updated Y component
   - Fixed Z issue
   
   ## Testing
   - Added unit tests for X
   - Verified integration with Y
   - Manual testing performed
   
   ## Checklist
   - [x] Code follows style guidelines
   - [x] Tests pass
   - [x] Documentation updated
   
   ## Related Issues
   Closes #123
   ```

4. **Wait for review**

## Review Process

### What We Look For

**Code Quality:**
- Follows style guidelines
- Well-structured and readable
- Appropriate use of abstractions
- Proper error handling

**Testing:**
- Adequate test coverage
- Tests are meaningful
- Edge cases considered

**Documentation:**
- Code is well-documented
- Changes documented in docs/
- Examples provided if applicable

**Functionality:**
- Solves the stated problem
- Doesn't break existing functionality
- Performs efficiently

### Review Timeline

- **Initial review**: Within 3-5 days
- **Follow-up**: As needed
- **Merge**: After approval and CI passes

### Addressing Feedback

```bash
# Make requested changes
git add .
git commit -m "Address review feedback"
git push origin feature/your-feature-name
```

### After Merge

```bash
# Update your local main
git checkout main
git pull upstream main

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## Types of Contributions

### Bug Reports

- Use GitHub Issues
- Include steps to reproduce
- Provide system information
- Include relevant logs
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Feature Requests

- Describe the feature
- Explain use case
- Consider impact on existing functionality
- Be open to discussion

### Code Contributions

- Bug fixes
- New features
- Performance improvements
- Refactoring

### Documentation

- Fix typos and errors
- Improve clarity
- Add examples
- Translate (if applicable)

### Testing

- Add missing tests
- Improve test coverage
- Add integration tests

## Development Tips

### Using the Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or in config.yaml
log_level: "DEBUG"
```

### Testing with Mock LLM

```python
# For testing without llama-server
class MockLLM:
    async def generate(self, prompt):
        return "Mock response"

# Use in tests
agent.llm_client = MockLLM()
```

### Performance Profiling

```python
import cProfile
import pstats

# Profile code
profiler = cProfile.Profile()
profiler.enable()

# Your code here
result = await execute_workflow(workflow)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

## Questions?

- Check existing documentation
- Search closed issues
- Ask in GitHub Discussions
- Create an issue

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see [LICENSE](../LICENSE)).
