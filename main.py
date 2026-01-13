import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

from src.config import load_config
from src.orchestrator import LangGraphOrchestrator


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
    
    logger.info("Starting Multi-Agent System with LangGraph Orchestration")
    logger.info(f"Workspace: {config.cursor_workspace}")
    
    Path(config.output_directory).mkdir(parents=True, exist_ok=True)
    
    orchestrator = LangGraphOrchestrator(
        cursor_workspace=config.cursor_workspace,
        config=config.to_dict()
    )
    
    logger.info("System initialized successfully")
    logger.info(f"Available agents: {len(orchestrator.agents)}")
    
    print("\n" + "="*80)
    print("LLM Multi-Agent System - LangGraph Orchestration")
    print("="*80)
    print("\nAvailable Workflow Types:")
    print("  1. Feature Development")
    print("  2. Bug Fix")
    print("\n" + "="*80 + "\n")
    
    requirement = input("Enter your requirement (or 'quit' to exit): ").strip()
    
    if requirement.lower() in ['quit', 'exit', 'q']:
        logger.info("Shutting down system")
        return
    
    if not requirement:
        logger.error("No requirement provided")
        return
    
    print("\nSelect workflow type:")
    print("  1. Feature Development")
    print("  2. Bug Fix")
    
    try:
        choice = int(input("\nEnter choice (1-2): ").strip())
        
        if choice == 1:
            workflow_type = "feature_development"
        elif choice == 2:
            workflow_type = "bug_fix"
            bug_description = input("Enter bug description: ").strip()
            if not bug_description:
                logger.error("Bug description required for bug fix workflow")
                return
        else:
            logger.error("Invalid choice, using default: feature_development")
            workflow_type = "feature_development"
    except ValueError:
        logger.error("Invalid input, using default: feature_development")
        workflow_type = "feature_development"
    
    logger.info(f"Processing requirement with workflow: {workflow_type}")
    print(f"\nExecuting {workflow_type} workflow...")
    print("This may take several minutes depending on the complexity...\n")
    
    try:
        if workflow_type == "bug_fix":
            final_state = await orchestrator.execute_bug_fix(
                requirement=requirement,
                bug_description=bug_description
            )
        else:
            final_state = await orchestrator.execute_feature_development(
                requirement=requirement
            )
        
        print("\n" + "="*80)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*80)
        
        # Extract the actual state from the event dict
        actual_state = list(final_state.values())[0] if final_state else {}
        
        print(f"\nWorkflow ID: {actual_state.get('workflow_id', 'N/A')}")
        print(f"Status: {actual_state.get('status', 'N/A')}")
        print(f"Completed Steps: {len(actual_state.get('completed_steps', []))}")
        print(f"Files Created: {len(actual_state.get('files_created', []))}")
        
        if actual_state.get('errors'):
            print(f"\nErrors: {len(actual_state.get('errors', []))}")
            for error in actual_state.get('errors', []):
                print(f"  - {error.get('step', 'unknown')}: {error.get('error', 'N/A')}")
        
        output_file = Path(config.output_directory) / f"langgraph_{actual_state.get('workflow_id', 'workflow')}.json"
        
        import json
        with open(output_file, 'w') as f:
            json.dump(actual_state, f, indent=2, default=str)
        
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
