"""Add app settings table.

Revision ID: 002_add_app_settings
Revises: 001_initial_schema
Create Date: 2026-01-15 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "002_add_app_settings"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("llm_base_url", sa.String(length=255), nullable=False),
        sa.Column("llm_api_key", sa.String(length=255), nullable=True),
        sa.Column("llm_model", sa.String(length=255), nullable=True),
        sa.Column("llm_timeout", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("app_settings")
