# System Architecture

## Overview

The LLM Multi-Agent System is a production-ready orchestration platform that coordinates specialized AI agents for automated software development. The architecture emphasizes local execution, privacy, modularity, and scalability.

## Design Principles

1. **Privacy-First**: 100% local execution with no external API dependencies
2. **Modular**: Loosely coupled components for flexibility
3. **Async**: Non-blocking operations for performance
4. **Extensible**: Easy to add new agents and workflows
5. **Production-Ready**: Comprehensive error handling and logging

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Interactive  │  │ Programmatic │  │   Example    │      │
│  │     CLI      │  │     API      │  │   Scripts    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                    Core Orchestration Layer                   │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │           AgentOrchestrator (Central Hub)          │     │
│  │  - Manages agent lifecycle                         │     │
│  │  - Coordinates task execution                      │     │
│  │  - Handles inter-agent communication               │     │
│  │  - Persists workflow results                       │     │
│  └────────┬───────────────────────────────┬───────────┘     │
│           │                               │                  │
│  ┌────────▼──────────┐         ┌─────────▼──────────┐      │
│  │  WorkflowEngine   │         │   TaskManager      │      │
│  │  - Workflow       │         │   - Task queue     │      │
│  │    templates      │         │   - Dependencies   │      │
│  │  - Custom         │         │   - Prioritization │      │
│  │    workflows      │         │   - State tracking │      │
│  │  - Execution flow │         │                    │      │
│  └───────────────────┘         └────────────────────┘      │
│                                                              │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
    ┌──────────┴─────────┐          ┌─────────▼─────────┐
    │                    │          │                    │
┌───▼──────┐  ┌─────────▼───┐  ┌───▼────┐  ┌──────────▼──┐
│Business  │  │  Developer  │  │   QA   │  │   DevOps    │
│ Analyst  │  │    Agent    │  │Engineer│  │  Engineer   │
└────┬─────┘  └──────┬──────┘  └───┬────┘  └──────┬──────┘
     │               │              │              │
     └───────────────┴──────────────┴──────────────┘
                     │
          ┌──────────▼──────────┐
          │   BaseAgent Core    │
          │  - LLM interaction  │
          │  - File operations  │
          │  - Error handling   │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │  Local llama-server │
          │    (llama.cpp)      │
          │  OpenAI-compatible  │
          │     API (v1)        │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │   Local LLM Model   │
          │   (Devstral GGUF)   │
          └─────────────────────┘
```

## Component Details

### 1. Client Layer

#### Interactive CLI (main.py)
```python
# Entry point for interactive usage
- User input handling
- Workflow type selection
- Progress monitoring
- Result presentation
```

**Features:**
- User-friendly prompts
- Real-time progress updates
- Error reporting
- Result summarization

#### Programmatic API
```python
from src.orchestrator import AgentOrchestrator, WorkflowEngine

# Direct Python API for integration
orchestrator = AgentOrchestrator(workspace=".")
workflow_engine = WorkflowEngine(orchestrator)
result = await workflow_engine.execute_workflow(...)
```

**Use Cases:**
- Integration with existing tools
- Automated pipelines
- Custom applications
- Batch processing

### 2. Core Orchestration Layer

#### AgentOrchestrator

**Responsibilities:**
- Initialize and manage agents
- Execute workflows
- Handle task dependencies
- Coordinate inter-agent communication
- Persist results

**Key Methods:**
```python
class AgentOrchestrator:
    def __init__(self, workspace: str, config: Dict)
    async def execute_workflow(self, workflow: List[Dict]) -> Dict
    async def execute_task(self, task: Task, agent_id: str) -> Task
    def get_agent_by_role(self, role: AgentRole) -> BaseAgent
    def get_system_status(self) -> Dict
