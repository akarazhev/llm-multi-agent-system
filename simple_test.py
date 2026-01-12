#!/usr/bin/env python3
"""
Simple single-agent test - much faster than full workflow
"""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()
load_dotenv()
sys.path.insert(0, str(PROJECT_ROOT))

from src.agents import DeveloperAgent
from src.agents.base_agent import Task


async def simple_test():
    print("="*80)
    print("Simple Developer Agent Test")
    print("="*80)
    
    # Create a developer agent
    agent = DeveloperAgent(
        agent_id="dev_simple",
        cursor_workspace=str(PROJECT_ROOT),
        config={'cursor_cli_path': 'cursor'}
    )
    
    print(f"\n✓ Agent created: {agent.agent_id}")
    
    # Simple task: Create a basic Python function
    task = Task(
        task_id="simple_001",
        description="Create a Python function to calculate factorial",
        context={
            "requirement": "Write a simple Python function called 'factorial' that takes an integer n and returns n!",
            "language": "python"
        }
    )
    
    print(f"✓ Task created: {task.description}")
    print("\n" + "-"*80)
    print("Executing task with local llama-server...")
    print("-"*80 + "\n")
    
    # Run the task
    completed_task = await agent.run_task(task)
    
    print("\n" + "="*80)
    if completed_task.result and not completed_task.error:
        print("✓ SUCCESS!")
        print("="*80)
        print("\nGenerated Code:")
        print("-"*80)
        print(completed_task.result.get('implementation', 'No implementation'))
        print("-"*80)
    else:
        print("✗ FAILED")
        print("="*80)
        if completed_task.error:
            print(f"\nError: {completed_task.error}")
    
    print("\n" + "="*80 + "\n")
    return completed_task.result is not None and not completed_task.error


if __name__ == "__main__":
    try:
        success = asyncio.run(simple_test())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
