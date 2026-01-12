# Cursor CLI Agent Orchestration System

## Overview

This project implements a sophisticated multi-agent system that orchestrates Cursor CLI agents to build complex software projects. The system coordinates specialized AI agents (Business Analyst, Developer, QA Engineer, DevOps Engineer, and Technical Writer) to collaboratively analyze requirements, design architecture, implement code, test, deploy, and document software projects.

## Architecture

### Core Components

1. **Agent System** (`src/agents/`)
   - `BaseAgent`: Abstract base class for all agents with Cursor CLI integration
   - `BusinessAnalystAgent`: Requirements analysis and user story creation
   - `DeveloperAgent`: Code implementation and architecture design
   - `QAEngineerAgent`: Test creation and quality assurance
   - `DevOpsEngineerAgent`: Infrastructure and deployment automation
   - `TechnicalWriterAgent`: Documentation creation

2. **Orchestrator** (`src/orchestrator/`)
   - `AgentOrchestrator`: Central coordinator for all agents
   - `TaskManager`: Task queue and dependency management
   - `WorkflowEngine`: Predefined workflow templates and execution

3. **Configuration** (`src/config/`)
   - `Settings`: Configuration management
   - YAML/JSON configuration support

## How It Works

### Agent Execution Flow

```
User Requirement
    ↓
Workflow Engine (selects workflow type)
    ↓
Task Creation (with dependencies)
    ↓
Agent Orchestrator (assigns tasks to agents)
    ↓
Individual Agents (execute via Cursor CLI)
    ↓
Task Results (collected and aggregated)
    ↓
Final Output (saved to output directory)
```

### Cursor CLI Integration

Each agent executes tasks by invoking the Cursor CLI with specialized prompts:

```python
cursor chat --file <files> --message <prompt> --workspace <workspace>
```

The system:
1. Constructs context-aware prompts based on agent role
2. Passes relevant files to Cursor CLI
3. Executes commands asynchronously
4. Captures and processes output
5. Handles errors and retries

## Workflow Types

### 1. Feature Development
Complete feature implementation workflow:
- Requirements analysis (BA)
- Architecture design (Developer)
- Implementation (Developer)
- Testing (QA)
- Infrastructure setup (DevOps)
- Documentation (Technical Writer)

### 2. Bug Fix
Focused bug resolution workflow:
- Bug analysis (QA)
- Bug fix implementation (Developer)
- Regression testing (QA)
- Release notes (Technical Writer)

### 3. Infrastructure
Infrastructure-focused workflow:
- Infrastructure design (DevOps)
- Implementation (DevOps)
- Testing (QA)
- Documentation (Technical Writer)

### 4. Documentation
Documentation-focused workflow:
- Requirements gathering (BA)
- Documentation creation (Technical Writer)
- Technical review (Developer)

### 5. Analysis
Analysis and feasibility study:
- Requirements gathering (BA)
- Technical feasibility (Developer)
- Infrastructure assessment (DevOps)
- Final analysis report (BA)

## Usage

### Basic Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Configure the system
cp .env.example .env
# Edit config.yaml with your settings

# Run the system
python main.py
```

### Programmatic Usage

```python
from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType

# Initialize orchestrator
orchestrator = AgentOrchestrator(
    cursor_workspace="/path/to/workspace"
)

# Create workflow engine
workflow_engine = WorkflowEngine(orchestrator)

# Execute workflow
result = await workflow_engine.execute_workflow(
    workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
    requirement="Create a REST API for user management",
    context={"language": "python", "framework": "fastapi"}
)
```

### Custom Workflows

```python
custom_workflow = [
    {
        "task_id": "task_001",
        "agent_role": "business_analyst",
        "description": "Analyze requirements",
        "context": {"requirement": "..."}
    },
    {
        "task_id": "task_002",
        "agent_role": "developer",
        "description": "Implement feature",
        "context": {"files": ["src/main.py"]},
        "dependencies": ["task_001"]
    }
]

