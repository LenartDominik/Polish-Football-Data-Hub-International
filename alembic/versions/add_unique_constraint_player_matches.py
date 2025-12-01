"""add unique constraint to player_matches

Revision ID: add_uq_player_match
Revises: 
Create Date: 2025-01-XX

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_uq_player_match'
down_revision = None  # Update this if you have other migrations
branch_labels = None
depends_on = None


def upgrade():
    # Add unique constraint to player_matches table
    op.create_unique_constraint(
        'uq_player_match',
        'player_matches',
        ['player_id', 'match_date', 'competition', 'opponent']
    )


def downgrade():
    # Remove unique constraint
    op.drop_constraint('uq_player_match', 'player_matches', type_='unique')
