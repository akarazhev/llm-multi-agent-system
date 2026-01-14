#!/usr/bin/env python3
"""
Interactive Chat Workflow Example

This example demonstrates the enhanced interactive chat-like communication
between agents in the multi-agent system. You'll see:

- Real-time agent messages and thinking processes
- Inter-agent communication and handoffs
- Progress tracking with visual indicators
- File operations and task completions
- Color-coded agent interactions
- Comprehensive chat logs

Run this example to see how agents collaborate in a chat-like interface!
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env file from project root
load_dotenv(PROJECT_ROOT / '.env')

from src.orchestrator import LangGraphOrchestrator


async def run_interactive_chat_workflow():
    """
    Run a feature development workflow with interactive chat display.
    
    This example shows how agents communicate in a natural, chat-like format,
    making it easy to follow the workflow and understand what each agent is doing.
    """
    
    # Create orchestrator with chat display enabled (default)
    orchestrator = LangGraphOrchestrator(
        workspace=str(PROJECT_ROOT),
        enable_chat_display=True  # Enable interactive chat display
    )
    
    # Define a realistic requirement
    requirement = """
    Create a RESTful API for a task management system with the following features:
    
    Features:
    - User authentication with JWT tokens
    - CRUD operations for tasks (create, read, update, delete)
    - Task assignment to users
    - Task status tracking (todo, in-progress, completed)
    - Task priority levels (low, medium, high)
    - Due date management
    - Task filtering and search
    
    Technical Requirements:
    - Python with FastAPI framework
    - PostgreSQL database
    - SQLAlchemy ORM
    - Pydantic models for validation
    - JWT-based authentication
    - RESTful API design
    - Comprehensive test coverage
    - Docker containerization
    - API documentation with OpenAPI/Swagger
    
    Target: 1000+ concurrent users
    """
    
    print("\n" + "="*80)
    print("🤖 INTERACTIVE MULTI-AGENT CHAT WORKFLOW")
    print("="*80)
    print("\nWatch as agents communicate and collaborate in real-time!")
    print("Each agent will share their thoughts, actions, and deliverables.\n")
    
    try:
        # Execute the workflow with interactive chat display
        final_state = await orchestrator.execute_feature_development(
            requirement=requirement,
            context={
                "target_users": "B2C customers",
                "concurrent_users": 1000,
                "language": "python",
                "framework": "fastapi",
                "database": "postgresql",
                "deployment": "docker",
            }
        )
        
        # Extract the actual state from the event dict
        actual_state = list(final_state.values())[0] if final_state else {}
        
        # Print final summary
        print("\n" + "="*80)
        print("📊 WORKFLOW SUMMARY")
        print("="*80)
        
        print(f"\n✓ Workflow ID: {actual_state.get('workflow_id', 'N/A')}")
        print(f"✓ Status: {actual_state.get('status', 'N/A').upper()}")
        print(f"✓ Completed Steps: {len(actual_state.get('completed_steps', []))}")
        print(f"✓ Files Created: {len(actual_state.get('files_created', []))}")
        
        if actual_state.get('errors'):
            print(f"\n⚠️  Errors Encountered: {len(actual_state.get('errors', []))}")
            for error in actual_state.get('errors', []):
                print(f"   - {error.get('step', 'unknown')}: {error.get('error', 'N/A')}")
        
        # Show created files
        files_created = actual_state.get('files_created', [])
        if files_created:
            print(f"\n📄 Files Created:")
            for i, file_path in enumerate(files_created[:10], 1):
                file_name = Path(file_path).name
                print(f"   {i}. {file_name}")
            if len(files_created) > 10:
                print(f"   ... and {len(files_created) - 10} more files")
        
        # Show output location
        output_dir = PROJECT_ROOT / "output"
        workflow_id = actual_state.get('workflow_id', 'workflow')
        
        print(f"\n📁 Results saved to:")
        print(f"   - Workflow data: {output_dir / f'langgraph_{workflow_id}.json'}")
        print(f"   - Chat log: {output_dir / f'chat_log_{workflow_id}.json'}")
        
        print("\n" + "="*80)
        print("✨ Workflow completed! Check the output directory for all generated files.")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error executing workflow: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


async def demo_chat_display_only():
    """
    Demonstrate the chat display capabilities without running actual agents.
    Useful for testing the UI/UX of the chat interface.
    """
    from src.utils.chat_display import AgentChatDisplay
    
    chat = AgentChatDisplay()
    
    chat.print_header("Multi-Agent Chat Display Demo")
    
    chat.system_message("Initializing multi-agent workflow...", "start")
    
    # Simulate Business Analyst
    chat.agent_message(
        "business_analyst",
        "Analyzing requirements for task management API...\n"
        "I'll focus on user stories, acceptance criteria, and data models.",
        message_type="thinking"
    )
    
    await asyncio.sleep(1)
    
    chat.agent_action(
        "business_analyst",
        "is creating user stories and requirements documentation",
        "Identifying 8 user stories and 24 acceptance criteria"
    )
    
    await asyncio.sleep(1)
    
    chat.agent_completed(
        "business_analyst",
        "Requirements analysis complete. Identified 8 user stories, 24 acceptance criteria, and 3 data models.",
        files_created=[
            "docs/requirements.md",
            "docs/user_stories.md",
            "docs/data_models.md"
        ]
    )
    
    # Simulate handoff to Developer
    chat.inter_agent_communication(
        "business_analyst",
        "developer",
        "Requirements analysis complete. Passing user stories and data models for architecture design.",
        communication_type="handoff"
    )
    
    await asyncio.sleep(1)
    
    # Simulate Developer
    chat.agent_message(
        "developer",
        "Received requirements. Designing RESTful API architecture...\n"
        "Planning: FastAPI routes, SQLAlchemy models, JWT authentication middleware.",
        message_type="thinking"
    )
    
    await asyncio.sleep(1)
    
    chat.agent_action(
        "developer",
        "is designing system architecture",
        "Creating API endpoints, database schema, and authentication flow"
    )
    
    await asyncio.sleep(1)
    
    chat.agent_completed(
        "developer",
        "Architecture design complete. Defined 12 API endpoints, 5 database tables, and authentication system.",
        files_created=[
            "architecture/api_design.md",
            "architecture/database_schema.sql",
            "architecture/auth_flow.md"
        ]
    )
    
    # Show workflow status
    chat.workflow_status(
        "workflow_demo_20260113",
        "running",
        "implementation",
        ["business_analyst", "architecture_design"]
    )
    
    await asyncio.sleep(1)
    
    # Simulate parallel execution
    chat.system_message(
        "Implementation complete. Starting parallel QA and DevOps tasks...",
        "info"
    )
    
    await asyncio.sleep(0.5)
    
    chat.inter_agent_communication(
        "developer",
        "qa_engineer",
        "Implementation complete. Ready for testing and quality assurance.",
        communication_type="handoff"
    )
    
    await asyncio.sleep(0.5)
    
    chat.inter_agent_communication(
        "developer",
        "devops_engineer",
        "Implementation complete. Ready for deployment infrastructure setup.",
        communication_type="handoff"
    )
    
    await asyncio.sleep(1)
    
    # Simulate QA Engineer
    chat.agent_message(
        "qa_engineer",
        "Creating comprehensive test suite...\n"
        "Planning unit tests, integration tests, and API endpoint tests.",
        message_type="thinking"
    )
    
    await asyncio.sleep(1)
    
    chat.agent_completed(
        "qa_engineer",
        "Test suite complete. Created 45 unit tests, 15 integration tests, and 12 API tests.",
        files_created=[
            "tests/test_auth.py",
            "tests/test_tasks.py",
            "tests/test_api.py"
        ]
    )
    
    # Show conversation summary
    await asyncio.sleep(1)
    chat.conversation_summary()
    
    print("\n✨ Chat display demo completed!")


if __name__ == "__main__":
    print("\nSelect demo mode:")
    print("  1. Full interactive workflow (requires llama-server)")
    print("  2. Chat display demo only (no llama-server needed)")
    
    try:
        choice = input("\nEnter choice (1-2, default: 2): ").strip() or "2"
        
        if choice == "1":
            exit_code = asyncio.run(run_interactive_chat_workflow())
            sys.exit(exit_code or 0)
        else:
            asyncio.run(demo_chat_display_only())
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
