# app/backend/models/competition_stats.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class CompetitionType(enum.Enum):
    """Typy rozgrywek"""
    LEAGUE = "league"
    DOMESTIC_CUP = "domestic_cup"
    EUROPEAN_CUP = "european_cup"
    NATIONAL_TEAM = "national_team"

class CompetitionStats(Base):
    """
    Statystyki zawodników z pola, podzielone na rozgrywki
    """
    __tablename__ = "competition_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    
    season = Column(String, nullable=False)
    competition_type = Column(String, nullable=False)
    competition_name = Column(String, nullable=False)
    
    # Podstawowe statystyki
    games = Column(Integer, default=0)
    games_starts = Column(Integer, default=0)
    minutes = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    
    # Zaawansowane statystyki
    xg = Column(Float, default=0.0)  # Expected Goals
    npxg = Column(Float, default=0.0)  # Non-Penalty xG
    xa = Column(Float, default=0.0)  # Expected Assists (xAG)
    penalty_goals = Column(Integer, default=0)  # Penalty goals scored
    shots = Column(Integer, default=0)
    shots_on_target = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    
    # Relacje
    player = relationship("Player", back_populates="competition_stats")
    
    # Constraint: jeden rekord na sezon/rozgrywki/gracza
    __table_args__ = (
        UniqueConstraint('player_id', 'season', 'competition_type', 'competition_name',
                         name='uq_player_season_competition'),
    )

    def __repr__(self):
        return f"<CompetitionStats player_id={self.player_id} season={self.season} competition={self.competition_name}>"
