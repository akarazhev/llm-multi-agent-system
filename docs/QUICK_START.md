# Quick Start Guide

Get up and running with the LLM Multi-Agent System in under 10 minutes.

## Prerequisites

Before you begin, ensure you have:

### Required

1. **Python 3.12**
   ```bash
   python3.12 --version
   # Should output: Python 3.12.x
   ```

2. **llama.cpp with llama-server**
   ```bash
   # macOS
   brew install llama.cpp
   
   # Or build from source
   git clone https://github.com/ggerganov/llama.cpp
   cd llama.cpp && make
   ```

3. **16GB+ RAM** (32GB recommended for better performance)

4. **50GB+ free disk space** (for models and outputs)

### Optional

- **Git** - For cloning the repository
- **GPU** - Apple Silicon (M1/M2/M3) or NVIDIA GPU for faster inference
- **VSCode/Cursor IDE** - For development

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/llm-multi-agent-system.git
cd llm-multi-agent-system

# Run automated setup
python setup.py
```

The setup script will:
- ✅ Check Python version
- ✅ Verify llama.cpp installation
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Create configuration files
- ✅ Verify installation

### Option 2: Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/llm-multi-agent-system.git
cd llm-multi-agent-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env

# 6. Edit .env file
nano .env  # or your preferred editor
```

## Configuration

### 1. Environment Variables (.env)

Create and configure your `.env` file:

```bash
# Local LLM Server Configuration (REQUIRED)
OPENAI_API_BASE=http://127.0.0.1:8080/v1
OPENAI_API_KEY=not-needed
OPENAI_API_MODEL=devstral

# Optional: Override workspace path
CURSOR_WORKSPACE=/path/to/your/workspace

# Optional: Agent configuration path
AGENT_CONFIG_PATH=config.yaml
```

**Important Notes:**
- `OPENAI_API_BASE` must point to your local llama-server
- `OPENAI_API_KEY` can be any value (not used for local server)
- `OPENAI_API_MODEL` should match your loaded model name

### 2. YAML Configuration (config.yaml)

Edit `config.yaml` to customize the system:

```yaml
# Workspace Settings
cursor_workspace: "."  # Current directory or specify path
output_directory: "./output"

# Logging
log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR
log_file: "logs/agent_system.log"

# LLM Server
llm_timeout: 300  # seconds

# Execution Settings
max_concurrent_agents: 5
task_retry_attempts: 3
task_timeout: 600  # seconds

# Message Bus
enable_message_bus: true
enable_task_persistence: false

# Agent Configurations
agents:
  business_analyst:
    enabled: true
    config:
      jira_integration: false
      confluence_integration: false
  
  developer:
    enabled: true
    config:
      languages:
        - python
        - javascript
        - typescript
      frameworks:
        - fastapi
        - react
        - django
      gitlab_integration: false
  
  qa_engineer:
    enabled: true
    config:
      test_frameworks:
        - pytest
        - jest
        - playwright
      coverage_threshold: 80
  
  devops_engineer:
    enabled: true
    config:
      platforms:
        - docker
        - kubernetes
        - aws
      ci_cd_tools:
        - gitlab-ci
        - github-actions
  
  technical_writer:
    enabled: true
    config:
      formats:
        - markdown
        - confluence
        - openapi
      style_guide: "google"
```

## Starting the System

### Step 1: Start Local LLM Server

```bash
# Start llama-server
./scripts/start_llama_server.sh

# Wait for startup message:
# "Server listening on http://127.0.0.1:8080"
```

**Verify server is running:**
```bash
# Check server status
./scripts/check_llama_server.sh

# Or manually
curl http://127.0.0.1:8080/v1/models
```

### Step 2: Run the Multi-Agent System

#### Interactive Mode

```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Run the system
python main.py
```

