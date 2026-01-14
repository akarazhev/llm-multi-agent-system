# Get Started with Interactive Chat - 5 Minutes

## What You'll Learn

In just 5 minutes, you'll see the new interactive chat interface in action and understand how to use it in your workflows.

## Step 1: Quick Demo (30 seconds)

No setup required! See the chat interface immediately:

```bash
python examples/interactive_chat_workflow.py
```

When prompted, **press 2** for instant demo mode.

**You'll see:**
- 💬 Color-coded agent messages
- 🔄 Inter-agent handoffs
- 📊 Progress bars
- ✅ Task completions
- 📄 File lists

**No llama-server needed!** This demo shows the interface without running actual agents.

## Step 2: Understand What You're Seeing (1 minute)

### Agent Colors

Each agent has a unique color:

| Color | Agent |
|-------|-------|
| 🔵 Cyan | Business Analyst |
| 🟢 Green | Developer |
| 🟡 Yellow | QA Engineer |
| 🟣 Magenta | DevOps Engineer |
| 🔵 Blue | Technical Writer |

### Message Types

| Icon | Meaning |
|------|---------|
| 🤔 | Thinking/Planning |
| ⚙️ | Working/In Progress |
| ✅ | Task Complete |
| 🔄 | Handoff to Another Agent |
| 📊 | Progress Update |
| 📄 | Files Created |

### Progress Bars

```
Progress: ████████████████░░░░░░░░░░░░░░░░░░░░ 40%
```

Visual indicator showing workflow completion percentage.

## Step 3: Try with Real Agents (2 minutes)

### Prerequisites

1. Start your llama-server:
   ```bash
   # Ensure your local LLM server is running on port 8080
   ```

2. Run the interactive example:
   ```bash
   python examples/interactive_chat_workflow.py
   ```

3. When prompted, **press 1** for full workflow

**Watch as real agents:**
- Analyze requirements
- Design architecture
- Implement code
- Create tests
- Set up deployment
- Write documentation

All with **real-time chat display!**

## Step 4: Use in Your Code (1 minute)

### It's Already Enabled!

The chat display is **on by default**. Just run your existing workflows:

```python
from src.orchestrator import LangGraphOrchestrator

# Chat display automatically shows!
orchestrator = LangGraphOrchestrator(workspace=".")

result = await orchestrator.execute_feature_development(
    requirement="Create a REST API for user authentication"
)

# Watch agents communicate in real-time
# Chat log automatically saved to output/
```

### That's It!

No configuration needed. The chat display just works.

## Step 5: Customize (Optional, 30 seconds)

### Disable Chat Display

If you prefer traditional logs:

```python
orchestrator = LangGraphOrchestrator(
    workspace=".",
    enable_chat_display=False  # Turn off chat
)
```

### Customize Chat

```python
from src.utils.chat_display import AgentChatDisplay

chat = AgentChatDisplay(
    show_timestamps=False,     # Hide timestamps
    show_agent_icons=True      # Show emoji icons
)
```

### Manual Usage

```python
chat = AgentChatDisplay()

chat.print_header("My Custom Workflow")
chat.agent_message("developer", "Starting implementation...", "thinking")
chat.agent_completed("developer", "Done!", ["app.py", "tests.py"])
chat.save_chat_log(Path("./my_chat.json"))
```

## Common Scenarios

### Scenario 1: I Want to See What's Happening

**Solution:** Just run your workflow. Chat is enabled by default!

```bash
python main.py
# Or
python examples/langgraph_feature_development.py
```

### Scenario 2: I Want Traditional Logs

**Solution:** Disable chat display:

```python
orchestrator = LangGraphOrchestrator(
    workspace=".",
    enable_chat_display=False
)
```

### Scenario 3: I Want to Export Chat History

**Solution:** It's automatic! After each workflow, find your chat log:

```
workspace/
  output/
    chat_log_workflow_YYYYMMDD_HHMMSS.json
```

### Scenario 4: Colors Don't Show

**Solution:** Install colorama:

```bash
pip install colorama
```

Already in requirements.txt if you installed normally.

## What's Next?

### Quick References

- **[1-page reference](CHAT_QUICK_REFERENCE.md)** - Commands and examples
- **[Full guide](INTERACTIVE_CHAT.md)** - Complete documentation
- **[Visual examples](CHAT_EXAMPLES.md)** - See output examples

### Try More Examples

```bash
# Feature development with chat
python examples/langgraph_feature_development.py

# Bug fix workflow with chat
python examples/langgraph_bug_fix.py

# Custom workflow with chat
python examples/custom_workflow.py
```

### Advanced Usage

Read the full guide: [INTERACTIVE_CHAT.md](INTERACTIVE_CHAT.md)

## Quick Troubleshooting

### Problem: No colors in terminal

**Fix:**
```bash
pip install colorama
```

### Problem: Chat not showing

**Check:**
```python
orchestrator = LangGraphOrchestrator(
    workspace=".",
    enable_chat_display=True  # Make sure it's True
)
```

### Problem: Too much output

**Solution:** Disable timestamps:
```python
chat = AgentChatDisplay(show_timestamps=False)
```

## Summary

**In 5 minutes you learned:**

✅ How to see the instant demo (no setup)
✅ What the colors and icons mean
✅ How to run with real agents
✅ That it's enabled by default in your code
✅ How to customize if needed

## The 30-Second Version

```bash
# See it now (no setup):
python examples/interactive_chat_workflow.py
# Press 2

# Use it (already enabled):
python main.py

# That's it! 🎉
```

## Need Help?

- **Examples don't work?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Want more details?** Read [INTERACTIVE_CHAT.md](INTERACTIVE_CHAT.md)
- **Quick commands?** See [CHAT_QUICK_REFERENCE.md](CHAT_QUICK_REFERENCE.md)

## One More Thing...

The chat log saves every conversation:

```json
[
  {
    "timestamp": "2026-01-13T12:00:00",
    "agent_id": "business_analyst",
    "message_type": "thinking",
    "message": "Analyzing requirements..."
  }
]
```

Perfect for debugging, auditing, or understanding how agents collaborate!

---

**You're all set! Try the demo now:**

```bash
python examples/interactive_chat_workflow.py
```

**Press 2 for instant demo** 🚀
