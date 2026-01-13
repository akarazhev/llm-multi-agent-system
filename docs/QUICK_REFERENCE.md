# Quick Reference Card - LangGraph Multi-Agent System

## 🚀 Installation (60 seconds)

```bash
# 1. Install Python 3.12 (if needed)
brew install python@3.12  # macOS

# 2. Create virtual environment with Python 3.12
python3.12 -m venv venv

# 3. Activate it
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 4. Install dependencies (inside venv, use pip)
pip install -r requirements.txt

# Or use automated script
./scripts/setup_langgraph.sh
```

## 🏃 Run Examples (Inside Virtual Environment)

```bash
# Activate venv first
source venv/bin/activate

# Then run with python (not python3!)
python examples/langgraph_feature_development.py

# Or use direct execution
./examples/langgraph_feature_development.py

# Or helper script
./scripts/run_example.sh examples/langgraph_feature_development.py
```

## 📚 Available Examples

| Script | Description | Time |
|--------|-------------|------|
| `langgraph_feature_development.py` | Full feature workflow with parallel execution | ~10-15 min |
| `langgraph_bug_fix.py` | Bug fix workflow (4 steps) | ~8-12 min |
| `langgraph_resume_workflow.py` | Resume interrupted workflow demo | ~5 min |
| `visualize_workflow.py` | Generate workflow diagrams | ~1 min |

## 💻 Code Templates

### Simple Workflow
```python
#!/usr/bin/env python3
import asyncio
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator

async def main():
    orchestrator = LangGraphOrchestrator(cursor_workspace=".")
    
    result = await orchestrator.execute_feature_development(
        requirement="Your requirement here",
        context={"language": "python", "framework": "fastapi"}
    )
    
    actual_state = list(result.values())[0] if result else {}
    print(f"Status: {actual_state.get('status')}")
    print(f"Files: {len(actual_state.get('files_created', []))}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Resume Workflow
```python
# Start with specific ID
result = await orchestrator.execute_feature_development(
    requirement="Build API",
    thread_id="my_project_001"
)

# [Interrupted]

# Resume later
result = await orchestrator.execute_feature_development(
    requirement="",
    thread_id="my_project_001"  # Same ID resumes
)
```

## 🛠️ Common Commands

```bash
# Check Python 3.12 is installed
python3.12 --version  # Should be 3.12.x

# Create and activate venv with Python 3.12
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies (inside venv, use pip not pip3)
pip install -r requirements.txt

# Start LLM server
./scripts/start_llama_server.sh

# Check server status
./scripts/check_llama_server.sh

# Run examples (inside venv, use python not python3!)
python examples/langgraph_feature_development.py
python examples/visualize_workflow.py
```

## 🔧 Troubleshooting

### "python3: command not found"
```bash
# Check if Python 3 is installed
python --version

# Install Python 3.12
brew install python@3.12  # macOS
```

### "No module named 'langgraph'"
```bash
# Make sure venv is activated
source venv/bin/activate

# Then install
pip install langgraph langchain-core aiosqlite
```

### "Checkpoint database locked"
```bash
rm checkpoints.db  # Delete and start fresh
```

### Check what's happening
```bash
tail -f logs/agent_system.log
```

## 📊 Performance Comparison

| Feature | Custom | LangGraph |
|---------|--------|-----------|
| Execution Time | 15-20 min | 10-15 min ⚡ |
| State Persistence | ❌ | ✅ 💾 |
| Parallel Execution | ❌ | ✅ ⚡ |
| Resume Workflows | ❌ | ✅ 💾 |
| Visualization | ❌ | ✅ 📊 |

## 🎯 Key Features

- ⚡ **30-40% faster** with parallel execution
- 💾 **Resume workflows** after interruption
- 📊 **Visualize workflows** as diagrams
- 🔀 **Smart routing** based on outputs
- ⏰ **Time-travel debugging** through checkpoints
- 🔄 **Backward compatible** with existing agents

## 📖 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| `LANGGRAPH_QUICK_START.md` | Get started fast | 5 min |
| `docs/LANGGRAPH_COMPARISON.md` | Custom vs LangGraph | 15 min |
| `docs/LANGGRAPH_INTEGRATION.md` | Complete reference | 1 hour |
| `PYTHON3_COMPATIBILITY_UPDATE.md` | Python3 fixes | 10 min |

## 🎓 Learning Path

### Beginner (30 min)
1. Read: `VENV_SETUP_GUIDE.md` (understand venv workflow)
2. Read: `LANGGRAPH_QUICK_START.md`
3. Run: `python examples/langgraph_feature_development.py` (inside venv)
4. Modify: Change the requirement in the example

### Intermediate (2 hours)
1. Read: `docs/LANGGRAPH_COMPARISON.md`
2. Run: All example scripts
3. Create: Your own workflow

### Advanced (1 day)
1. Read: `docs/LANGGRAPH_INTEGRATION.md`
2. Build: Custom workflow graphs
3. Implement: Human-in-the-loop approvals

## 🔗 Quick Links

```bash
# Start here
cat LANGGRAPH_QUICK_START.md

# Compare approaches
cat docs/LANGGRAPH_COMPARISON.md

# Full guide
cat docs/LANGGRAPH_INTEGRATION.md

# Python3 compatibility
cat PYTHON3_COMPATIBILITY_UPDATE.md
```

## ✅ Pre-flight Checklist

- [ ] **Python 3.12 installed** (`python3.12 --version`)
- [ ] Virtual environment created with Python 3.12 (`python3.12 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Python verified inside venv (`python --version` shows 3.12.x)
- [ ] Dependencies installed inside venv (`pip install -r requirements.txt`)
- [ ] LLM server running (`./scripts/start_llama_server.sh`)
- [ ] Environment configured (`.env` file)

## 🚦 Quick Test

```bash
# 1. Create and activate venv with Python 3.12 (30 sec)
python3.12 -m venv venv
source venv/bin/activate

# 2. Verify Python version
python --version  # Should show 3.12.x

# 3. Install (30 sec)
pip install -r requirements.txt

# 4. Run example (2 min, inside venv use python)
python examples/langgraph_feature_development.py

# 5. Check output
ls output/

# Success! 🎉
```

## 📞 Get Help

```bash
# Show help for any example
python3 examples/langgraph_feature_development.py --help

# Run with helper script (shows Python version)
./scripts/run_example.sh examples/langgraph_feature_development.py

# Check logs
tail -f logs/agent_system.log
```

## 🎁 Bonus Tips

1. **Direct execution**: Add shebang, chmod +x, run with `./script.py`
2. **Use helper script**: Automatic Python detection
3. **Checkpoints**: Resume any workflow with same `thread_id`
4. **Visualization**: Generate diagrams to share with team
5. **Context is key**: More context = better results

---

**Last Updated:** January 13, 2026  
**Version:** 1.0.0 (LangGraph + Python3 Compatible)  
**Status:** ✅ Production Ready

**Quick Start:**
```bash
python3.12 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python examples/langgraph_feature_development.py
```