You'll see:
```
================================================================================
LLM Multi-Agent System - Local LLM Orchestration
================================================================================

Available Workflow Types:
  1. feature_development
  2. bug_fix
  3. infrastructure
  4. documentation
  5. analysis

================================================================================

Enter your requirement (or 'quit' to exit): _
```

#### Example Session

```
Enter your requirement: Create a REST API for user authentication with JWT tokens

Select workflow type:
  1. feature_development
  2. bug_fix
  3. infrastructure
  4. documentation
  5. analysis

Enter choice (1-5): 1

Executing feature_development workflow...
This may take several minutes depending on the complexity...

[ba_001] Starting task: feature_development_1_20240115103000
[ba_001] Completed task: feature_development_1_20240115103000
[dev_001] Starting task: feature_development_2_20240115103045
[dev_001] Completed task: feature_development_2_20240115103045
[dev_001] Starting task: feature_development_3_20240115103130
...

================================================================================
WORKFLOW COMPLETED SUCCESSFULLY
================================================================================

Workflow Type: feature_development
Total Tasks: 6
Completed At: 2024-01-15T10:35:00

Task Results:

  Task: feature_development_1_20240115103000
  Status: ✓ Completed

  Task: feature_development_2_20240115103045
  Status: ✓ Completed

...

Results saved to: output/workflow_feature_development_2024-01-15T10-35-00.json

================================================================================
```

## Running Examples

The project includes several example scripts:

### 1. Simple Workflow

```bash
python examples/simple_workflow.py
```

Creates a REST API with JWT authentication using the feature development workflow.

### 2. Custom Workflow

```bash
python examples/custom_workflow.py
```

Demonstrates creating a custom workflow for specific requirements.

### 3. E-commerce Catalog

```bash
python examples/ecommerce_catalog.py
```

Generates a complete e-commerce product catalog system.

### 4. Blog Platform

```bash
python examples/blog_platform.py
```

Creates a blog platform with posts, comments, and user management.

### 5. Agent Status Monitor

```bash
python examples/agent_status_monitor.py
```

Shows real-time status of all agents in the system.

## Understanding the Output

### Console Output

The system provides real-time progress updates:

```
[agent_id] Starting task: task_id
[agent_id] Processing: description
[agent_id] Created 3 files
[agent_id] Completed task: task_id
```

**Log Levels:**
- `INFO`: Normal operation
- `WARNING`: Non-critical issues
- `ERROR`: Failures requiring attention

### File Output

#### 1. Workflow Results (JSON)

Location: `output/workflow_<type>_<timestamp>.json`

```json
{
  "workflow_id": "workflow_20240115_103000",
  "workflow_completed": true,
  "total_tasks": 6,
  "completed_at": "2024-01-15T10:35:00",
  "tasks": {
    "feature_development_1": {
      "task_id": "feature_development_1",
      "description": "Analyze requirements",
      "context": {...},
      "completed_at": "2024-01-15T10:31:00",
      "result": {
        "status": "completed",
        "files_created": [...]
      }
    }
  }
}
```

#### 2. Workflow Summary (Markdown)

Location: `output/workflow_summary_<workflow_id>.md`

```markdown
# Workflow Summary: workflow_20240115_103000

**Completed at:** 2024-01-15T10:35:00
**Total tasks:** 6
**Status:** ✓ Completed

## Generated Files

### feature_development_1
**Agent:** business_analyst
**Description:** Analyze requirements
- `generated/requirements/user_stories.md`
- `generated/requirements/acceptance_criteria.md`

...
```

#### 3. Generated Files

Location: `output/generated/<task_id>/<agent_role>/`

Example structure:
```
output/generated/
└── feature_development_1_20240115103000/
    ├── business_analyst/
    │   ├── requirements.md
    │   └── user_stories.md
    ├── developer/
    │   ├── api/
    │   │   ├── main.py
    │   │   └── auth.py
    │   └── tests/
    │       └── test_auth.py
    └── technical_writer/
        └── API_DOCUMENTATION.md
```

