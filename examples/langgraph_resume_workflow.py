#!/usr/bin/env python3
"""
LangGraph Workflow Resume Example

Demonstrates how to resume an interrupted workflow using LangGraph's
checkpoint persistence feature.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator
from src.config.settings import load_config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Demonstrate workflow resumption"""
    
    print("=" * 70)
    print("LangGraph Workflow Resume Example")
    print("=" * 70)
    print()
    
    print("This example demonstrates LangGraph's checkpoint persistence feature.")
    print("You can interrupt the workflow (Ctrl+C) and resume it later.")
    print()
    
    # Load configuration
    try:
        config = load_config()
        workspace = config.workspace
    except Exception as e:
        logger.warning(f"Could not load config: {e}, using defaults")
        workspace = "."
        config = {
            "workspace": workspace,
            "agents": {}
        }
    
    # Create orchestrator
    orchestrator = LangGraphOrchestrator(
        workspace=workspace,
        config=config.__dict__ if hasattr(config, '__dict__') else config
    )
    
    # Check for existing checkpoints
    checkpoint_db = Path(workspace) / "checkpoints.db"
    
    if checkpoint_db.exists():
        print(f"✓ Found checkpoint database: {checkpoint_db}")
        print()
        print("Options:")
        print("  1. Resume an existing workflow")
        print("  2. Start a new workflow")
        print()
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            thread_id = input("Enter workflow ID (thread_id) to resume: ").strip()
            
            if thread_id:
                print(f"\nResuming workflow: {thread_id}")
                print("Note: The workflow will continue from its last checkpoint.")
                print()
                
                # Resume workflow
                try:
                    final_state = await orchestrator.execute_feature_development(
                        requirement="Resuming from checkpoint...",
                        thread_id=thread_id
                    )
                    
                    print("\n✓ Workflow resumed and completed!")
                    actual_state = list(final_state.values())[0] if final_state else {}
                    print(f"Status: {actual_state.get('status', 'N/A')}")
                    print(f"Completed Steps: {actual_state.get('completed_steps', [])}")
                    
                except Exception as e:
                    print(f"\n✗ Error resuming workflow: {e}")
                    logger.error(f"Resume failed: {e}", exc_info=True)
                
                return
    else:
        print("No checkpoint database found. Starting new workflow...")
        print()
    
    # Start new workflow with known thread_id for easy resumption
    thread_id = "demo_workflow_001"
    
    requirement = """
    Create a simple blog API with:
    - Post creation and retrieval
    - Comment system
    - User authentication
    - Tag support
    """
    
    print(f"Starting new workflow with thread_id: {thread_id}")
    print("You can interrupt this with Ctrl+C and resume later using:")
    print(f"  thread_id='{thread_id}'")
    print()
    print("Requirement:")
    print("-" * 70)
    print(requirement.strip())
    print("-" * 70)
    print()
    
    try:
        final_state = await orchestrator.execute_feature_development(
            requirement=requirement,
            thread_id=thread_id
        )
        
        print("\n✓ Workflow completed!")
        actual_state = list(final_state.values())[0] if final_state else {}
        print(f"Status: {actual_state.get('status', 'N/A')}")
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Workflow Interrupted!")
        print("=" * 70)
        print()
        print("The workflow state has been saved to checkpoint database.")
        print("To resume, run this script again and select option 1.")
        print(f"Use thread_id: {thread_id}")
        print()
        print("Or use the Python API:")
        print(f"""
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator

orchestrator = LangGraphOrchestrator(workspace=".")
final_state = await orchestrator.execute_feature_development(
    requirement="Resuming...",
    thread_id="{thread_id}"
)
        """)
        print()
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        logger.error(f"Workflow failed: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
