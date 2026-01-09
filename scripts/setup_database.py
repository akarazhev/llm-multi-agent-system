"""
Database setup script.

Creates initial database schema and tables using SQLAlchemy models.
"""

from sqlalchemy.exc import OperationalError

from src.config import settings
from src.utils.database import init_db, engine
from src.models.db_models import Base


def create_tables():
    """Create database tables using SQLAlchemy models."""
    try:
        print("Initializing database...")
        print(f"Connecting to: {settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}")
        
        # Create all tables defined in models
        init_db()
        
        print("✅ Database setup completed successfully!")
        print("Tables created:")
        print("  - workflows")
        print("  - agent_outputs")
        print("  - shared_context")
    except OperationalError as e:
        print(f"❌ Error connecting to database: {e}")
        print("Make sure PostgreSQL is running and credentials are correct.")
        print(f"Connection string: postgresql://{settings.postgres_user}:***@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}")
        raise
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise
    finally:
        engine.dispose()


if __name__ == "__main__":
    create_tables()


