#!/usr/bin/env python3
"""
Quick test script to verify cursor-agent-tools integration
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.agents import BusinessAnalystAgent
from src.agents.base_agent import Task


async def test_agent():
    """Test a single agent with a simple task"""
    
    print("="*80)
    print("Testing Cursor Agent Tools Integration")
    print("="*80)
    
    # Create a Business Analyst agent
    agent = BusinessAnalystAgent(
        agent_id="test_ba",
        cursor_workspace="/Users/andrey.karazhev/Developer/spg/llm-multi-agent-system",
        config={'cursor_cli_path': 'cursor'}
    )
    
    print(f"\n✓ Created agent: {agent.agent_id}")
    print(f"  Role: {agent.role.value}")
    print(f"  Status: {agent.status.value}")
    
    # Create a simple test task
    task = Task(
        task_id="test_001",
        description="Analyze a simple requirement",
        context={
            "requirement": "Create a simple REST API endpoint that returns 'Hello World'"
        }
    )
    
    print(f"\n✓ Created task: {task.task_id}")
    print(f"  Description: {task.description}")
    
    print("\n" + "-"*80)
    print("Executing task...")
    print("-"*80 + "\n")
    
    try:
        # Run the task
        completed_task = await agent.run_task(task)
        
        print("\n" + "="*80)
        if completed_task.result:
            print("✓ TEST PASSED - Task completed successfully!")
            print("="*80)
            print("\nAgent Response:")
            print("-"*80)
            print(completed_task.result.get('analysis', 'No analysis'))
            print("-"*80)
        else:
            print("✗ TEST FAILED - Task did not complete")
            print("="*80)
            if completed_task.error:
                print(f"\nError: {completed_task.error}")
        
        print(f"\nTask Status:")
        print(f"  Completed: {completed_task.completed_at is not None}")
        print(f"  Has Result: {completed_task.result is not None}")
        print(f"  Has Error: {completed_task.error is not None}")
        
        return completed_task.result is not None and not completed_task.error
        
    except Exception as e:
        print("\n" + "="*80)
        print("✗ TEST FAILED - Exception occurred")
        print("="*80)
        print(f"\nException: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    print("\nChecking API configuration...")
    
    import os
    from dotenv import load_dotenv
    
    # Load .env file if it exists
    load_dotenv()
    
    has_anthropic = bool(os.getenv('ANTHROPIC_API_KEY'))
    has_openai = bool(os.getenv('OPENAI_API_KEY'))
    has_ollama = bool(os.getenv('OLLAMA_HOST'))
    
    print(f"  Anthropic API: {'✓ Configured' if has_anthropic else '✗ Not configured'}")
    print(f"  OpenAI API: {'✓ Configured' if has_openai else '✗ Not configured'}")
    print(f"  Ollama: {'✓ Configured' if has_ollama else '✗ Not configured'}")
    
    if not (has_anthropic or has_openai or has_ollama):
        print("\n⚠️  WARNING: No API keys configured!")
        print("   Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or OLLAMA_HOST in .env file")
        print("\nTo test:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your API key")
        print("  3. Run this test again")
        return False
    
    # Run the test
    success = await test_agent()
    
    print("\n" + "="*80)
    if success:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("❌ TESTS FAILED")
    print("="*80 + "\n")
    
    return success


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
