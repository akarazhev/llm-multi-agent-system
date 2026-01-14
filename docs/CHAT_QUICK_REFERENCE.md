# Interactive Chat - Quick Reference

## One-Minute Guide

### Enable Chat Display (Default)

```python
from src.orchestrator import LangGraphOrchestrator

# Chat is enabled by default!
orchestrator = LangGraphOrchestrator(workspace=".")
await orchestrator.execute_feature_development(requirement="...")
```

### Try the Demo

```bash
python examples/interactive_chat_workflow.py
# Select option 2 for instant demo (no llama-server needed)
```

## Visual Legend

### Agent Colors

| Agent | Color | Role |
|-------|-------|------|
| Business Analyst | 🔵 Cyan | Requirements & User Stories |
| Developer | 🟢 Green | Architecture & Implementation |
| QA Engineer | 🟡 Yellow | Testing & Quality |
| DevOps Engineer | 🟣 Magenta | Infrastructure & Deployment |
| Technical Writer | 🔵 Blue | Documentation |
| System | ⚪ White | System Messages |

### Icons

| Icon | Meaning |
|------|---------|
| 🚀 | Start / Initiation |
| ⚙️ | Working / In Progress |
| 🤔 | Thinking / Planning |
| ✅ | Completed Successfully |
| ❌ | Error |
| 💬 | Chat Message |
| 🔄 | Handoff / Transfer |
| ℹ️ | Information |
| 📄 | File Operation |
| 📊 | Progress / Status |

## Quick Examples

### Basic Chat Display

```python
from src.utils.chat_display import AgentChatDisplay

chat = AgentChatDisplay()
chat.agent_message("developer", "Starting work...", "thinking")
chat.agent_completed("developer", "Done!", ["file1.py", "file2.py"])
```

### Progress Tracking

```python
from src.utils.chat_display import ProgressTracker

tracker = ProgressTracker(total_steps=5)
tracker.update("step_name")  # Shows progress bar
```

### Disable Chat

```python
orchestrator = LangGraphOrchestrator(
    workspace=".",
    enable_chat_display=False  # Disable
)
```

## Output Examples

### Agent Message
```
🤔 Business Analyst:
  Analyzing requirements...
  Creating user stories.
```

### Agent Action
```
⚙️ Developer is implementing the API
  Writing FastAPI endpoints and models
```

### Task Completion
```
✅ QA Engineer completed task
  Created 45 tests with 95% coverage
  📄 Files created: 3
    • test_api.py
    • test_models.py
    • test_integration.py
```

### Handoff
```
🔄 Business Analyst → Developer
  Requirements complete. Ready for design.
```

### Progress Bar
```
Progress: ████████████████░░░░░░░░░░░░░░░░░░░░ 40%
Current: implementation
```

### Workflow Status
```
ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: running
  Current Step: implementation
  Progress: 3 steps completed
  ████████████████████░░░░░░░░ 50%
```

## API Quick Reference

### AgentChatDisplay Methods

```python
chat = AgentChatDisplay()

# Display methods
chat.print_header("Title")
chat.agent_message(agent_id, message, message_type, to_agent)
chat.agent_action(agent_id, action, details)
chat.agent_thinking(agent_id, thought)
chat.agent_completed(agent_id, summary, files_created)
chat.agent_error(agent_id, error)
chat.inter_agent_communication(from_agent, to_agent, message)
chat.system_message(message, message_type)
chat.workflow_status(workflow_id, status, step, completed_steps)

# Summary and export
chat.conversation_summary()
chat.save_chat_log(path)
```

### Message Types

- `"start"` - Workflow initiation
- `"thinking"` - Agent reasoning
- `"working"` - Active work
- `"completed"` - Task done
- `"error"` - Error state
- `"info"` - Information
- `"handoff"` - Inter-agent transfer

## Configuration

### With Timestamps

```python
chat = AgentChatDisplay(
    show_timestamps=True,      # [HH:MM:SS] prefix
    show_agent_icons=True      # Use emoji icons
)
```

### Without Timestamps

```python
chat = AgentChatDisplay(show_timestamps=False)
```

## File Locations

### Chat Logs

```
workspace/
  output/
    chat_log_workflow_YYYYMMDD_HHMMSS.json    # Chat history
    langgraph_workflow_YYYYMMDD_HHMMSS.json   # Workflow results
```

### Examples

```
examples/
  interactive_chat_workflow.py    # Interactive demo
```

### Documentation

```
docs/
  INTERACTIVE_CHAT.md            # Full guide
  CHAT_QUICK_REFERENCE.md        # This file
```

## Common Tasks

### 1. Run Demo

```bash
python examples/interactive_chat_workflow.py
# Option 2 = instant demo
```

### 2. Enable in Code

```python
orchestrator = LangGraphOrchestrator(
    workspace=".",
    enable_chat_display=True  # Already default
)
```

### 3. Disable in Code

```python
orchestrator = LangGraphOrchestrator(
    workspace=".",
    enable_chat_display=False
)
```

### 4. Manual Chat Display

```python
from src.utils.chat_display import AgentChatDisplay

chat = AgentChatDisplay()
chat.print_header("My Workflow")
# ... use chat methods ...
chat.save_chat_log(Path("./chat.json"))
```

### 5. Access from Orchestrator

```python
orchestrator = LangGraphOrchestrator(workspace=".")

if orchestrator.chat_display:
    orchestrator.chat_display.system_message("Custom message")
```

## Troubleshooting

### No Colors?

Install colorama:
```bash
pip install colorama
```

### No Output?

Check if chat is enabled:
```python
print(orchestrator.enable_chat_display)  # Should be True
```

### Too Verbose?

Disable timestamps:
```python
chat = AgentChatDisplay(show_timestamps=False)
```

## Links

- **Full Guide**: [INTERACTIVE_CHAT.md](INTERACTIVE_CHAT.md)
- **Update Summary**: [INTERACTIVE_CHAT_UPDATE.md](INTERACTIVE_CHAT_UPDATE.md)
- **Examples**: [examples/interactive_chat_workflow.py](../examples/interactive_chat_workflow.py)
- **Main README**: [README.md](../README.md)

---

**Quick Start**: `python examples/interactive_chat_workflow.py` → Option 2 🚀
