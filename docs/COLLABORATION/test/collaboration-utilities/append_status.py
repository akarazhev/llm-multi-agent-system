#!/usr/bin/env python3
"""
Safely append agent status update to collaboration session file.

This utility implements append-only approach for Agent Status sections,
preventing conflicts when multiple agents update their status simultaneously.

Usage:
    python append_status.py <session_file> <agent_id> <status_content>
    
    python append_status.py session.md "Agent 4" "Active, working on utilities"
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


def find_agent_status_section(content: str, agent_id: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Find the Agent Status section for specific agent.
    
    Returns:
        Tuple of (start_line, end_line) or (None, None) if not found
    """
    lines = content.split('\n')
    start_idx = None
    end_idx = None
    
    # Pattern: "## Agent X - Current Status" or "## Agent X - Status"
    pattern = rf'^##\s+{re.escape(agent_id)}\s+-\s+(Current\s+)?Status'
    
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.IGNORECASE):
            start_idx = i
            break
    
    if start_idx is None:
        return None, None
    
    # Find the next agent status section or end of file
    for i in range(start_idx + 1, len(lines)):
        if re.match(r'^##\s+Agent\s+', lines[i]):
            end_idx = i
            break
    
    if end_idx is None:
        end_idx = len(lines)
    
    return start_idx, end_idx


def format_status_update(
    agent_id: str,
    status_content: str,
    timestamp: Optional[datetime] = None
) -> str:
    """
    Format a status update block.
    
    Args:
        agent_id: Agent identifier
        status_content: Status update content (can be multi-line)
        timestamp: Timestamp (default: current time)
    
    Returns:
        Formatted markdown status update block
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    # Count existing status updates for this agent
    update_number = 1  # Will be determined when appending
    
    status_block = f"""
---

## {agent_id} - Status Update #{update_number}
**Timestamp**: {timestamp_str}
**Last Activity**: {timestamp_str} ✅
**Heartbeat Status**: ✅ Active

**Status**:
{status_content}

**Previous Status**: See above status blocks

---
"""
    return status_block


def append_status_with_retry(
    session_file: Path,
    agent_id: str,
    status_content: str,
    max_retries: int = MAX_RETRIES
) -> bool:
    """
    Safely append status update with retry mechanism.
    
    Args:
        session_file: Path to collaboration session file
        agent_id: Agent identifier
        status_content: Status update content
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
            
            # Find agent status section
            start_idx, end_idx = find_agent_status_section(current_content, agent_id)
            
            if start_idx is None:
                # Agent status section doesn't exist, create it at end of file
                lines = current_content.split('\n')
                new_status = format_status_update(agent_id, status_content)
                new_content = current_content + '\n' + new_status
            else:
                # Count existing updates
                lines = current_content.split('\n')
                section_content = '\n'.join(lines[start_idx:end_idx])
                update_count = len(re.findall(rf'Status Update #(\d+)', section_content)) + 1
                
                # Format new status update
                status_block = format_status_update(agent_id, status_content)
                # Replace update number
                status_block = status_block.replace('Status Update #1', f'Status Update #{update_count}')
                
                # Insert before end of section
                new_lines = lines[:end_idx] + [status_block] + lines[end_idx:]
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
            
            # Write back
            session_file.write_text(new_content, encoding='utf-8')
            
            print(f"✅ Successfully appended status update from {agent_id}")
            print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Safely append agent status update to collaboration session file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python append_status.py session.md "Agent 4" "Active, working on utilities"
  python append_status.py session.md "Agent 4" "Completed heartbeat implementation"
        """
    )
    
    parser.add_argument('session_file', type=str, help='Path to collaboration session file')
    parser.add_argument('agent_id', type=str, help='Agent ID (e.g., "Agent 4")')
    parser.add_argument('status_content', type=str, help='Status update content')
    parser.add_argument('--max-retries', type=int, default=MAX_RETRIES, help=f'Maximum retry attempts (default: {MAX_RETRIES})')
    
    args = parser.parse_args()
    
    session_file = Path(args.session_file)
    
    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        sys.exit(1)
    
    success = append_status_with_retry(
        session_file,
        args.agent_id,
        args.status_content,
        args.max_retries
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
