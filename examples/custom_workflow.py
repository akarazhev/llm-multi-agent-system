#!/usr/bin/env python3
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


async def run_custom_workflow():
    orchestrator = LangGraphOrchestrator(
        workspace=str(PROJECT_ROOT)
    )
    
    requirement = """
    Build an e-commerce platform with product catalog, shopping cart, and payment integration.
    
    Requirements:
    - Target users: B2C customers
    - Scale: 10,000 daily active users
    - Microservices architecture with services: product-service, cart-service, payment-service, user-service
    - Implement product service first with Python/FastAPI
    - Create comprehensive test suite (unit, integration, e2e)
    - Set up Kubernetes deployment on AWS
    - Create API documentation (OpenAPI format)
    """
    
    print("Executing custom e-commerce workflow...\n")
    
    final_state = await orchestrator.execute_feature_development(
        requirement=requirement,
        context={
            "target_users": "B2C customers",
            "scale": "10,000 daily active users",
            "architecture": "microservices",
            "services": ["product-service", "cart-service", "payment-service", "user-service"],
            "language": "python",
            "framework": "fastapi",
            "deployment": "kubernetes",
            "cloud": "aws"
        }
    )
    
    print("\n" + "="*80)
    print("Custom Workflow Results")
    print("="*80)
    
    # Extract the actual state from the event dict
    actual_state = list(final_state.values())[0] if final_state else {}
    
    print(f"\nWorkflow ID: {actual_state.get('workflow_id', 'N/A')}")
    print(f"Status: {actual_state.get('status', 'N/A')}")
    print(f"Completed Steps: {', '.join(actual_state.get('completed_steps', []))}")
    print(f"Files Created: {len(actual_state.get('files_created', []))}")
    
    if actual_state.get('errors'):
        print(f"\nErrors: {len(actual_state.get('errors', []))}")
        for error in actual_state.get('errors', []):
            status = "✗" if error else "✓"
            print(f"{status} {error.get('step', 'unknown')}: {error.get('error', 'N/A')}")
    
    print(f"\nCompleted at: {actual_state.get('completed_at', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(run_custom_workflow())
