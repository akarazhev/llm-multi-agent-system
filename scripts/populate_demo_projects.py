#!/usr/bin/env python3
"""
Populate database with demo projects based on examples.
This script creates demo projects that can be displayed in the UI.
"""
import asyncio
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
# Try to load .env if it exists (not required in Docker/Podman)
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    load_dotenv(env_file)
sys.path.insert(0, str(PROJECT_ROOT))

from src.db.database import async_session
from src.db.models import Project


# Demo project definitions based on examples
DEMO_PROJECTS = [
    {
        "name": "Task Management API",
        "description": "A comprehensive Task Management REST API with JWT authentication, CRUD operations, WebSocket notifications, and PostgreSQL database. Built with FastAPI and includes Docker deployment configuration.",
        "icon": "📋",
        "status": "active",
        "type": "api",
        "tech_stack": {
            "languages": ["Python"],
            "frameworks": ["FastAPI"],
            "databases": ["PostgreSQL"],
            "tools": ["Docker", "pytest", "JWT", "WebSockets"]
        },
        "integrations": {
            "git": {
                "platform": "github",
                "url": "https://github.com/demo/task-management-api",
                "branch": "main",
                "connected": True,
                "lastSync": (datetime.utcnow() - timedelta(hours=2)).isoformat()
            },
            "jira": {
                "enabled": True,
                "projectKey": "TASK",
                "url": "https://demo.atlassian.net"
            }
        },
        "stats": {
            "totalWorkflows": 3,
            "activeWorkflows": 1,
            "completedWorkflows": 2,
            "failedWorkflows": 0,
            "teamSize": 4,
            "aiAgentsCount": 5,
            "filesGenerated": 47,
            "linesOfCode": 3240
        },
        "ai_agents": ["business_analyst", "developer", "qa_engineer", "devops_engineer", "technical_writer"],
        "team_members": [
            {"id": "user1", "name": "John Doe", "role": "Project Manager"},
            {"id": "user2", "name": "Jane Smith", "role": "Backend Developer"},
            {"id": "user3", "name": "Bob Johnson", "role": "QA Engineer"},
            {"id": "user4", "name": "Alice Williams", "role": "DevOps Engineer"}
        ]
    },
    {
        "name": "E-commerce Product Catalog",
        "description": "A full-stack e-commerce platform with product management, shopping cart, Stripe payment integration, React frontend with Tailwind CSS, and comprehensive admin dashboard. Includes user reviews and ratings system.",
        "icon": "🛒",
        "status": "active",
        "type": "webapp",
        "tech_stack": {
            "languages": ["Python", "TypeScript", "JavaScript"],
            "frameworks": ["FastAPI", "React", "Tailwind CSS"],
            "databases": ["PostgreSQL", "Redis"],
            "tools": ["Docker", "Nginx", "Stripe", "pytest", "React Testing Library"]
        },
        "integrations": {
            "git": {
                "platform": "gitlab",
                "url": "https://gitlab.com/demo/ecommerce-catalog",
                "branch": "main",
                "connected": True,
                "lastSync": (datetime.utcnow() - timedelta(hours=5)).isoformat()
            },
            "slack": {
                "enabled": True,
                "channel": "#ecommerce-dev"
            }
        },
        "stats": {
            "totalWorkflows": 5,
            "activeWorkflows": 2,
            "completedWorkflows": 3,
            "failedWorkflows": 0,
            "teamSize": 6,
            "aiAgentsCount": 5,
            "filesGenerated": 89,
            "linesOfCode": 7820
        },
        "ai_agents": ["business_analyst", "developer", "qa_engineer", "devops_engineer", "technical_writer"],
        "team_members": [
            {"id": "user1", "name": "John Doe", "role": "Product Owner"},
            {"id": "user2", "name": "Jane Smith", "role": "Full Stack Developer"},
            {"id": "user3", "name": "Bob Johnson", "role": "Frontend Developer"},
            {"id": "user4", "name": "Alice Williams", "role": "Backend Developer"},
            {"id": "user5", "name": "Charlie Brown", "role": "QA Engineer"},
            {"id": "user6", "name": "Diana Prince", "role": "UI/UX Designer"}
        ]
    },
    {
        "name": "Blog Platform with CMS",
        "description": "A modern blog platform with content management system featuring rich markdown editor, categories and tags, SEO optimization, comment system with moderation, user roles and permissions, media management, and RSS feed generation.",
        "icon": "📝",
        "status": "completed",
        "type": "webapp",
        "tech_stack": {
            "languages": ["Python", "TypeScript", "JavaScript"],
            "frameworks": ["FastAPI", "React", "Tailwind CSS"],
            "databases": ["PostgreSQL"],
            "tools": ["Docker", "Nginx", "pytest", "React Testing Library", "Markdown"]
        },
        "integrations": {
            "git": {
                "platform": "github",
                "url": "https://github.com/demo/blog-platform",
                "branch": "main",
                "connected": True,
                "lastSync": (datetime.utcnow() - timedelta(days=1)).isoformat()
            },
            "confluence": {
                "url": "https://demo.atlassian.net/wiki",
                "spaceKey": "BLOG",
                "connected": True,
                "lastSync": (datetime.utcnow() - timedelta(days=2)).isoformat()
            }
        },
        "stats": {
            "totalWorkflows": 4,
            "activeWorkflows": 0,
            "completedWorkflows": 4,
            "failedWorkflows": 0,
            "teamSize": 5,
            "aiAgentsCount": 5,
            "filesGenerated": 72,
            "linesOfCode": 6150
        },
        "ai_agents": ["business_analyst", "developer", "qa_engineer", "devops_engineer", "technical_writer"],
        "team_members": [
            {"id": "user1", "name": "John Doe", "role": "Content Manager"},
            {"id": "user2", "name": "Jane Smith", "role": "Full Stack Developer"},
            {"id": "user3", "name": "Bob Johnson", "role": "Frontend Developer"},
            {"id": "user4", "name": "Alice Williams", "role": "SEO Specialist"},
            {"id": "user5", "name": "Charlie Brown", "role": "Technical Writer"}
        ]
    },
    {
        "name": "Interactive Chat Workflow",
        "description": "An interactive chat-like workflow system with real-time agent communication display, color-coded agents, live progress bars, inter-agent handoff visualization, and automatic chat log export.",
        "icon": "💬",
        "status": "active",
        "type": "workflow",
        "tech_stack": {
            "languages": ["Python"],
            "frameworks": ["FastAPI", "LangGraph"],
            "databases": ["PostgreSQL"],
            "tools": ["Docker", "pytest", "Colorama"]
        },
        "integrations": {
            "git": {
                "platform": "github",
                "url": "https://github.com/demo/interactive-chat",
                "branch": "main",
                "connected": True,
                "lastSync": (datetime.utcnow() - timedelta(minutes=30)).isoformat()
            }
        },
        "stats": {
            "totalWorkflows": 2,
            "activeWorkflows": 1,
            "completedWorkflows": 1,
            "failedWorkflows": 0,
            "teamSize": 3,
            "aiAgentsCount": 5,
            "filesGenerated": 28,
            "linesOfCode": 1890
        },
        "ai_agents": ["business_analyst", "developer", "qa_engineer", "devops_engineer", "technical_writer"],
        "team_members": [
            {"id": "user1", "name": "John Doe", "role": "Product Manager"},
            {"id": "user2", "name": "Jane Smith", "role": "Developer"},
            {"id": "user3", "name": "Bob Johnson", "role": "QA Engineer"}
        ]
    }
]


