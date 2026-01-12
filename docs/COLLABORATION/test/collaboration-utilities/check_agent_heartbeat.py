#!/usr/bin/env python3
"""
Heartbeat monitoring utility for multi-agent collaboration sessions.

This script parses collaboration session files and checks agent activity
based on `last_activity` timestamps. Agents with no activity for >15 minutes
are considered inactive.

Usage:
    python check_agent_heartbeat.py <session_file>
    python check_agent_heartbeat.py COLLABORATION_SESSION_2026-01-10_14-21-28.md
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple


# Timeout in minutes
HEARTBEAT_TIMEOUT_MINUTES = 15


def parse_last_activity(content: str, agent_id: str) -> Optional[datetime]:
    """
    Extract last_activity timestamp for a specific agent from session file.
    
    Args:
        content: Content of the collaboration session file
        agent_id: Agent identifier (e.g., "Agent 1", "Agent-001")
    
    Returns:
        datetime object if found, None otherwise
    """
    # Pattern to match "Last Activity: YYYY-MM-DD HH:MM:SS" in agent sections
    patterns = [
        # Pattern 1: In "Agent X - Current Status" sections
        rf"##\s+{re.escape(agent_id)}\s+-\s+Current\s+Status[^#]*?Last\s+Activity[:\s]+(\d{{4}}-\d{{2}}-\d{{2}}\s+\d{{2}}:\d{{2}}:\d{{2}})",
        # Pattern 2: In agent introduction sections
        rf"###\s+{re.escape(agent_id)}[^#]*?last_activity[:\s]+(\d{{4}}-\d{{2}}-\d{{2}}\s+\d{{2}}:\d{{2}}:\d{{2}})",
        # Pattern 3: Generic "Last Activity" pattern
        rf"Last\s+Activity[:\s]+(\d{{4}}-\d{{2}}-\d{{2}}\s+\d{{2}}:\d{{2}}:\d{{2}})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            try:
                timestamp_str = match.group(1)
                return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
    
    return None


def get_heartbeat_status(last_activity: Optional[datetime]) -> Tuple[str, str, Optional[int]]:
    """
    Determine heartbeat status based on last_activity timestamp.
    
    Args:
        last_activity: datetime of last activity, or None if not found
    
    Returns:
        Tuple of (status_emoji, status_text, minutes_since_activity)
    """
    if last_activity is None:
        return "❌", "Offline", None
    
    now = datetime.now()
    delta = now - last_activity
    minutes_since = int(delta.total_seconds() / 60)
    
    if minutes_since <= HEARTBEAT_TIMEOUT_MINUTES:
        return "✅", "Active", minutes_since
    elif minutes_since <= HEARTBEAT_TIMEOUT_MINUTES * 2:
        return "⚠️", "Inactive", minutes_since
    else:
        return "❌", "Offline", minutes_since


def check_session_heartbeat(session_file: Path) -> Dict[str, Dict]:
    """
    Check heartbeat status for all agents in a collaboration session.
    
    Args:
        session_file: Path to collaboration session markdown file
    
    Returns:
        Dictionary mapping agent_id to heartbeat information
    """
    if not session_file.exists():
        raise FileNotFoundError(f"Session file not found: {session_file}")
    
    content = session_file.read_text(encoding='utf-8')
    
    # Find all agent identifiers in the file
    agent_pattern = r'Agent\s+([0-9]+|[\w-]+)'
    agent_ids = set(re.findall(agent_pattern, content, re.IGNORECASE))
    
    # Also try to find agent IDs from section headers
    section_pattern = r'###\s+Agent\s+([0-9]+)'
    section_agents = re.findall(section_pattern, content)
    agent_ids.update(section_agents)
    
    results = {}
    
    # Check heartbeat for each agent
    for agent_num in sorted(set(agent_ids), key=lambda x: int(x) if x.isdigit() else 999):
        agent_id = f"Agent {agent_num}"
        last_activity = parse_last_activity(content, agent_id)
        status_emoji, status_text, minutes_since = get_heartbeat_status(last_activity)
        
        results[agent_id] = {
            'last_activity': last_activity.strftime("%Y-%m-%d %H:%M:%S") if last_activity else None,
            'status_emoji': status_emoji,
            'status_text': status_text,
            'minutes_since': minutes_since,
        }
    
    return results


def print_heartbeat_report(results: Dict[str, Dict], session_file: Path):
    """Print formatted heartbeat report."""
    print(f"\n{'='*60}")
    print(f"Heartbeat Report: {session_file.name}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Timeout Threshold: {HEARTBEAT_TIMEOUT_MINUTES} minutes")
    print(f"{'='*60}\n")
    
    if not results:
        print("⚠️  No agents found in session file.")
        return
    
    print(f"{'Agent':<15} {'Status':<12} {'Last Activity':<20} {'Time Since':<15}")
    print("-" * 60)
    
    for agent_id, info in sorted(results.items()):
        status_display = f"{info['status_emoji']} {info['status_text']}"
        last_act = info['last_activity'] or "Unknown"
        time_since = f"{info['minutes_since']} min" if info['minutes_since'] is not None else "N/A"
        
        print(f"{agent_id:<15} {status_display:<12} {last_act:<20} {time_since:<15}")
    
    print("\n" + "="*60)
    
    # Summary
    active_count = sum(1 for r in results.values() if r['status_text'] == 'Active')
    inactive_count = sum(1 for r in results.values() if r['status_text'] == 'Inactive')
    offline_count = sum(1 for r in results.values() if r['status_text'] == 'Offline')
    
    print(f"\nSummary: {len(results)} agents - {active_count} Active, {inactive_count} Inactive, {offline_count} Offline")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python check_agent_heartbeat.py <session_file>")
        print("Example: python check_agent_heartbeat.py COLLABORATION_SESSION_2026-01-10_14-21-28.md")
        sys.exit(1)
    
    session_file = Path(sys.argv[1])
    
    try:
        results = check_session_heartbeat(session_file)
        print_heartbeat_report(results, session_file)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing session file: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
