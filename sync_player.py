"""
Synchronize Polish players with FBref using Playwright scraper
Syncs both competition stats and match logs for current season
This script uses browser automation for reliable data fetching

Usage:
    python sync_playwright.py "Player Name"                    # Current season
    python sync_playwright.py "Player Name" --all-seasons      # All seasons  
    python sync_playwright.py "Player Name" --season=2024-2025 # Specific season
"""
import sys
import asyncio
from datetime import date, datetime
from typing import Optional, List
import logging

sys.path.append('.')

from sqlalchemy import text
from app.backend.database import SessionLocal
from app.backend.models.player import Player
from app.backend.models.player_match import PlayerMatch
from app.backend.models.competition_stats import CompetitionStats, CompetitionType
from app.backend.models.goalkeeper_stats import GoalkeeperStats
from app.backend.services.fbref_playwright_scraper import FBrefPlaywrightScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def reset_sequences_if_needed(db):
    """Reset PostgreSQL sequences to avoid ID conflicts after bulk deletes"""
    try:
        # Only run for PostgreSQL databases
        db_url = str(db.bind.url)
        if 'postgresql' in db_url or 'postgres' in db_url:
            logger.debug("🔧 Resetting PostgreSQL sequences...")
            db.execute(text("SELECT setval('competition_stats_id_seq', (SELECT COALESCE(MAX(id), 1) FROM competition_stats));"))
            db.execute(text("SELECT setval('goalkeeper_stats_id_seq', (SELECT COALESCE(MAX(id), 1) FROM goalkeeper_stats));"))
            db.commit()
            logger.debug("✅ Sequences reset successfully")
    except Exception as e:
        logger.warning(f"⚠️ Could not reset sequences (may not be PostgreSQL): {e}")


def get_competition_type(competition_name: str) -> str:
    """Determine competition type from competition name"""
    if not competition_name:
        return "LEAGUE"
    
    comp_lower = competition_name.lower()
    
    # National team (CHECK FIRST - before UEFA competitions)
    # This prevents international matches from being classified as European cups
    if any(keyword in comp_lower for keyword in [
        'national team', 'reprezentacja', 'international',
        'friendlies', 'wcq', 'world cup', 'uefa euro', 'copa am?rica'
    ]):
        return "NATIONAL_TEAM"
    
    # Domestic cups (CHECK SECOND - before European competitions)
    # This prevents domestic cups from being classified as European competitions
    if any(keyword in comp_lower for keyword in [
        'copa del rey', 'copa', 'pokal', 'coupe', 'coppa',
        'fa cup', 'league cup', 'efl', 'carabao',
        'dfb-pokal', 'dfl-supercup', 'supercoca', 'supercoppa',
        'u.s. open cup'
    ]):
        return "DOMESTIC_CUP"
    
    # European club competitions
    if any(keyword in comp_lower for keyword in [
        'champions league', 'europa league', 'conference league', 
        'uefa', 'champions lg', 'europa lg', 'conf lg', 'ucl', 'uel', 'uecl'
    ]):
        return "EUROPEAN_CUP"
    
    # Default to league
    return "LEAGUE"


def get_season_date_range(season: str):
    """Get date range for a season (e.g., 2024-2025 -> July 2024 to June 2025)"""
    if '-' in season:
        year_start = int(season.split('-')[0])
        year_end = int(season.split('-')[1])
        return date(year_start, 7, 1), date(year_end, 6, 30)
    else:
        # Calendar year for national team (e.g., "2024" -> Jan-Dec 2024)
        year = int(season)
        return date(year, 1, 1), date(year, 12, 31)


