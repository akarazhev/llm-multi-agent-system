#!/usr/bin/env python3
"""
Example: Build a Blog Platform with CMS using the multi-agent system
"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / '.env')

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import LangGraphOrchestrator
from src.config import load_config


async def build_blog_platform():
    """
    Build a complete Blog Platform with CMS using the multi-agent system.
    
    This example demonstrates:
    - Requirements analysis for content management
    - Full-stack blog platform implementation
    - SEO optimization
    - Comprehensive testing
    - Production deployment
    - Complete documentation
    """
    
    print("="*80)
    print("Building Blog Platform with CMS using Multi-Agent System")
    print("="*80)
    
    config = load_config()
    
    orchestrator = LangGraphOrchestrator(
        cursor_workspace=config.cursor_workspace,
        config=config.to_dict()
    )
    
    requirement = """
    Create a Blog Platform with Content Management System (CMS) with the following features:
    
    1. Blog Post Management:
       - Create, edit, delete blog posts
       - Rich text editor with markdown support
       - Post fields: title, slug, content, excerpt, featured_image, status, published_at
       - Post statuses: draft, published, archived
       - Auto-save drafts
       - Post scheduling (publish at specific date/time)
       - Post revisions and version history
    
    2. Content Organization:
       - Categories (hierarchical)
       - Tags (flat, multiple per post)
       - Featured posts
       - Related posts suggestions
    
    3. User Management:
       - User roles: admin, editor, author, subscriber
       - User authentication and authorization
       - User profiles with bio and avatar
       - Author pages showing their posts
    
    4. Comments System:
       - Nested comments (replies)
       - Comment moderation (approve/reject)
       - Comment notifications
       - Spam protection
       - Guest commenting (optional)
    
    5. Search and Discovery:
       - Full-text search across posts
       - Filter by category, tag, author, date
       - Archive pages (by month/year)
       - Popular posts
       - Recent posts
    
    6. SEO Features:
       - SEO-friendly URLs (slugs)
       - Meta tags (title, description, keywords)
       - Open Graph tags for social sharing
       - XML sitemap generation
       - RSS feed
       - Canonical URLs
    
    7. Media Management:
       - Image upload and management
       - Image optimization and resizing
       - Media library
       - Featured images for posts
    
    8. Admin Dashboard:
       - Post management interface
       - User management
       - Comment moderation
       - Analytics (views, popular posts)
       - Settings management
    
    9. Frontend Features:
       - Responsive design (mobile-first)
       - Homepage with latest posts
       - Post detail pages
       - Category and tag pages
       - Author pages
       - Search results page
       - Archive pages
       - About and Contact pages
    
    10. Technical Stack:
        Backend:
        - Python 3.11+ with FastAPI
        - PostgreSQL database
        - SQLAlchemy ORM
        - JWT authentication
        - Markdown to HTML conversion
        - Image processing (Pillow)
        
        Frontend:
        - React 18+ with TypeScript
        - Tailwind CSS for styling
        - React Router for navigation
        - Rich text editor (TipTap or similar)
        - React Query for data fetching
        
        Deployment:
        - Docker + Docker Compose
        - Nginx for static files
        - SSL/TLS support
    
    11. API Endpoints:
        Posts:
        - GET /posts - List posts (public)
        - GET /posts/{slug} - Get post by slug (public)
        - POST /posts - Create post (authenticated)
        - PUT /posts/{id} - Update post (authenticated)
        - DELETE /posts/{id} - Delete post (authenticated)
        - GET /posts/{id}/revisions - Get post revisions
        
        Categories:
        - GET /categories - List categories
        - POST /categories - Create category (admin)
        - PUT /categories/{id} - Update category (admin)
        - DELETE /categories/{id} - Delete category (admin)
        
        Tags:
        - GET /tags - List tags
        - POST /tags - Create tag (admin)
        
        Comments:
        - GET /posts/{id}/comments - Get post comments
        - POST /posts/{id}/comments - Add comment
        - PUT /comments/{id} - Update comment
        - DELETE /comments/{id} - Delete comment
        - POST /comments/{id}/approve - Approve comment (admin)
        
        Users:
        - POST /auth/register - User registration
        - POST /auth/login - User login
        - GET /auth/me - Get current user
        - GET /users/{id} - Get user profile
        - PUT /users/{id} - Update user profile
        
        Media:
        - POST /media/upload - Upload image
        - GET /media - List media files
        - DELETE /media/{id} - Delete media file
        
        SEO:
        - GET /sitemap.xml - XML sitemap
        - GET /rss.xml - RSS feed
    
    12. Additional Features:
        - Email notifications for comments
        - Social sharing buttons
        - Reading time estimation
        - Table of contents for long posts
        - Code syntax highlighting
        - Dark mode support
    """
    
    context = {
        "language": "python",
        "framework": "fastapi",
        "database": "postgresql",
        "frontend": "react",
        "styling": "tailwindcss",
        "editor": "markdown",
        "deployment": "docker",
        "testing_framework": "pytest"
    }
    
    print("\nRequirement Summary:")
    print("-" * 80)
    print("Building a Blog Platform with:")
    print("  • Rich markdown editor with auto-save")
    print("  • Categories, tags, and SEO optimization")
    print("  • Comment system with moderation")
    print("  • User roles and permissions")
    print("  • Media management")
    print("  • Admin dashboard")
    print("  • React frontend with Tailwind CSS")
    print("  • Docker deployment")
    print("\n" + "-" * 80)
    print("\nStarting workflow execution...")
    print("This will take several minutes as each agent completes their work.\n")
    
    try:
        final_state = await orchestrator.execute_feature_development(
            requirement=requirement,
            context=context
        )
        
        print("\n" + "="*80)
        print("✓ WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*80)
        
        # Extract the actual state from the event dict
        actual_state = list(final_state.values())[0] if final_state else {}
        
        print(f"\nWorkflow ID: {actual_state.get('workflow_id', 'N/A')}")
        print(f"Status: {actual_state.get('status', 'N/A')}")
        print(f"Completed Steps: {len(actual_state.get('completed_steps', []))}")
        print(f"Files Created: {len(actual_state.get('files_created', []))}")
        print(f"Completed At: {actual_state.get('completed_at', 'N/A')}")
        
        print("\n" + "-"*80)
        print("Workflow Summary:")
        print("-"*80)
        
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
        
        if actual_state.get('errors'):
            print(f"\nErrors: {len(actual_state.get('errors', []))}")
            for error in actual_state.get('errors', []):
                print(f"  ✗ {error.get('step', 'unknown')}: {error.get('error', 'N/A')}")
        
        print("\n" + "="*80)
        print("Next Steps:")
        print("="*80)
        print("1. Review the generated code in your workspace")
        print("2. Configure email settings in .env file")
        print("3. Run backend: docker-compose up")
        print("4. Run frontend: cd frontend && npm install && npm start")
        print("5. Access the blog: http://localhost:3000")
        print("6. Access admin: http://localhost:3000/admin")
        print("7. Access API docs: http://localhost:8000/docs")
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
        result = asyncio.run(build_blog_platform())
        print("✓ Blog Platform build complete!")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nBuild interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)
