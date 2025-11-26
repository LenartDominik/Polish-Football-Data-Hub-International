from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.player import PlayerResponse, PlayerCreate
from ..models.player import Player
from datetime import date
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=list[PlayerResponse])
def get_all_players(db: Session = Depends(get_db)):
    """Zwraca wszystkich piłkarzy z bazy"""
    try:
        players = db.query(Player).all()
        logger.info(f"Found {len(players)} players in database")
        if players:
            logger.info(f"First player: id={players[0].id}, name={players[0].name}, api_id={players[0].api_id}")
        return players
    except Exception as e:
        logger.error(f"Error getting players: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Zwraca konkretnego piłkarza"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Piłkarz nie znaleziony")
    return player

# ============================================================================
# OLD ENDPOINTS REMOVED
# ============================================================================
# The following endpoints have been removed as they used deprecated services:
# 
# 1. API-Football integration (football_api.py):
#    - GET /sync/api - Synchronized players from API-Football
#
# 2. Player season stats table (deprecated):
#    - POST /{player_id}/sync/current-season
#    - GET /fbref/search/{player_name}
#    - POST /fbref/sync/{player_name}
#    - POST /fbref/sync-all
#
# These have been replaced by:
# - sync_playwright.py (for individual player sync)
# - sync_all_playwright.py (for bulk sync)
# These scripts write directly to competition_stats and goalkeeper_stats tables.
#
# See CLEANUP_OLD_ENDPOINTS.md for details.
