"""Initial schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-01-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("icon", sa.String(length=32), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("owner_id", sa.String(length=255), nullable=False),
        sa.Column("team_members", postgresql.JSONB(), nullable=False),
        sa.Column("ai_agents", postgresql.JSONB(), nullable=False),
        sa.Column("integrations", postgresql.JSONB(), nullable=False),
        sa.Column("tech_stack", postgresql.JSONB(), nullable=False),
        sa.Column("stats", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("last_activity", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "agents",
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("capabilities", postgresql.JSONB(), nullable=False),
        sa.Column("current_task", sa.Text(), nullable=True),
        sa.Column("completed_tasks", sa.Integer(), nullable=False),
        sa.Column("failed_tasks", sa.Integer(), nullable=False),
        sa.Column("avg_task_duration", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_active", sa.DateTime(), nullable=True),
        sa.Column("configuration", postgresql.JSONB(), nullable=False),
        sa.Column("metrics", postgresql.JSONB(), nullable=False),
        sa.Column("assigned_projects", postgresql.JSONB(), nullable=False),
    )

    op.create_table(
        "workflows",
        sa.Column("workflow_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("workflow_type", sa.String(length=50), nullable=False),
        sa.Column("requirement", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("current_step", sa.String(length=255), nullable=True),
        sa.Column("completed_steps", postgresql.JSONB(), nullable=False),
        sa.Column("total_steps", sa.Integer(), nullable=False),
        sa.Column("progress_percentage", sa.Integer(), nullable=False),
        sa.Column("files_created", postgresql.JSONB(), nullable=False),
        sa.Column("errors", postgresql.JSONB(), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("assigned_agents", postgresql.JSONB(), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("tags", postgresql.JSONB(), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("metrics", postgresql.JSONB(), nullable=False),
        sa.Column("steps", postgresql.JSONB(), nullable=False),
        sa.Column("artifacts", postgresql.JSONB(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="SET NULL"),
    )

    op.create_table(
        "agent_messages",
        sa.Column("message_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workflow_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("agent_name", sa.String(length=255), nullable=False),
        sa.Column("agent_role", sa.String(length=50), nullable=False),
        sa.Column("message_type", sa.String(length=50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("addressed_to", postgresql.JSONB(), nullable=False),
        sa.Column("addressed_to_names", postgresql.JSONB(), nullable=False),
        sa.Column("parent_message_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("requires_response", sa.Boolean(), nullable=False),
        sa.Column("urgency", sa.String(length=50), nullable=False),
        sa.Column("attachments", postgresql.JSONB(), nullable=False),
        sa.Column("is_edited", sa.Boolean(), nullable=False),
        sa.Column("edited_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflows.workflow_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.agent_id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["parent_message_id"], ["agent_messages.message_id"], ondelete="SET NULL"),
    )

    op.create_table(
        "decisions",
        sa.Column("decision_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workflow_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("problem", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("variants", postgresql.JSONB(), nullable=False),
        sa.Column("chosen_variant_id", sa.String(length=100), nullable=True),
        sa.Column("votes", postgresql.JSONB(), nullable=False),
        sa.Column("justification", sa.Text(), nullable=True),
        sa.Column("responsible_agents", postgresql.JSONB(), nullable=False),
        sa.Column("discussion_thread_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflows.workflow_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["discussion_thread_id"], ["agent_messages.message_id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    op.drop_table("decisions")
    op.drop_table("agent_messages")
    op.drop_table("workflows")
    op.drop_table("agents")
    op.drop_table("projects")
