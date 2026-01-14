# LLM Multi-Agent System

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A production-ready multi-agent orchestration system powered by local LLMs for automated software development workflows.

## ⚠️ Important: Python 3.12 Required

**This project requires Python 3.12.x**

- Install: `brew install python@3.12` (macOS)
- Create venv: `python3.12 -m venv venv`
- See: [`START_HERE.md`](docs/START_HERE.md) for complete setup

> Python 3.14 and other versions are NOT supported due to LangChain/LangGraph compatibility.

## 🎯 Overview

This system orchestrates specialized AI agents that collaborate to handle complete software development lifecycles—from requirements analysis to deployment and documentation. Built with privacy-first principles, it runs **100% locally** using llama.cpp, ensuring no data leaves your machine.

### Key Features

- 🤖 **5 Specialized AI Agents** - Business Analyst, Developer, QA Engineer, DevOps Engineer, Technical Writer
- 💬 **Interactive Chat Display** - Watch agents communicate in real-time with color-coded chat interface
- 🔄 **LangGraph Orchestration** - Advanced workflow engine with parallel execution and state persistence
- ⚡ **Parallel Agent Execution** - QA and DevOps run simultaneously (30-40% faster)
- 💾 **State Persistence** - Resume interrupted workflows from checkpoints
- 🏠 **100% Local Execution** - No cloud APIs, complete data privacy, zero costs
- 📋 **Flexible Workflow Engine** - Custom workflows or use predefined templates
- 🔧 **Production-Ready** - Comprehensive error handling, logging, and monitoring
- 📊 **Real-time Status Tracking** - Monitor agent progress and task completion with visual progress bars
- 🧪 **Fully Tested** - Comprehensive test suite included

### 🚀 Production Enhancements (New!)

- ⚡ **Streaming Responses** - Real-time token streaming for immediate feedback (enabled by default)
- 🔄 **Retry Logic** - Exponential backoff with jitter for transient failure recovery
- 🛡️ **Circuit Breaker** - Prevents cascade failures with automatic recovery detection
- 🔌 **Connection Pooling** - Efficient connection reuse with health monitoring
- 📝 **Structured Logging** - JSON-formatted logs with correlation IDs for traceability
- 📊 **Metrics Collection** - Built-in performance monitoring and statistics
- ✅ **Config Validation** - Comprehensive validation with clear error messages
- 🎯 **Enhanced System Prompts** - Professional, production-ready prompts for all agents

**See**: [Production-Ready Guide](docs/PRODUCTION_READY_GUIDE.md) | [Migration Guide](docs/MIGRATION_GUIDE.md)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Multi-Agent Orchestrator                     │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────┐        │
│  │   Workflow   │  │   Agent    │  │     Task     │        │
│  │    Engine    │←→│ Orchestrator│←→│   Manager    │        │
│  └──────────────┘  └────────────┘  └──────────────┘        │
└─────────────┬───────────────────────────────────────────────┘
              │
    ┌─────────┴──────────┐
    │                    │
┌───▼───┐  ┌──────▼──────┐  ┌────▼────┐  ┌────▼─────┐
│Business│  │  Developer  │  │   QA    │  │  DevOps  │
│Analyst │  │    Agent    │  │ Engineer│  │ Engineer │
└────────┘  └─────────────┘  └─────────┘  └──────────┘
                    │
         ┌──────────▼───────────┐
         │  Local llama-server  │
         │   (llama.cpp)        │
         └──────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12** (required - install with `brew install python@3.12`)
- **llama.cpp** installed (with llama-server)
- 16GB+ RAM recommended
- macOS, Linux, or Windows

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/llm-multi-agent-system.git
cd llm-multi-agent-system

# Run automated setup
python setup.py
```

This will:
1. Check Python version
2. Verify llama.cpp installation
3. Create virtual environment
4. Install dependencies
5. Set up configuration files

### Manual Setup (Alternative)

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (inside venv, use python/pip)
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start local LLM server (ensure llama-server is running on port 8080)

# Run the system (inside venv, use python)
python main.py
```

### Configuration

Edit `config.yaml`:

```yaml
workspace: "."  # Your workspace path
log_level: "INFO"

# LLM Configuration (Production-Ready)
llm_timeout: 300
llm_max_retries: 3
llm_retry_initial_delay: 1.0
llm_retry_max_delay: 60.0
llm_circuit_breaker_threshold: 5
llm_circuit_breaker_timeout: 60.0
llm_stream_responses: true  # Enable streaming

# Orchestration
max_concurrent_agents: 5

# Monitoring & Logging
enable_structured_logging: true
enable_metrics: true

# Agent configurations
agents:
  developer:
    languages: [python, javascript, typescript]
  qa_engineer:
    test_frameworks: [pytest, jest, playwright]
```

Edit `.env`:

```bash
# LLM Server Configuration
OPENAI_API_BASE=http://127.0.0.1:8080/v1
OPENAI_API_KEY=not-needed
OPENAI_API_MODEL=devstral
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2048

# Retry & Resilience
LLM_MAX_RETRIES=3
LLM_RETRY_INITIAL_DELAY=1.0
LLM_RETRY_MAX_DELAY=60.0
LLM_CIRCUIT_BREAKER_THRESHOLD=5
LLM_CIRCUIT_BREAKER_TIMEOUT=60.0

# Logging
LOG_LEVEL=INFO
STRUCTURED_LOGGING=true

# See .env.example for full configuration options
```

## 💡 Usage

### Interactive Mode

```bash
python main.py
```

You'll be prompted to:
1. Enter your requirement
2. Select a workflow type
3. Monitor execution
4. Review results in `output/` directory

### Interactive Chat Display (New! ✨)

**Watch agents communicate in real-time** with our new interactive chat interface:

```bash
# Run the interactive example
python examples/interactive_chat_workflow.py
```

**Features:**
- 💬 Color-coded agent messages and thoughts
- 🔄 Visual handoffs between agents
- 📊 Real-time progress bars
- ✅ Task completion summaries
- 📄 File operation tracking
- 📝 Automatic chat log export

**Example Output:**
```
🤔 Business Analyst:
  Analyzing requirements for task management API...
  Identifying user stories and acceptance criteria.

✅ Business Analyst completed task
  Created 8 user stories with 24 acceptance criteria
  📄 Files created: 2
    • requirements.md
    • user_stories.md

🔄 Business Analyst → Developer
  Requirements complete. Passing user stories for design.

Progress: ████████████████░░░░░░░░░░░░░░░░░░░░ 40%
```

See [Interactive Chat Guide](docs/INTERACTIVE_CHAT.md) for full details.

### LangGraph Orchestration (Recommended)

**New!** Use LangGraph for advanced features like parallel execution and state persistence:

```python
import asyncio
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator

async def main():
    # Initialize orchestrator with interactive chat display
    orchestrator = LangGraphOrchestrator(
        workspace=".",
        enable_chat_display=True  # Watch agents communicate!
    )
    
    # Execute with parallel QA + DevOps (30-40% faster)
    result = await orchestrator.execute_feature_development(
        requirement="Create REST API for user authentication with JWT",
        context={
            "language": "python",
            "framework": "fastapi"
        }
    )
    
    print(f"Workflow completed: {result['status']}")
    print(f"Files created: {len(result['files_created'])}")

asyncio.run(main())
```

**Run it:**
```bash
# Inside virtual environment (use python)
python examples/langgraph_feature_development.py

# Outside virtual environment (use python3)
python3 examples/langgraph_feature_development.py
```

**Key Benefits:**
- ⚡ 30-40% faster with parallel execution
- 💬 Interactive chat display (enabled by default)
- 💾 Resume interrupted workflows
- 🔀 Smart conditional routing
- 📊 Workflow visualization

See [LangGraph Integration Guide](docs/LANGGRAPH_INTEGRATION.md) for details.

### LangGraph Orchestration

```python
import asyncio
from src.orchestrator import LangGraphOrchestrator

async def main():
    orchestrator = LangGraphOrchestrator(workspace=".")
    
    final_state = await orchestrator.execute_feature_development(
        requirement="Create REST API for user authentication with JWT",
        context={
            "language": "python",
            "framework": "fastapi"
        }
    )
    
    # Extract the actual state from the event dict
    actual_state = list(final_state.values())[0] if final_state else {}
    print(f"Workflow completed: {len(actual_state.get('completed_steps', []))} steps")
    print(f"Status: {actual_state.get('status', 'N/A')}")

asyncio.run(main())
```