```

**State Management:**
```python
{
    "agents": {
        "ba_001": BusinessAnalystAgent,
        "dev_001": DeveloperAgent,
        "qa_001": QAEngineerAgent,
        "devops_001": DevOpsEngineerAgent,
        "writer_001": TechnicalWriterAgent
    },
    "task_results": {
        "task_id": Task
    },
    "message_bus": asyncio.Queue
}
```

#### WorkflowEngine

**Responsibilities:**
- Define workflow templates
- Create custom workflows
- Manage workflow execution
- Handle step dependencies

**Workflow Templates:**
```python
WorkflowType.FEATURE_DEVELOPMENT = [
    {
        "step": 1,
        "agent_role": "business_analyst",
        "task_type": "requirements_analysis",
        "description": "Analyze requirements",
        "depends_on": []
    },
    {
        "step": 2,
        "agent_role": "developer",
        "task_type": "architecture_design",
        "description": "Design architecture",
        "depends_on": [1]
    },
    # ... more steps
]
```

**Key Features:**
- 5 predefined workflow types
- Custom workflow creation
- Dependency resolution
- Context passing between agents

#### TaskManager

**Responsibilities:**
- Task queue management
- Dependency tracking
- Priority handling
- Task state persistence

**Task Model:**
```python
@dataclass
class Task:
    task_id: str
    description: str
    context: Dict[str, Any]
    priority: int = 1
    dependencies: List[str] = []
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
```

### 3. Agent Layer

#### BaseAgent (Abstract Base Class)

**Core Functionality:**
```python
class BaseAgent(ABC):
    # Initialization
    def __init__(self, agent_id, role, workspace, config)
    
    # Abstract methods (must implement)
    async def process_task(self, task: Task) -> Dict[str, Any]
    def get_system_prompt(self) -> str
    
    # LLM Communication
    async def execute_llm_task(self, prompt, files, timeout) -> Dict
    async def _call_local_llama_server(self, system_prompt, user_prompt, timeout) -> Dict
    
    # Task Execution
    async def run_task(self, task: Task) -> Task
    
    # Communication
    async def send_message(self, message: AgentMessage)
    async def receive_message(self) -> AgentMessage
    
    # Status
    def get_status(self) -> Dict[str, Any]
```

**Agent State:**
```python
{
    "agent_id": str,
    "role": AgentRole,
    "status": AgentStatus,  # IDLE, WORKING, WAITING, COMPLETED, ERROR
    "current_task": Optional[Task],
    "task_history": List[Task],
    "message_queue": asyncio.Queue
}
```

#### Specialized Agents

##### BusinessAnalystAgent
- Requirements analysis
- User story creation
- Acceptance criteria
- Feasibility assessment

##### DeveloperAgent
- Code implementation
- Architecture design
- Code review
- Technical documentation
- Supports: Python, JavaScript, TypeScript

##### QAEngineerAgent
- Test suite creation
- Quality assurance
- Bug reporting
- Test frameworks: pytest, Jest, Playwright

##### DevOpsEngineerAgent
- Infrastructure as Code
- CI/CD pipelines
- Deployment automation
- Platforms: Docker, Kubernetes, AWS

##### TechnicalWriterAgent
- API documentation
- User guides
- Release notes
- Formats: Markdown, Confluence, OpenAPI

### 4. LLM Integration Layer

#### Local llama-server

**Configuration:**
```bash
llama-server \
  -hf unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL \
  -ngl 99 \
  --ctx-size 16384 \
  --host 127.0.0.1 \
  --port 8080
```

**API Compatibility:**
- OpenAI-compatible API (v1)
- Standard chat completions endpoint
- Streaming support
- Model selection

**Communication Flow:**
```
BaseAgent.execute_llm_task()
    ↓
AsyncOpenAI(base_url="http://127.0.0.1:8080/v1")
    ↓
client.chat.completions.create(
    model="devstral",
    messages=[system_prompt, user_prompt]
)
    ↓
Response → Task Result
```

### 5. Utility Layer

#### FileWriter

**Responsibilities:**
- Parse LLM responses
- Extract code blocks
- Write files to disk
- Handle multiple formats

**Supported Formats:**
```python
# Code block with filename
```python:path/to/file.py
code here
```

# File: format
File: `path/to/file.py`
```python
code here
```

# Multiple files
Multiple file structures in single response
```

**Key Methods:**
```python
class FileWriter:
    def parse_code_blocks(self, text: str) -> List[Dict]
    def write_code_blocks(self, text, task_id, agent_role) -> List[str]
    def extract_file_structure(self, text: str) -> Dict[str, str]
    def write_file(self, filename, content, task_id, agent_role) -> str
    def write_json(self, filename, data, task_id, agent_role) -> str
