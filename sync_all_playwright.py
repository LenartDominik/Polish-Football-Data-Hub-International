"""
Sync all Polish players using Playwright scraper
This script syncs ALL players in the database with proper rate limiting
"""
import sys
import asyncio
from datetime import datetime, date
import logging

sys.path.append('.')

from app.backend.database import SessionLocal
from app.backend.models.player import Player
from app.backend.services.fbref_playwright_scraper import FBrefPlaywrightScraper
from sync_player import sync_player

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'sync_playwright_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)


async def sync_all_players(limit: int = None, headless: bool = True, save_all_seasons: bool = False, target_season: str = "2025-2026"):
    """
    Sync all players in the database
    
    Args:
        limit: Maximum number of players to sync (None = all)
        headless: Run browser in headless mode
        save_all_seasons: If True, save all seasons. If False, only current season
        target_season: Target season to sync (default: 2025-2026)
    """
    db = SessionLocal()
    
    try:
        # Get all players
        query = db.query(Player).order_by(Player.name)
        if limit:
            query = query.limit(limit)
        
        players = query.all()
        
        logger.info("=" * 70)
        logger.info(f"🚀 FULL SYNC - Starting sync for {len(players)} players")
        logger.info("=" * 70)
        logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Target season: {target_season}")
        logger.info(f"Save all seasons: {save_all_seasons}")
        logger.info(f"Headless mode: {headless}")
        logger.info(f"Rate limit: 12 seconds per player")
        estimated_time = len(players) * 12 / 60
        logger.info(f"Estimated time: {estimated_time:.1f} minutes")
        logger.info("=" * 70)
        
        start_time = datetime.now()
        synced = 0
        failed = 0
        failed_players = []
        
        # Initialize Playwright scraper
        async with FBrefPlaywrightScraper(headless=headless, rate_limit_seconds=12.0) as scraper:
            
            for idx, player in enumerate(players, 1):
                try:
                    logger.info(f"\n{'='*70}")
                    logger.info(f"Player {idx}/{len(players)}: {player.name}")
                    logger.info(f"{'='*70}")
                    
                    # Sync player (will use search by default)
                    success = await sync_player(scraper, db, player, use_search=True, save_all_seasons=save_all_seasons, target_season=target_season)
                    
                    if success:
                        synced += 1
                    else:
                        failed += 1
                        failed_players.append(player.name)
                    
                    # Progress report every 10 players
                    if idx % 10 == 0:
                        elapsed = (datetime.now() - start_time).total_seconds()
                        avg_time = elapsed / idx
                        remaining = (len(players) - idx) * avg_time / 60
                        
                        logger.info(f"\n{'='*70}")
                        logger.info(f"📊 PROGRESS REPORT - {idx}/{len(players)} players processed")
                        logger.info(f"{'='*70}")
                        logger.info(f"✅ Synced: {synced}")
                        logger.info(f"❌ Failed: {failed}")
                        logger.info(f"⏱️ Average time per player: {avg_time:.1f}s")
                        logger.info(f"⏳ Estimated remaining time: {remaining:.1f} minutes")
                        logger.info(f"{'='*70}")
                
                except KeyboardInterrupt:
                    logger.warning("\n⚠️ Sync interrupted by user!")
                    break
                    
                except Exception as e:
                    logger.error(f"❌ Unexpected error for {player.name}: {e}", exc_info=True)
                    failed += 1
                    failed_players.append(player.name)
        
        # Final summary
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        logger.info(f"\n{'='*70}")
        logger.info(f"✅ SYNC COMPLETE!")
        logger.info(f"{'='*70}")
        logger.info(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Total time: {total_time/60:.1f} minutes")
        logger.info(f"{'='*70}")
        logger.info(f"Total players: {len(players)}")
        logger.info(f"✅ Successfully synced: {synced}")
        logger.info(f"❌ Failed: {failed}")
        logger.info(f"Success rate: {synced/len(players)*100:.1f}%")
        logger.info(f"{'='*70}")
        
        if failed_players:
            logger.info(f"\n❌ Failed players ({len(failed_players)}):")
            for name in failed_players:
                logger.info(f"   - {name}")
        
        logger.info(f"\n💾 Log saved to: sync_playwright_{datetime.now().strftime('%Y%m%d')}_*.log")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"❌ Fatal error during sync: {e}", exc_info=True)
    finally:
        db.close()


def main():
    """Main entry point"""
    
    # Parse command line arguments
    limit = None
    headless = True
    save_all_seasons = False
    target_season = "2025-2026"
    
    for arg in sys.argv[1:]:
        if arg == '--visible':
            headless = False
        elif arg == '--all-seasons':
            save_all_seasons = True
        elif arg.startswith('--limit='):
            try:
                limit = int(arg.split('=')[1])
            except ValueError:
                logger.error(f"Invalid limit value: {arg}")
                sys.exit(1)
        elif arg.startswith('--season='):
            target_season = arg.split('=')[1]
    
    # Show warning for full sync
    if not limit:
        logger.warning("\n⚠️ WARNING: You are about to sync ALL players in the database!")
        logger.warning("This may take a long time and use significant bandwidth.")
        
        try:
            response = input("\nDo you want to continue? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                logger.info("Sync cancelled by user.")
                return
        except KeyboardInterrupt:
            logger.info("\nSync cancelled by user.")
            return
    
    # Run sync
    asyncio.run(sync_all_players(limit=limit, headless=headless, save_all_seasons=save_all_seasons, target_season=target_season))


if __name__ == "__main__":
    main()
