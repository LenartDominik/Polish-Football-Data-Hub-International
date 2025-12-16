from alembic import op
import sqlalchemy as sa

# Identyfikatory migracji
revision = '3bc2b3fe1c2c'
down_revision = '0001_create_players_table'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # W SQLite możemy dodać warunek sprawdzający, czy tabela istnieje
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Analogicznie sprawdź i utwórz inne tabele:
    if 'live_matches' not in inspector.get_table_names():
        op.create_table(
            'live_matches',
            sa.Column('id', sa.INTEGER(), primary_key=True, nullable=False),
            sa.Column('match_id', sa.INTEGER(), nullable=True),
            sa.Column('competition', sa.VARCHAR(), nullable=True),
            sa.Column('home_team', sa.VARCHAR(), nullable=True),
            sa.Column('away_team', sa.VARCHAR(), nullable=True),
            sa.Column('home_score', sa.INTEGER(), nullable=True),
            sa.Column('away_score', sa.INTEGER(), nullable=True),
            sa.Column('status', sa.VARCHAR(), nullable=True),
            sa.Column('kickoff_time', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
            sa.Column('matchday', sa.INTEGER(), nullable=True),
            sa.Column('season', sa.VARCHAR(), nullable=True),
            sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        )
        op.create_index('ix_live_matches_match_id', 'live_matches', ['match_id'], unique=True)
        op.create_index('ix_live_matches_id', 'live_matches', ['id'])


    if 'player_live_stats' not in inspector.get_table_names():
        op.create_table(
            'player_live_stats',
            sa.Column('id', sa.INTEGER(), primary_key=True, nullable=False),
            sa.Column('player_id', sa.INTEGER(), nullable=True),
            sa.Column('match_id', sa.INTEGER(), nullable=True),
            sa.Column('goals', sa.INTEGER(), nullable=True),
            sa.Column('assists', sa.INTEGER(), nullable=True),
            sa.Column('yellow_cards', sa.INTEGER(), nullable=True),
            sa.Column('red_cards', sa.INTEGER(), nullable=True),
            sa.Column('minutes_played', sa.INTEGER(), nullable=True),
            sa.Column('is_live', sa.BOOLEAN(), nullable=True),
            sa.Column('team', sa.VARCHAR(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
            sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
            sa.ForeignKeyConstraint(['player_id'], ['players.id']),
            sa.ForeignKeyConstraint(['match_id'], ['live_matches.id']),
        )
        op.create_index('ix_player_live_stats_player_id', 'player_live_stats', ['player_id'])
        op.create_index('ix_player_live_stats_match_id', 'player_live_stats', ['match_id'])
        op.create_index('ix_player_live_stats_id', 'player_live_stats', ['id'])


    if 'player_matches' not in inspector.get_table_names():
        op.create_table(
            'player_matches',
            sa.Column('id', sa.INTEGER(), primary_key=True, nullable=False),
            sa.Column('player_id', sa.INTEGER(), nullable=False),
            sa.Column('match_date', sa.DATE(), nullable=False),
            sa.Column('competition', sa.VARCHAR(), nullable=True),
            sa.Column('round', sa.VARCHAR(), nullable=True),
            sa.Column('venue', sa.VARCHAR(), nullable=True),
            sa.Column('opponent', sa.VARCHAR(), nullable=True),
            sa.Column('result', sa.VARCHAR(), nullable=True),
            sa.Column('minutes_played', sa.INTEGER(), nullable=True),
            sa.Column('goals', sa.INTEGER(), nullable=True),
            sa.Column('assists', sa.INTEGER(), nullable=True),
            sa.Column('shots', sa.INTEGER(), nullable=True),
            sa.Column('shots_on_target', sa.INTEGER(), nullable=True),
            sa.Column('xg', sa.FLOAT(), nullable=True),
            sa.Column('xa', sa.FLOAT(), nullable=True),
            sa.Column('passes_completed', sa.INTEGER(), nullable=True),
            sa.Column('passes_attempted', sa.INTEGER(), nullable=True),
            sa.Column('pass_completion_pct', sa.FLOAT(), nullable=True),
            sa.Column('key_passes', sa.INTEGER(), nullable=True),
            sa.Column('tackles', sa.INTEGER(), nullable=True),
            sa.Column('interceptions', sa.INTEGER(), nullable=True),
            sa.Column('blocks', sa.INTEGER(), nullable=True),
            sa.Column('touches', sa.INTEGER(), nullable=True),
            sa.Column('dribbles_completed', sa.INTEGER(), nullable=True),
            sa.Column('carries', sa.INTEGER(), nullable=True),
            sa.Column('fouls_committed', sa.INTEGER(), nullable=True),
            sa.Column('fouls_drawn', sa.INTEGER(), nullable=True),
            sa.Column('yellow_cards', sa.INTEGER(), nullable=True),
            sa.Column('red_cards', sa.INTEGER(), nullable=True),
            sa.ForeignKeyConstraint(['player_id'], ['players.id']),
        )
        op.create_index('ix_player_matches_player_id', 'player_matches', ['player_id'])
        op.create_index('ix_player_matches_match_date', 'player_matches', ['match_date'])
        op.create_index('ix_player_matches_id', 'player_matches', ['id'])

def downgrade() -> None:
    op.drop_table('player_matches')
    op.drop_table('live_matches')
    op.drop_table('player_live_stats')