def fix_missing_minutes_from_matchlogs(db, player: Player):
    """
    Fix missing minutes in competition_stats and goalkeeper_stats by calculating from match logs.
    FBref sometimes doesn't provide minutes data in season stats tables.
    """
    logger.info(f"🔧 Checking for missing minutes data...")
    
    # Find all competition stats with 0 minutes but games > 0
    comp_stats_to_fix = db.query(CompetitionStats).filter(
        CompetitionStats.player_id == player.id,
        CompetitionStats.minutes == 0,
        CompetitionStats.games > 0
    ).all()
    
    # Find all goalkeeper stats with 0 minutes but games > 0
    from app.backend.models.goalkeeper_stats import GoalkeeperStats
    gk_stats_to_fix = db.query(GoalkeeperStats).filter(
        GoalkeeperStats.player_id == player.id,
        GoalkeeperStats.minutes == 0,
        GoalkeeperStats.games > 0
    ).all()
    
    total_to_fix = len(comp_stats_to_fix) + len(gk_stats_to_fix)
    
    if total_to_fix == 0:
        logger.info("✅ No missing minutes data")
        return
    
    logger.info(f"⚠️ Found {total_to_fix} records with missing minutes data ({len(comp_stats_to_fix)} comp + {len(gk_stats_to_fix)} gk)")
    
    fixed_count = 0
    
    # Fix competition stats
    for stat in comp_stats_to_fix:
        # Get date range for this season
        try:
            season_start, season_end = get_season_date_range(stat.season)
        except Exception as e:
            logger.warning(f"Could not parse season {stat.season}: {e}")
            continue
        
        # Get all match logs for this season and competition
        # Use flexible matching for competition names (handle different formats)
        comp_name_lower = stat.competition_name.lower()
        
        # Map common variations
        comp_mappings = {
            'europa lg': ['europa lg', 'europa league', 'uefa europa league'],
            'champions lg': ['champions lg', 'champions league', 'uefa champions league'],
            'conf lg': ['conf lg', 'conference league', 'uefa conference league'],
            'süper lig': ['süper lig', 'super lig'],
            'serie a': ['serie a'],
            'la liga': ['la liga', 'laliga'],
            'premier league': ['premier league'],
            'bundesliga': ['bundesliga'],
        }
        
        # Find matches for this competition (try multiple name variations)
        search_terms = [stat.competition_name]
        for key, variations in comp_mappings.items():
            if key in comp_name_lower:
                search_terms = variations
                break
        
        matches = []
        for term in search_terms:
            term_matches = db.query(PlayerMatch).filter(
                PlayerMatch.player_id == player.id,
                PlayerMatch.match_date >= season_start,
                PlayerMatch.match_date <= season_end,
                PlayerMatch.competition.ilike(f"%{term}%")
            ).all()
            matches.extend(term_matches)
        
        # Remove duplicates
        matches = list({m.id: m for m in matches}.values())
        
        if not matches:
            continue
        
        # Calculate total minutes
        total_minutes = sum(m.minutes_played or 0 for m in matches)
        
        if total_minutes > 0:
            stat.minutes = total_minutes
            fixed_count += 1
            logger.info(f"  ✅ [COMP] {stat.season} {stat.competition_name}: {total_minutes} min from {len(matches)} matches")
    
    # Fix goalkeeper stats
    for stat in gk_stats_to_fix:
        # Get date range for this season
        try:
            season_start, season_end = get_season_date_range(stat.season)
        except Exception as e:
            logger.warning(f"Could not parse season {stat.season}: {e}")
            continue
        
        # Get all match logs for this season and competition
        # Use flexible matching for competition names (handle different formats)
        comp_name_lower = stat.competition_name.lower()
        
        # Map common variations
        comp_mappings = {
            'europa lg': ['europa lg', 'europa league', 'uefa europa league'],
            'champions lg': ['champions lg', 'champions league', 'uefa champions league'],
            'conf lg': ['conf lg', 'conference league', 'uefa conference league'],
            'süper lig': ['süper lig', 'super lig'],
            'serie a': ['serie a'],
            'la liga': ['la liga', 'laliga'],
            'premier league': ['premier league'],
            'bundesliga': ['bundesliga'],
        }
        
        # Find matches for this competition (try multiple name variations)
        search_terms = [stat.competition_name]
        for key, variations in comp_mappings.items():
            if key in comp_name_lower:
                search_terms = variations
                break
        
        matches = []
        for term in search_terms:
            term_matches = db.query(PlayerMatch).filter(
                PlayerMatch.player_id == player.id,
                PlayerMatch.match_date >= season_start,
                PlayerMatch.match_date <= season_end,
                PlayerMatch.competition.ilike(f"%{term}%")
            ).all()
            matches.extend(term_matches)
        
        # Remove duplicates
        matches = list({m.id: m for m in matches}.values())
        
        if not matches:
            continue
        
        # Calculate total minutes
        total_minutes = sum(m.minutes_played or 0 for m in matches)
        
        if total_minutes > 0:
            stat.minutes = total_minutes
            fixed_count += 1
            logger.info(f"  ✅ [GK] {stat.season} {stat.competition_name}: {total_minutes} min from {len(matches)} matches")
    
    if fixed_count > 0:
        db.commit()
        logger.info(f"✅ Fixed {fixed_count} records with missing minutes!")


