# LangGraph Quick Start Guide

Get started with LangGraph orchestration in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies (30 seconds)

```bash
# Option 1: Automated setup
./scripts/setup_langgraph.sh

# Option 2: Manual
pip install -r requirements.txt
```

### 2. Start Local LLM Server (if not running)

```bash
./scripts/start_llama_server.sh
```

### 3. Run Your First LangGraph Workflow (2 minutes)

```bash
python examples/langgraph_feature_development.py
```

That's it! You now have:
- ✅ Parallel agent execution (30-40% faster)
- ✅ State persistence (resume interrupted workflows)
- ✅ Checkpoint-based time travel
- ✅ Workflow visualization

---

## 📝 Your First LangGraph Script

### Simple Example

Create `my_workflow.py`:

```python
import asyncio
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator

async def main():
    # Initialize orchestrator
    orchestrator = LangGraphOrchestrator(cursor_workspace=".")
    
    # Run feature development workflow
    result = await orchestrator.execute_feature_development(
        requirement="Create a REST API for a todo list application",
        context={
            "language": "python",
            "framework": "fastapi",
            "database": "sqlite"
        }
    )
    
    # Show results
    actual_state = list(result.values())[0] if result else {}
    print(f"\n✅ Workflow completed!")
    print(f"Status: {actual_state.get('status')}")
    print(f"Files created: {len(actual_state.get('files_created', []))}")
    
    # List some files
    for file in actual_state.get('files_created', [])[:5]:
        print(f"  • {file}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
# Inside venv
python my_workflow.py

# Outside venv
python3 my_workflow.py
```

---

## 🎯 Common Use Cases

### Use Case 1: Feature Development

```python
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator

orchestrator = LangGraphOrchestrator(cursor_workspace=".")

result = await orchestrator.execute_feature_development(
    requirement="""
    Create a user authentication system with:
    - JWT tokens
    - Password hashing
    - Email verification
    - Password reset
    """,
    context={
        "language": "python",
        "framework": "fastapi",
        "database": "postgresql"
    }
)
```

**What happens:**
1. Business Analyst → Requirements analysis
2. Developer → Architecture design
3. Developer → Implementation
4. **[PARALLEL]** QA Engineer + DevOps Engineer
5. Technical Writer → Documentation

**Time saved:** 30-40% vs sequential execution

---

### Use Case 2: Bug Fix

```python
result = await orchestrator.execute_bug_fix(
    requirement="Fix login token expiration bug",
    bug_description="""
    Current: Tokens never expire
    Expected: Expire after 1 hour
    Impact: Security vulnerability
    """
)
```

**What happens:**
1. QA Engineer → Bug analysis
2. Developer → Bug fix
3. QA Engineer → Regression testing
4. Technical Writer → Release notes

---

### Use Case 3: Resume Interrupted Workflow

```python
# Start workflow with specific ID
result = await orchestrator.execute_feature_development(
    requirement="Build API",
    thread_id="my_api_project_001"
)

# [Interrupted with Ctrl+C]

# Resume later (same thread_id)
result = await orchestrator.execute_feature_development(
    requirement="",  # Not used when resuming
    thread_id="my_api_project_001"  # Same ID = resume from checkpoint
)
```

---

## 🔍 Monitor Progress

### Real-time Progress Tracking

```python
app = await orchestrator.build_feature_development_graph()
config = {"configurable": {"thread_id": "my_workflow"}}

# Stream events for real-time updates
async for event in app.astream(initial_state, config):
    for node_name, node_state in event.items():
        print(f"✓ Completed: {node_name}")
        step = node_state.get('current_step', 'unknown')
        files = len(node_state.get('files_created', []))
        print(f"  Current step: {step}")
        print(f"  Files so far: {files}")
```

---

## 📊 Visualize Your Workflow

```bash
python3 examples/visualize_workflow.py
```