result = await orchestrator.execute_workflow(custom_workflow)
```

## Configuration

### config.yaml

```yaml
cursor_workspace: "/path/to/workspace"
log_level: "INFO"
cursor_timeout: 300
max_concurrent_agents: 5

agents:
  developer:
    languages: [python, javascript, typescript]
    frameworks: [fastapi, react, django]
  
  qa_engineer:
    test_frameworks: [pytest, jest, playwright]
    coverage_threshold: 80
  
  devops_engineer:
    platforms: [docker, kubernetes, aws]
```

## Agent Capabilities

### Business Analyst Agent
- Requirements analysis and breakdown
- User story creation with acceptance criteria
- Business value assessment
- Dependency and risk identification
- Jira ticket structure recommendations

### Developer Agent
- Clean, production-ready code implementation
- Architecture design following SOLID principles
- Code review and refactoring
- Unit and integration test creation
- Technical documentation

### QA Engineer Agent
- Comprehensive test plan creation
- Automated test script development
- Coverage analysis
- Bug reporting with reproduction steps
- Performance and load testing

### DevOps Engineer Agent
- Infrastructure as Code (Docker, Kubernetes, Terraform)
- CI/CD pipeline design and implementation
- Monitoring and logging setup
- Security configuration
- Deployment automation

### Technical Writer Agent
- API documentation (OpenAPI/Swagger)
- User guides and tutorials
- Architecture documentation
- Release notes and changelogs
- Knowledge base articles

## Task Management

### Task Dependencies

Tasks can specify dependencies to ensure proper execution order:

```python
Task(
    task_id="implement_feature",
    description="Implement user authentication",
    dependencies=["design_architecture", "setup_database"]
)
```

### Task Priority

Tasks support priority levels (higher number = higher priority):

```python
Task(
    task_id="critical_bug_fix",
    description="Fix security vulnerability",
    priority=10  # High priority
)
```

## Output

Results are saved to the configured output directory:

```
output/
├── workflow_feature_development_2024-01-12T15-30-00.json
├── workflow_bug_fix_2024-01-12T16-45-00.json
└── agent_status.json
```

## Examples

See the `examples/` directory for:
- `simple_workflow.py`: Basic workflow execution
- `custom_workflow.py`: Custom workflow creation
- `agent_status_monitor.py`: Agent status monitoring

## Error Handling

The system includes comprehensive error handling:
- Automatic retry on transient failures
- Timeout management for long-running tasks
- Graceful degradation on agent failures
- Detailed error logging

## Logging

Logs are written to both console and file:
- Console: Real-time progress updates
- File: Detailed execution logs with timestamps

Configure logging in `config.yaml`:

```yaml
log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR
log_file: "logs/agent_system.log"
```

## Best Practices

1. **Clear Requirements**: Provide detailed, unambiguous requirements
2. **Appropriate Workflow**: Choose the workflow type that matches your task
3. **Context Matters**: Include relevant context (files, frameworks, constraints)
4. **Monitor Progress**: Check logs for real-time execution status
5. **Review Output**: Always review generated code and documentation

## Limitations

- Requires Cursor CLI to be installed and accessible
- Execution time depends on task complexity
- Quality depends on requirement clarity
- Cursor CLI must have access to the workspace

## Troubleshooting

### Cursor CLI Not Found
```bash
# Ensure Cursor CLI is in PATH
which cursor

# Or specify full path in config.yaml
cursor_cli_path: "/Applications/Cursor.app/Contents/Resources/app/bin/cursor"
```

### Timeout Errors
```yaml
# Increase timeout in config.yaml
cursor_timeout: 600  # 10 minutes
task_timeout: 900    # 15 minutes
```

### Agent Failures
- Check logs for detailed error messages
- Verify workspace permissions
- Ensure all required files exist
- Review task dependencies

## Future Enhancements

- Integration with Jira, Confluence, and GitLab APIs
- Real-time collaboration between agents
- Learning from past executions
- Custom agent creation
- Web-based dashboard
- Parallel task execution optimization