def save_competition_stats(db, player: Player, stats_list: List[dict], current_season: str = "2025-2026", save_all: bool = False):
    # DEBUG: Print all parsed stats for this player and season
    logger.info(f"[DEBUG] Parsed stats for {player.name} (season={current_season}):")
    for s in stats_list:
        if s.get('season') == current_season:
            logger.info(f"[DEBUG] {s}")
    """
    Save competition statistics to database
    
    Args:
        db: Database session
        player: Player object
        stats_list: List of competition stats dictionaries
        current_season: Current season to focus on (default: 2025-2026)
        save_all: If True, save all seasons. If False, only save current season
    """
    saved_count = 0
    
    if save_all:
        # Save all seasons
        logger.info(f"📊 Saving ALL seasons ({len(stats_list)} records)")
        current_stats = stats_list
        
        # Delete all existing stats for this player
        db.query(CompetitionStats).filter(
            CompetitionStats.player_id == player.id
        ).delete()
        
        db.query(GoalkeeperStats).filter(
            GoalkeeperStats.player_id == player.id
        ).delete()
        db.flush()  # Flush to clear session and avoid ID conflicts
        
        # Reset sequences for PostgreSQL to prevent ID conflicts
        reset_sequences_if_needed(db)
    else:
        # Filter for current season stats only - include all season variants (2025-2026, 2026, 2025)
        season_variants = [current_season, current_season.replace("-", "/"), current_season.split("-")[0], current_season.split("-")[-1]]
        current_stats = [s for s in stats_list if s.get('season') in season_variants]
        
        logger.info(f"📊 Found {len(current_stats)} stats for season {current_season} (from {len(stats_list)} total)")
        
        if not current_stats:
            logger.warning(f"No stats found for season {current_season}, using most recent season")
            # Get the most recent season
            if stats_list:
                seasons = [s.get('season', '') for s in stats_list if s.get('season')]
                if seasons:
                    latest_season = sorted(seasons)[-1]
                    current_stats = [s for s in stats_list if s.get('season') == latest_season]
                    current_season = latest_season
        
        # Delete existing stats for target season and all variants
        for season_variant in season_variants:
            db.query(CompetitionStats).filter(
                CompetitionStats.player_id == player.id,
                CompetitionStats.season == season_variant
            ).delete()
            
            db.query(GoalkeeperStats).filter(
                GoalkeeperStats.player_id == player.id,
                GoalkeeperStats.season == season_variant
            ).delete()
        db.flush()  # Flush to clear session and avoid ID conflicts
        logger.info(f"🗑️ Cleared existing stats for seasons: {season_variants}")
        
        # Reset sequences for PostgreSQL to prevent ID conflicts
        reset_sequences_if_needed(db)
    
    # Deduplicate stats by season/competition combination
    seen = set()
    deduplicated_stats = []
    for stat_data in current_stats:
        key = (stat_data.get('season'), stat_data.get('competition_name'))
        if key not in seen:
            seen.add(key)
            deduplicated_stats.append(stat_data)
        else:
            logger.warning(f"  ⚠️ Skipping duplicate: {stat_data.get('season')} - {stat_data.get('competition_name')}")
    
    for stat_data in deduplicated_stats:
        try:
            # Get competition type - now using VARCHAR instead of ENUM
            comp_type_raw = stat_data.get('competition_type')
            if comp_type_raw:
                if isinstance(comp_type_raw, str):
                    comp_type = comp_type_raw.upper()
                elif isinstance(comp_type_raw, CompetitionType):
                    comp_type = comp_type_raw.value.upper()
                else:
                    comp_type = get_competition_type(stat_data.get('competition_name', ''))
            else:
                comp_type = get_competition_type(stat_data.get('competition_name', ''))

            # DEBUG: log stat_data for current season
            if player.is_goalkeeper and stat_data.get('season') == current_season:
                logger.info(f"[GK_STATDATA_DEBUG] {stat_data}")

            if player.is_goalkeeper:
                # Map advanced goalkeeper stats using Playwright scraper keys (no 'gk_' prefix)
                gk_stat = GoalkeeperStats(
                    player_id=player.id,
                    season=stat_data.get('season', current_season),
                    competition_type=comp_type,
                    competition_name=stat_data.get('competition_name', ''),
                    games=stat_data.get('games', 0) or 0,
                    games_starts=stat_data.get('games_starts', 0) or 0,
                    minutes=stat_data.get('minutes', 0) or 0,
                    goals_against=stat_data.get('goals_against', 0) or 0,
                    goals_against_per90=stat_data.get('ga90', 0.0) or stat_data.get('goals_against_per90', 0.0) or 0.0,
                    shots_on_target_against=stat_data.get('sota', 0) or stat_data.get('shots_on_target_against', 0) or 0,
                    saves=stat_data.get('saves', 0) or 0,
                    save_percentage=stat_data.get('save_pct', 0.0) or 0.0,
                    clean_sheets=stat_data.get('clean_sheets', 0) or 0,
                    clean_sheet_percentage=stat_data.get('clean_sheets_pct', 0.0) or 0.0,
                    wins=stat_data.get('wins', 0) or 0,
                    draws=stat_data.get('draws', 0) or stat_data.get('ties', 0) or 0,
                    losses=stat_data.get('losses', 0) or 0,
                    penalties_attempted=stat_data.get('pens_att', 0) or 0,
                    penalties_allowed=stat_data.get('pens_allowed', 0) or 0,
                    penalties_saved=stat_data.get('pens_saved', 0) or 0,
                    penalties_missed=stat_data.get('pens_missed', 0) or 0,
                    post_shot_xg=stat_data.get('psxg', 0.0) or 0.0
                )
                db.add(gk_stat)
                logger.info(f"  💾 Saved GK stats: {stat_data.get('competition_name')} - {stat_data.get('games', 0)} games")
            else:
                # Save outfield player stats
                comp_stat = CompetitionStats(
                    player_id=player.id,
                    season=stat_data.get('season', current_season),
                    competition_type=comp_type,
                    competition_name=stat_data.get('competition_name', ''),
                    games=stat_data.get('games', 0) or 0,
                    games_starts=stat_data.get('games_starts', 0) or 0,
                    minutes=stat_data.get('minutes', 0) or 0,
                    goals=stat_data.get('goals', 0) or 0,
                    assists=stat_data.get('assists', 0) or 0,
                    xg=stat_data.get('xg', 0.0) or 0.0,
                    npxg=stat_data.get('npxg', 0.0) or 0.0,
                    xa=stat_data.get('xa', 0.0) or 0.0,
                    penalty_goals=stat_data.get('penalty_goals', 0) or 0,
                    shots=stat_data.get('shots', 0) or 0,
                    shots_on_target=stat_data.get('shots_on_target', 0) or 0,
                    yellow_cards=stat_data.get('yellow_cards', 0) or 0,
                    red_cards=stat_data.get('red_cards', 0) or 0,
                )
                db.add(comp_stat)
                logger.info(f"  💾 Saved stats: {stat_data.get('competition_name')} - {stat_data.get('goals', 0)}G {stat_data.get('assists', 0)}A in {stat_data.get('games', 0)} games")
            
            saved_count += 1
        except Exception as e:
            logger.error(f"  ❌ Error saving stat: {e}")
    
    return saved_count


