#!/usr/bin/env python3
"""
Example: Build an E-commerce Product Catalog with the multi-agent system
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


async def build_ecommerce_catalog():
    """
    Build a complete E-commerce Product Catalog using the multi-agent system.
    
    This example demonstrates:
    - Requirements analysis for e-commerce features
    - Full-stack architecture (Backend API + React Frontend)
    - Payment integration with Stripe
    - Comprehensive testing
    - Production deployment setup
    - Complete documentation
    """
    
    print("="*80)
    print("Building E-commerce Product Catalog with Multi-Agent System")
    print("="*80)
    
    config = load_config()
    
    orchestrator = LangGraphOrchestrator(
        workspace=config.workspace,
        config=config.to_dict(),
        enable_chat_display=True
    )
    
    requirement = """
    Create an E-commerce Product Catalog with the following features:
    
    1. Product Management:
       - Product CRUD operations (admin only)
       - Product fields: name, description, price, stock, images, category, tags, rating
       - Multiple product images with primary image
       - Product variants (size, color, etc.)
       - Inventory tracking
    
    2. Search and Filtering:
       - Full-text search across products
       - Filter by: category, price range, rating, availability
       - Sort by: price, popularity, newest, rating
       - Pagination support
    
    3. Shopping Cart:
       - Add/remove items from cart
       - Update quantities
       - Cart persistence (session-based)
       - Calculate totals with tax
    
    4. Order Management:
       - Place orders
       - Order history for users
       - Order status tracking (pending, processing, shipped, delivered)
       - Email notifications for order updates
    
    5. Payment Integration:
       - Stripe payment processing
       - Secure payment handling
       - Payment confirmation
       - Refund support
    
    6. User Features:
       - User registration and authentication
       - User profiles
       - Wishlist functionality
       - Product reviews and ratings
    
    7. Admin Dashboard:
       - Product management interface
       - Order management
       - User management
       - Sales analytics
    
    8. Frontend (React):
       - Modern, responsive UI with Tailwind CSS
       - Product listing page with filters
       - Product detail page
       - Shopping cart page
       - Checkout flow
       - User dashboard
       - Admin panel
    
    9. Technical Stack:
       Backend:
       - Python 3.11+ with FastAPI
       - PostgreSQL database
       - SQLAlchemy ORM
       - Stripe API integration
       - JWT authentication
       - Redis for caching
       
       Frontend:
       - React 18+ with TypeScript
       - Tailwind CSS for styling
       - React Router for navigation
       - Axios for API calls
       - Context API for state management
       
       Deployment:
       - Docker + Docker Compose
       - Nginx reverse proxy
       - SSL/TLS certificates
    
    10. API Endpoints:
        Products:
        - GET /products - List products with filters
        - GET /products/{id} - Get product details
        - POST /products - Create product (admin)
        - PUT /products/{id} - Update product (admin)
        - DELETE /products/{id} - Delete product (admin)
        
        Cart:
        - GET /cart - Get user's cart
        - POST /cart/items - Add item to cart
        - PUT /cart/items/{id} - Update cart item
        - DELETE /cart/items/{id} - Remove from cart
        
        Orders:
        - POST /orders - Create order
        - GET /orders - List user's orders
        - GET /orders/{id} - Get order details
        
        Payment:
        - POST /payment/create-intent - Create Stripe payment intent
        - POST /payment/confirm - Confirm payment
        
        Auth:
        - POST /auth/register - User registration
        - POST /auth/login - User login
        - GET /auth/me - Get current user
    """
    
    context = {
        "language": "python",
        "framework": "fastapi",
        "database": "postgresql",
        "frontend": "react",
        "styling": "tailwindcss",
        "payment": "stripe",
        "deployment": "docker",
        "testing_framework": "pytest"
    }
    
    print("\nRequirement Summary:")
    print("-" * 80)
    print("Building an E-commerce Product Catalog with:")
    print("  • Product management with search and filters")
    print("  • Shopping cart and checkout")
    print("  • Stripe payment integration")
    print("  • Order tracking and management")
    print("  • React frontend with Tailwind CSS")
    print("  • Admin dashboard")
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
        print("2. Set up Stripe API keys in .env file")
        print("3. Run backend: docker-compose up")
        print("4. Run frontend: cd frontend && npm install && npm start")
        print("5. Access the app: http://localhost:3000")
        print("6. Access API docs: http://localhost:8000/docs")
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
        result = asyncio.run(build_ecommerce_catalog())
        print("✓ E-commerce Product Catalog build complete!")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nBuild interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)
