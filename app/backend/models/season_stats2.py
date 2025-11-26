from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class PlayerSeasonStats(Base):
    """Statystyki gracza dla konkretnego sezonu"""
    __tablename__ = "player_season_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    season = Column(Integer, nullable=False, index=True)  # Rok rozpoczęcia sezonu (np. 2023 dla 2023/2024)
    
    # Podstawowe statystyki
    matches = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    
    # Zaawansowane statystyki (FBref)
    xG = Column(Float, nullable=True)  # Expected Goals
    xA = Column(Float, nullable=True)  # Expected Assists
    progressive_passes = Column(Integer, nullable=True)
    progressive_carries = Column(Integer, nullable=True)
    starts = Column(Integer, nullable=True)  # Liczba meczów od pierwszej minuty
    
    # Dodatkowe informacje
    team = Column(String, nullable=True)  # Klub w którym grał w tym sezonie
    league = Column(String, nullable=True)  # Liga w której grał
    
    # Relacja do gracza
    player = relationship("Player", back_populates="season_stats")
