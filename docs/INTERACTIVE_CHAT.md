# Interactive Chat Communication

The LLM Multi-Agent System now features an **interactive chat-like interface** that makes it easy to follow agent communications in real-time. This document explains how to use and customize the interactive chat display.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Chat Display Components](#chat-display-components)
- [Customization](#customization)
- [Examples](#examples)
- [Chat Log Export](#chat-log-export)
- [API Reference](#api-reference)

## Overview

The interactive chat display transforms technical log output into a natural, conversation-like interface where you can see:

- 💬 Agent messages and thoughts
- 🔄 Inter-agent handoffs and communications
- ⚙️ Real-time action updates
- ✅ Task completions with deliverables
- 📊 Progress tracking
- ⚠️ Errors and warnings
- 📄 File operations

All communications are color-coded by agent role for easy visual distinction.

## Features

### 🎨 Color-Coded Agents

Each agent has a unique color for easy identification:

- **Business Analyst**: Cyan
- **Developer**: Green
- **QA Engineer**: Yellow
- **DevOps Engineer**: Magenta
- **Technical Writer**: Blue
- **System**: White

### 📝 Message Types

Different message types with visual indicators:

- 🚀 **Start**: Workflow or task initiation
- ⚙️ **Working**: Agent performing an action
- 🤔 **Thinking**: Agent reasoning or planning
- ✅ **Completed**: Task completion
- ❌ **Error**: Error messages
- 💬 **Chat**: General communication
- 🔄 **Handoff**: Inter-agent communication
- ℹ️ **Info**: System information

### 📊 Progress Tracking

Visual progress bars and status indicators:

```
Progress: ████████████████░░░░░░░░░░░░░░░░░░░░ 60%
Current: implementation

Workflow Status
  ID: workflow_20260113_120000
  Status: running
  Current Step: implementation
  Progress: 3 steps completed
  ████████████████████░░░░░░░░ 50%
```

### 📄 File Operation Tracking

See files as they're created by agents:

```
✅ Developer created: api_endpoints.py
✅ Developer created: models.py
✅ Developer created: schemas.py
```

## Quick Start

### Enable Interactive Chat (Default)

The chat display is **enabled by default**. Simply run any workflow:

```python
from src.orchestrator import LangGraphOrchestrator

orchestrator = LangGraphOrchestrator(
    workspace="./my_workspace",
    enable_chat_display=True  # Default: True
)

# Run a workflow - chat display automatically shows
await orchestrator.execute_feature_development(
    requirement="Create a REST API..."
)
```

### Disable Interactive Chat

If you prefer traditional logging:

```python
orchestrator = LangGraphOrchestrator(
    workspace="./my_workspace",
    enable_chat_display=False  # Disable chat display
)
```

### Run the Interactive Example

Try the comprehensive example:

```bash
# Run the interactive chat workflow example
python examples/interactive_chat_workflow.py

# Select option 2 for a quick demo (no llama-server needed)
```

## Chat Display Components

### Agent Messages

Agents share their thoughts and plans:

```python
chat_display.agent_message(
    "business_analyst",
    "Analyzing requirements for the e-commerce platform...\n"
    "Identifying key user stories and acceptance criteria.",
    message_type="thinking"
)
```

Output:
```
🤔 Business Analyst:
  Analyzing requirements for the e-commerce platform...
  Identifying key user stories and acceptance criteria.
```

### Agent Actions

Track what agents are doing:

```python
chat_display.agent_action(
    "developer",
    "is implementing the API endpoints",
    "Writing FastAPI routes and middleware"
)
```

Output:
```
⚙️ Developer is implementing the API endpoints
  Writing FastAPI routes and middleware
```

### Task Completion

Celebrate completions with summaries:

```python
chat_display.agent_completed(
    "qa_engineer",
    "Test suite complete. Created 45 unit tests with 95% coverage.",
    files_created=["tests/test_api.py", "tests/test_models.py"]
)
```

Output:
```
✅ QA Engineer completed task
  Test suite complete. Created 45 unit tests with 95% coverage.
  📄 Files created: 2
    • test_api.py
    • test_models.py
```

### Inter-Agent Communication

See handoffs between agents:

```python
chat_display.inter_agent_communication(
    "business_analyst",
    "developer",
    "Requirements analysis complete. Passing user stories for design.",
    communication_type="handoff"
)
```

Output:
```
🔄 Business Analyst → Developer
  Requirements analysis complete. Passing user stories for design.
```

### Error Messages

Clear error reporting:

```python
chat_display.agent_error(
    "developer",
    "Database connection failed: Connection timeout"
)
```

Output:
```
❌ Developer encountered an error
  Database connection failed: Connection timeout
```

### Workflow Status

Track overall progress:

```python
chat_display.workflow_status(
    workflow_id="workflow_20260113_120000",
    status="running",
    step="implementation",
    completed_steps=["business_analyst", "architecture_design"]
)
```

## Customization

### Custom Chat Display

Create your own chat display instance:

```python
from src.utils.chat_display import AgentChatDisplay

# Create with custom settings
chat = AgentChatDisplay(
    show_timestamps=True,      # Show [HH:MM:SS] timestamps
    show_agent_icons=True      # Show emoji icons
)

# Use in your code
chat.print_header("My Custom Workflow")
chat.agent_message("developer", "Starting work...")
chat.agent_completed("developer", "Work complete!")
```

### Progress Tracker

Track custom workflows:

```python
from src.utils.chat_display import ProgressTracker

tracker = ProgressTracker(total_steps=5)

# Update as you complete steps
tracker.update("requirements_analysis")
tracker.update("design")
tracker.update("implementation")
# Shows: Progress: ████████████████████████░░░░░░░░ 60%
```

### Without Timestamps

For cleaner output:

```python
chat = AgentChatDisplay(show_timestamps=False)
```

## Examples

### Basic Workflow with Chat

```python
import asyncio
from src.orchestrator import LangGraphOrchestrator

async def main():
    orchestrator = LangGraphOrchestrator(
        workspace="./workspace",
        enable_chat_display=True
    )
    
    result = await orchestrator.execute_feature_development(
        requirement="Create a user authentication system"
    )
    
    print("Workflow complete!")

asyncio.run(main())
```

### Manual Chat Display

```python
from src.utils.chat_display import AgentChatDisplay

chat = AgentChatDisplay()

chat.print_header("Manual Workflow Demo")

# Simulate agent work
chat.agent_message("business_analyst", "Analyzing requirements...", "thinking")
chat.agent_action("business_analyst", "is creating user stories")
chat.agent_completed(
    "business_analyst",
    "Created 5 user stories",
    files_created=["requirements.md"]
)

# Show handoff
chat.inter_agent_communication(
    "business_analyst",
    "developer",
    "Requirements ready for implementation"
)

# Show summary
chat.conversation_summary()
```

### Demo Mode

Run a visual demo without actual agents:

```bash
python examples/interactive_chat_workflow.py

# Select option 2 for demo mode
```

## Chat Log Export

All chat communications are automatically saved to JSON files for later analysis.

### Automatic Export

When running workflows, chat logs are saved automatically:

```python
orchestrator = LangGraphOrchestrator(workspace="./workspace")
result = await orchestrator.execute_feature_development(requirement="...")

# Chat log automatically saved to:
# ./workspace/output/chat_log_workflow_YYYYMMDD_HHMMSS.json
```

### Manual Export

Save chat logs manually:

```python
from pathlib import Path

chat = AgentChatDisplay()

# ... use chat display ...

# Save to custom location
chat.save_chat_log(Path("./logs/my_chat.json"))
```

### Chat Log Format

```json
[
  {
    "timestamp": "2026-01-13T12:00:00.123456",
    "agent_id": "business_analyst",
    "to_agent": null,
    "message_type": "thinking",
    "message": "Analyzing requirements..."
  },
  {
    "timestamp": "2026-01-13T12:05:00.123456",
    "agent_id": "business_analyst",
    "to_agent": "developer",
    "message_type": "handoff",
    "message": "Requirements complete. Ready for design."
  }
]
```

### Conversation Summary

Get statistics about the conversation:

```python
chat.conversation_summary()
```

Output:
```
═══════════════════════════════════════
  Conversation Summary
═══════════════════════════════════════

Total messages: 24

Messages per agent:
  Business Analyst: 6
  Developer: 8
  QA Engineer: 5
  DevOps Engineer: 3
  Technical Writer: 2
```

## API Reference

### AgentChatDisplay

Main class for interactive chat display.

#### Constructor

```python
AgentChatDisplay(
    show_timestamps: bool = True,
    show_agent_icons: bool = True
)
```

#### Methods

**`print_header(title: str)`**
- Print a styled header for sections

**`agent_message(agent_id: str, message: str, message_type: str = "info", to_agent: Optional[str] = None)`**
- Display an agent message
- `message_type`: "info", "thinking", "working", "start", etc.

**`agent_action(agent_id: str, action: str, details: Optional[str] = None)`**
- Show an agent performing an action

**`agent_thinking(agent_id: str, thought: str)`**
- Display agent reasoning

**`agent_completed(agent_id: str, summary: str, files_created: Optional[List[str]] = None)`**
- Show task completion with deliverables

**`agent_error(agent_id: str, error: str)`**
- Display error messages

**`workflow_status(workflow_id: str, status: str, step: str, completed_steps: List[str])`**
- Show overall workflow progress

**`inter_agent_communication(from_agent: str, to_agent: str, message: str, communication_type: str = "handoff")`**
- Display communication between agents

**`system_message(message: str, message_type: str = "info")`**
- Display system-level messages

**`file_operation(agent_id: str, operation: str, file_path: str, success: bool = True)`**
- Show file operations

**`conversation_summary()`**
- Display conversation statistics

**`save_chat_log(output_path: Path)`**
- Export chat history to JSON

### ProgressTracker

Track and display workflow progress.

#### Constructor

```python
ProgressTracker(total_steps: int = 6)
```

#### Methods

**`update(step_name: str)`**
- Update progress with new completed step

## Best Practices

### 1. Use Descriptive Messages

```python
# ✅ Good - descriptive and informative
chat.agent_message(
    "developer",
    "Designing RESTful API with 12 endpoints:\n"
    "- Authentication endpoints (login, logout, refresh)\n"
    "- User management (CRUD operations)\n"
    "- Resource endpoints (tasks, projects)"
)

# ❌ Bad - too vague
chat.agent_message("developer", "Working on API")
```

### 2. Show Progress Regularly

```python
# Update workflow status at key milestones
chat.workflow_status(
    workflow_id,
    "running",
    "implementation",
    completed_steps
)
```

### 3. Use Handoffs for Context

```python
# Show what's being passed between agents
chat.inter_agent_communication(
    "business_analyst",
    "developer",
    "Requirements complete. Key outputs:\n"
    "- 8 user stories\n"
    "- 3 data models\n"
    "- API specifications"
)
```

### 4. Include File Information

```python
# List specific files created
chat.agent_completed(
    "developer",
    "Implementation complete",
    files_created=[
        "src/api/endpoints.py",
        "src/models/user.py",
        "src/schemas/task.py"
    ]
)
```

### 5. Save Chat Logs

```python
# Always save chat logs for later review
chat.save_chat_log(Path("./logs/workflow_chat.json"))
chat.conversation_summary()
```

## Troubleshooting

### Colors Not Showing

**Problem**: Terminal doesn't show colors

**Solution**: Make sure `colorama` is installed:
```bash
pip install colorama
```

On Windows, colorama automatically handles ANSI color codes.

### Chat Display Not Appearing

**Problem**: No chat output during workflow

**Solution**: Ensure chat display is enabled:
```python
orchestrator = LangGraphOrchestrator(
    workspace="./workspace",
    enable_chat_display=True  # Make sure this is True
)
```

### Timestamps Cluttering Output

**Problem**: Too many timestamps

**Solution**: Disable timestamps:
```python
chat = AgentChatDisplay(show_timestamps=False)
```

## Integration with Existing Code

### Update Existing Workflows

To add chat display to existing code:

```python
# Before
orchestrator = LangGraphOrchestrator(workspace="./workspace")

# After - no changes needed! Chat is enabled by default
orchestrator = LangGraphOrchestrator(workspace="./workspace")

# Or explicitly enable
orchestrator = LangGraphOrchestrator(
    workspace="./workspace",
    enable_chat_display=True
)
```

### Programmatic Access

Access chat display from orchestrator:

```python
orchestrator = LangGraphOrchestrator(workspace="./workspace")

# Access chat display
if orchestrator.chat_display:
    orchestrator.chat_display.system_message("Custom message")
```

## Next Steps

- Try the [interactive example](../examples/interactive_chat_workflow.py)
- Review [agent specifications](./AGENT_SPECS.md)
- Learn about [LangGraph integration](./LANGGRAPH_INTEGRATION.md)
- Read the [API reference](./API_REFERENCE.md)

## Feedback

The interactive chat display is designed to make multi-agent workflows more transparent and easier to follow. If you have suggestions for improvements, please open an issue on GitHub!
