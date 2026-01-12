import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

from src.config import load_config
from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType


def setup_logging(log_level: str, log_file: Optional[str] = None):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers
    )


async def main():
    config = load_config()
    
    setup_logging(config.log_level, config.log_file)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Multi-Agent System with Cursor CLI Orchestration")
    logger.info(f"Workspace: {config.cursor_workspace}")
    
    Path(config.output_directory).mkdir(parents=True, exist_ok=True)
    
    orchestrator = AgentOrchestrator(
        cursor_workspace=config.cursor_workspace,
        config=config.to_dict()
    )
    
    workflow_engine = WorkflowEngine(orchestrator)
    
    logger.info("System initialized successfully")
    logger.info(f"Available agents: {len(orchestrator.agents)}")
    
    print("\n" + "="*80)
    print("LLM Multi-Agent System - Cursor CLI Orchestration")
    print("="*80)
    print("\nAvailable Workflow Types:")
    for i, wf_type in enumerate(workflow_engine.list_workflow_types(), 1):
        print(f"  {i}. {wf_type}")
    print("\n" + "="*80 + "\n")
    
    requirement = input("Enter your requirement (or 'quit' to exit): ").strip()
    
    if requirement.lower() in ['quit', 'exit', 'q']:
        logger.info("Shutting down system")
        return
    
    if not requirement:
        logger.error("No requirement provided")
        return
    
    print("\nSelect workflow type:")
    for i, wf_type in enumerate(workflow_engine.list_workflow_types(), 1):
        print(f"  {i}. {wf_type}")
    
    try:
        choice = int(input("\nEnter choice (1-5): ").strip())
        workflow_types = list(WorkflowType)
        
        if 1 <= choice <= len(workflow_types):
            selected_workflow = workflow_types[choice - 1]
        else:
            logger.error("Invalid choice, using default: FEATURE_DEVELOPMENT")
            selected_workflow = WorkflowType.FEATURE_DEVELOPMENT
    except ValueError:
        logger.error("Invalid input, using default: FEATURE_DEVELOPMENT")
        selected_workflow = WorkflowType.FEATURE_DEVELOPMENT
    
    logger.info(f"Processing requirement with workflow: {selected_workflow.value}")
    print(f"\nExecuting {selected_workflow.value} workflow...")
    print("This may take several minutes depending on the complexity...\n")
    
    try:
        result = await workflow_engine.execute_workflow(
            workflow_type=selected_workflow,
            requirement=requirement
        )
        
        print("\n" + "="*80)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"\nWorkflow Type: {result['workflow_type']}")
        print(f"Total Tasks: {result['result']['total_tasks']}")
        print(f"Completed At: {result['result']['completed_at']}")
        
        print("\nTask Results:")
        for task_id, task in result['result']['results'].items():
            print(f"\n  Task: {task_id}")
            print(f"  Status: {'✓ Completed' if task.result else '✗ Failed'}")
            if task.error:
                print(f"  Error: {task.error}")
        
        output_file = Path(config.output_directory) / f"workflow_{selected_workflow.value}_{result['result']['completed_at'].replace(':', '-')}.json"
        
        import json
        with open(output_file, 'w') as f:
            json.dump({
                'workflow_type': result['workflow_type'],
                'requirement': requirement,
                'completed_at': result['result']['completed_at'],
                'total_tasks': result['result']['total_tasks'],
                'tasks': {
                    task_id: {
                        'task_id': task.task_id,
                        'description': task.description,
                        'completed': task.completed_at is not None,
                        'error': task.error
                    }
                    for task_id, task in result['result']['results'].items()
                }
            }, f, indent=2)
        
        print(f"\nResults saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Error executing workflow: {e}", exc_info=True)
        print(f"\n✗ Error: {e}")
        return 1
    
    print("\n" + "="*80 + "\n")
    logger.info("System shutdown complete")
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code or 0)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
