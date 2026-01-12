# LLM Multi-Agent System - Cursor CLI Orchestration

## Project Overview

This project implements a sophisticated multi-agent system that orchestrates **Cursor CLI agents** to build complex software projects. The system coordinates specialized AI agents (Business Analyst, Developer, QA Engineer, DevOps Engineer, and Technical Writer) to collaboratively analyze requirements, design architecture, implement code, test, deploy, and document software projects.

**Key Features:**
- 🤖 **5 Specialized AI Agents** working in coordination
- 🔄 **Automated Workflow Orchestration** with dependency management
- 💻 **Cursor CLI Integration** for intelligent code generation
- 📋 **Predefined Workflow Templates** for common scenarios
- 🎯 **Custom Workflow Support** for specific needs
- 📊 **Real-time Status Monitoring** and logging
- 🔧 **Flexible Configuration** via YAML/JSON

## Table of Contents

1. [Brainstorming Session](#brainstorming-session)
2. [Architecture Design](#architecture-design)
3. [Technology Stack](#technology-stack)
4. [Implementation Plan](#implementation-plan)
5. [Agent Specifications](#agent-specifications)
6. [Integration Details](#integration-details)
7. [Workflow Engine](#workflow-engine)
8. [Risk Assessment](#risk-assessment)

## Brainstorming Session

### Participants

- **Agent 1**: Product Manager / Business Analyst
- **Agent 2**: Solution Architect / Tech Lead
- **Agent 3**: DevOps / Infrastructure Engineer
- **Agent 4**: QA / Quality Assurance Engineer

### Session Results

See [BRAINSTORMING.md](./docs/BRAINSTORMING.md) for detailed brainstorming notes from all agents.

## Architecture Design

See [ARCHITECTURE.md](./docs/ARCHITECTURE.md) for detailed architecture documentation.

## Technology Stack

See [TECH_STACK.md](./docs/TECH_STACK.md) for complete technology stack details.

## Implementation Plan

See [IMPLEMENTATION_PLAN.md](./docs/IMPLEMENTATION_PLAN.md) for detailed 20-week implementation roadmap.

## Quick Start

### Prerequisites

- **Python 3.11+**
- **Cursor IDE** with CLI installed (https://cursor.sh)
- Git (optional)

### Installation

```bash
# Navigate to project directory
cd llm-multi-agent-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional)
cp .env.example .env

# Update config.yaml with your workspace path
# Edit cursor_workspace in config.yaml

# Run the system
python main.py
```

### First Run

```bash
python main.py
```

You'll be prompted to:
1. Enter a requirement (e.g., "Create a REST API for user authentication")
2. Select a workflow type (1-5)
3. Wait for agents to complete their tasks
4. Review results in the `output/` directory

See [QUICK_START.md](./docs/QUICK_START.md) for detailed instructions.

## Project Structure

```
llm-multi-agent-system/
├── docs/                           # Documentation
│   ├── BRAINSTORMING.md           # Brainstorming session notes
│   ├── ARCHITECTURE.md            # System architecture
│   ├── TECH_STACK.md              # Technology stack details
│   ├── IMPLEMENTATION_PLAN.md     # Implementation roadmap
│   ├── AGENT_SPECS.md             # Agent specifications
│   ├── CURSOR_CLI_ORCHESTRATION.md # Cursor CLI integration guide
│   └── QUICK_START.md             # Quick start guide
├── src/                            # Source code
│   ├── agents/                    # Agent implementations
│   │   ├── base_agent.py          # Base agent class with Cursor CLI integration
│   │   ├── business_analyst.py    # Business Analyst agent
│   │   ├── developer.py           # Developer agent
│   │   ├── qa_engineer.py         # QA Engineer agent
│   │   ├── devops_engineer.py     # DevOps Engineer agent
│   │   └── technical_writer.py    # Technical Writer agent
│   ├── orchestrator/              # Orchestration logic
│   │   ├── agent_orchestrator.py  # Main orchestrator
│   │   ├── task_manager.py        # Task queue and dependency management
│   │   └── workflow_engine.py     # Workflow templates and execution
│   ├── config/                    # Configuration management
│   │   └── settings.py            # Settings and config loading
│   └── utils/                     # Utility modules
│       └── file_writer.py         # File writing utilities
├── tests/                          # Test suite
│   ├── simple_test.py             # Simple workflow tests
│   ├── test_agent.py              # Agent functionality tests
│   ├── test_all_formats.py        # File format tests
│   ├── test_file_writer.py        # File writer tests
│   ├── test_full_response.py      # Full response tests
│   ├── test_nested_blocks.py      # Nested block tests
│   ├── test_no_backticks.py       # No backticks tests
│   └── test_no_duplicates.py      # Duplicate prevention tests
├── examples/                       # Example scripts
│   ├── simple_workflow.py         # Basic workflow example
│   ├── custom_workflow.py         # Custom workflow example
│   └── agent_status_monitor.py    # Agent monitoring example
├── output/                         # Generated output files
├── logs/                           # Log files
├── config.yaml                     # Main configuration file
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
├── main.py                         # Main entry point
└── README.md                       # This file
```

## Workflow Types

The system supports 5 predefined workflow types:

1. **Feature Development** - Complete feature implementation from requirements to deployment
2. **Bug Fix** - Focused bug resolution with testing and documentation
3. **Infrastructure** - Infrastructure design, implementation, and documentation
4. **Documentation** - Comprehensive documentation creation and review
5. **Analysis** - Feasibility studies and technical analysis

## Usage Examples

### Interactive Mode

```bash
python main.py
```

### Programmatic Usage

```python
from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType

orchestrator = AgentOrchestrator(cursor_workspace="/path/to/workspace")
workflow_engine = WorkflowEngine(orchestrator)

result = await workflow_engine.execute_workflow(
    workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
    requirement="Create a REST API for user management"
)
```

### Run Examples

```bash
# Simple workflow
python examples/simple_workflow.py

# Custom workflow
python examples/custom_workflow.py

# Monitor agent status
python examples/agent_status_monitor.py
```

## Testing

The project includes a comprehensive test suite in the `tests/` directory:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_agent.py

# Run with verbose output
python -m pytest tests/ -v

# Run individual test files
python tests/simple_test.py
python tests/test_file_writer.py
python tests/test_all_formats.py
```

**Test Coverage:**
- **Agent functionality**: Core agent behavior and workflows
- **File writer**: File writing and format handling
- **Response parsing**: LLM response processing
- **Format handling**: Multiple file format support
- **Edge cases**: Nested blocks, duplicates, special characters

## Agent Capabilities

- **Business Analyst**: Requirements analysis, user stories, Jira ticket structure
- **Developer**: Code implementation, architecture design, code review
- **QA Engineer**: Test creation, quality assurance, bug reporting
- **DevOps Engineer**: Infrastructure as code, CI/CD, deployment automation
- **Technical Writer**: API docs, user guides, release notes

## Documentation

All detailed documentation is located in the `docs/` directory:

- **[Quick Start Guide](./docs/QUICK_START.md)** - Get started in 5 minutes
- **[Cursor CLI Orchestration](./docs/CURSOR_CLI_ORCHESTRATION.md)** - Complete system guide
- **[Testing Guide](./docs/TESTING.md)** - Comprehensive testing documentation
- [Brainstorming Notes](./docs/BRAINSTORMING.md)
- [Architecture Design](./docs/ARCHITECTURE.md)
- [Technology Stack](./docs/TECH_STACK.md)
- [Implementation Plan](./docs/IMPLEMENTATION_PLAN.md)
- [Agent Specifications](./docs/AGENT_SPECS.md)
- [Integration Guide](./docs/INTEGRATIONS.md)

## System Requirements

- Python 3.11 or higher
- Cursor IDE with CLI installed
- 4GB RAM minimum (8GB recommended)
- macOS, Linux, or Windows

## Configuration

Edit `config.yaml` to customize:

```yaml
cursor_workspace: "/path/to/your/workspace"
log_level: "INFO"
cursor_timeout: 300
max_concurrent_agents: 5

agents:
  developer:
    languages: [python, javascript, typescript]
  qa_engineer:
    test_frameworks: [pytest, jest, playwright]
  devops_engineer:
    platforms: [docker, kubernetes, aws]
```

## Output

Results are saved in the `output/` directory as JSON files containing:
- Workflow type and requirement
- Task execution details
- Agent results and outputs
- Completion timestamps

## Troubleshooting

**Cursor CLI not found:**
```bash
# Verify Cursor CLI is installed
cursor --version

# Or specify full path in config.yaml
cursor_cli_path: "/Applications/Cursor.app/Contents/Resources/app/bin/cursor"
```

**Task timeout:**
```yaml
# Increase timeout in config.yaml
cursor_timeout: 600
task_timeout: 900
```

See [CURSOR_CLI_ORCHESTRATION.md](./docs/CURSOR_CLI_ORCHESTRATION.md) for more troubleshooting tips.

## Contributing

Contributions are welcome! This project is fully implemented and ready for use. Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

TBD - To be determined based on project requirements.
