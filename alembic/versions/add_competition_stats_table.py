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
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'competition_stats' in inspector.get_table_names():
        return

    op.create_table(
        'competition_stats',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('player_id', sa.Integer, sa.ForeignKey('players.id', ondelete='CASCADE'), nullable=False),
        sa.Column('season', sa.String, nullable=False),
        sa.Column('competition_type', sa.String, nullable=False),
        sa.Column('competition_name', sa.String, nullable=False),
        sa.Column('games', sa.Integer, nullable=False, server_default='0'),
        sa.Column('games_starts', sa.Integer, nullable=False, server_default='0'),
        sa.Column('minutes', sa.Integer, nullable=False, server_default='0'),
        sa.Column('goals', sa.Integer, nullable=False, server_default='0'),
        sa.Column('assists', sa.Integer, nullable=False, server_default='0'),
        sa.Column('xg', sa.Float, nullable=False, server_default='0'),
        sa.Column('xa', sa.Float, nullable=False, server_default='0'),
        sa.Column('shots', sa.Integer, nullable=False, server_default='0'),
        sa.Column('shots_on_target', sa.Integer, nullable=False, server_default='0'),
        sa.Column('yellow_cards', sa.Integer, nullable=False, server_default='0'),
        sa.Column('red_cards', sa.Integer, nullable=False, server_default='0'),
        sa.UniqueConstraint(
            'player_id', 'season', 'competition_type', 'competition_name',
            name='uq_player_season_competition'
        ),
    )

    op.create_index('ix_competition_stats_player_id', 'competition_stats', ['player_id'])


def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'competition_stats' not in inspector.get_table_names():
        return

    op.drop_index('ix_competition_stats_player_id', table_name='competition_stats')
    op.drop_table('competition_stats')
