# Multi-Agent Collaboration

This directory is for collaboration session files created by agents when working together.

## Documentation

For complete documentation on multi-agent collaboration, see:

- **Full Protocol**: [`../AGENT_COLLABORATION_PROTOCOL.md`](../AGENT_COLLABORATION_PROTOCOL.md)
- **Usage Guide**: [`../../.cursor/rules/MULTI_AGENT_COLLABORATION_USAGE.md`](../../.cursor/rules/MULTI_AGENT_COLLABORATION_USAGE.md)
- **Rule File**: [`../../.cursor/rules/multi-agent-collaboration.mdc`](../../.cursor/rules/multi-agent-collaboration.mdc)

## Session Files

When multiple agents collaborate, they create session files in the `docs/` directory:

- `docs/COLLABORATION_SESSION_[TIMESTAMP].md` - Main collaboration session files

## Collaboration Analysis

### First Multi-Agent Session (2026-01-10)

**Issue**: The collaboration protocol was not properly followed - agents worked in isolation in separate worktree directories.

**Analysis Document**: 
- [`../COLLABORATION_ANALYSIS_2026-01-10.md`](../COLLABORATION_ANALYSIS_2026-01-10.md) - Complete analysis of what went wrong and consolidated results from 4 agents

**Agent Results** (stored in worktree directories):
- **ds-store-dla**: `~/.cursor/worktrees/llm-multi-agent-system/dla/docs/`
- **mac-cleanup-cok**: `~/.cursor/worktrees/llm-multi-agent-system/cok/docs/`
- **adapt-ui-doc-scx**: `~/.cursor/worktrees/llm-multi-agent-system/scx/docs/`
- **2026-01-10-dnkl-gsq**: `~/.cursor/worktrees/llm-multi-agent-system/gsq/docs/`

**Key Findings**:
- ❌ Agents worked in isolation (different worktree directories)
- ❌ No unified collaboration file created
- ✅ Each agent produced quality analysis independently
- ✅ Results were successfully consolidated post-session

**Lessons Learned**:
- Need automatic agent detection mechanism
- All agents must work in main project directory
- Unified collaboration file must be created automatically
- Sequential interaction protocol needs better technical implementation

## Quick Start

1. Start 2+ agents simultaneously (e.g., "4x Auto" in Cursor)
2. Agents automatically detect each other and create a collaboration file
3. Agents introduce themselves and assign roles
4. Agents discuss and reach consensus on decisions
5. All work is documented in the session file

## Activation

The rule activates automatically when 2+ agents are detected, or manually:

```
@multi-agent-collaboration
```
