#!/usr/bin/env python3
"""
LangGraph Bug Fix Workflow Example

Demonstrates the bug fix workflow with LangGraph orchestration.
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
    """Run bug fix workflow with LangGraph"""
    
    print("=" * 70)
    print("LangGraph Bug Fix Workflow")
    print("=" * 70)
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
    print("Initializing LangGraph Orchestrator...")
    orchestrator = LangGraphOrchestrator(
        workspace=workspace,
        config=config.__dict__ if hasattr(config, '__dict__') else config
    )
    print("✓ Orchestrator initialized")
    print()
    
    # Define bug
    requirement = "Fix authentication token expiration bug"
    bug_description = """
    Bug: JWT tokens are not expiring correctly in the authentication system.
    
    Current Behavior:
    - Tokens set with 1-hour expiration remain valid indefinitely
    - Token refresh mechanism not working
    - No proper token invalidation on logout
    
    Expected Behavior:
    - Tokens should expire after the configured time period
    - Token refresh should generate new valid tokens
    - Logout should invalidate tokens immediately
    
    Environment:
    - FastAPI application
    - JWT tokens with RS256 algorithm
    - Redis for token blacklist
    
    Steps to Reproduce:
    1. Login and receive JWT token with exp=3600 (1 hour)
    2. Wait 2 hours
    3. Make authenticated API call with expired token
    4. Request still succeeds (should fail with 401)
    
    Suspected Root Cause:
    - Token expiration not being checked properly in middleware
    - Possible timezone issue with datetime comparison
    - Token blacklist not being consulted
    """
    
    print("Bug Report:")
    print("-" * 70)
    print(f"Title: {requirement}")
    print()
    print(bug_description.strip())
    print("-" * 70)
    print()
    
    print("Executing Bug Fix Workflow...")
    print("Steps:")
    print("  1. QA Engineer → Bug Analysis & Reproduction")
    print("  2. Developer → Bug Fix Implementation")
    print("  3. QA Engineer → Regression Testing")
    print("  4. Technical Writer → Release Notes")
    print()
    print("Starting execution...")
    print("=" * 70)
    print()
    
    try:
        # Execute workflow
        final_state = await orchestrator.execute_bug_fix(
            requirement=requirement,
            bug_description=bug_description
        )
        
        print()
        print("=" * 70)
        print("Bug Fix Workflow Completed!")
        print("=" * 70)
        print()
        
        # Extract actual state
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
            for file_path in files_created:
                print(f"  • {file_path}")
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
        
        print("Check the 'output' directory for detailed results!")
        print()
        
    except Exception as e:
        print()
        print("Error executing bug fix workflow:", str(e))
        logger.error(f"Bug fix workflow failed: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