async def sync_match_logs_for_season(scraper: FBrefPlaywrightScraper, db, player: Player, season: str):
    """Sync match logs for a specific season"""
    logger.info(f"📋 Syncing match logs for {player.name} ({season})")
    
    # Get FBref ID
    fbref_id = getattr(player, 'fbref_id', None) or getattr(player, 'api_id', None)
    if not fbref_id:
        logger.warning(f"⚠️ No FBref ID for {player.name}")
        return 0
    
    match_logs = await scraper.get_player_match_logs(fbref_id, player.name, season)
    if not match_logs:
        logger.warning(f"⚠️ No match logs found for {season}")
        return 0
    
    logger.info(f"📊 Found {len(match_logs)} matches")
    
    # Parse season to get date range (e.g., 2025-2026 = July 1, 2025 to June 30, 2026)
    from datetime import date
    year_start = int(season.split('-')[0])
    year_end = year_start + 1
    season_start = date(year_start, 7, 1)
    season_end = date(year_end, 6, 30)
    
    # Delete existing matches for this season only
    deleted = db.query(PlayerMatch).filter(
        PlayerMatch.player_id == player.id,
        PlayerMatch.match_date >= season_start,
        PlayerMatch.match_date <= season_end
    ).delete(synchronize_session='fetch')
    
    # Commit deletion immediately
    db.commit()
    
    if deleted > 0:
        logger.info(f"🗑️ Deleted {deleted} existing match logs for {season}")
    
    saved_count = 0
    skipped_duplicates = 0
    for match_data in match_logs:
        try:
            # Parse date
            match_date_str = match_data.get('match_date')
            if match_date_str:
                try:
                    match_date = datetime.strptime(match_date_str, '%Y-%m-%d').date()
                except:
                    try:
                        parts = match_date_str.split('-')
                        if len(parts) == 3:
                            match_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
                        else:
                            match_date = date.today()
                    except:
                        match_date = date.today()
            else:
                match_date = date.today()
            
            # Create match record
            match = PlayerMatch(
                player_id=player.id,
                match_date=match_date,
                competition=match_data.get('competition', ''),
                round=match_data.get('round', ''),
                venue=match_data.get('venue', ''),
                opponent=match_data.get('opponent', ''),
                result=match_data.get('result', ''),
                minutes_played=match_data.get('minutes_played', 0) or 0,
                goals=match_data.get('goals', 0) or 0,
                assists=match_data.get('assists', 0) or 0,
                shots=match_data.get('shots', 0) or 0,
                shots_on_target=match_data.get('shots_on_target', 0) or 0,
                xg=match_data.get('xg', 0.0) or 0.0,
                xa=match_data.get('xa', 0.0) or 0.0,
                passes_completed=match_data.get('passes_completed', 0) or 0,
                passes_attempted=match_data.get('passes_attempted', 0) or 0,
                pass_completion_pct=match_data.get('pass_completion_pct', 0.0) or 0.0,
                key_passes=match_data.get('key_passes', 0) or 0,
                tackles=match_data.get('tackles', 0) or 0,
                interceptions=match_data.get('interceptions', 0) or 0,
                blocks=match_data.get('blocks', 0) or 0,
                touches=match_data.get('touches', 0) or 0,
            )
            db.add(match)
            saved_count += 1
        except Exception as e:
            # Check if it's a duplicate error
            if 'uq_player_match' in str(e) or 'UNIQUE constraint' in str(e):
                skipped_duplicates += 1
                db.rollback()
            else:
                logger.error(f"❌ Error saving match: {e}")
                db.rollback()
    
    db.commit()
    
    if skipped_duplicates > 0:
        logger.info(f"⚠️ Skipped {skipped_duplicates} duplicate matches")
    
    logger.info(f"✅ Saved {saved_count} matches for {season}")
    return saved_count


