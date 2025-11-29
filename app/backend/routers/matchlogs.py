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


router = APIRouter(prefix="/matchlogs", tags=["matchlogs"])


@router.get("/{player_id}")
def get_player_matches(
    player_id: int,
    season: Optional[str] = Query(None, description="Filter by season (e.g., '2025-2026')"),
    competition: Optional[str] = Query(None, description="Filter by competition"),
    limit: Optional[int] = Query(100, description="Maximum number of matches to return"),
    db: Session = Depends(get_db)
):
    """
    Get match logs (detailed match statistics) for a specific player

    **Endpoint:** GET /api/matchlogs/{player_id}
    
    This endpoint returns detailed match-by-match statistics for a player.
    You can filter by season and competition, and limit the number of results.
    
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
        # Filter by season dates (e.g., 2025-2026 = July 1, 2025 to June 30, 2026)
        # For international matches (WCQ, Nations League, etc.), also include matches from the target year
        from datetime import date
        from sqlalchemy import or_, extract
        year_start = int(season.split('-')[0])
        year_end = year_start + 1
        season_start = date(year_start, 7, 1)
        season_end = date(year_end, 6, 30)
        
        # International competitions that span multiple seasons
        international_comps = ['WCQ', 'World Cup', 'UEFA Nations League', 'UEFA Euro Qualifying', 
                               'UEFA Euro', 'Friendlies (M)', 'Copa América']
        
        # Club matches: date range, International matches: target year
        query = query.filter(
            or_(
                # Club matches within season dates
                (PlayerMatch.match_date >= season_start) & (PlayerMatch.match_date <= season_end),
                # International matches in target year
                (PlayerMatch.competition.in_(international_comps)) & 
                (extract('year', PlayerMatch.match_date).in_([year_start, year_end]))
            )
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


@router.get("/{player_id}/stats")
def get_player_match_stats_summary(
    player_id: int,
    season: Optional[str] = Query(None, description="Filter by season"),
    competition: Optional[str] = Query(None, description="Filter by competition"),
    db: Session = Depends(get_db)
):
    """
    Get aggregated match statistics for a player

    **Endpoint:** GET /api/matchlogs/{player_id}/stats
    
    Returns summary statistics calculated from all match logs:
    - Total matches, goals, assists, minutes
    - Average performance metrics per match
    - Filterable by season and competition
    
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
            # Filter by season dates (e.g., 2025-2026 = July 1, 2025 to June 30, 2026)
            # For international matches, also include matches from the target year
            from datetime import date
            from sqlalchemy import or_, extract
            year_start = int(season.split('-')[0])
            year_end = year_start + 1
            season_start = date(year_start, 7, 1)
            season_end = date(year_end, 6, 30)
            
            # International competitions that span multiple seasons
            international_comps = ['WCQ', 'World Cup', 'UEFA Nations League', 'UEFA Euro Qualifying', 
                                   'UEFA Euro', 'Friendlies (M)', 'Copa América']
            
            # Club matches: date range, International matches: target year
            query = query.filter(
                or_(
                    # Club matches within season dates
                    (PlayerMatch.match_date >= season_start) & (PlayerMatch.match_date <= season_end),
                    # International matches in target year
                    (PlayerMatch.competition.in_(international_comps)) & 
                    (extract('year', PlayerMatch.match_date).in_([year_start, year_end]))
                )
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


@router.get("/match/{match_id}")
def get_match_details(match_id: int, db: Session = Depends(get_db)):
    """
    Get detailed statistics for a specific match

    **Endpoint:** GET /api/matchlogs/match/{match_id}
    
    Returns comprehensive performance data for a single match including:
    - Match information (date, competition, opponent, result)
    - Performance (goals, assists, minutes)
    - Shooting, passing, defense, possession statistics
    - Discipline (fouls, cards)
    
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