```

## Data Flow

### Complete Workflow Execution

```
1. User submits requirement via CLI/API
   ↓
2. WorkflowEngine creates workflow from template
   ↓
3. AgentOrchestrator receives workflow
   ↓
4. For each workflow step:
   a. Check dependencies satisfied
   b. Create Task with context
   c. Assign to appropriate Agent
   d. Agent calls local llama-server
   e. Parse and process LLM response
   f. Write generated files
   g. Store task result
   h. Update shared context
   ↓
5. All steps complete
   ↓
6. AgentOrchestrator saves workflow results
   ↓
7. Generate summary and return to user
```

### Task Execution Flow

```
AgentOrchestrator.execute_task(task, agent_id)
    ↓
Agent.run_task(task)
    ↓
Agent.process_task(task)
    ↓
Agent.execute_llm_task(prompt, files)
    ↓
Agent._call_local_llama_server(system, user, timeout)
    ↓
AsyncOpenAI.chat.completions.create()
    ↓
Parse LLM response
    ↓
FileWriter.write_code_blocks()
    ↓
Return task result with created files
    ↓
AgentOrchestrator stores result
```

## Configuration Management

### Settings Hierarchy

```
1. Environment Variables (.env)
   OPENAI_API_BASE=http://127.0.0.1:8080/v1
   OPENAI_API_KEY=not-needed
   OPENAI_API_MODEL=devstral

2. YAML Configuration (config.yaml)
   workspace: "."
   log_level: "INFO"
   llm_timeout: 300
   agents:
     developer:
       languages: [python, javascript]

3. Runtime Configuration
   Passed during initialization
   Can override settings
```

### Configuration Loading

```python
class Settings:
    @classmethod
    def from_dict(cls, config: Dict) -> Settings
    
    def to_dict(self) -> Dict

def load_config(config_path: Optional[str]) -> Settings:
    # Load .env
    load_dotenv()
    
    # Load YAML
    config_data = yaml.safe_load(config_file)
    
    # Resolve paths
    # Apply environment overrides
    
    return Settings.from_dict(config_data)
```

## Error Handling

### Error Types & Strategies

```python
1. LLM Server Errors
   - Connection refused → Start server
   - Timeout → Increase timeout
   - Invalid response → Retry with backoff

2. Task Execution Errors
   - Agent failure → Log and mark task as failed
   - Dependency error → Fail dependent tasks
   - Validation error → Return error to user

3. File Operation Errors
   - Write permission → Log warning, continue
   - Invalid path → Create directories
   - Disk full → Fail gracefully

4. Configuration Errors
   - Missing .env → Fail with clear message
   - Invalid YAML → Fail with validation error
   - Missing model → Provide setup instructions
