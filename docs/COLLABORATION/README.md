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