async def sync_player(scraper: FBrefPlaywrightScraper, db, player: dict, use_search: bool = True, save_all_seasons: bool = False, target_season: str = "2025-2026") -> bool:
    """
    Synchronize a single player
    
    Args:
        scraper: Playwright scraper instance
        db: Database session
        player: Player to sync
        use_search: If True, search by name. If False, use player.fbref_id if available
        save_all_seasons: If True, save all seasons. If False, only current season
        target_season: Target season to sync (default: 2025-2026)
    
    Returns:
        True if successful, False otherwise
    """
    player_name = player.get('name')
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"🔄 Syncing: {player_name}")
        logger.info(f"{'='*60}")
        
        player_data = None
        
        # Try to fetch by ID if available (check both fbref_id and api_id)
        fbref_id = player.get('fbref_id') or player.get('api_id')
        if not use_search and fbref_id:
            logger.info(f"📌 Using FBref ID: {fbref_id}")
            player_data = await scraper.get_player_by_id(fbref_id, player_name)
        
        # Fall back to search if ID method failed or wasn't used
        if not player_data:
            logger.info(f"🔍 Searching by name: {player_name}")
            player_data = await scraper.search_player(player_name)
        
        if not player_data:
            logger.warning(f"❌ No data found for {player_name}")
            return False
        
        # Update player info
        if player_data.get('name'):
            logger.info(f"✅ Found: {player_data['name']}")
        
        # Save FBref ID if found (use api_id field)
        if player_data.get('player_id'):
            # Update in DB if needed
            db_player = db.query(Player).filter(Player.id == player['id']).first()
            if db_player:
                if not hasattr(db_player, 'fbref_id'):
                    if not db_player.api_id or db_player.api_id != player_data['player_id']:
                        db_player.api_id = player_data['player_id']
                        logger.info(f"💾 Saved FBref ID to api_id: {db_player.api_id}")
                else:
                    if not db_player.fbref_id:
                        db_player.fbref_id = player_data['player_id']
                        logger.info(f"💾 Saved FBref ID: {db_player.fbref_id}")
                db_player.last_updated = date.today()
                db.commit()
        
        # Save competition stats
        if player_data.get('competition_stats'):
            stats_count = len(player_data['competition_stats'])
            logger.info(f"📊 Processing {stats_count} competition records...")
            # Get db_player again (in case not yet fetched)
            db_player = db.query(Player).filter(Player.id == player['id']).first()
            if db_player:
                saved = save_competition_stats(
                    db, 
                    db_player, 
                    player_data['competition_stats'],
                    current_season=target_season,
                    save_all=save_all_seasons
                )
                logger.info(f"✅ Saved {saved} competition stats")
            else:
                logger.warning(f"❌ DB player not found for stats saving")
        else:
            logger.warning(f"⚠️ No competition stats found")
        
        # Save match logs for target season (only if not saving all seasons)
        if not save_all_seasons:
            db_player = db.query(Player).filter(Player.id == player['id']).first()
            if db_player:
                logger.info(f"\n📋 Syncing match logs for {target_season}...")
                matches_saved = await sync_match_logs_for_season(scraper, db, db_player, target_season)
                logger.info(f"✅ Saved {matches_saved} match logs")
                
                # Fix missing minutes in competition stats using match logs
                if matches_saved > 0:
                    fix_missing_minutes_from_matchlogs(db, db_player)
            else:
                logger.warning(f"❌ DB player not found for match logs")
        
        db.commit()
        logger.info(f"✅ Successfully synced {player_name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error syncing {player_name}: {e}", exc_info=True)
        db.rollback()
        return False


