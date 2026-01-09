"""
SQLAlchemy database models.

Defines the database schema for workflows, agent outputs, and shared context.
"""

from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from src.utils.database import Base


class WorkflowDB(Base):
    """Workflow database model."""

    __tablename__ = "workflows"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    request_id = Column(String(255), unique=True, nullable=False, index=True)
    requirements = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="pending", index=True)
    current_step = Column(String(255), default="initial")
    agent_outputs = Column(JSON, default={})
    shared_context = Column(JSON, default={})
    jira_tickets = Column(JSON, default=[])
    confluence_pages = Column(JSON, default=[])
    gitlab_repos = Column(JSON, default=[])
    errors = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    agent_outputs_rel = relationship("AgentOutputDB", back_populates="workflow", cascade="all, delete-orphan")
    shared_context_rel = relationship("SharedContextDB", back_populates="workflow", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "request_id": self.request_id,
            "requirements": self.requirements,
            "status": self.status,
            "current_step": self.current_step,
            "agent_outputs": self.agent_outputs,
            "shared_context": self.shared_context,
            "jira_tickets": self.jira_tickets,
            "confluence_pages": self.confluence_pages,
            "gitlab_repos": self.gitlab_repos,
            "errors": self.errors,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AgentOutputDB(Base):
    """Agent output database model."""

    __tablename__ = "agent_outputs"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    workflow_id = Column(PostgresUUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_name = Column(String(100), nullable=False)
    output_type = Column(String(50), nullable=False)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    workflow = relationship("WorkflowDB", back_populates="agent_outputs_rel")

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "workflow_id": str(self.workflow_id),
            "agent_name": self.agent_name,
            "output_type": self.output_type,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SharedContextDB(Base):
    """Shared context database model."""

    __tablename__ = "shared_context"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    workflow_id = Column(PostgresUUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String(100))

    # Relationships
    workflow = relationship("WorkflowDB", back_populates="shared_context_rel")

    # Unique constraint on workflow_id and key
    __table_args__ = (
        Index("idx_shared_context_workflow_key", "workflow_id", "key", unique=True),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "workflow_id": str(self.workflow_id),
            "key": self.key,
            "value": self.value,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": self.updated_by,
        }
