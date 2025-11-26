"""
Model dla live meczów (OpenLigaDB)
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from ..database import Base
from datetime import datetime


class LiveMatch(Base):
    __tablename__ = "live_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, unique=True, index=True)  # ID z OpenLigaDB
    competition = Column(String)  # Bundesliga 1, Champions League, etc.
    home_team = Column(String)
    away_team = Column(String)
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    status = Column(String)  # SCHEDULED, LIVE, FINISHED
    kickoff_time = Column(DateTime)
    matchday = Column(Integer, nullable=True)
    season = Column(String)  # np. "2024/2025"
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<LiveMatch {self.home_team} vs {self.away_team} ({self.status})>"
