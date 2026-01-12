#!/usr/bin/env python3
"""
Safely append a discussion message to a collaboration session file.

This utility implements the append-only approach for Discussion Log section,
preventing conflicts when multiple agents edit the same file simultaneously.

Usage:
    python append_discussion.py <session_file> <agent_id> <message_type> <topic> <content>
    
    python append_discussion.py COLLABORATION_SESSION_*.md "Agent 4" "Response" "Test" "Hello team!"
    
Or use interactively:
    python append_discussion.py <session_file>
"""

import argparse
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


MAX_RETRIES = 3
RETRY_DELAY = 0.2  # seconds


def find_discussion_section(content: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Find the Discussion Log section in the session file.
    
    Returns:
        Tuple of (start_line, end_line) or (None, None) if not found
    """
    lines = content.split('\n')
    start_idx = None
    end_idx = None
    
    # Find "## 3. Discussion Log" section
    for i, line in enumerate(lines):
        if re.match(r'^##\s+3\.\s+Discussion\s+Log', line, re.IGNORECASE):
            start_idx = i
            break
    
    if start_idx is None:
        return None, None
    
    # Find the next major section (## 4.)
    for i in range(start_idx + 1, len(lines)):
        if re.match(r'^##\s+[4-9]\.', lines[i]):
            end_idx = i
            break
    
    if end_idx is None:
        end_idx = len(lines)
    
    return start_idx, end_idx


def format_discussion_message(
    agent_id: str,
    message_type: str,
    topic: str,
    content: str,
    timestamp: Optional[datetime] = None
) -> str:
    """
    Format a discussion message according to protocol.
    
    Args:
        agent_id: Agent identifier (e.g., "Agent 4", "Agent-004")
        message_type: Type of message (Question, Proposal, Response, Decision, etc.)
        topic: Topic of discussion
        content: Message content
        timestamp: Timestamp (default: current time)
    
    Returns:
        Formatted markdown message
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"""---

#### {agent_id} → All Agents
**Type**: {message_type}
**Topic**: {topic}
**Timestamp**: {timestamp_str}

**Content**:
> {content.replace(chr(10), chr(10) + '> ')}

**Action Required**:
- [ ] Response needed from other agents
- [ ] Information sharing only

---
"""
    return message


def append_discussion(
    session_file: Path,
    agent_id: str,
    message_type: str,
    topic: str,
    content: str,
    max_retries: int = MAX_RETRIES
) -> bool:
    """
    Safely append a discussion message to session file with retry mechanism.
    
    Args:
        session_file: Path to collaboration session file
        agent_id: Agent identifier
        message_type: Type of message
        topic: Topic of discussion
        content: Message content
        max_retries: Maximum number of retry attempts
    
    Returns:
        True if successful, False otherwise
    """
    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        return False
    
    for attempt in range(max_retries):
        try:
            # Read current content
            current_content = session_file.read_text(encoding='utf-8')
            content_hash_before = hash(current_content)
            
            # Find Discussion Log section
            start_idx, end_idx = find_discussion_section(current_content)
            
            if start_idx is None:
                print("Error: Discussion Log section not found in session file", file=sys.stderr)
                return False
            
            # Format new message
            new_message = format_discussion_message(agent_id, message_type, topic, content)
            
            # Split content into lines
            lines = current_content.split('\n')
            
            # Insert new message before the end of Discussion Log section
            insert_position = end_idx
            
            # Try to find a good insertion point (before "## 4." or at end of section)
            for i in range(end_idx - 1, start_idx, -1):
                if lines[i].strip() and not lines[i].startswith('---'):
                    insert_position = i + 1
                    break
            
            # Insert new message
            new_lines = lines[:insert_position] + [new_message] + lines[insert_position:]
            new_content = '\n'.join(new_lines)
            
            # Verify file hasn't changed (simple check)
            try:
                verify_content = session_file.read_text(encoding='utf-8')
                if hash(verify_content) != content_hash_before:
                    if attempt < max_retries - 1:
                        print(f"⚠️  File changed during update, retrying... (attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                        time.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
                        continue
                    else:
                        print("⚠️  File changed during update, but max retries reached. Update may have conflicts.", file=sys.stderr)
            except Exception:
                pass  # If we can't verify, proceed anyway
            
            # Write back (this is atomic for most file systems)
            session_file.write_text(new_content, encoding='utf-8')
            
            print(f"✅ Successfully appended message from {agent_id} to Discussion Log")
            print(f"   Type: {message_type}, Topic: {topic}")
            print(f"   File: {session_file}")
            return True
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️  Error on attempt {attempt + 1}/{max_retries}: {e}", file=sys.stderr)
                print(f"   Retrying in {RETRY_DELAY * (attempt + 1)} seconds...", file=sys.stderr)
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                print(f"❌ Error after {max_retries} attempts: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                return False
    
    return False


def interactive_mode(session_file: Path):
    """Interactive mode for appending discussion messages."""
    print(f"Interactive mode: Appending to {session_file.name}")
    print("Enter discussion message details (press Enter to skip prompts):\n")
    
    agent_id = input("Agent ID (e.g., 'Agent 4'): ").strip()
    if not agent_id:
        print("Error: Agent ID is required", file=sys.stderr)
        return False
    
    message_type = input("Message Type (Question/Proposal/Response/Decision/etc.): ").strip() or "Response"
    topic = input("Topic: ").strip()
    if not topic:
        print("Error: Topic is required", file=sys.stderr)
        return False
    
    print("\nEnter message content (end with empty line or Ctrl+D):")
    content_lines = []
    try:
        while True:
            line = input()
            content_lines.append(line)
    except EOFError:
        pass
    
    content = '\n'.join(content_lines).strip()
    if not content:
        print("Error: Content is required", file=sys.stderr)
        return False
    
    return append_discussion(session_file, agent_id, message_type, topic, content)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Safely append a discussion message to collaboration session file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python append_discussion.py session.md "Agent 4" "Response" "Test" "Hello team!"
  python append_discussion.py session.md  # Interactive mode
        """
    )
    
    parser.add_argument('session_file', type=str, help='Path to collaboration session file')
    parser.add_argument('agent_id', nargs='?', type=str, help='Agent ID (e.g., "Agent 4")')
    parser.add_argument('message_type', nargs='?', type=str, help='Message type (Question/Proposal/Response/etc.)')
    parser.add_argument('topic', nargs='?', type=str, help='Discussion topic')
    parser.add_argument('content', nargs='?', type=str, help='Message content')
    
    args = parser.parse_args()
    
    session_file = Path(args.session_file)
    
    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        sys.exit(1)
    
    # Interactive mode if not all arguments provided
    if not all([args.agent_id, args.message_type, args.topic, args.content]):
        success = interactive_mode(session_file)
    else:
        success = append_discussion(
            session_file,
            args.agent_id,
            args.message_type,
            args.topic,
            args.content
        )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
