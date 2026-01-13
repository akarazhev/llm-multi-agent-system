# API Reference

Complete API reference for programmatic usage of the LLM Multi-Agent System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Classes](#core-classes)
3. [Agent Classes](#agent-classes)
4. [Workflow Engine](#workflow-engine)
5. [Configuration](#configuration)
6. [Utilities](#utilities)
7. [Examples](#examples)

## Getting Started

### Installation

```python
# Import core components
from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType
from src.config import load_config
```

### Basic Usage

```python
import asyncio
from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType

async def main():
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(cursor_workspace=".")
    
    # Create workflow engine
    workflow_engine = WorkflowEngine(orchestrator)
    
    # Execute workflow
    result = await workflow_engine.execute_workflow(
        workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
        requirement="Create a REST API for user authentication"
    )
    
    print(f"Completed {result['result']['total_tasks']} tasks")

asyncio.run(main())
```

## Core Classes

### AgentOrchestrator

Main orchestration hub that manages agents and executes workflows.

#### Constructor

```python
AgentOrchestrator(
    cursor_workspace: str,
    config: Optional[Dict[str, Any]] = None
)
```

**Parameters:**
- `cursor_workspace` (str): Path to workspace directory
- `config` (Dict, optional): Configuration dictionary

**Returns:** AgentOrchestrator instance

**Example:**
```python
from src.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(
    cursor_workspace="/path/to/workspace",
    config={
        "log_level": "INFO",
        "cursor_timeout": 300,
        "agents": {
            "developer": {
                "languages": ["python", "javascript"]
            }
        }
    }
)
```

#### Methods

##### execute_workflow()

Execute a complete workflow.

```python
async def execute_workflow(
    workflow: List[Dict[str, Any]]
) -> Dict[str, Any]
```

**Parameters:**
- `workflow` (List[Dict]): List of workflow steps

**Returns:** Dict containing:
- `workflow_completed` (bool): Whether workflow completed successfully
- `workflow_id` (str): Unique workflow identifier
- `total_tasks` (int): Number of tasks executed
- `results` (Dict[str, Task]): Task results by task_id
- `completed_at` (str): ISO timestamp of completion

**Example:**
```python
workflow = [
    {
        "task_id": "analyze",
        "agent_role": "business_analyst",
        "description": "Analyze requirements",
        "context": {"requirement": "Create REST API"},
        "dependencies": []
    },
    {
        "task_id": "implement",
        "agent_role": "developer",
        "description": "Implement API",
        "context": {"requirement": "Create REST API"},
        "dependencies": ["analyze"]
    }
]

result = await orchestrator.execute_workflow(workflow)
```

##### execute_task()

Execute a single task.

```python
async def execute_task(
    task: Task,
    agent_id: str
) -> Task
```

**Parameters:**
- `task` (Task): Task object to execute
- `agent_id` (str): ID of agent to execute task

**Returns:** Completed Task object

**Example:**
```python
from src.agents.base_agent import Task

task = Task(
    task_id="task_001",
    description="Implement user authentication",
    context={"framework": "fastapi"}
)

completed_task = await orchestrator.execute_task(task, "dev_001")
```

##### get_agent_by_role()

Get agent by role.

```python
def get_agent_by_role(
    role: AgentRole
) -> Optional[BaseAgent]
```

**Parameters:**
- `role` (AgentRole): Role enum value

**Returns:** Agent instance or None

**Example:**
```python
from src.agents.base_agent import AgentRole

developer = orchestrator.get_agent_by_role(AgentRole.DEVELOPER)
```

##### get_agent_by_id()

Get agent by ID.

```python
def get_agent_by_id(
    agent_id: str
) -> Optional[BaseAgent]
```

**Parameters:**
- `agent_id` (str): Agent identifier

**Returns:** Agent instance or None

**Example:**
```python
agent = orchestrator.get_agent_by_id("dev_001")
```

##### get_system_status()

Get current system status.

```python
def get_system_status() -> Dict[str, Any]
```

**Returns:** Dict containing:
- `total_agents` (int): Number of agents
- `agents` (Dict): Status of each agent
- `total_tasks_completed` (int): Completed task count
- `timestamp` (str): Current timestamp

**Example:**
```python
status = orchestrator.get_system_status()
print(f"Total agents: {status['total_agents']}")
print(f"Tasks completed: {status['total_tasks_completed']}")
```

### WorkflowEngine

Manages workflow templates and execution.

#### Constructor

```python
WorkflowEngine(orchestrator: AgentOrchestrator)
```

**Parameters:**
- `orchestrator` (AgentOrchestrator): Orchestrator instance

**Example:**
```python
from src.orchestrator import WorkflowEngine

workflow_engine = WorkflowEngine(orchestrator)
```

#### Methods

##### execute_workflow()

Execute a predefined workflow.

```python
async def execute_workflow(
    workflow_type: WorkflowType,
    requirement: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `workflow_type` (WorkflowType): Type of workflow
- `requirement` (str): Requirement description
- `context` (Dict, optional): Additional context

**Returns:** Dict containing:
- `workflow_type` (str): Workflow type executed
- `requirement` (str): Original requirement
- `result` (Dict): Execution results

**Example:**
```python
from src.orchestrator.workflow_engine import WorkflowType

result = await workflow_engine.execute_workflow(
    workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
    requirement="Create user authentication API",
    context={
        "language": "python",
        "framework": "fastapi",
        "database": "postgresql"
    }
)
```

##### create_workflow()

Create a workflow from template.

```python
def create_workflow(
    workflow_type: WorkflowType,
    requirement: str,
    context: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]
```

**Parameters:**
- `workflow_type` (WorkflowType): Type of workflow
- `requirement` (str): Requirement description
- `context` (Dict, optional): Additional context

**Returns:** List of workflow step dictionaries

**Example:**
```python
workflow = workflow_engine.create_workflow(
    workflow_type=WorkflowType.BUG_FIX,
    requirement="Fix memory leak in data processor",
    context={"priority": "high"}
)
```

##### get_workflow_template()

Get workflow template definition.

```python
def get_workflow_template(
    workflow_type: WorkflowType
) -> List[Dict[str, Any]]
```

**Parameters:**
- `workflow_type` (WorkflowType): Type of workflow

**Returns:** List of template step dictionaries

**Example:**
```python
template = workflow_engine.get_workflow_template(
    WorkflowType.INFRASTRUCTURE
)
```

##### list_workflow_types()

List available workflow types.

```python
def list_workflow_types() -> List[str]
```

**Returns:** List of workflow type names

**Example:**
```python
types = workflow_engine.list_workflow_types()
# ['feature_development', 'bug_fix', 'infrastructure', ...]
```

### WorkflowType Enum

Available workflow types.

```python
from enum import Enum

class WorkflowType(Enum):
    FEATURE_DEVELOPMENT = "feature_development"
    BUG_FIX = "bug_fix"
    INFRASTRUCTURE = "infrastructure"
    DOCUMENTATION = "documentation"
    ANALYSIS = "analysis"
```

**Usage:**
```python
from src.orchestrator.workflow_engine import WorkflowType

# Use in workflow execution
result = await workflow_engine.execute_workflow(
    workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
    requirement="..."
)
```

## Agent Classes

### BaseAgent (Abstract)

Base class for all agents.

```python
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(
        self,
        agent_id: str,
        role: AgentRole,
        cursor_workspace: str,
        config: Optional[Dict[str, Any]] = None
    )
```

#### Abstract Methods

Must be implemented by subclasses:

```python
@abstractmethod
async def process_task(self, task: Task) -> Dict[str, Any]:
    """Process a task and return results"""
    pass

@abstractmethod
def get_system_prompt(self) -> str:
    """Return system prompt for this agent"""
    pass
```

#### Methods

##### run_task()

Execute a task.

```python
async def run_task(self, task: Task) -> Task
```

**Parameters:**
- `task` (Task): Task to execute

**Returns:** Completed Task with results

##### execute_cursor_command()

Execute LLM command.

```python
async def execute_cursor_command(
    prompt: str,
    files: Optional[List[str]] = None,
    timeout: int = 300
) -> Dict[str, Any]
```

**Parameters:**
- `prompt` (str): Prompt for LLM
- `files` (List[str], optional): Files to include in context
- `timeout` (int): Timeout in seconds

**Returns:** Dict with:
- `success` (bool): Whether command succeeded
- `stdout` (str): LLM response
- `stderr` (str): Error messages
- `error` (str): Error description if failed

##### get_status()

Get agent status.

```python
def get_status() -> Dict[str, Any]
```

**Returns:** Dict with:
- `agent_id` (str): Agent identifier
- `role` (str): Agent role
- `status` (str): Current status
- `current_task` (str): Current task ID or None
- `completed_tasks` (int): Number of completed tasks

### Specialized Agents

#### BusinessAnalystAgent

```python
from src.agents import BusinessAnalystAgent

agent = BusinessAnalystAgent(
    agent_id="ba_001",
    cursor_workspace=".",
    config={"jira_integration": False}
)
```

**Capabilities:**
- Requirements analysis
- User story creation
- Acceptance criteria definition

#### DeveloperAgent

```python
from src.agents import DeveloperAgent

agent = DeveloperAgent(
    agent_id="dev_001",
    cursor_workspace=".",
    config={"languages": ["python", "javascript"]}
)
```

**Capabilities:**
- Code implementation
- Architecture design
- Code review
- Technical documentation

#### QAEngineerAgent

```python
from src.agents import QAEngineerAgent

agent = QAEngineerAgent(
    agent_id="qa_001",
    cursor_workspace=".",
    config={"test_frameworks": ["pytest", "jest"]}
)
```

**Capabilities:**
- Test suite creation
- Quality assurance
- Bug reporting

#### DevOpsEngineerAgent

```python
from src.agents import DevOpsEngineerAgent

agent = DevOpsEngineerAgent(
    agent_id="devops_001",
    cursor_workspace=".",
    config={"platforms": ["docker", "kubernetes"]}
)
```

**Capabilities:**
- Infrastructure as Code
- CI/CD pipelines
- Deployment automation

#### TechnicalWriterAgent

```python
from src.agents import TechnicalWriterAgent

agent = TechnicalWriterAgent(
    agent_id="writer_001",
    cursor_workspace=".",
    config={"formats": ["markdown", "openapi"]}
)
```

**Capabilities:**
- API documentation
- User guides
- Release notes

### Data Models

#### Task

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any

@dataclass
class Task:
    task_id: str
    description: str
    context: Dict[str, Any]
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
```

**Example:**
```python
from src.agents.base_agent import Task

task = Task(
    task_id="impl_001",
    description="Implement user authentication",
    context={
        "framework": "fastapi",
        "database": "postgresql"
    },
    priority=1,
    dependencies=["design_001"]
)
```

#### AgentRole

```python
from enum import Enum

class AgentRole(Enum):
    BUSINESS_ANALYST = "business_analyst"
    DEVELOPER = "developer"
    QA_ENGINEER = "qa_engineer"
    DEVOPS_ENGINEER = "devops_engineer"
    TECHNICAL_WRITER = "technical_writer"
```

#### AgentStatus

```python
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"
```

## Configuration

### Settings Class

```python
from src.config import Settings, load_config

# Load from file
config = load_config("config.yaml")

# Create manually
settings = Settings(
    cursor_workspace="/path/to/workspace",
    log_level="INFO",
    cursor_timeout=300,
    agents={
        "developer": {
            "languages": ["python"]
        }
    }
)

# Convert to dict
config_dict = settings.to_dict()
```

### load_config()

```python
def load_config(config_path: Optional[str] = None) -> Settings
```

**Parameters:**
- `config_path` (str, optional): Path to config file (YAML or JSON)

**Returns:** Settings object

**Example:**
```python
from src.config import load_config

config = load_config("config.prod.yaml")
orchestrator = AgentOrchestrator(
    cursor_workspace=config.cursor_workspace,
    config=config.to_dict()
)
```

## Utilities

### FileWriter

Utility for parsing LLM responses and writing files.

```python
from src.utils import FileWriter

file_writer = FileWriter(
    workspace_root="/path/to/workspace",
    output_dir="generated"
)
```

#### Methods

##### parse_code_blocks()

Parse code blocks from text.

```python
def parse_code_blocks(text: str) -> List[Dict[str, str]]
```

**Returns:** List of dicts with:
- `language` (str): Programming language
- `filename` (str): Filename
- `content` (str): Code content

##### write_code_blocks()

Parse and write code blocks to files.

```python
def write_code_blocks(
    text: str,
    task_id: str,
    agent_role: str,
    base_path: Optional[str] = None
) -> List[str]
```

**Returns:** List of created file paths

##### extract_file_structure()

Extract multiple files from structured text.

```python
def extract_file_structure(text: str) -> Dict[str, str]
```

**Returns:** Dict mapping filenames to content

##### write_file()

Write a single file.

```python
def write_file(
    filename: str,
    content: str,
    task_id: str,
    agent_role: str,
    base_path: Optional[str] = None
) -> str
```

**Returns:** Path to created file

## Examples

### Example 1: Simple Workflow

```python
import asyncio
from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType
from src.config import load_config

async def run_simple_workflow():
    # Load configuration
    config = load_config()
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(
        cursor_workspace=config.cursor_workspace,
        config=config.to_dict()
    )
    
    # Create workflow engine
    workflow_engine = WorkflowEngine(orchestrator)
    
    # Execute workflow
    result = await workflow_engine.execute_workflow(
        workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
        requirement="Create a REST API for task management",
        context={
            "language": "python",
            "framework": "fastapi",
            "database": "postgresql"
        }
    )
    
    # Process results
    print(f"Workflow completed: {result['workflow_type']}")
    print(f"Total tasks: {result['result']['total_tasks']}")
    
    for task_id, task in result['result']['results'].items():
        print(f"\nTask: {task_id}")
        print(f"  Status: {task.completed_at is not None}")
        if task.result:
            files = task.result.get('files_created', [])
            print(f"  Files created: {len(files)}")

asyncio.run(run_simple_workflow())
```

### Example 2: Custom Workflow

```python
import asyncio
from src.orchestrator import AgentOrchestrator

async def run_custom_workflow():
    orchestrator = AgentOrchestrator(cursor_workspace=".")
    
    # Define custom workflow
    workflow = [
        {
            "task_id": "analyze_performance",
            "agent_role": "developer",
            "description": "Analyze application performance",
            "context": {
                "requirement": "Identify performance bottlenecks"
            },
            "dependencies": []
        },
        {
            "task_id": "optimize_code",
            "agent_role": "developer",
            "description": "Optimize slow code paths",
            "context": {
                "requirement": "Fix performance issues"
            },
            "dependencies": ["analyze_performance"]
        },
        {
            "task_id": "verify_optimization",
            "agent_role": "qa_engineer",
            "description": "Verify performance improvements",
            "context": {
                "requirement": "Benchmark optimized code"
            },
            "dependencies": ["optimize_code"]
        }
    ]
    
    result = await orchestrator.execute_workflow(workflow)
    return result

asyncio.run(run_custom_workflow())
```

### Example 3: Direct Agent Usage

```python
import asyncio
from src.agents import DeveloperAgent
from src.agents.base_agent import Task

async def use_agent_directly():
    # Initialize agent
    agent = DeveloperAgent(
        agent_id="dev_direct",
        cursor_workspace=".",
        config={"languages": ["python"]}
    )
    
    # Create task
    task = Task(
        task_id="direct_task",
        description="Create a simple calculator class",
        context={
            "language": "python",
            "requirements": "Basic arithmetic operations"
        }
    )
    
    # Execute task
    completed_task = await agent.run_task(task)
    
    # Check results
    if completed_task.result:
        print("Task completed successfully")
        print(f"Files created: {completed_task.result.get('files_created')}")
    else:
        print(f"Task failed: {completed_task.error}")

asyncio.run(use_agent_directly())
```

### Example 4: Monitoring System Status

```python
import asyncio
from src.orchestrator import AgentOrchestrator

async def monitor_system():
    orchestrator = AgentOrchestrator(cursor_workspace=".")
    
    # Get system status
    status = orchestrator.get_system_status()
    
    print(f"Total agents: {status['total_agents']}")
    print(f"Tasks completed: {status['total_tasks_completed']}")
    
    print("\nAgent Status:")
    for agent_id, agent_status in status['agents'].items():
        print(f"  {agent_id}:")
        print(f"    Role: {agent_status['role']}")
        print(f"    Status: {agent_status['status']}")
        print(f"    Completed Tasks: {agent_status['completed_tasks']}")

monitor_system()
```

### Example 5: Error Handling

```python
import asyncio
from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType

async def handle_errors():
    try:
        orchestrator = AgentOrchestrator(cursor_workspace=".")
        workflow_engine = WorkflowEngine(orchestrator)
        
        result = await workflow_engine.execute_workflow(
            workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
            requirement="Invalid requirement that might fail"
        )
        
        # Check for errors in results
        for task_id, task in result['result']['results'].items():
            if task.error:
                print(f"Task {task_id} failed: {task.error}")
            
    except Exception as e:
        print(f"Workflow execution failed: {e}")
        # Handle error appropriately
        raise

asyncio.run(handle_errors())
```

## Best Practices

### 1. Always Use Async/Await

```python
# Good
async def main():
    result = await workflow_engine.execute_workflow(...)

# Bad
def main():
    result = workflow_engine.execute_workflow(...)  # Wrong!
```

### 2. Proper Error Handling

```python
try:
    result = await orchestrator.execute_workflow(workflow)
except Exception as e:
    logger.error(f"Workflow failed: {e}", exc_info=True)
    # Handle appropriately
```

### 3. Use Configuration Files

```python
# Good
config = load_config("config.yaml")
orchestrator = AgentOrchestrator(
    cursor_workspace=config.cursor_workspace,
    config=config.to_dict()
)

# Avoid hardcoding
```

### 4. Monitor Task Results

```python
for task_id, task in result['result']['results'].items():
    if task.error:
        logger.error(f"Task {task_id} failed: {task.error}")
    if task.result:
        files = task.result.get('files_created', [])
        logger.info(f"Task {task_id} created {len(files)} files")
```

### 5. Clean Up Resources

```python
async def main():
    orchestrator = None
    try:
        orchestrator = AgentOrchestrator(cursor_workspace=".")
        result = await orchestrator.execute_workflow(workflow)
    finally:
        # Clean up if needed
        pass
```

## Type Hints

All classes and methods use Python type hints:

```python
from typing import Dict, List, Optional, Any

async def execute_workflow(
    workflow: List[Dict[str, Any]]
) -> Dict[str, Any]:
    ...
```

Use type hints in your code for better IDE support and type checking.

## See Also

- [Quick Start Guide](QUICK_START.md) - Getting started
- [Architecture](ARCHITECTURE.md) - System design
- [Examples](../examples/) - More examples
- [Testing](TESTING.md) - Testing guide

---

For more information, consult the source code documentation or create an issue on GitHub.