async def populate_demo_projects(owner_id: str = "demo-user"):
    """
    Populate database with demo projects.
    
    Args:
        owner_id: The owner ID for the projects (default: "demo-user")
    """
    print("="*80)
    print("Populating Database with Demo Projects")
    print("="*80)
    print()
    
    # Check database connection
    try:
        from src.db.database import DATABASE_URL
        print(f"Database URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'configured'}")
    except Exception as e:
        print(f"⚠️  Warning: Could not get database URL: {e}")
    
    print()
    
    async with async_session() as session:
        # Check if projects already exist
        from sqlalchemy import select
        result = await session.execute(select(Project))
        existing_projects = result.scalars().all()
        
        if existing_projects:
            print(f"Found {len(existing_projects)} existing projects in database.")
            response = input("Do you want to add demo projects anyway? (y/n): ").strip().lower()
            if response != 'y':
                print("Aborted.")
                return
        
        print(f"Creating {len(DEMO_PROJECTS)} demo projects...")
        print()
        
        created_count = 0
        for project_data in DEMO_PROJECTS:
            try:
                # Check if project with same name already exists
                result = await session.execute(
                    select(Project).where(Project.name == project_data["name"])
                )
                existing = result.scalars().first()
                
                if existing:
                    print(f"  ⚠️  Project '{project_data['name']}' already exists, skipping...")
                    continue
                
                # Create timestamps
                now = datetime.utcnow()
                created_at = now - timedelta(days=len(DEMO_PROJECTS) - created_count)
                last_activity = now - timedelta(hours=created_count * 2)
                
                # Create project
                project = Project(
                    id=uuid.uuid4(),
                    name=project_data["name"],
                    description=project_data["description"],
                    icon=project_data["icon"],
                    status=project_data["status"],
                    type=project_data["type"],
                    owner_id=owner_id,
                    team_members=project_data["team_members"],
                    ai_agents=project_data["ai_agents"],
                    integrations=project_data["integrations"],
                    tech_stack=project_data["tech_stack"],
                    stats=project_data["stats"],
                    created_at=created_at,
                    updated_at=now,
                    last_activity=last_activity
                )
                
                session.add(project)
                created_count += 1
                print(f"  ✓ Created project: {project_data['icon']} {project_data['name']}")
                
            except Exception as e:
                print(f"  ✗ Error creating project '{project_data['name']}': {e}")
                continue
        
        # Commit all projects
        try:
            await session.commit()
            print()
            print("="*80)
            print(f"✓ Successfully created {created_count} demo projects!")
            print("="*80)
            print()
            print("Projects are now available in the UI.")
            print("You can view them by accessing the projects list in the frontend.")
            
        except Exception as e:
            await session.rollback()
            print()
            print("="*80)
            print(f"✗ Error committing projects: {e}")
            print("="*80)
            raise


async def main():
    """Main entry point"""
    try:
        # You can customize the owner_id here or pass it as an argument
        owner_id = "demo-user"
        
        if len(sys.argv) > 1:
            owner_id = sys.argv[1]
        
        await populate_demo_projects(owner_id=owner_id)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
