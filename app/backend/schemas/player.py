from pydantic import BaseModel
from datetime import date
from typing import Optional, Union


class PlayerBase(BaseModel):
    name: str
    team: str
    league: str
    nationality: str = "Poland"
    position: Optional[str] = None


class PlayerCreate(PlayerBase):
    api_id: Optional[str] = None  # Zmienione z int na Optional[str]


class PlayerResponse(PlayerBase):
    id: int
    api_id: Optional[Union[str, int]] = None
    last_updated: Optional[date] = None
    
    class Config:
        from_attributes = True

