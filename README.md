# LLM Multi-Agent System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A production-ready multi-agent orchestration system powered by local LLMs for automated software development workflows.

## 🎯 Overview

This system orchestrates specialized AI agents that collaborate to handle complete software development lifecycles—from requirements analysis to deployment and documentation. Built with privacy-first principles, it runs **100% locally** using llama.cpp, ensuring no data leaves your machine.

### Key Features

- 🤖 **5 Specialized AI Agents** - Business Analyst, Developer, QA Engineer, DevOps Engineer, Technical Writer
- 🔄 **Automated Workflow Orchestration** - Predefined templates for common development scenarios
- 🏠 **100% Local Execution** - No cloud APIs, complete data privacy, zero costs
- 📋 **Flexible Workflow Engine** - Custom workflows or use predefined templates
- 🔧 **Production-Ready** - Comprehensive error handling, logging, and monitoring
- 📊 **Real-time Status Tracking** - Monitor agent progress and task completion
- 🧪 **Fully Tested** - Comprehensive test suite included

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

- **Python 3.11+**
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
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start local LLM server
./scripts/start_llama_server.sh

# Run the system
python main.py
```

### Configuration

Edit `config.yaml`:

```yaml
cursor_workspace: "."  # Your workspace path
log_level: "INFO"
cursor_timeout: 300
max_concurrent_agents: 5

# Agent configurations
agents:
  developer:
    languages: [python, javascript, typescript]
  qa_engineer:
    test_frameworks: [pytest, jest, playwright]
```

Edit `.env`:

```bash
OPENAI_API_BASE=http://127.0.0.1:8080/v1
OPENAI_API_KEY=not-needed
OPENAI_API_MODEL=devstral
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

### Programmatic Usage

```python
import asyncio
from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType

async def main():
    orchestrator = AgentOrchestrator(cursor_workspace=".")
    workflow_engine = WorkflowEngine(orchestrator)
    
    result = await workflow_engine.execute_workflow(
        workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
        requirement="Create REST API for user authentication with JWT",
        context={
            "language": "python",
            "framework": "fastapi"
        }
    )
    
    print(f"Workflow completed: {result['result']['total_tasks']} tasks")

asyncio.run(main())
```

### Examples

Run example workflows:

```bash
# Simple workflow
python examples/simple_workflow.py

# Custom workflow
python examples/custom_workflow.py

# E-commerce catalog generator
python examples/ecommerce_catalog.py

# Monitor agents
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

- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in 5 minutes
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[Local-Only Mode](docs/LOCAL_ONLY_MODE.md)** - Privacy-first local execution
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[API Reference](docs/API_REFERENCE.md)** - Programmatic usage
- **[Testing Guide](docs/TESTING.md)** - Testing documentation
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Contributing](docs/CONTRIBUTING.md)** - Development guidelines

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
CURSOR_WORKSPACE=/path/to/workspace
```

### YAML Configuration (config.yaml)

```yaml
# Workspace settings
cursor_workspace: "."
output_directory: "./output"
log_level: "INFO"
log_file: "logs/agent_system.log"

# Execution settings
cursor_timeout: 300
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
./scripts/start_llama_server.sh
```

**Task timeout**
```yaml
# Increase in config.yaml
cursor_timeout: 600
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
- Python 3.11+
- 16GB RAM
- 8-core CPU
- 50GB disk space

### Recommended
- Python 3.11+
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

# Install dev dependencies
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

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

**Built with ❤️ for developers who value privacy and local control.**

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/yourusername/llm-multi-agent-system).
