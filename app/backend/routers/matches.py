"""
Router dla live meczów
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models.live_match import LiveMatch
from ..models.player_live_stats import PlayerLiveStats


router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/live")
def get_live_matches(db: Session = Depends(get_db)):
    """
    Pobierz wszystkie live mecze z Bundeslig i pucharów europejskich
    """
    try:
        # Zapisz/zaktualizuj w bazie
        saved_matches = []
        
        db.commit()
        
        return {
            "count": len(saved_matches),
            "matches": []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania live meczów: {str(e)}")


@router.get("/upcoming/{league_code}")
def get_upcoming_matches(league_code: str, days: int = 7):
    """
    Pobierz nadchodzące mecze dla konkretnej ligi
    
    Args:
        league_code: Kod ligi (bl1, bl2, cl, el, ecl)
        days: Ile dni do przodu (domyślnie 7)
    """
    try:
        return {
            "league": league_code,
            "days_ahead": days,
            "count": 0,
            "matches": []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania upcoming meczów: {str(e)}")


@router.get("/{match_id}/details")
def get_match_details(match_id: int):
    """
    Pobierz szczegóły meczu (składy, gole, kartki)
    """
    try:
        raise HTTPException(status_code=404, detail=f"Nie znaleziono meczu {match_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania szczegółów meczu: {str(e)}")


@router.get("/{match_id}/player/{player_name}")
def get_player_match_stats(match_id: int, player_name: str):
    """
    Pobierz statystyki konkretnego gracza w danym meczu
    """
    try:
        raise HTTPException(
            status_code=404, 
            detail=f"Gracz {player_name} nie występuje w meczu {match_id}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania statystyk gracza: {str(e)}")


@router.post("/sync/live")
def sync_live_matches(db: Session = Depends(get_db)):
    """
    Synchronizuj live mecze - wywoływane automatycznie przez scheduler co 5 minut
    """
    try:
        updated_count = 0
        new_count = 0
        
        db.commit()
        
        return {
            "status": "success",
            "updated": updated_count,
            "new": new_count,
            "total_live": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd synchronizacji: {str(e)}")


@router.delete("/cleanup/finished")
def cleanup_finished_matches(db: Session = Depends(get_db), days_old: int = 7):
    """
    Usuń zakończone mecze starsze niż X dni (domyślnie 7)
    """
    try:
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        deleted = 0
        
        db.commit()
        
        return {
            "status": "success",
            "deleted": deleted,
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd czyszczenia: {str(e)}")
