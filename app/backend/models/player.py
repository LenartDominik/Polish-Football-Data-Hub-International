# app/backend/models/player.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from ..database import Base
from .season_stats import PlayerSeasonStats
from .player_match import PlayerMatch


class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(String, unique=True, index=True, nullable=True) 
    name = Column(String, index=True)
    team = Column(String)
    league = Column(String)
    nationality = Column(String)
    position = Column(String, nullable=True)
    last_updated = Column(Date)
    
    # Relacje - istniejące
    season_stats = relationship(
        "PlayerSeasonStats", 
        back_populates="player", 
        cascade="all, delete-orphan"
    )
    
    matches = relationship(
        "PlayerMatch", 
        back_populates="player",
        cascade="all, delete-orphan"
    )
    
    # Relacje - NOWE dla statystyk z podziałem na rozgrywki
    competition_stats = relationship(
        "CompetitionStats", 
        back_populates="player", 
        cascade="all, delete-orphan"
    )
    
    goalkeeper_stats = relationship(
        "GoalkeeperStats", 
        back_populates="player", 
        cascade="all, delete-orphan"
    )
    
    # Property pomocnicza
    @property
    def is_goalkeeper(self):
        """Sprawdza czy gracz jest bramkarzem"""
        if not self.position:
            return False
        return 'GK' in self.position.upper() or 'GOALKEEPER' in self.position.upper()
    
    def __repr__(self):
        return f"<Player {self.name} ({self.position}) - {self.team}>"

