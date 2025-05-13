"""Add ai_feedback column to mood_entry

Revision ID: add_ai_feedback_column
Revises: ebbb39146b0d
Create Date: 2025-05-13 22:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_ai_feedback_column'
down_revision = 'ebbb39146b0d'
branch_labels = None
depends_on = None


def upgrade():
    # Use direct SQL to add the column since we've had issues with migrations
    op.execute('ALTER TABLE mood_entry ADD COLUMN ai_feedback TEXT')


def downgrade():
    # SQLite doesn't support dropping columns directly
    # This is a placeholder - in SQLite you'd need to recreate the table
    pass 