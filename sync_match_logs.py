"""
Sync match logs (detailed match statistics) for players
Usage: python sync_match_logs.py "Player Name" [--season YYYY-YYYY]
"""
import sys
import asyncio
from datetime import datetime, date
import logging

sys.path.append('.')

from app.backend.database import SessionLocal
from app.backend.models.player import Player
from app.backend.models.player_match import PlayerMatch
from app.backend.services.fbref_playwright_scraper import FBrefPlaywrightScraper

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def sync_player_matches(scraper: FBrefPlaywrightScraper, db, player: Player, season: str = "2025-2026") -> int:
    """
    Sync match logs for a player
    
    Args:
        scraper: FBref Playwright scraper instance
        db: Database session
        player: Player object
        season: Season to sync (default: 2025-2026)
    
    Returns:
        Number of matches synced
    """
    logger.info(f"🏆 Syncing match logs for {player['name']} ({season})")
    # Get FBref ID
    fbref_id = player.get('fbref_id') or player.get('api_id')
    if not fbref_id:
        logger.warning(f"⚠️ No FBref ID for {player['name']}. Searching...")
        # Try to find player first
        player_data = await scraper.search_player(player['name'])
        if player_data and player_data.get('player_id'):
            fbref_id = player_data['player_id']
            # Update in DB if possible
            db_player = db.query(Player).filter(Player.id == player['id']).first()
            if db_player:
                db_player.api_id = fbref_id
                db.commit()
            logger.info(f"✅ Found FBref ID: {fbref_id}")
        else:
            logger.error(f"❌ Could not find player on FBref")
            return 0
    # Get match logs
    match_logs = await scraper.get_player_match_logs(fbref_id, player['name'], season)
    if not match_logs:
        logger.warning(f"⚠️ No match logs found for {season}")
        return 0
    logger.info(f"📊 Found {len(match_logs)} matches")
    # Delete existing matches for this season
    db.query(PlayerMatch).filter(
        PlayerMatch.player_id == player['id']
    ).delete()
    # Save matches
    saved_count = 0
    for match_data in match_logs:
        try:
            # Parse date - scraper returns 'match_date' key
            match_date_str = match_data.get('match_date')
            if match_date_str:
                try:
                    # FBref format is usually "2024-11-03" or similar
                    match_date = datetime.strptime(match_date_str, '%Y-%m-%d').date()
                except:
                    # Try alternative formats
                    try:
                        # Try "YYYY-MM-DD"
                        parts = match_date_str.split('-')
                        if len(parts) == 3:
                            match_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
                        else:
                            logger.warning(f"Could not parse date: {match_date_str}, using today")
                            match_date = date.today()
                    except:
                        logger.warning(f"Could not parse date: {match_date_str}, using today")
                        match_date = date.today()
            else:
                logger.warning(f"No date in match data, using today")
                match_date = date.today()
            # Create match record
            match = PlayerMatch(
                player_id=player['id'],
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
            logger.error(f"❌ Error saving match: {e}")
    db.commit()
    logger.info(f"✅ Saved {saved_count} matches for {player['name']} ({season})")
    return saved_count

async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print('  python sync_match_logs.py "Robert Lewandowski"')
        print('  python sync_match_logs.py "Michał Helik" --season 2024-2025')
        sys.exit(1)
    player_name = sys.argv[1]
    # Parse season
    season = "2025-2026"
    if '--season' in sys.argv:
        try:
            season_idx = sys.argv.index('--season')
            season = sys.argv[season_idx + 1]
        except:
            pass
    logger.info("=" * 60)
    logger.info(f"SYNC MATCH LOGS: {player_name}")
    logger.info(f"Season: {season}")
    logger.info("=" * 60)
    db = SessionLocal()
    try:
        # Find player
        player = db.query(Player).filter(Player.name.ilike(f"%{player_name}%")).first()
        if not player:
            logger.error(f"❌ Player not found: {player_name}")
            logger.info("💡 Add player first with: python quick_add_player.py")
            sys.exit(1)
        logger.info(f"✅ Found player: {player.name} (ID: {player.id})")
        # Sync matches
        async with FBrefPlaywrightScraper(headless=True, rate_limit_seconds=12.0) as scraper:
            # Convert ORM to dict for sync_player_matches
            player_data = {
                'id': player.id,
                'name': player.name,
                'team': player.team,
                'league': player.league,
                'nationality': player.nationality,
                'position': player.position,
                'last_updated': player.last_updated,
                'fbref_id': getattr(player, 'fbref_id', None),
                'api_id': getattr(player, 'api_id', None)
            }
            matches_count = await sync_player_matches(scraper, db, player_data, season)
        logger.info("=" * 60)
        if matches_count > 0:
            logger.info(f"✅ SUCCESS: Synced {matches_count} matches")
        else:
            logger.warning(f"⚠️ No matches synced")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
