"""Add mood analysis tables

Revision ID: 7b37823fcdec
Revises: 80d45a144edd
Create Date: 2025-05-06 15:30:01.653536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b37823fcdec'
down_revision = '80d45a144edd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mood_entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('energy_level', sa.Integer(), nullable=False),
    sa.Column('happiness', sa.Integer(), nullable=False),
    sa.Column('anxiety', sa.Integer(), nullable=False),
    sa.Column('stress', sa.Integer(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('color_suggestion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mood_entry_id', sa.Integer(), nullable=False),
    sa.Column('primary_color', sa.String(length=6), nullable=False),
    sa.Column('secondary_color', sa.String(length=6), nullable=True),
    sa.Column('accent_color', sa.String(length=6), nullable=True),
    sa.Column('effect_name', sa.String(length=50), nullable=True),
    sa.Column('brightness', sa.Integer(), nullable=False),
    sa.Column('was_applied', sa.Boolean(), nullable=True),
    sa.Column('user_rating', sa.Integer(), nullable=True),
    sa.Column('applied_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['mood_entry_id'], ['mood_entry.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('color_suggestion')
    op.drop_table('mood_entry')
    # ### end Alembic commands ###
