# How to Use Multi-Agent Collaboration Rule

## Quick Start

### 1. Automatic Activation

The rule activates **automatically** when:
- You run 2 or more agents simultaneously (e.g., "4x Auto" mode in Cursor)
- Multiple agents are detected working on the same task

### 2. Manual Activation

You can manually activate the rule by:

**Option A: Reference in your prompt**
```
Use the multi-agent-collaboration rule to work with other agents
```

**Option B: Use the rule tag**
```
@multi-agent-collaboration
```

**Option C: Explicit instruction**
```
Follow the multi-agent collaboration protocol from .cursor/rules/multi-agent-collaboration.mdc
```

---

## Step-by-Step Usage Guide

### Step 1: Start Multiple Agents

1. In Cursor, select "4x Auto" or start multiple agents
2. Give them a task to work on together
3. The rule will automatically activate

### Step 2: Agents Will Automatically:

1. **Detect each other** - First agent creates collaboration file
2. **Introduce themselves** - Each agent states their role and expertise
3. **Negotiate roles** - Agents agree on role distribution
4. **Start discussion** - Begin structured conversation about the task

### Step 3: Monitor the Process

Check the collaboration file:
```
docs/COLLABORATION_SESSION_[TIMESTAMP].md
```

This file contains:
- Agent introductions
- Role assignments
- All discussions
- Decisions and consensus
- Step-by-step execution

---

## File Locations

### Rule File
```
.cursor/rules/multi-agent-collaboration.mdc
```

### Documentation
```
docs/AGENT_COLLABORATION_PROTOCOL.md
```

### Collaboration Sessions
```
docs/COLLABORATION_SESSION_[TIMESTAMP].md
```

---

## Common Use Cases

### Use Case 1: Architecture Design

**Prompt:**
```
4 agents: Design the frontend architecture for our application
```

**What happens:**
- Agents will introduce themselves (Architect, UX Designer, Product Manager, Developer)
- They'll discuss technology choices
- Reach consensus on stack
- Document decisions

### Use Case 2: Feature Planning

**Prompt:**
```
3 agents: Plan the user authentication feature
```

**What happens:**
- Agents assign roles (Product Manager, Security Expert, Developer)
- Discuss requirements
- Plan implementation steps
- Document the plan

### Use Case 3: Code Review

**Prompt:**
```
2 agents: Review this code and suggest improvements
```

**What happens:**
- Agents coordinate review approach
- Discuss findings
- Agree on recommendations
- Document review results

---

## Configuration

### Rule Settings

The rule is configured in `.cursor/rules/multi-agent-collaboration.mdc`:

```yaml
---
name: Multi-Agent Collaborative Workflow
description: Rule for collaborative work of multiple agents
alwaysApply: false  # Set to true to always apply
tags: [agents, collaboration, communication, workflow]
---
```

**Note**: `alwaysApply: false` means the rule activates automatically when 2+ agents are detected, but you can also reference it manually.

### Customization

You can customize:
- Document naming format
- Role types
- Communication format
- Decision-making process

Edit `.cursor/rules/multi-agent-collaboration.mdc` to customize.

---

## Troubleshooting

### Problem: Agents aren't collaborating

**Solution:**
1. Check if rule file exists: `.cursor/rules/multi-agent-collaboration.mdc`
2. Explicitly reference the rule: `@multi-agent-collaboration`
3. Verify agents are actually running simultaneously

### Problem: Agents working in separate files

**Solution:**
1. Remind agents: "Work in the same collaboration file"
2. Point them to existing session file
3. Reference the rule explicitly

### Problem: Agents not waiting for responses

**Solution:**
1. Remind: "Wait for all agents to respond before proceeding"
2. Reference the rule: `@multi-agent-collaboration`
3. Check if collaboration file is being updated

### Problem: No consensus reached

**Solution:**
1. Agents should document disagreements
2. Use majority vote if needed
3. Escalate to human input if critical

---

## Best Practices

1. **Start with clear task**: Give agents a well-defined task
2. **Monitor progress**: Check collaboration file regularly
3. **Intervene if needed**: If agents get stuck, provide guidance
4. **Review decisions**: Check final decisions before implementation
5. **Use appropriate number**: 2-4 agents usually work best

---

## Examples

### Example 1: Simple Activation

**User prompt:**
```
Use 4 agents to design the API structure
```

**Agents will:**
- Automatically detect each other
- Create collaboration file
- Introduce and assign roles
- Discuss API design
- Document decisions

### Example 2: Explicit Reference

**User prompt:**
```
@multi-agent-collaboration
4 agents: Plan the database schema
```

**Agents will:**
- Follow the protocol explicitly
- Create structured discussion
- Reach consensus on schema
- Document everything

### Example 3: Resuming Session

**User prompt:**
```
Continue the collaboration session from docs/COLLABORATION_SESSION_2024-12-19_14-30-00.md
```

**Agents will:**
- Read existing file
- Understand current state
- Continue from where they left off
- Update the file

---

## Rule File Structure

```
.cursor/rules/
├── multi-agent-collaboration.mdc          # Main rule file
└── MULTI_AGENT_COLLABORATION_USAGE.md     # This usage guide

docs/
├── AGENT_COLLABORATION_PROTOCOL.md        # Full protocol documentation
└── COLLABORATION_SESSION_*.md             # Session files (created automatically)
```

---

## Additional Resources

- **Full Protocol**: See `docs/AGENT_COLLABORATION_PROTOCOL.md` for complete documentation
- **Rule File**: See `.cursor/rules/multi-agent-collaboration.mdc` for rule definition
- **Examples**: Check existing collaboration session files in `docs/`

---

## Support

If you encounter issues:
1. Check the rule file exists and is properly formatted
2. Verify agents are running simultaneously
3. Explicitly reference the rule: `@multi-agent-collaboration`
4. Check collaboration file for agent activity

---

**Version**: 1.0  
**Last Updated**: 2024-12-19
