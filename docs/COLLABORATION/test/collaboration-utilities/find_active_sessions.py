#!/usr/bin/env python3
"""
Find active collaboration sessions utility.

This script searches for active collaboration session files in the specified
directory and returns information about active sessions based on agent activity.

Usage:
    python find_active_sessions.py [--dir <directory>] [--min-agents <number>]
    
Environment Variable:
    COLLABORATION_SESSIONS_DIR - Default directory to search (if not specified)
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


def find_session_files(directory: Path) -> List[Path]:
    """Find all collaboration session files in directory."""
    pattern = r"COLLABORATION_SESSION_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.md"
    session_files = []
    
    for file_path in directory.rglob("*.md"):
        if re.match(pattern, file_path.name):
            session_files.append(file_path)
    
    return sorted(session_files, reverse=True)  # Most recent first


def parse_session_metadata(file_path: Path) -> Dict:
    """Parse basic metadata from session file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        metadata = {
            'file': file_path,
            'name': file_path.name,
            'path': str(file_path),
            'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
            'agents': [],
            'session_id': None,
            'date': None,
            'status': 'unknown',
        }
        
        # Extract session ID
        id_match = re.search(r'Session ID[:\s]+([A-Z0-9_-]+)', content, re.IGNORECASE)
        if id_match:
            metadata['session_id'] = id_match.group(1)
        
        # Extract date
        date_match = re.search(r'\*\*Date\*\*[:\s]+(\d{4}-\d{2}-\d{2})', content, re.IGNORECASE)
        if date_match:
            metadata['date'] = date_match.group(1)
        
        # Count agents
        agent_matches = re.findall(r'###\s+Agent\s+([0-9]+)', content)
        unique_agents = set(agent_matches)
        metadata['agents'] = sorted([f"Agent {a}" for a in unique_agents], key=lambda x: int(x.split()[1]))
        metadata['agent_count'] = len(unique_agents)
        
        # Check status
        if '✅ Active' in content or 'Status.*✅.*Active' in content:
            metadata['status'] = 'active'
        elif 'Phase 1 COMPLETE' in content or 'Phase 2' in content:
            metadata['status'] = 'in_progress'
        elif 'COMPLETE' in content or 'complete' in content.lower():
            metadata['status'] = 'complete'
        
        return metadata
    except Exception as e:
        return {
            'file': file_path,
            'name': file_path.name,
            'error': str(e)
        }


def is_recently_active(metadata: Dict, hours: int = 24) -> bool:
    """Check if session was recently active."""
    if 'modified' not in metadata:
        return False
    return datetime.now() - metadata['modified'] < timedelta(hours=hours)


def find_active_sessions(directory: Optional[Path] = None, min_agents: int = 1, recent_hours: int = 24) -> List[Dict]:
    """
    Find active collaboration sessions.
    
    Args:
        directory: Directory to search (default: COLLABORATION_SESSIONS_DIR env var or current dir)
        min_agents: Minimum number of agents required for session to be considered active
        recent_hours: Sessions modified within this many hours are considered recent
    
    Returns:
        List of session metadata dictionaries
    """
    if directory is None:
        env_dir = os.getenv('COLLABORATION_SESSIONS_DIR')
        if env_dir:
            directory = Path(env_dir)
        else:
            directory = Path.cwd()
    
    directory = Path(directory)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    session_files = find_session_files(directory)
    sessions = []
    
    for file_path in session_files:
        metadata = parse_session_metadata(file_path)
        
        # Filter by agent count
        if metadata.get('agent_count', 0) >= min_agents:
            # Check if recently active
            if is_recently_active(metadata, recent_hours):
                metadata['recently_active'] = True
            else:
                metadata['recently_active'] = False
            
            sessions.append(metadata)
    
    return sessions


def print_sessions_report(sessions: List[Dict]):
    """Print formatted sessions report."""
    if not sessions:
        print("\n⚠️  No active collaboration sessions found.")
        return
    
    print(f"\n{'='*80}")
    print(f"Active Collaboration Sessions Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Found: {len(sessions)} session(s)")
    print(f"{'='*80}\n")
    
    print(f"{'Session ID':<30} {'Date':<12} {'Agents':<20} {'Status':<15} {'Modified':<20}")
    print("-" * 80)
    
    for session in sessions:
        session_id = session.get('session_id', session['name'][:28]) or 'N/A'
        date = session.get('date', 'N/A')
        agents = f"{session.get('agent_count', 0)} ({', '.join(session.get('agents', [])[:3])})" if session.get('agents') else '0'
        status = session.get('status', 'unknown')
        modified = session['modified'].strftime('%Y-%m-%d %H:%M:%S') if 'modified' in session else 'N/A'
        
        # Truncate if too long
        if len(agents) > 18:
            agents = agents[:15] + '...'
        
        print(f"{session_id:<30} {date:<12} {agents:<20} {status:<15} {modified:<20}")
    
    print("\n" + "="*80)
    
    # Summary
    active_count = sum(1 for s in sessions if s.get('recently_active', False))
    total_agents = sum(s.get('agent_count', 0) for s in sessions)
    
    print(f"\nSummary: {len(sessions)} sessions, {active_count} recently active, {total_agents} total agents")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Find active collaboration sessions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python find_active_sessions.py
  python find_active_sessions.py --dir ./docs/COLLABORATION
  python find_active_sessions.py --min-agents 2 --recent-hours 12
  COLLABORATION_SESSIONS_DIR=/path/to/sessions python find_active_sessions.py
        """
    )
    
    parser.add_argument(
        '--dir', '-d',
        type=str,
        help='Directory to search for session files (default: COLLABORATION_SESSIONS_DIR env var or current directory)'
    )
    parser.add_argument(
        '--min-agents', '-m',
        type=int,
        default=1,
        help='Minimum number of agents required (default: 1)'
    )
    parser.add_argument(
        '--recent-hours', '-r',
        type=int,
        default=24,
        help='Sessions modified within this many hours are considered recent (default: 24)'
    )
    
    args = parser.parse_args()
    
    directory = Path(args.dir) if args.dir else None
    
    try:
        sessions = find_active_sessions(directory, args.min_agents, args.recent_hours)
        print_sessions_report(sessions)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
