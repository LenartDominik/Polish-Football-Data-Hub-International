"""
Alembic migration: create players table
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_players_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'players',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('api_id', sa.String, unique=True, index=True, nullable=True),
        sa.Column('name', sa.String, index=True),
        sa.Column('team', sa.String),
        sa.Column('league', sa.String),
        sa.Column('nationality', sa.String),
        sa.Column('position', sa.String, nullable=True),
        sa.Column('last_updated', sa.Date),
    )

def downgrade():
    op.drop_table('players')
