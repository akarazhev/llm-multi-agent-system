# Multi-Agent Collaboration Test Directory

This directory is used for testing the multi-agent collaboration protocol.

## Active Sessions

Current active session: `COLLABORATION_SESSION_2026-01-10_14-21-28.md`

## How to Join a Session

1. Check for active session files: `COLLABORATION_SESSION_*.md`
2. Read the latest session file
3. Add your agent introduction to the "Agent Introductions" section
4. Follow the protocol defined in `.cursor/rules/multi-agent-collaboration.mdc`

## Agent Detection

**Current Method**: File-based detection
- Agents scan this directory for session files
- Latest timestamp = most recent session
- Agents read session file to detect other participants

## Session Structure

Each session file follows this structure:
1. Agent Introductions
2. Role Assignment
3. Discussion Log
4. Decisions & Consensus
5. Step-by-Step Execution
6. Final Deliverables
7. Open Questions

## Protocol Reference

See: `.cursor/rules/multi-agent-collaboration.mdc`
