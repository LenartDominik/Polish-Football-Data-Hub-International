"""
Alembic migration: create goalkeeper_stats table
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.sqlite as sqlite
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_goalkeeper_stats_table'
down_revision = 'add_competition_stats_table'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'goalkeeper_stats',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('player_id', sa.Integer, sa.ForeignKey('players.id', ondelete='CASCADE'), nullable=False),
        sa.Column('season', sa.String, nullable=False),
        sa.Column('competition_type', sa.String, nullable=False),
        sa.Column('competition_name', sa.String, nullable=False),
        sa.Column('games', sa.Integer, default=0),
        sa.Column('games_starts', sa.Integer, default=0),
        sa.Column('minutes', sa.Integer, default=0),
        sa.Column('goals_against', sa.Integer, default=0),
        sa.Column('goals_against_per90', sa.Float, default=0.0),
        sa.Column('shots_on_target_against', sa.Integer, default=0),
        sa.Column('saves', sa.Integer, default=0),
        sa.Column('save_percentage', sa.Float, default=0.0),
        sa.Column('clean_sheets', sa.Integer, default=0),
        sa.Column('clean_sheet_percentage', sa.Float, default=0.0),
        sa.Column('wins', sa.Integer, default=0),
        sa.Column('draws', sa.Integer, default=0),
        sa.Column('losses', sa.Integer, default=0),
        sa.Column('penalties_attempted', sa.Integer, default=0),
        sa.Column('penalties_allowed', sa.Integer, default=0),
        sa.Column('penalties_saved', sa.Integer, default=0),
        sa.Column('penalties_missed', sa.Integer, default=0),
        sa.Column('post_shot_xg', sa.Float, default=0.0),
        sa.UniqueConstraint('player_id', 'season', 'competition_type', 'competition_name', name='uq_gk_player_season_competition'),
    )

def downgrade():
    op.drop_table('goalkeeper_stats')
