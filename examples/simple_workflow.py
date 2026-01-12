import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType
from src.config import load_config


async def run_simple_workflow():
    config = load_config()
    
    orchestrator = AgentOrchestrator(
        cursor_workspace=config.cursor_workspace,
        config=config.to_dict()
    )
    
    workflow_engine = WorkflowEngine(orchestrator)
    
    requirement = "Create a REST API endpoint for user authentication with JWT tokens"
    
    print(f"Processing requirement: {requirement}\n")
    
    result = await workflow_engine.execute_workflow(
        workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
        requirement=requirement,
        context={
            "language": "python",
            "framework": "fastapi",
            "database": "postgresql"
        }
    )
    
    print("\nWorkflow completed!")
    print(f"Total tasks: {result['result']['total_tasks']}")
    print(f"Completed at: {result['result']['completed_at']}")
    
    for task_id, task in result['result']['results'].items():
        print(f"\nTask {task_id}:")
        print(f"  Description: {task.description}")
        print(f"  Status: {'Completed' if task.result else 'Failed'}")


if __name__ == "__main__":
    asyncio.run(run_simple_workflow())
