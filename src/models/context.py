"""
Shared context models for agent communication.
"""

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SharedContext(BaseModel):
    """Shared context entry for agent collaboration."""

    workflow_id: UUID = Field(..., description="Associated workflow ID")
    key: str = Field(..., description="Context key")
    value: Any = Field(..., description="Context value")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")
    updated_by: Optional[str] = Field(None, description="Agent that last updated this")


class ContextUpdate(BaseModel):
    """Context update request."""

    workflow_id: UUID = Field(..., description="Workflow ID")
    key: str = Field(..., description="Context key to update")
    value: Any = Field(..., description="New value")
    agent_name: str = Field(..., description="Agent making the update")


