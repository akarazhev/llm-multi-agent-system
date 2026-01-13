#!/usr/bin/env python3
"""
LangGraph Feature Development Example

Demonstrates how to use the LangGraph orchestrator for feature development
with parallel execution, state persistence, and progress monitoring.
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
    """Run feature development workflow with LangGraph"""
    
    print("=" * 70)
    print("LangGraph Feature Development Workflow")
    print("=" * 70)
    print()
    
    # Load configuration
    try:
        config = load_config()
        workspace = config.cursor_workspace
    except Exception as e:
        logger.warning(f"Could not load config: {e}, using defaults")
        workspace = "."
        config = {
            "cursor_workspace": workspace,
            "agents": {}
        }
    
    # Create orchestrator
    print("Initializing LangGraph Orchestrator...")
    orchestrator = LangGraphOrchestrator(
        cursor_workspace=workspace,
        config=config.__dict__ if hasattr(config, '__dict__') else config
    )
    print("✓ Orchestrator initialized with state persistence enabled")
    print()
    
    # Define requirement
    requirement = """
    Create a REST API for an e-commerce product catalog with the following features:
    
    1. Product CRUD operations (Create, Read, Update, Delete)
    2. Category management
    3. Search and filtering capabilities
    4. Product image upload support
    5. Inventory tracking
    6. Price management with discounts
    
    Technical Requirements:
    - Use FastAPI framework
    - PostgreSQL database with SQLAlchemy ORM
    - JWT authentication
    - OpenAPI documentation
    - Docker containerization
    - Pytest for testing (minimum 80% coverage)
    """
    
    print("Requirement:")
    print("-" * 70)
    print(requirement.strip())
    print("-" * 70)
    print()
    
    # Additional context
    context = {
        "language": "python",
        "framework": "fastapi",
        "database": "postgresql",
        "deployment": "docker",
        "test_framework": "pytest",
        "min_coverage": 80
    }
    
    print("Executing workflow with LangGraph...")
    print("Features enabled:")
    print("  • Parallel execution (QA + DevOps run simultaneously)")
    print("  • State persistence (can resume if interrupted)")
    print("  • Conditional routing (stops on errors)")
    print("  • Progress monitoring")
    print()
    print("Workflow steps:")
    print("  1. Business Analyst → Requirements Analysis")
    print("  2. Developer → Architecture Design")
    print("  3. Developer → Implementation")
    print("  4. [PARALLEL] QA Engineer → Testing + DevOps → Infrastructure")
    print("  5. Technical Writer → Documentation")
    print()
    print("Starting execution...")
    print("=" * 70)
    print()
    
    try:
        # Execute workflow
        final_state = await orchestrator.execute_feature_development(
            requirement=requirement,
            context=context
        )
        
        print()
        print("=" * 70)
        print("Workflow Completed!")
        print("=" * 70)
        print()
        
        # Extract the actual state from the event dict
        actual_state = list(final_state.values())[0] if final_state else {}
        
        # Display results
        print("Results Summary:")
        print(f"  Workflow ID: {actual_state.get('workflow_id', 'N/A')}")
        print(f"  Status: {actual_state.get('status', 'N/A')}")
        print(f"  Completed Steps: {len(actual_state.get('completed_steps', []))}")
        print()
        
        # Files created
        files_created = actual_state.get('files_created', [])
        if files_created:
            print(f"Files Created ({len(files_created)}):")
            for file_path in files_created[:20]:  # Show first 20
                print(f"  • {file_path}")
            if len(files_created) > 20:
                print(f"  ... and {len(files_created) - 20} more")
        else:
            print("Files Created: None")
        print()
        
        # Errors
        errors = actual_state.get('errors', [])
        if errors:
            print(f"Errors ({len(errors)}):")
            for error in errors:
                print(f"  • Step: {error.get('step', 'unknown')}")
                print(f"    Error: {error.get('error', 'N/A')}")
        else:
            print("Errors: None")
        print()
        
        # Agent outputs
        print("Agent Outputs:")
        if actual_state.get('business_analysis'):
            print("  ✓ Business Analysis completed")
        if actual_state.get('architecture'):
            print("  ✓ Architecture Design completed")
        if actual_state.get('implementation'):
            print("  ✓ Implementation completed")
        if actual_state.get('tests'):
            print("  ✓ Test Suite completed")
        if actual_state.get('infrastructure'):
            print("  ✓ Infrastructure completed")
        if actual_state.get('documentation'):
            print("  ✓ Documentation completed")
        print()
        
        print("Check the 'output' directory for detailed results!")
        print(f"Results saved to: output/langgraph_{actual_state.get('workflow_id', 'unknown')}.json")
        print()
        
    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("Workflow Interrupted!")
        print("=" * 70)
        print()
        print("The workflow state has been saved to the checkpoint database.")
        print("You can resume it later by providing the same thread_id.")
        print()
        
    except Exception as e:
        print()
        print("=" * 70)
        print("Error!")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        logger.error(f"Workflow execution failed: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
