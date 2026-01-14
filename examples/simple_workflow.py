import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / '.env')

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import LangGraphOrchestrator
from src.config import load_config


async def run_simple_workflow():
    config = load_config()
    
    orchestrator = LangGraphOrchestrator(
        workspace=config.workspace,
        config=config.to_dict()
    )
    
    requirement = "Create a REST API endpoint for user authentication with JWT tokens"
    
    print(f"Processing requirement: {requirement}\n")
    
    final_state = await orchestrator.execute_feature_development(
        requirement=requirement,
        context={
            "language": "python",
            "framework": "fastapi",
            "database": "postgresql"
        }
    )
    
    print("\nWorkflow completed!")
    
    # Extract the actual state from the event dict
    actual_state = list(final_state.values())[0] if final_state else {}
    
    print(f"Workflow ID: {actual_state.get('workflow_id', 'N/A')}")
    print(f"Status: {actual_state.get('status', 'N/A')}")
    print(f"Completed Steps: {len(actual_state.get('completed_steps', []))}")
    print(f"Files Created: {len(actual_state.get('files_created', []))}")
    
    if actual_state.get('errors'):
        print(f"\nErrors: {len(actual_state.get('errors', []))}")
        for error in actual_state.get('errors', []):
            print(f"  - {error.get('step', 'unknown')}: {error.get('error', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(run_simple_workflow())