async def sync_players_list(players: List[Player], use_search: bool = True, headless: bool = True, save_all_seasons: bool = False, target_season: str = "2025-2026"):
    """
    Sync multiple players using Playwright scraper
    
    Args:
        players: List of players to sync
        use_search: If True, search by name. If False, use fbref_id
        headless: Run browser in headless mode
        save_all_seasons: If True, save all seasons. If False, only current season
        target_season: Target season to sync (default: 2025-2026)
    """
    db = SessionLocal()
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 Starting sync for {len(players)} players")
        logger.info(f"Target season: {target_season}")
        logger.info(f"Save all seasons: {save_all_seasons}")
        logger.info(f"{'='*60}")
        # Initialize scraper
        async with FBrefPlaywrightScraper(headless=headless, rate_limit_seconds=12.0) as scraper:
            synced = 0
            failed = 0
            for idx, player in enumerate(players):
                # Convert ORM Player to dict for sync_player
                player_data = {
                    'id': player.id,
                    'name': player.name,
                    'team': player.team,
                    'league': player.league,
                    'nationality': player.nationality,
                    'position': player.position,
                    'last_updated': player.last_updated,
                    'fbref_id': getattr(player, 'fbref_id', None),
                    'api_id': getattr(player, 'api_id', None),
                    'is_goalkeeper': player.is_goalkeeper
                }
                success = await sync_player(scraper, db, player_data, use_search=use_search, save_all_seasons=save_all_seasons, target_season=target_season)
                if success:
                    synced += 1
                else:
                    failed += 1
                # Progress indicator
                logger.info(f"\n📈 Progress: {idx + 1}/{len(players)} (✅ {synced} synced, ❌ {failed} failed)")
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ Sync complete!")
        logger.info(f"{'='*60}")
        logger.info(f"Total players: {len(players)}")
        logger.info(f"Successfully synced: {synced}")
        logger.info(f"Failed: {failed}")
        logger.info(f"{'='*60}")
    finally:
        db.close()


