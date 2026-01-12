#!/usr/bin/env python3
"""
Safely append a decision to Decisions & Consensus section.

This utility implements append-only approach for Decisions section,
preventing conflicts when multiple agents add decisions simultaneously.

Usage:
    python append_decision.py <session_file> <agent_id> <decision_title> <decision_content> [--status <status>] [--voting <voting>]
"""

import argparse
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


MAX_RETRIES = 3
RETRY_DELAY = 0.2


def find_decisions_section(content: str) -> Tuple[Optional[int], Optional[int]]:
    """Find the Decisions & Consensus section."""
    lines = content.split('\n')
    start_idx = None
    end_idx = None
    
    # Pattern: "## 4. Decisions & Consensus"
    for i, line in enumerate(lines):
        if re.match(r'^##\s+4\.\s+Decisions\s+&\s+Consensus', line, re.IGNORECASE):
            start_idx = i
            break
    
    if start_idx is None:
        return None, None
    
    # Find next major section (## 5.)
    for i in range(start_idx + 1, len(lines)):
        if re.match(r'^##\s+[5-9]\.', lines[i]):
            end_idx = i
            break
    
    if end_idx is None:
        end_idx = len(lines)
    
    return start_idx, end_idx


def get_next_decision_number(content: str) -> int:
    """Get the next decision number."""
    decision_matches = re.findall(r'^###\s+Decision\s+(\d+):', content, re.MULTILINE)
    if decision_matches:
        return max(int(n) for n in decision_matches) + 1
    return 1


def format_decision(
    decision_number: int,
    agent_id: str,
    decision_title: str,
    decision_content: str,
    status: str = "⏳ Pending Consensus",
    voting: str = "Awaiting votes",
    timestamp: Optional[datetime] = None
) -> str:
    """Format a decision block."""
    if timestamp is None:
        timestamp = datetime.now()
    
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    decision_block = f"""
### Decision {decision_number}: {decision_title}

**Proposed by**: {agent_id}
**Timestamp**: {timestamp_str}
**Status**: {status}

**Content**:
{decision_content}

**Voting**: {voting}

**Rationale**: 
[To be documented]

**Action Items**:
- [ ] Review by all agents
- [ ] Reach consensus
- [ ] Document final decision

---
"""
    return decision_block


def append_decision_with_retry(
    session_file: Path,
    agent_id: str,
    decision_title: str,
    decision_content: str,
    status: str = "⏳ Pending Consensus",
    voting: str = "Awaiting votes",
    max_retries: int = MAX_RETRIES
) -> bool:
    """Safely append decision with retry mechanism."""
    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        return False
    
    for attempt in range(max_retries):
        try:
            current_content = session_file.read_text(encoding='utf-8')
            content_hash_before = hash(current_content)
            
            start_idx, end_idx = find_decisions_section(current_content)
            
            if start_idx is None:
                print("Error: Decisions & Consensus section not found", file=sys.stderr)
                return False
            
            decision_number = get_next_decision_number(current_content)
            decision_block = format_decision(
                decision_number, agent_id, decision_title, decision_content, status, voting
            )
            
            lines = current_content.split('\n')
            new_lines = lines[:end_idx] + [decision_block] + lines[end_idx:]
            new_content = '\n'.join(new_lines)
            
            # Verify file hasn't changed
            try:
                verify_content = session_file.read_text(encoding='utf-8')
                if hash(verify_content) != content_hash_before:
                    if attempt < max_retries - 1:
                        print(f"⚠️  File changed, retrying... (attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                        time.sleep(RETRY_DELAY * (attempt + 1))
                        continue
            except Exception:
                pass
            
            session_file.write_text(new_content, encoding='utf-8')
            
            print(f"✅ Successfully appended Decision {decision_number} from {agent_id}")
            print(f"   Decision: {decision_title}")
            print(f"   Status: {status}")
            print(f"   File: {session_file}")
            return True
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️  Error on attempt {attempt + 1}/{max_retries}: {e}", file=sys.stderr)
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
        description='Safely append decision to Decisions & Consensus section',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python append_decision.py session.md "Agent 4" "Protocol Update" "Update protocol with new rules"
  python append_decision.py session.md "Agent 4" "Approved Decision" "Decision content" --status "✅ Approved" --voting "4/4 agents"
        """
    )
    parser.add_argument('session_file', type=str, help='Path to session file')
    parser.add_argument('agent_id', type=str, help='Agent ID')
    parser.add_argument('decision_title', type=str, help='Decision title')
    parser.add_argument('decision_content', type=str, help='Decision content')
    parser.add_argument('--status', type=str, default='⏳ Pending Consensus', help='Decision status')
    parser.add_argument('--voting', type=str, default='Awaiting votes', help='Voting status')
    parser.add_argument('--max-retries', type=int, default=MAX_RETRIES, help='Max retries')
    
    args = parser.parse_args()
    
    success = append_decision_with_retry(
        Path(args.session_file),
        args.agent_id,
        args.decision_title,
        args.decision_content,
        args.status,
        args.voting,
        args.max_retries
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