### Examples

Run example workflows:

```bash
# Inside virtual environment (recommended)
source venv/bin/activate
python examples/langgraph_feature_development.py  # Parallel execution demo
python examples/langgraph_bug_fix.py              # Bug fix workflow
python examples/langgraph_resume_workflow.py      # Resume interrupted workflow
python examples/visualize_workflow.py             # Generate workflow diagrams

# Outside virtual environment (use python3)
python3 examples/langgraph_feature_development.py
python3 examples/simple_workflow.py
python examples/custom_workflow.py
python examples/ecommerce_catalog.py
python examples/agent_status_monitor.py
```

## 📋 Workflow Types

### 1. Feature Development
Complete feature implementation from requirements to deployment.

**Steps:**
1. Business Analyst - Requirements analysis
2. Developer - Architecture design
3. Developer - Implementation
4. QA Engineer - Testing
5. DevOps Engineer - Deployment setup
6. Technical Writer - Documentation

### 2. Bug Fix
Focused bug resolution with testing and documentation.

**Steps:**
1. QA Engineer - Bug analysis and reproduction
2. Developer - Fix implementation
3. QA Engineer - Regression testing
4. Technical Writer - Release notes

### 3. Infrastructure
Infrastructure design, implementation, and documentation.

**Steps:**
1. DevOps Engineer - Infrastructure design
2. DevOps Engineer - IaC implementation
3. QA Engineer - Infrastructure testing
4. Technical Writer - Operations documentation

### 4. Documentation
Comprehensive documentation creation and review.

**Steps:**
1. Business Analyst - Documentation requirements
2. Technical Writer - Documentation creation
3. Developer - Technical review

### 5. Analysis
Feasibility studies and technical analysis.

**Steps:**
1. Business Analyst - Requirements gathering
2. Developer - Technical feasibility
3. DevOps Engineer - Infrastructure assessment
4. Business Analyst - Final analysis report

## 🤖 Agent Capabilities

### Business Analyst
- Requirements analysis and documentation
- User story creation
- Acceptance criteria definition
- Feasibility assessment

### Developer
- Code implementation (Python, JavaScript, TypeScript)
- Architecture design
- Code review
- Technical documentation
- Supports: FastAPI, React, Django, Node.js

### QA Engineer
- Test suite creation
- Test execution
- Bug reporting
- Quality metrics
- Supports: pytest, Jest, Playwright

### DevOps Engineer
- Infrastructure as Code
- CI/CD pipeline configuration
- Deployment automation
- Monitoring setup
- Supports: Docker, Kubernetes, AWS, GitLab CI

### Technical Writer
- API documentation
- User guides
- Release notes
- Operations manuals
- Formats: Markdown, Confluence, OpenAPI

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_agent.py

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run individual test files
python tests/simple_test.py
python tests/test_file_writer.py
```

**Test Coverage:**
- Agent functionality and workflows
- File writer and format handling
- Response parsing and extraction
- Edge cases and error handling
- Integration tests

## 📁 Project Structure

```
llm-multi-agent-system/
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── base_agent.py    # Base agent class
│   │   ├── business_analyst.py
│   │   ├── developer.py
│   │   ├── qa_engineer.py
│   │   ├── devops_engineer.py
│   │   └── technical_writer.py
│   ├── orchestrator/        # Orchestration logic
│   │   ├── agent_orchestrator.py
│   │   ├── task_manager.py
│   │   └── workflow_engine.py
│   ├── config/              # Configuration
│   │   └── settings.py
│   └── utils/               # Utilities
│       └── file_writer.py
├── tests/                   # Test suite
├── examples/                # Example scripts
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
├── output/                  # Generated outputs
├── logs/                    # Log files
├── config.yaml              # Main configuration
├── .env.example             # Environment template
├── requirements.txt         # Dependencies
├── setup.py                 # Setup script
└── main.py                  # Entry point
```

## 📚 Documentation

Comprehensive guides in the `docs/` directory:

- **[START_HERE.md](docs/START_HERE.md)** - ⭐ Complete setup and getting started guide
- **[LangGraph Integration](docs/LANGGRAPH_INTEGRATION.md)** - Advanced orchestration with parallel execution
- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in 5 minutes
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[Agent Specifications](docs/AGENT_SPECS.md)** - Detailed agent capabilities
- **[Local-Only Mode](docs/LOCAL_ONLY_MODE.md)** - Privacy-first local execution
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[API Reference](docs/API_REFERENCE.md)** - Programmatic usage
- **[Tech Stack](docs/TECH_STACK.md)** - Technologies used
- **[Integrations](docs/INTEGRATIONS.md)** - Third-party integrations
- **[Testing Guide](docs/TESTING.md)** - Testing documentation
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Contributing](docs/CONTRIBUTING.md)** - Development guidelines
- **[Changelog](docs/CHANGELOG.md)** - Version history

## 🔒 Privacy & Security

### 100% Local Execution
- All processing happens on your machine
- No data sent to external services
- No API keys required (except dummy for local server)
- No internet connection needed after model download

### Security Features
- Local-only llama-server binding (127.0.0.1)
- No external network calls
- Workspace isolation
- Secure file handling

## 🎛️ Configuration

### Environment Variables (.env)

```bash
# Local LLM Server (REQUIRED)
OPENAI_API_BASE=http://127.0.0.1:8080/v1
OPENAI_API_KEY=not-needed
OPENAI_API_MODEL=devstral