### Log Files

Location: `logs/agent_system.log`

```
2024-01-15 10:30:00,123 - __main__ - INFO - Starting Multi-Agent System
2024-01-15 10:30:00,456 - orchestrator - INFO - Initialized 5 agents
2024-01-15 10:30:15,789 - ba_001 - INFO - Starting task: feature_development_1
...
```

## Common Workflows

### 1. Feature Development

**Use Case:** Implement a complete new feature

**Example:**
```
Requirement: Create a REST API for user management with CRUD operations, 
             JWT authentication, and PostgreSQL database

Workflow: feature_development (option 1)
```

**What You Get:**
- ✅ Requirements analysis and user stories
- ✅ System architecture design
- ✅ Complete implementation (API endpoints, models, authentication)
- ✅ Test suite (unit tests, integration tests)
- ✅ Deployment configuration (Docker, docker-compose)
- ✅ API documentation

**Duration:** 10-20 minutes

### 2. Bug Fix

**Use Case:** Fix a bug with tests and documentation

**Example:**
```
Requirement: Fix memory leak in data processing module when handling 
             large datasets

Workflow: bug_fix (option 2)
```

**What You Get:**
- ✅ Bug analysis and reproduction steps
- ✅ Root cause identification
- ✅ Fix implementation
- ✅ Regression tests
- ✅ Updated documentation

**Duration:** 5-10 minutes

### 3. Infrastructure Setup

**Use Case:** Set up deployment infrastructure

**Example:**
```
Requirement: Set up Kubernetes deployment with auto-scaling, 
             monitoring, and CI/CD pipeline

Workflow: infrastructure (option 3)
```

**What You Get:**
- ✅ Infrastructure design
- ✅ Kubernetes manifests (deployments, services, ingress)
- ✅ Helm charts
- ✅ CI/CD pipeline configuration
- ✅ Monitoring setup
- ✅ Operations documentation

**Duration:** 10-15 minutes

### 4. Documentation

**Use Case:** Create comprehensive documentation

**Example:**
```
Requirement: Create API documentation for the payment service including 
             OpenAPI spec, user guide, and examples

Workflow: documentation (option 4)
```

**What You Get:**
- ✅ OpenAPI/Swagger specification
- ✅ API reference documentation
- ✅ User guide with examples
- ✅ Integration guide
- ✅ Troubleshooting section

**Duration:** 5-10 minutes

### 5. Technical Analysis

**Use Case:** Feasibility study or technical assessment

**Example:**
```
Requirement: Analyze feasibility of migrating from monolith to 
             microservices architecture

Workflow: analysis (option 5)
```

**What You Get:**
- ✅ Current state analysis
- ✅ Technical feasibility assessment
- ✅ Cost-benefit analysis
- ✅ Migration strategy
- ✅ Risk assessment
- ✅ Recommendations

**Duration:** 10-15 minutes

## Best Practices

### 1. Write Clear Requirements

**❌ Poor:**
```
Create an API
```

**✅ Good:**
```
Create a REST API for user management with:
- User registration and login
- JWT token authentication
- Password reset functionality
- User profile management (CRUD)
- PostgreSQL database
- Python/FastAPI framework
- pytest test coverage
```

### 2. Specify Context

Include relevant technical details:
- **Language**: Python, JavaScript, TypeScript, Go
- **Framework**: FastAPI, Express, Django, React
- **Database**: PostgreSQL, MongoDB, MySQL
- **Platform**: Docker, Kubernetes, AWS, GCP
- **Testing**: pytest, Jest, Playwright
- **CI/CD**: GitHub Actions, GitLab CI

### 3. Choose Appropriate Workflow

- **New feature** → feature_development
- **Fixing bugs** → bug_fix
- **Infrastructure** → infrastructure
- **Documentation** → documentation
- **Planning/research** → analysis

### 4. Review Generated Code

