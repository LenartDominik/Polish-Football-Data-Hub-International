"""add npxg and penalty stats to competition_stats

Revision ID: add_npxg_penalty
Revises: 
Create Date: 2025-01-XX

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_npxg_penalty'
down_revision = 'add_goalkeeper_stats_table'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to competition_stats
    op.add_column(
        'competition_stats',
        sa.Column('npxg', sa.Float(), nullable=False, server_default=sa.text('0.0'))
    )
    op.add_column(
        'competition_stats',
        sa.Column('penalty_goals', sa.Integer(), nullable=False, server_default=sa.text('0'))
    )


def downgrade():
    op.drop_column('competition_stats', 'penalty_goals')
    op.drop_column('competition_stats', 'npxg')
