#!/usr/bin/env python3
"""
Safely append a step to Step-by-Step Execution section.

This utility implements append-only approach for Steps section,
preventing conflicts when multiple agents add steps simultaneously.

Usage:
    python append_step.py <session_file> <agent_id> <step_name> <description> [--status <status>]
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


def find_steps_section(content: str) -> Tuple[Optional[int], Optional[int]]:
    """Find the Step-by-Step Execution section."""
    lines = content.split('\n')
    start_idx = None
    end_idx = None
    
    # Pattern: "## 5. Step-by-Step Execution"
    for i, line in enumerate(lines):
        if re.match(r'^##\s+5\.\s+Step-by-Step\s+Execution', line, re.IGNORECASE):
            start_idx = i
            break
    
    if start_idx is None:
        return None, None
    
    # Find next major section (## 6.)
    for i in range(start_idx + 1, len(lines)):
        if re.match(r'^##\s+[6-9]\.', lines[i]):
            end_idx = i
            break
    
    if end_idx is None:
        end_idx = len(lines)
    
    return start_idx, end_idx


def get_next_step_number(content: str) -> int:
    """Get the next step number."""
    step_matches = re.findall(r'^###\s+Step\s+(\d+):', content, re.MULTILINE)
    if step_matches:
        return max(int(n) for n in step_matches) + 1
    return 1


def format_step(
    step_number: int,
    agent_id: str,
    step_name: str,
    description: str,
    status: str = "🔄 In Progress",
    timestamp: Optional[datetime] = None
) -> str:
    """Format a step block."""
    if timestamp is None:
        timestamp = datetime.now()
    
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    step_block = f"""
### Step {step_number}: {step_name}
**Performed by**: {agent_id}
**Status**: {status}
**Timestamp**: {timestamp_str}

**Description**: 
{description}

**Changes Made**:
- [To be documented by {agent_id}]

**Impact on Other Agents**:
- [To be documented]

**Questions / Blockers**:
- None currently

**Next Agent Action**:
- [To be determined]

---
"""
    return step_block


def append_step_with_retry(
    session_file: Path,
    agent_id: str,
    step_name: str,
    description: str,
    status: str = "🔄 In Progress",
    max_retries: int = MAX_RETRIES
) -> bool:
    """Safely append step with retry mechanism."""
    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        return False
    
    for attempt in range(max_retries):
        try:
            current_content = session_file.read_text(encoding='utf-8')
            content_hash_before = hash(current_content)
            
            start_idx, end_idx = find_steps_section(current_content)
            
            if start_idx is None:
                print("Error: Step-by-Step Execution section not found", file=sys.stderr)
                return False
            
            step_number = get_next_step_number(current_content)
            step_block = format_step(step_number, agent_id, step_name, description, status)
            
            lines = current_content.split('\n')
            new_lines = lines[:end_idx] + [step_block] + lines[end_idx:]
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
            
            print(f"✅ Successfully appended Step {step_number} from {agent_id}")
            print(f"   Step: {step_name}")
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
        description='Safely append step to Step-by-Step Execution section'
    )
    parser.add_argument('session_file', type=str, help='Path to session file')
    parser.add_argument('agent_id', type=str, help='Agent ID')
    parser.add_argument('step_name', type=str, help='Step name')
    parser.add_argument('description', type=str, help='Step description')
    parser.add_argument('--status', type=str, default='🔄 In Progress', help='Step status')
    parser.add_argument('--max-retries', type=int, default=MAX_RETRIES, help='Max retries')
    
    args = parser.parse_args()
    
    success = append_step_with_retry(
        Path(args.session_file),
        args.agent_id,
        args.step_name,
        args.description,
        args.status,
        args.max_retries
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
