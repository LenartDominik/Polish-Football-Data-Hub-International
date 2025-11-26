"""
Alembic migration: create competition_stats table
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.sqlite as sqlite
import enum

# revision identifiers, used by Alembic.
revision = 'add_competition_stats_table'
down_revision = '3bc2b3fe1c2c'
branch_labels = None
depends_on = None



def upgrade():
    pass  # Tabela competition_stats już istnieje, nie twórz ponownie

def downgrade():
    op.drop_table('competition_stats')