This generates:
- Mermaid diagram code (paste into https://mermaid.live/)
- ASCII art representation
- Detailed workflow structure

**Example Output:**
```
    ┌─────────────────────┐
    │  Business Analyst   │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │  Developer          │
    │  (Implementation)   │
    └──────────┬──────────┘
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌──────────────┐  ┌──────────────┐
│ QA Engineer  │  │ DevOps Eng.  │
│  PARALLEL    │  │  EXECUTION   │
└──────────────┘  └──────────────┘
```

---

## 🐛 Debug with Time Travel

```python
# Get all checkpoints for a workflow
app = await orchestrator.build_feature_development_graph()
config = {"configurable": {"thread_id": "workflow_123"}}

checkpoints = []
async for checkpoint in app.aget_state_history(config):
    checkpoints.append(checkpoint)
    print(f"Step: {checkpoint.values['current_step']}")
    print(f"Time: {checkpoint.values.get('started_at', 'N/A')}")

# Inspect state at specific checkpoint
state_at_step_3 = checkpoints[3]
print("\nWhat was implemented?")
print(state_at_step_3.values.get('implementation'))

# Files created up to this point
print("\nFiles at this checkpoint:")
for file in state_at_step_3.values.get('files_created', []):
    print(f"  • {file}")
```

---

## ⚙️ Configuration

### Basic Configuration

```python
orchestrator = LangGraphOrchestrator(
    cursor_workspace=".",              # Your project directory
    config={                           # Same config as before
        "agents": {
            "developer": {
                "languages": ["python", "javascript"],
                "frameworks": ["fastapi", "react"]
            }
        }
    },
    checkpoint_db="./checkpoints.db"   # Where to store state
)
```

### Advanced: Custom Checkpoint Location

```python
orchestrator = LangGraphOrchestrator(
    cursor_workspace=".",
    checkpoint_db="/path/to/my/checkpoints.db"
)
```

---

## 💡 Pro Tips

### 1. Use Descriptive Thread IDs

```python
# Bad
thread_id = "workflow_001"

# Good
thread_id = f"ecommerce_api_{datetime.now().strftime('%Y%m%d_%H%M')}"
```

### 2. Check Checkpoint Database

```bash
# See checkpoint database size
ls -lh checkpoints.db

# Clean up old checkpoints (optional)
rm checkpoints.db  # Loses resume capability
```

### 3. Handle Interruptions Gracefully

```python
try:
    result = await orchestrator.execute_feature_development(
        requirement="Build API",
        thread_id="my_workflow"
    )
except KeyboardInterrupt:
    print("\nWorkflow interrupted but saved!")
    print("Resume with: thread_id='my_workflow'")
except Exception as e:
    print(f"Error: {e}")
    # Check logs for details
```

### 4. Pass Context for Better Results

```python
context = {
    "language": "python",
    "framework": "fastapi",
    "database": "postgresql",
    "test_framework": "pytest",
    "test_coverage": 80,
    "deployment": "docker",
    "authentication": "jwt",
    "api_style": "restful"
}

result = await orchestrator.execute_feature_development(
    requirement="Build API",
    context=context  # More context = better results
)
```

---

## 🎓 Learn More

### Example Scripts

All examples are ready to run:

```bash
# Feature development with parallel execution
python examples/langgraph_feature_development.py

# Bug fix workflow
python examples/langgraph_bug_fix.py

# Resume interrupted workflow
python examples/langgraph_resume_workflow.py

# Generate workflow visualization
python examples/visualize_workflow.py
```

### Documentation

- **[Full Integration Guide](docs/LANGGRAPH_INTEGRATION.md)** - Complete reference
- **[Comparison Guide](docs/LANGGRAPH_COMPARISON.md)** - LangGraph vs Custom
- **[Architecture](docs/ARCHITECTURE.md)** - System design

---

## 🔧 Troubleshooting

### Issue: "No module named 'langgraph'"

**Solution:**
```bash
# Inside virtual environment (recommended)
source venv/bin/activate
pip install langgraph langchain-core aiosqlite

# Outside virtual environment (not recommended)
pip3 install --user langgraph langchain-core aiosqlite
```

### Issue: Checkpoint database locked

**Solution:**
```bash
# Delete and start fresh
rm checkpoints.db

# Or use different database
orchestrator = LangGraphOrchestrator(
    cursor_workspace=".",
    checkpoint_db="./checkpoints_new.db"
)
```

### Issue: Workflow seems stuck

**Check logs:**
```bash
tail -f logs/agent_system.log
```

**Likely cause:** One agent taking longer than expected. This is normal.

### Issue: Want to see what's happening

**Check which Python is being used:**
```bash
# Outside venv
python3.12 --version  # Should be 3.12.x

# Inside venv
python --version  # Should be 3.12.x
```

**Add progress monitoring:**
```python
app = await orchestrator.build_feature_development_graph()
config = {"configurable": {"thread_id": "my_workflow"}}

async for event in app.astream(initial_state, config):
    print(f"Event: {event}")  # See real-time updates
```

---

## ✅ Checklist

Before running your first workflow:

- [ ] **Python 3.12 installed** (`python3.12 --version`)
- [ ] Virtual environment created with Python 3.12 (`python3.12 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Python version verified inside venv (`python --version` shows 3.12.x)
- [ ] Dependencies installed inside venv (`pip install -r requirements.txt`)
- [ ] Local LLM server running (`./scripts/start_llama_server.sh`)
- [ ] Environment configured (`.env` file set up)
- [ ] Workspace directory exists

---

## 🎉 Next Steps

1. **Run the examples** to see LangGraph in action
   ```bash
   # Inside venv
   source venv/bin/activate
   python examples/langgraph_feature_development.py
   ```

2. **Create your own workflow** by copying an example
   ```bash
   cp examples/langgraph_feature_development.py my_workflow.py
   # Edit my_workflow.py with your requirements
   python my_workflow.py  # inside venv
   ```

3. **Explore advanced features**
   - Custom workflow graphs
   - Human-in-the-loop approvals
   - Multi-level conditional routing
   - Error recovery strategies

4. **Read the full guide**
   - [LangGraph Integration Guide](docs/LANGGRAPH_INTEGRATION.md)
   - [Comparison with Custom Orchestration](docs/LANGGRAPH_COMPARISON.md)

---

## 📚 Quick Reference

### Import
```python
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator
```

### Initialize
```python
orchestrator = LangGraphOrchestrator(cursor_workspace=".")
```

### Execute
```python
result = await orchestrator.execute_feature_development(
    requirement="Your requirement here",
    context={"language": "python"}
)
```

### Resume
```python
result = await orchestrator.execute_feature_development(
    requirement="",
    thread_id="workflow_to_resume"
)
```

### Monitor
```python
app = await orchestrator.build_feature_development_graph()
async for event in app.astream(state, config):
    print(event)
```

---

**Ready to build?**
```bash
# Create and activate venv with Python 3.12
python3.12 -m venv venv && source venv/bin/activate

# Then run
python examples/langgraph_feature_development.py
```

For questions, check the [full documentation](docs/LANGGRAPH_INTEGRATION.md) or open a GitHub issue.

Happy coding! 🚀
