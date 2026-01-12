#!/usr/bin/env python3
"""
Example: Build a Task Management API with the multi-agent system
"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.orchestrator.workflow_engine import WorkflowType
from src.config import load_config


async def build_task_management_api():
    """
    Build a complete Task Management API using the multi-agent system.
    
    This example demonstrates:
    - Requirements analysis by Business Analyst
    - Architecture design and implementation by Developer
    - Comprehensive testing by QA Engineer
    - Docker deployment setup by DevOps Engineer
    - Complete documentation by Technical Writer
    """
    
    print("="*80)
    print("Building Task Management API with Multi-Agent System")
    print("="*80)
    
    config = load_config()
    
    orchestrator = AgentOrchestrator(
        cursor_workspace=config.cursor_workspace,
        config=config.to_dict()
    )
    
    workflow_engine = WorkflowEngine(orchestrator)
    
    requirement = """
    Create a Task Management REST API with the following features:
    
    1. User Authentication:
       - JWT-based authentication
       - User registration and login
       - Password hashing with bcrypt
    
    2. Task Management:
       - Create, read, update, delete tasks
       - Task fields: title, description, status, priority, due_date, assigned_to
       - Task statuses: TODO, IN_PROGRESS, REVIEW, DONE
       - Task priorities: LOW, MEDIUM, HIGH, URGENT
    
    3. Real-time Features:
       - WebSocket support for real-time task updates
       - Notifications when tasks are assigned or updated
    
    4. Technical Requirements:
       - Language: Python 3.11+
       - Framework: FastAPI
       - Database: PostgreSQL
       - ORM: SQLAlchemy
       - Authentication: JWT (python-jose)
       - WebSockets: FastAPI WebSocket support
       - Testing: pytest with 80%+ coverage
       - Deployment: Docker + Docker Compose
    
    5. API Endpoints:
       - POST /auth/register - User registration
       - POST /auth/login - User login
       - GET /tasks - List all tasks (with filters)
       - POST /tasks - Create new task
       - GET /tasks/{id} - Get task details
       - PUT /tasks/{id} - Update task
       - DELETE /tasks/{id} - Delete task
       - WS /ws/tasks - WebSocket for real-time updates
    
    6. Documentation:
       - OpenAPI/Swagger documentation
       - README with setup instructions
       - API usage examples
    """
    
    context = {
        "language": "python",
        "framework": "fastapi",
        "database": "postgresql",
        "deployment": "docker",
        "testing_framework": "pytest",
        "authentication": "jwt"
    }
    
    print("\nRequirement Summary:")
    print("-" * 80)
    print("Building a Task Management API with:")
    print("  • User authentication (JWT)")
    print("  • Full CRUD operations for tasks")
    print("  • Real-time WebSocket notifications")
    print("  • PostgreSQL database")
    print("  • Docker deployment")
    print("  • Comprehensive tests and documentation")
    print("\n" + "-" * 80)
    print("\nStarting workflow execution...")
    print("This will take several minutes as each agent completes their work.\n")
    
    try:
        result = await workflow_engine.execute_workflow(
            workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
            requirement=requirement,
            context=context
        )
        
        print("\n" + "="*80)
        print("✓ WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*80)
        
        print(f"\nWorkflow Type: {result['workflow_type']}")
        print(f"Total Tasks: {result['result']['total_tasks']}")
        print(f"Completed At: {result['result']['completed_at']}")
        
        print("\n" + "-"*80)
        print("Task Results Summary:")
        print("-"*80)
        
        for task_id, task in result['result']['results'].items():
            status_icon = "✓" if task.result and not task.error else "✗"
            print(f"\n{status_icon} {task_id}")
            print(f"   Description: {task.description}")
            print(f"   Status: {'Completed' if task.result else 'Failed'}")
            if task.error:
                print(f"   Error: {task.error}")
        
        print("\n" + "="*80)
        print("Next Steps:")
        print("="*80)
        print("1. Review the generated code in your workspace")
        print("2. Check the output/ directory for detailed results")
        print("3. Run the tests: pytest")
        print("4. Start the API: docker-compose up")
        print("5. Access Swagger docs: http://localhost:8000/docs")
        print("\n" + "="*80 + "\n")
        
        return result
        
    except Exception as e:
        print("\n" + "="*80)
        print("✗ WORKFLOW FAILED")
        print("="*80)
        print(f"\nError: {e}")
        print("\nCheck logs/agent_system.log for detailed error information")
        raise


if __name__ == "__main__":
    try:
        result = asyncio.run(build_task_management_api())
        print("✓ Task Management API build complete!")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nBuild interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)
