#!/usr/bin/env python3
import asyncio
import sys
import os
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

from src.orchestrator import AgentOrchestrator
from src.agents.base_agent import Task
from src.agents import AgentRole


async def run_custom_workflow():
    orchestrator = AgentOrchestrator(
        cursor_workspace=str(PROJECT_ROOT)
    )
    
    custom_workflow = [
        {
            "task_id": "analyze_001",
            "agent_role": "business_analyst",
            "description": "Analyze the e-commerce platform requirements",
            "context": {
                "requirement": "Build an e-commerce platform with product catalog, shopping cart, and payment integration",
                "target_users": "B2C customers",
                "scale": "10,000 daily active users"
            }
        },
        {
            "task_id": "design_001",
            "agent_role": "developer",
            "description": "Design the microservices architecture",
            "context": {
                "requirement": "Microservices architecture for e-commerce",
                "services": ["product-service", "cart-service", "payment-service", "user-service"]
            },
            "dependencies": ["analyze_001"]
        },
        {
            "task_id": "implement_001",
            "agent_role": "developer",
            "description": "Implement the product service",
            "context": {
                "service": "product-service",
                "language": "python",
                "framework": "fastapi"
            },
            "dependencies": ["design_001"]
        },
        {
            "task_id": "test_001",
            "agent_role": "qa_engineer",
            "description": "Create test suite for product service",
            "context": {
                "service": "product-service",
                "test_types": ["unit", "integration", "e2e"]
            },
            "dependencies": ["implement_001"]
        },
        {
            "task_id": "deploy_001",
            "agent_role": "devops_engineer",
            "description": "Set up Kubernetes deployment for product service",
            "context": {
                "service": "product-service",
                "platform": "kubernetes",
                "cloud": "aws"
            },
            "dependencies": ["test_001"]
        },
        {
            "task_id": "document_001",
            "agent_role": "technical_writer",
            "description": "Create API documentation for product service",
            "context": {
                "service": "product-service",
                "doc_type": "api",
                "format": "openapi"
            },
            "dependencies": ["implement_001"]
        }
    ]
    
    print("Executing custom e-commerce workflow...\n")
    
    result = await orchestrator.execute_workflow(custom_workflow)
    
    print("\n" + "="*80)
    print("Custom Workflow Results")
    print("="*80)
    
    for task_id, task in result['results'].items():
        status = "✓" if task.result and not task.error else "✗"
        print(f"\n{status} {task_id}: {task.description}")
        if task.error:
            print(f"  Error: {task.error}")
    
    print(f"\nTotal tasks: {result['total_tasks']}")
    print(f"Completed at: {result['completed_at']}")


if __name__ == "__main__":
    asyncio.run(run_custom_workflow())