Always review and test generated code before production use:
1. Check for security issues
2. Verify business logic
3. Run tests
4. Review dependencies
5. Validate configurations

### 5. Monitor Progress

- Watch console output for progress
- Check `logs/agent_system.log` for details
- Monitor llama-server logs if issues occur

## Testing Your Installation

### Run the Test Suite

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run specific test
python tests/simple_test.py

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

**Expected Output:**
```
tests/test_agent.py::test_agent_initialization PASSED
tests/test_file_writer.py::test_parse_code_blocks PASSED
tests/test_file_writer.py::test_extract_file_structure PASSED
...

====== 15 passed in 2.34s ======
```

### Verify Individual Components

```bash
# Test file writer
python tests/test_file_writer.py

# Test response parsing
python tests/test_all_formats.py

# Test nested blocks
python tests/test_nested_blocks.py
```

## Troubleshooting

### Issue: "OPENAI_API_BASE not configured"

**Cause:** Environment variable not set

**Solution:**
```bash
# Add to .env
echo "OPENAI_API_BASE=http://127.0.0.1:8080/v1" >> .env
echo "OPENAI_API_KEY=not-needed" >> .env
echo "OPENAI_API_MODEL=devstral" >> .env

# Or export directly
export OPENAI_API_BASE=http://127.0.0.1:8080/v1
```

### Issue: "Connection refused"

**Cause:** llama-server not running

**Solution:**
```bash
# Start the server
./scripts/start_llama_server.sh

# Verify it's running
curl http://127.0.0.1:8080/health
```

### Issue: "ModuleNotFoundError"

**Cause:** Dependencies not installed or wrong Python environment

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Task timeout"

**Cause:** Task taking longer than configured timeout

**Solution:**
```yaml
# Increase timeout in config.yaml
cursor_timeout: 600  # 10 minutes
task_timeout: 900    # 15 minutes
```

### Issue: Slow Performance

**Cause:** Limited resources or CPU-only inference

**Solution:**
```bash
# Check if GPU is being used
./scripts/check_llama_server.sh

# For Apple Silicon, ensure Metal is enabled
export LLAMA_GPU_LAYERS=99

# For CPU-only, reduce context size
export LLAMA_CTX_SIZE=4096
```

### Issue: Out of Memory

**Cause:** Model too large for available RAM

**Solution:**
```bash
# Use smaller quantization
export LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"

# Reduce context size
export LLAMA_CTX_SIZE=4096

# Reduce GPU layers (offload less to GPU)
export LLAMA_GPU_LAYERS=32
```

## Next Steps

Now that you're set up, explore more:

1. **Try Examples**
   ```bash
   python examples/simple_workflow.py
   python examples/blog_platform.py
   ```

2. **Read Documentation**
   - [Architecture](ARCHITECTURE.md) - System design
   - [API Reference](API_REFERENCE.md) - Programmatic usage
   - [Testing Guide](TESTING.md) - Testing details
   - [Deployment](DEPLOYMENT.md) - Production deployment

3. **Create Custom Workflows**
   - Study example workflows
   - Create your own templates
   - Customize agent prompts

4. **Monitor Performance**
   - Review generated code quality
   - Measure workflow execution times
   - Optimize configuration

5. **Contribute**
   - Report issues
   - Suggest improvements
   - Submit pull requests

## Getting Help

- **Documentation**: Check `docs/` directory
- **Examples**: Review `examples/` directory
- **Logs**: Check `logs/agent_system.log`
- **Issues**: Report on GitHub

## Quick Reference

```bash
# Start llama-server
./scripts/start_llama_server.sh

# Stop llama-server
./scripts/stop_llama_server.sh

# Check server status
./scripts/check_llama_server.sh

# Run system
python main.py

# Run tests
python -m pytest tests/ -v

# View logs
tail -f logs/agent_system.log

# View llama-server logs
tail -f logs/llama-server.log
```

Happy orchestrating! 🚀
