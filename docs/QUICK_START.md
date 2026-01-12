# Quick Start Guide

## Prerequisites

1. **Python 3.11+**
   ```bash
   python --version
   ```

2. **Cursor CLI**
   - Install Cursor IDE from https://cursor.sh
   - Ensure CLI is accessible:
   ```bash
   cursor --version
   ```

3. **Git** (optional, for version control)

## Installation

### Step 1: Clone or Navigate to Project

```bash
cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` if needed (optional for basic usage).

### Step 5: Update Configuration

Edit `config.yaml` to set your workspace path:

```yaml
cursor_workspace: "/Users/andrey.karazhev/Developer/spg/llm-multi-agent-system"
```

## Running the System

### Interactive Mode

```bash
python main.py
```

Follow the prompts:
1. Enter your requirement (e.g., "Create a REST API for user authentication")
2. Select workflow type (1-5)
3. Wait for execution to complete
4. Check results in the `output/` directory

### Example Output

```
================================================================================
LLM Multi-Agent System - Cursor CLI Orchestration
================================================================================

Available Workflow Types:
  1. feature_development
  2. bug_fix
  3. infrastructure
  4. documentation
  5. analysis

================================================================================

Enter your requirement (or 'quit' to exit): Create a REST API for user management

Select workflow type:
  1. feature_development
  2. bug_fix
  3. infrastructure
  4. documentation
  5. analysis

Enter choice (1-5): 1

Executing feature_development workflow...
This may take several minutes depending on the complexity...

[Agent ba_001] Starting task: req_analysis
[Agent ba_001] Completed task: req_analysis
[Agent dev_001] Starting task: architecture_design
...
```

## Running Examples

### Simple Workflow

```bash
python examples/simple_workflow.py
```

This runs a predefined workflow for creating a REST API with JWT authentication.

### Custom Workflow

```bash
python examples/custom_workflow.py
```

This demonstrates how to create a custom workflow for an e-commerce platform.

### Agent Status Monitor

```bash
python examples/agent_status_monitor.py
```

This shows the current status of all agents in the system.

## Understanding the Output

### Console Output

- Real-time progress updates
- Task completion status
- Error messages (if any)
- Summary of results

### File Output

Results are saved in `output/` directory:

```
output/
└── workflow_feature_development_2024-01-12T15-30-00.json
```

Example output file:

```json
{
  "workflow_type": "feature_development",
  "requirement": "Create a REST API for user management",
  "completed_at": "2024-01-12T15:30:00",
  "total_tasks": 6,
  "tasks": {
    "req_analysis": {
      "task_id": "req_analysis",
      "description": "Analyze the requirement and create user stories",
      "completed": true,
      "error": null
    },
    ...
  }
}
```

## Common Use Cases

### 1. Feature Development

```bash
python main.py
```

**Requirement**: "Create a user authentication system with email verification"

**Workflow**: feature_development (option 1)

**Result**: Complete implementation including:
- Requirements analysis
- Architecture design
- Code implementation
- Test suite
- Infrastructure setup
- Documentation

### 2. Bug Fix

```bash
python main.py
```

**Requirement**: "Fix the memory leak in the data processing module"

**Workflow**: bug_fix (option 2)

**Result**:
- Bug analysis and reproduction
- Fix implementation
- Regression tests
- Release notes

### 3. Infrastructure Setup

```bash
python main.py
```

**Requirement**: "Set up Kubernetes deployment with auto-scaling"

**Workflow**: infrastructure (option 3)

**Result**:
- Infrastructure design
- IaC implementation (K8s manifests)
- Testing procedures
- Operations documentation

### 4. Documentation

```bash
python main.py
```

**Requirement**: "Create API documentation for the payment service"

**Workflow**: documentation (option 4)

**Result**:
- Documentation requirements
- Complete API docs
- Technical review

### 5. Feasibility Analysis

```bash
python main.py
```

**Requirement**: "Analyze feasibility of migrating to microservices architecture"

**Workflow**: analysis (option 5)

**Result**:
- Requirements analysis
- Technical feasibility assessment
- Infrastructure requirements
- Final recommendation report

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements
   - ❌ "Create an API"
   - ✅ "Create a REST API for user management with CRUD operations, JWT authentication, and PostgreSQL database"

2. **Include Context**: Mention technologies, constraints, and preferences
   - Language: Python, JavaScript, etc.
   - Framework: FastAPI, Express, Django, etc.
   - Database: PostgreSQL, MongoDB, etc.
   - Deployment: Docker, Kubernetes, AWS, etc.

3. **Choose Right Workflow**: Match workflow to your task type
   - New feature → feature_development
   - Fixing bugs → bug_fix
   - Setting up infra → infrastructure
   - Writing docs → documentation
   - Planning/analysis → analysis

4. **Monitor Logs**: Check `logs/agent_system.log` for detailed execution info

5. **Review Output**: Always review generated code and documentation before using in production

## Troubleshooting

### Issue: "Cursor command not found"

**Solution**: Add Cursor CLI to PATH or specify full path in config.yaml:

```yaml
cursor_cli_path: "/Applications/Cursor.app/Contents/Resources/app/bin/cursor"
```

### Issue: "Permission denied"

**Solution**: Ensure workspace directory has proper permissions:

```bash
chmod -R u+rw /path/to/workspace
```

### Issue: "Task timeout"

**Solution**: Increase timeout in config.yaml:

```yaml
cursor_timeout: 600  # 10 minutes
task_timeout: 900    # 15 minutes
```

### Issue: "Agent failed to complete task"

**Solution**:
1. Check logs: `logs/agent_system.log`
2. Verify requirement clarity
3. Ensure all dependencies are met
4. Try with simpler requirement first

## Next Steps

1. **Explore Examples**: Run all example scripts to understand capabilities
2. **Read Documentation**: Check `docs/CURSOR_CLI_ORCHESTRATION.md` for details
3. **Customize Configuration**: Adjust `config.yaml` for your needs
4. **Create Custom Workflows**: Build workflows specific to your projects
5. **Integrate with Tools**: Connect to Jira, GitLab, Confluence (future feature)

## Getting Help

- Check logs: `logs/agent_system.log`
- Review documentation: `docs/`
- Examine examples: `examples/`
- Verify configuration: `config.yaml`

## What's Next?

Now that you have the system running, try:

1. Running a simple workflow with the examples
2. Creating your own custom workflow
3. Monitoring agent status
4. Experimenting with different workflow types
5. Adjusting configuration for your specific needs

Happy orchestrating! 🚀
