"""
Router for player matchlogs (detailed match statistics)
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ..database import get_db
from ..models.player_match import PlayerMatch
from ..models.player import Player


router = APIRouter(prefix="/api/players", tags=["matchlogs"])


@router.get("/{player_id}/matches")
def get_player_matches(
    player_id: int,
    season: Optional[str] = Query(None, description="Filter by season (e.g., '2025-2026')"),
    competition: Optional[str] = Query(None, description="Filter by competition"),
    limit: Optional[int] = Query(100, description="Maximum number of matches to return"),
    db: Session = Depends(get_db)
):
    """
    Get match logs (detailed match statistics) for a specific player
    
    Parameters:
    - player_id: Player ID
    - season: Optional season filter (e.g., "2025-2026")
    - competition: Optional competition filter (e.g., "La Liga")
    - limit: Maximum number of matches (default: 100)
    
    Returns:
    - List of matches with detailed statistics
    """
    # Check if player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Build query
    query = db.query(PlayerMatch).filter(PlayerMatch.player_id == player_id)
    
    # Apply filters
    if season:
        # Filter by year in match_date (season 2025-2026 includes matches from 2025 and 2026)
        year_start = int(season.split('-')[0])
        query = query.filter(
            db.func.strftime('%Y', PlayerMatch.match_date).in_([str(year_start), str(year_start + 1)])
        )
    
    if competition:
        query = query.filter(PlayerMatch.competition.ilike(f"%{competition}%"))
    
    # Order by date (most recent first)
    query = query.order_by(PlayerMatch.match_date.desc())
    
    # Limit results
    if limit:
        query = query.limit(limit)
    
    matches = query.all()
    
    return {
        "player_id": player_id,
        "player_name": player.name,
        "total_matches": len(matches),
        "filters": {
            "season": season,
            "competition": competition
        },
        "matches": [
            {
                "id": match.id,
                "date": match.match_date.isoformat() if match.match_date else None,
                "competition": match.competition,
                "round": match.round,
                "venue": match.venue,
                "opponent": match.opponent,
                "result": match.result,
                "minutes_played": match.minutes_played,
                "goals": match.goals,
                "assists": match.assists,
                "shots": match.shots,
                "shots_on_target": match.shots_on_target,
                "xg": match.xg,
                "xa": match.xa,
                "passes_completed": match.passes_completed,
                "passes_attempted": match.passes_attempted,
                "pass_completion_pct": match.pass_completion_pct,
                "key_passes": match.key_passes,
                "tackles": match.tackles,
                "interceptions": match.interceptions,
                "blocks": match.blocks,
                "touches": match.touches,
                "dribbles_completed": match.dribbles_completed,
                "carries": match.carries,
                "fouls_committed": match.fouls_committed,
                "fouls_drawn": match.fouls_drawn,
                "yellow_cards": match.yellow_cards,
                "red_cards": match.red_cards
            }
            for match in matches
        ]
    }


@router.get("/{player_id}/matches/stats")
def get_player_match_stats_summary(
    player_id: int,
    season: Optional[str] = Query(None, description="Filter by season"),
    competition: Optional[str] = Query(None, description="Filter by competition"),
    db: Session = Depends(get_db)
):
    """
    Get aggregated match statistics for a player
    
    Returns summary statistics calculated from matchlogs
    """
    # Check if player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Build query
    query = db.query(PlayerMatch).filter(PlayerMatch.player_id == player_id)
    
    # Apply filters
    if season:
        try:
            year_start = int(season.split('-')[0])
            query = query.filter(
                db.func.strftime('%Y', PlayerMatch.match_date).in_([str(year_start), str(year_start + 1)])
            )
        except:
            # If season parsing fails, skip filter
            pass
    
    if competition:
        query = query.filter(PlayerMatch.competition.ilike(f"%{competition}%"))
    
    matches = query.all()
    
    if not matches:
        return {
            "player_id": player_id,
            "player_name": player.name,
            "message": "No matches found for the specified filters"
        }
    
    # Calculate aggregates
    total_matches = len(matches)
    total_minutes = sum(m.minutes_played or 0 for m in matches)
    total_goals = sum(m.goals or 0 for m in matches)
    total_assists = sum(m.assists or 0 for m in matches)
    total_shots = sum(m.shots or 0 for m in matches)
    total_shots_on_target = sum(m.shots_on_target or 0 for m in matches)
    total_xg = sum(m.xg or 0 for m in matches)
    total_xa = sum(m.xa or 0 for m in matches)
    total_yellow_cards = sum(m.yellow_cards or 0 for m in matches)
    total_red_cards = sum(m.red_cards or 0 for m in matches)
    
    # Calculate averages
    avg_minutes = total_minutes / total_matches if total_matches > 0 else 0
    avg_goals = total_goals / total_matches if total_matches > 0 else 0
    avg_assists = total_assists / total_matches if total_matches > 0 else 0
    
    return {
        "player_id": player_id,
        "player_name": player.name,
        "filters": {
            "season": season,
            "competition": competition
        },
        "summary": {
            "total_matches": total_matches,
            "total_minutes": total_minutes,
            "total_goals": total_goals,
            "total_assists": total_assists,
            "total_shots": total_shots,
            "total_shots_on_target": total_shots_on_target,
            "total_xg": round(total_xg, 2),
            "total_xa": round(total_xa, 2),
            "total_yellow_cards": total_yellow_cards,
            "total_red_cards": total_red_cards,
            "avg_minutes_per_match": round(avg_minutes, 1),
            "avg_goals_per_match": round(avg_goals, 2),
            "avg_assists_per_match": round(avg_assists, 2)
        }
    }


@router.get("/matches/{match_id}")
def get_match_details(match_id: int, db: Session = Depends(get_db)):
    """
    Get detailed statistics for a specific match
    
    Parameters:
    - match_id: Match ID
    
    Returns:
    - Detailed match statistics including player performance
    """
    match = db.query(PlayerMatch).filter(PlayerMatch.id == match_id).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Get player info
    player = db.query(Player).filter(Player.id == match.player_id).first()
    
    return {
        "match_id": match.id,
        "player": {
            "id": player.id if player else None,
            "name": player.name if player else None,
            "team": player.team if player else None
        },
        "match_info": {
            "date": match.match_date.isoformat() if match.match_date else None,
            "competition": match.competition,
            "round": match.round,
            "venue": match.venue,
            "opponent": match.opponent,
            "result": match.result
        },
        "performance": {
            "minutes_played": match.minutes_played,
            "goals": match.goals,
            "assists": match.assists
        },
        "shooting": {
            "shots": match.shots,
            "shots_on_target": match.shots_on_target,
            "xg": match.xg
        },
        "passing": {
            "passes_completed": match.passes_completed,
            "passes_attempted": match.passes_attempted,
            "pass_completion_pct": match.pass_completion_pct,
            "key_passes": match.key_passes,
            "xa": match.xa
        },
        "defense": {
            "tackles": match.tackles,
            "interceptions": match.interceptions,
            "blocks": match.blocks
        },
        "possession": {
            "touches": match.touches,
            "dribbles_completed": match.dribbles_completed,
            "carries": match.carries
        },
        "discipline": {
            "fouls_committed": match.fouls_committed,
            "fouls_drawn": match.fouls_drawn,
            "yellow_cards": match.yellow_cards,
            "red_cards": match.red_cards
        }
    }
