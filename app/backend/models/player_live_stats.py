"""
Model dla statystyk gracza w live meczu
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime


class PlayerLiveStats(Base):
    __tablename__ = "player_live_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    match_id = Column(Integer, ForeignKey("live_matches.id"), index=True)
    
    # Statystyki z meczu
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    
    # Status
    is_live = Column(Boolean, default=False)  # Czy mecz trwa w tej chwili
    team = Column(String)  # Nazwa drużyny w meczu
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # Usunięto back_populates="live_stats" bo relacja jest zakomentowana w Player
    player = relationship("Player")
    match = relationship("LiveMatch")
    
    def __repr__(self):
        return f"<PlayerLiveStats player_id={self.player_id} match_id={self.match_id} goals={self.goals}>"