# Optional: Workspace override
WORKSPACE=/path/to/workspace
```

### YAML Configuration (config.yaml)

```yaml
# Workspace settings
workspace: "."
output_directory: "./output"
log_level: "INFO"
log_file: "logs/agent_system.log"

# Execution settings
llm_timeout: 300
max_concurrent_agents: 5
task_retry_attempts: 3
task_timeout: 600

# Agent-specific configurations
agents:
  developer:
    enabled: true
    languages: [python, javascript, typescript]
  qa_engineer:
    enabled: true
    test_frameworks: [pytest, jest, playwright]
```

## 🛠️ Troubleshooting

### Common Issues

**"OPENAI_API_BASE not configured"**
```bash
echo "OPENAI_API_BASE=http://127.0.0.1:8080/v1" >> .env
```

**"Connection refused"**
```bash
# Ensure your local LLM server is running on port 8080
```

**Task timeout**
```yaml
# Increase in config.yaml
llm_timeout: 600
task_timeout: 900
```

For more solutions, see [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## 🌟 Use Cases

- **Rapid Prototyping** - Quickly generate full-stack applications
- **Code Generation** - Automated implementation of features
- **Documentation** - Auto-generate comprehensive docs
- **Testing** - Create complete test suites
- **Infrastructure** - Generate IaC and deployment configs
- **Analysis** - Technical feasibility studies
- **Learning** - Study AI-generated implementations

## 🚦 System Requirements

### Minimum
- **Python 3.12** (required)
- 16GB RAM
- 8-core CPU
- 50GB disk space

### Recommended
- **Python 3.12** (required)
- 32GB+ RAM
- Apple Silicon (M1/M2/M3) or NVIDIA GPU
- 100GB+ disk space

## 📊 Performance

- **Initial Response**: < 5 seconds
- **Agent Execution**: 10-60 seconds per agent
- **Full Workflow**: 5-30 minutes (complexity dependent)
- **Model Loading**: 30-60 seconds (first run)

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repo
git clone https://github.com/yourusername/llm-multi-agent-system.git
cd llm-multi-agent-system

# Create virtual environment with Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dev dependencies (inside venv, use python/pip)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **llama.cpp** - Local LLM inference
- **Devstral** - Default coding model
- **OpenAI** - API compatibility standard
- **FastAPI** - (Example framework in generated code)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/llm-multi-agent-system/issues)
- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)

## 🗺️ Roadmap

- [ ] Web UI for workflow management
- [ ] Additional agent types (Security, Data Engineer)
- [ ] Workflow visualization
- [ ] Integration with popular tools (Jira, Confluence)
- [ ] Multi-language support for prompts
- [ ] Workflow templates marketplace
- [ ] Real-time collaboration features

## 📈 Version History

See [CHANGELOG.md](docs/CHANGELOG.md) for detailed version history.

---

**Built with ❤️ for developers who value privacy and local control.**

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/yourusername/llm-multi-agent-system).