def get_players_from_args(db) -> List[Player]:
    """Get players based on command line arguments"""
    if len(sys.argv) > 1:
        player_names = sys.argv[1:]
        players = []
        
        for name in player_names:
            player = db.query(Player).filter(Player.name.ilike(f"%{name}%")).first()
            if player:
                players.append(player)
                logger.info(f"✅ Found player: {player.name}")
            else:
                logger.warning(f"❌ Player not found: {name}")
        
        return players
    else:
        # Get all players
        return db.query(Player).all()


def main():
    """Main entry point"""
    db = SessionLocal()
    
    try:
        # Get players to sync
        players = get_players_from_args(db)
        
        if not players:
            logger.error("No players to sync!")
            return
        
        # Check if we should use headless mode (default: yes)
        headless = '--visible' not in sys.argv
        
        # Check if we should use search (default: yes)
        use_search = '--use-id' not in sys.argv
        
        # Check if we should save all seasons (default: no, only current season)
        save_all_seasons = '--all-seasons' in sys.argv
        
        # Get target season (default: 2025-2026)
        target_season = "2025-2026"
        for arg in sys.argv:
            if arg.startswith('--season='):
                target_season = arg.split('=')[1]
        
        # Run async sync
        asyncio.run(sync_players_list(players, use_search=use_search, headless=headless, save_all_seasons=save_all_seasons, target_season=target_season))
        
    finally:
        db.close()


if __name__ == "__main__":
    main()

