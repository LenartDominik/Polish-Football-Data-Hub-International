"""
Quick add player script - No prompts, just arguments
Usage: python quick_add_player.py "Player Name" "Team" "League" "Position" [--sync]

Examples:
  python quick_add_player.py "Jakub Kiwior" "Arsenal" "Premier League" "DF"
  python quick_add_player.py "Jakub Kiwior" "Arsenal" "Premier League" "DF" --sync
  python quick_add_player.py "Jan Bednarek" "Southampton" "Premier League" "DF" --sync-matches-only
"""
import sys
import asyncio
sys.path.append('.')

from app.backend.database import SessionLocal
from app.backend.models.player import Player
from app.backend.services.fbref_playwright_scraper import FBrefPlaywrightScraper
from sync_playwright import sync_player
from sync_match_logs import sync_player_matches
from datetime import date


def quick_add_player(name, team, league, position, nationality="Polish"):
    """Quickly add a player to database"""
    db = SessionLocal()
    
    try:
        # Check if exists
        existing = db.query(Player).filter(Player.name.ilike(f"%{name}%")).first()
        player_obj = None
        if existing:
            print(f"⚠️  Player already exists: {existing.name} (ID: {existing.id})")
            # Update info
            existing.team = team
            existing.league = league
            existing.position = position
            existing.last_updated = date.today()
            db.commit()
            print(f"✅ Updated player info")
            player_obj = existing
        else:
            # Create new
            new_player = Player(
                name=name,
                team=team,
                league=league,
                nationality=nationality,
                position=position,
                last_updated=date.today()
            )
            db.add(new_player)
            db.commit()
            db.refresh(new_player)
            print(f"✅ Added: {new_player.name} (ID: {new_player.id})")
            player_obj = new_player
        # Prepare dict before closing session
        player_data = {
            'id': player_obj.id,
            'name': player_obj.name,
            'team': player_obj.team,
            'league': player_obj.league,
            'nationality': player_obj.nationality,
            'position': player_obj.position,
            'last_updated': player_obj.last_updated,
            'fbref_id': getattr(player_obj, 'fbref_id', None),
            'api_id': getattr(player_obj, 'api_id', None),
            'is_goalkeeper': player_obj.is_goalkeeper
        }
        return player_data
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return None
    finally:
        db.close()


async def quick_sync(player, sync_stats=True, sync_matches=True):
    """Quick sync player data"""
    db = SessionLocal()
    try:
        # player is already a dict, just use it directly
        player_data = player
        if sync_stats:
            print(f"📊 Syncing career stats...")
            async with FBrefPlaywrightScraper(headless=True, rate_limit_seconds=12.0) as scraper:
                success = await sync_player(scraper, db, player_data, use_search=True, save_all_seasons=True, target_season="2025-2026")
                if success:
                    print(f"✅ Career stats synced")
        if sync_matches:
            print(f"🏆 Syncing match logs...")
            async with FBrefPlaywrightScraper(headless=True, rate_limit_seconds=12.0) as scraper:
                matches = await sync_player_matches(scraper, db, player_data, "2025-2026")
                if matches > 0:
                    print(f"✅ Synced {matches} matches")
                else:
                    print(f"⚠️ No matches found")
    finally:
        db.close()


def main():
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)
    
    name = sys.argv[1]
    team = sys.argv[2]
    league = sys.argv[3]
    position = sys.argv[4].upper()
    
    if position not in ['FW', 'MF', 'DF', 'GK']:
        print(f"❌ Invalid position: {position}. Use FW, MF, DF, or GK")
        sys.exit(1)
    
    # Check flags
    sync_all = '--sync' in sys.argv
    sync_stats_only = '--sync-stats-only' in sys.argv
    sync_matches_only = '--sync-matches-only' in sys.argv
    
    print(f"\n{'='*60}")
    print(f"Adding: {name}")
    print(f"Team: {team} ({league})")
    print(f"Position: {position}")
    print(f"{'='*60}\n")
    
    # Add player
    player = quick_add_player(name, team, league, position)
    
    if not player:
        print("❌ Failed to add player")
        sys.exit(1)
    
    # Sync if requested
    if sync_all or sync_stats_only or sync_matches_only:
        print(f"\n{'='*60}")
        print("SYNCING FROM FBREF...")
        print(f"{'='*60}\n")
        
        sync_stats = sync_all or sync_stats_only
        sync_matches = sync_all or sync_matches_only
        
        asyncio.run(quick_sync(player, sync_stats, sync_matches))
    
    print(f"\n{'='*60}")
    print("✅ DONE!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
