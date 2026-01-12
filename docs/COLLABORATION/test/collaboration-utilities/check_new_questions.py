#!/usr/bin/env python3
"""
Check for new questions and action items in collaboration session file.

This utility implements the Mandatory File Check Protocol proposed by Agent 3,
automatically detecting new questions, action items, and critical issues.

Usage:
    python check_new_questions.py <session_file> [--agent <agent_id>]
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple


def find_questions_in_content(content: str) -> List[Dict]:
    """Find all questions in session file."""
    questions = []
    
    # Pattern 1: Explicit question markers
    question_patterns = [
        r'❓\s+(.+?)(?:\n|$)',
        r'\*\*Вопрос\*\*[:\s]+(.+?)(?:\n|$)',
        r'Questions?[:\s]+(.+?)(?:\n|$)',
        r'\?\s+(.+?)(?:\n|$)',
    ]
    
    # Pattern 2: Action Required sections
    action_pattern = r'Action Required[:\s]*\n((?:- \[[ x]\]\s+.+?\n?)+)'
    
    # Pattern 3: Critical markers
    critical_pattern = r'(🚨|🔴|⚠️)\s+CRITICAL[:\s]+(.+?)(?:\n|$)'
    
    lines = content.split('\n')
    
    # Search for questions
    for i, line in enumerate(lines):
        for pattern in question_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                questions.append({
                    'type': 'question',
                    'text': match.group(1).strip(),
                    'line': i + 1,
                    'context': '\n'.join(lines[max(0, i-2):min(len(lines), i+3)])
                })
    
    # Search for Action Required
    action_matches = re.finditer(action_pattern, content, re.MULTILINE | re.DOTALL)
    for match in action_matches:
        actions = match.group(1)
        for action_line in actions.split('\n'):
            if action_line.strip() and not action_line.strip().startswith('- [x]'):
                questions.append({
                    'type': 'action_required',
                    'text': action_line.strip(),
                    'line': content[:match.start()].count('\n') + 1,
                    'context': match.group(0)
                })
    
    # Search for critical issues
    critical_matches = re.finditer(critical_pattern, content, re.MULTILINE)
    for match in critical_matches:
        questions.append({
            'type': 'critical',
            'text': match.group(2).strip(),
            'line': content[:match.start()].count('\n') + 1,
            'context': match.group(0)
        })
    
    return questions


def find_unanswered_questions(content: str, agent_id: str = None) -> List[Dict]:
    """Find questions that haven't been answered by specified agent."""
    all_questions = find_questions_in_content(content)
    
    # Get all agent responses
    if agent_id:
        agent_responses = re.findall(
            rf'####\s+{re.escape(agent_id)}[^#]*?Timestamp[:\s]+(\d{{4}}-\d{{2}}-\d{{2}}\s+\d{{2}}:\d{{2}}:\d{{2}})',
            content,
            re.DOTALL
        )
        last_response_time = max(agent_responses) if agent_responses else None
    else:
        last_response_time = None
    
    # Filter unanswered questions (simplified - check if question is recent)
    unanswered = []
    for q in all_questions:
        # Simple heuristic: if question is in recent Discussion Log messages
        if 'Discussion Log' in q.get('context', ''):
            unanswered.append(q)
    
    return unanswered


def print_questions_report(questions: List[Dict], session_file: Path, agent_id: str = None):
    """Print formatted questions report."""
    print(f"\n{'='*80}")
    print(f"New Questions & Action Items Report")
    print(f"Session: {session_file.name}")
    if agent_id:
        print(f"Agent: {agent_id}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    if not questions:
        print("✅ No new questions or action items found.")
        return
    
    # Group by type
    by_type = {}
    for q in questions:
        q_type = q.get('type', 'unknown')
        if q_type not in by_type:
            by_type[q_type] = []
        by_type[q_type].append(q)
    
    # Print by type
    for q_type in ['critical', 'question', 'action_required']:
        if q_type not in by_type:
            continue
        
        type_name = {
            'critical': '🚨 CRITICAL ISSUES',
            'question': '❓ QUESTIONS',
            'action_required': '📋 ACTION REQUIRED'
        }.get(q_type, q_type.upper())
        
        print(f"\n{type_name}:")
        print("-" * 80)
        
        for i, q in enumerate(by_type[q_type], 1):
            print(f"\n{i}. Line {q.get('line', 'N/A')}:")
            print(f"   {q.get('text', 'N/A')[:100]}")
            if len(q.get('text', '')) > 100:
                print(f"   ...")
    
    print(f"\n{'='*80}")
    print(f"Summary: {len(questions)} items found")
    print(f"  - Critical: {len(by_type.get('critical', []))}")
    print(f"  - Questions: {len(by_type.get('question', []))}")
    print(f"  - Actions: {len(by_type.get('action_required', []))}")
    print(f"{'='*80}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Check for new questions and action items in collaboration session',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_new_questions.py session.md
  python check_new_questions.py session.md --agent-id "Agent 4"
  python check_new_questions.py session.md -a "Agent 4"
  python check_new_questions.py session.md --critical-only
        """
    )
    parser.add_argument('session_file', type=str, help='Path to session file')
    parser.add_argument('--agent-id', '-a', type=str, dest='agent', help='Agent ID to check unanswered questions for')
    
    args = parser.parse_args()
    
    session_file = Path(args.session_file)
    
    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        content = session_file.read_text(encoding='utf-8')
        
        if args.agent:
            questions = find_unanswered_questions(content, args.agent)
        else:
            questions = find_questions_in_content(content)
        
        print_questions_report(questions, session_file, args.agent)
        
        # Exit code: 0 if no questions, 1 if questions found (for automation)
        sys.exit(1 if questions else 0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