```

### Retry Logic

```python
# Task retry with exponential backoff
max_retries = config.task_retry_attempts  # Default: 3
for attempt in range(max_retries):
    try:
        result = await agent.run_task(task)
        break
    except TransientError as e:
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise
```

## Performance Considerations

### Optimization Strategies

1. **Async Operations**
   - All I/O operations are async
   - Agents can work in parallel
   - Non-blocking LLM calls

2. **Context Management**
   - Limit LLM context size
   - Truncate large file contents
   - Share context efficiently

3. **Resource Management**
   - Connection pooling
   - File handle management
   - Memory-efficient parsing

4. **Caching**
   - Model weights cached in RAM
   - Configuration cached
   - Parsed results cached

### Performance Metrics

```python
Expected Performance:
- Agent initialization: < 1 second
- Task assignment: < 100ms
- LLM inference: 10-60 seconds (model dependent)
- File writing: < 100ms
- Full workflow: 5-30 minutes
```

## Scalability

### Current Implementation

- **Single Process**: All agents in one process
- **Async Execution**: Multiple agents can work simultaneously
- **Local Model**: Single llama-server instance
- **File-based Output**: Results saved to disk

### Future Scaling Options

1. **Multi-Process**
   - Separate process per agent
   - Process pool for agents
   - IPC for communication

2. **Distributed**
   - Multiple llama-server instances
   - Load balancing
   - Distributed task queue

3. **Database Integration**
   - PostgreSQL for state
   - Redis for caching
   - Message queue (RabbitMQ)

## Security

### Current Security Measures

1. **Local-Only Execution**
   - No external network calls
   - All data stays on machine
   - No API keys exposed

2. **Workspace Isolation**
   - Configurable workspace directory
   - File operations within workspace
   - Path validation

3. **Input Validation**
   - Configuration validation
   - Task parameter validation
   - File path sanitization

4. **Logging**
   - Structured logging
   - Sensitive data filtering
   - Audit trail

## Monitoring & Observability

### Logging

```python
# Structured logging with context
logger.info(f"[{agent_id}] Starting task: {task_id}")
logger.error(f"[{agent_id}] Error: {error}", exc_info=True)
```

**Log Levels:**
- DEBUG: Detailed execution flow
- INFO: Task progress and completion
- WARNING: Non-critical issues
- ERROR: Failures and exceptions

### Metrics

Available via `AgentOrchestrator.get_system_status()`:

```python
{
    "total_agents": 5,
    "agents": {
        "agent_id": {
            "role": "developer",
            "status": "working",
            "current_task": "task_123",
            "completed_tasks": 5
        }
    },
    "total_tasks_completed": 25,
    "timestamp": "2024-01-15T10:30:00"
}
```

### Output Files

1. **Workflow Results** (`output/workflow_*.json`)
   - Complete workflow execution details
   - Task results and errors
   - Created files list
   - Timestamps

2. **Workflow Summary** (`output/workflow_summary_*.md`)
   - Human-readable summary
   - Generated files
   - Task status
   - Completion metrics

3. **Agent Outputs** (`output/generated/`)
   - Generated code files
   - Documentation
   - Test files
   - Configuration files

## Extension Points

### Adding New Agents

```python
from src.agents.base_agent import BaseAgent, AgentRole

class CustomAgent(BaseAgent):
    def __init__(self, agent_id, workspace, config):
        super().__init__(agent_id, AgentRole.CUSTOM, workspace, config)
    
    def get_system_prompt(self) -> str:
        return "Your custom system prompt..."
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        # Your custom logic
        result = await self.execute_llm_task(prompt)
        return {"status": "completed", ...}
```

### Adding New Workflows

```python
# In WorkflowEngine
CUSTOM_WORKFLOW = [
    {
        "step": 1,
        "agent_role": "your_agent",
        "task_type": "your_task_type",
        "description": "Task description",
        "depends_on": []
    },
    # More steps...
]

workflow_templates[WorkflowType.CUSTOM] = CUSTOM_WORKFLOW
```

### Custom File Writers

```python
class CustomFileWriter(FileWriter):
    def parse_custom_format(self, text: str) -> List[Dict]:
        # Your custom parsing logic
        pass
    
    def write_custom_output(self, data, task_id, agent_role):
        # Your custom writing logic
        pass
```

## Deployment Architecture

### Development Environment

```
Local Machine
├── Python venv
├── llama-server (local)
├── Project workspace
├── Generated output
└── Log files
```

### Production Considerations

1. **Resource Allocation**
   - Dedicated server/workstation
   - GPU for faster inference
   - SSD for fast I/O

2. **Process Management**
   - systemd service for llama-server
   - Process monitoring
   - Auto-restart on failure

3. **Backup & Recovery**
   - Regular output backups
   - Configuration versioning
   - Log rotation

4. **Updates**
   - Model updates
   - System updates
   - Dependency updates

## Best Practices

### Code Organization

1. Keep agents focused and single-purpose
2. Use type hints for clarity
3. Follow async/await patterns
4. Handle errors gracefully
5. Log important events

### Configuration

1. Use environment variables for secrets
2. Use YAML for structured configuration
3. Validate configuration on startup
4. Provide sensible defaults

### Testing

1. Unit tests for components
2. Integration tests for workflows
3. Test error scenarios
4. Test file parsing edge cases

### Performance

1. Use async for I/O operations
2. Limit LLM context size
3. Batch operations when possible
4. Monitor resource usage

## Conclusion

This architecture provides a solid foundation for a production-ready multi-agent system with:

- ✅ Clean separation of concerns
- ✅ Extensible design
- ✅ Privacy-first approach
- ✅ Production-ready error handling
- ✅ Comprehensive logging
- ✅ Scalability options

The system is designed to be both powerful for complex workflows and simple to use for common tasks.
