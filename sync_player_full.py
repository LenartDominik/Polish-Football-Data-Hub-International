"""
Full player sync - Competition stats + Match logs for ALL seasons
Usage: python sync_player_full.py "Player Name" [--seasons 2023-2024 2024-2025 2025-2026]
"""
import sys
import asyncio
from datetime import datetime, date
import logging
import argparse
from collections import defaultdict 

sys.path.append('.')

from sqlalchemy import text
from app.backend.database import SessionLocal
from app.backend.models.player import Player
from app.backend.models.player_match import PlayerMatch
from app.backend.models.competition_stats import CompetitionStats
from app.backend.models.goalkeeper_stats import GoalkeeperStats
from app.backend.services.fbref_playwright_scraper import FBrefPlaywrightScraper

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def reset_sequences_if_needed():
    """Reset PostgreSQL sequences (Safe & Independent Session)"""
    db = SessionLocal() 
    try:
        db_url = str(db.bind.url)
        if 'postgresql' in db_url or 'postgres' in db_url:
            # logger.info("🔧 Resetting PostgreSQL sequences...")
            db.execute(text("SELECT setval('competition_stats_id_seq', (SELECT COALESCE(MAX(id), 1) FROM competition_stats));"))
            db.execute(text("SELECT setval('goalkeeper_stats_id_seq', (SELECT COALESCE(MAX(id), 1) FROM goalkeeper_stats));"))
            db.execute(text("SELECT setval('player_matches_id_seq', (SELECT COALESCE(MAX(id), 1) FROM player_matches));"))
            db.commit()
    except Exception as e:
        logger.warning(f"⚠️ Sequence reset warning: {e}")
        db.rollback()
    finally:
        db.close() 

def get_season_date_range(season: str):
    """Get date range for a season (Helper - No DB needed)"""
    if '-' in season:
        try:
            year_start = int(season.split('-')[0])
            year_end = int(season.split('-')[1])
            return date(year_start, 7, 1), date(year_end, 6, 30)
        except:
             return date.today(), date.today()
    else:
        try:
            year = int(season)
            return date(year, 1, 1), date(year, 12, 31)
        except:
             return date.today(), date.today()

def sync_competition_stats_from_matches(player_id: int) -> int:
    """
    Synchronize competition_stats from player_matches.
    Safe for Supabase Port 6543 (Independent Session).
    """
    db = SessionLocal()
    try:
        matches = db.query(PlayerMatch).filter(PlayerMatch.player_id == player_id).all()
        if not matches: return 0
        
        stats_dict = defaultdict(lambda: {
            'games': 0, 'goals': 0, 'assists': 0, 'minutes': 0,
            'xg': 0.0, 'xa': 0.0, 'games_starts': 0
        })
        
        for match in matches:
            year = match.match_date.year
            month = match.match_date.month
            if month >= 7: season = f"{year}-{year+1}"
            else: season = f"{year-1}-{year}"
            
            international_comps = ['WCQ', 'World Cup', 'UEFA Nations League', 'UEFA Euro Qualifying', 'UEFA Euro', 'Friendlies (M)', 'Copa América']
            if match.competition in international_comps: season = str(year)
            
            competition_name = f'National Team {season}' if match.competition in international_comps else match.competition
            
            key = (season, competition_name)
            stats_dict[key]['games'] += 1
            stats_dict[key]['goals'] += match.goals or 0
            stats_dict[key]['assists'] += match.assists or 0
            stats_dict[key]['minutes'] += match.minutes_played or 0
            stats_dict[key]['xg'] += match.xg or 0.0
            stats_dict[key]['xa'] += match.xa or 0.0
            stats_dict[key]['games_starts'] += 1 if (match.minutes_played or 0) > 45 else 0
        
        updated = 0
        for (season, competition), stats in stats_dict.items():
            record = db.query(CompetitionStats).filter(
                CompetitionStats.player_id == player_id,
                CompetitionStats.season == season,
                CompetitionStats.competition_name == competition
            ).first()
            
            comp_type = 'LEAGUE'
            if 'Cup' in competition or 'Pokal' in competition: comp_type = 'CUP'
            elif 'National Team' in competition: comp_type = 'NATIONAL_TEAM'
            elif 'Champions League' in competition or 'Europa' in competition: comp_type = 'INTERNATIONAL_CUP'

            if record:
                record.games = stats['games']
                record.goals = stats['goals']
                record.assists = stats['assists']
                record.minutes = stats['minutes']
                record.xg = stats['xg']
                record.xa = stats['xa']
                record.games_starts = stats['games_starts']
            else:
                record = CompetitionStats(
                    player_id=player_id, season=season, competition_name=competition, competition_type=comp_type,
                    games=stats['games'], goals=stats['goals'], assists=stats['assists'], minutes=stats['minutes'],
                    xg=stats['xg'], xa=stats['xa'], games_starts=stats['games_starts']
                )
                db.add(record)
            updated += 1
        
        db.commit()
        return updated
    except Exception as e:
        logger.error(f"Error syncing competition_stats from matches: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

def fix_missing_minutes_from_matchlogs(player_id: int):
    """Fix missing minutes using match logs (Independent Session)."""
    db = SessionLocal()
    try:
        comp_stats_to_fix = db.query(CompetitionStats).filter(CompetitionStats.player_id == player_id, CompetitionStats.minutes == 0, CompetitionStats.games > 0).all()
        gk_stats_to_fix = db.query(GoalkeeperStats).filter(GoalkeeperStats.player_id == player_id, GoalkeeperStats.minutes == 0, GoalkeeperStats.games > 0).all()
        
        total_to_fix = len(comp_stats_to_fix) + len(gk_stats_to_fix)
        if total_to_fix == 0: return

        fixed_count = 0
        for stat in comp_stats_to_fix:
            try: season_start, season_end = get_season_date_range(stat.season)
            except: continue
            matches = db.query(PlayerMatch).filter(PlayerMatch.player_id == player_id, PlayerMatch.match_date >= season_start, PlayerMatch.match_date <= season_end, PlayerMatch.competition.ilike(f"%{stat.competition_name}%")).all()
            if not matches: continue
            total_minutes = sum(m.minutes_played or 0 for m in matches)
            if total_minutes > 0:
                stat.minutes = total_minutes
                fixed_count += 1
        
        for stat in gk_stats_to_fix:
            try: season_start, season_end = get_season_date_range(stat.season)
            except: continue
            matches = db.query(PlayerMatch).filter(PlayerMatch.player_id == player_id, PlayerMatch.match_date >= season_start, PlayerMatch.match_date <= season_end, PlayerMatch.competition.ilike(f"%{stat.competition_name}%")).all()
            if not matches: continue
            total_minutes = sum(m.minutes_played or 0 for m in matches)
            if total_minutes > 0:
                stat.minutes = total_minutes
                fixed_count += 1
                
        if fixed_count > 0:
            db.commit()
            logger.info(f"✅ Fixed {fixed_count} records with missing minutes!")
    except Exception as e:
        logger.error(f"Error fixing minutes: {e}")
        db.rollback()
    finally:
        db.close()

async def sync_competition_stats(scraper: FBrefPlaywrightScraper, player_info: dict) -> int:
    """Sync competition stats (Safe for Port 6543 - API First, DB Second)."""
    player_id = player_info['id']
    player_name = player_info['name']
    player_api_id = player_info.get('api_id')
    
    logger.info(f"🏆 Syncing competition stats for {player_name}")
    
    # --- FAZA 1: API ---
    try:
        player_data = await scraper.get_player_by_id(player_api_id, player_name)
    except Exception as e:
        logger.error(f"Scraper error: {e}")
        return 0

    if not player_data or not player_data.get('competition_stats'):
        logger.warning("⚠️ No competition stats found")
        return 0

    # --- FAZA 2: BAZA DANYCH ---
    db = SessionLocal()
    try:
        player = db.query(Player).get(player_id)
        if player:
            if player_data.get('team'): player.team = player_data['team']
            if player_data.get('competition_stats'):
                sorted_stats = sorted(player_data['competition_stats'], key=lambda x: x.get('season', ''), reverse=True)
                for stat in sorted_stats:
                    if stat.get('competition_type') == 'LEAGUE':
                        player.league = stat.get('competition_name')
                        if stat.get('squad'): player.team = stat.get('squad')
                        break
            db.add(player)
        
        db.query(CompetitionStats).filter(CompetitionStats.player_id == player_id).delete(synchronize_session=False)
        db.query(GoalkeeperStats).filter(GoalkeeperStats.player_id == player_id).delete(synchronize_session=False)
        
        seen = set()
        deduplicated_stats = []
        for stat_data in player_data['competition_stats']:
            key = (stat_data.get('season'), stat_data.get('competition_name'), stat_data.get('competition_type'))
            if key not in seen:
                seen.add(key)
                deduplicated_stats.append(stat_data)
        
        saved_count = 0
        for stat in deduplicated_stats:
            try:
                is_gk_stat = any(k in stat for k in ['goals_against', 'saves', 'clean_sheets'])
                if is_gk_stat:
                    gk_stat = GoalkeeperStats(
                        player_id=player_id, season=stat.get('season', ''), competition_name=stat.get('competition_name', ''), competition_type=stat.get('competition_type', ''),
                        games=stat.get('games'), games_starts=stat.get('games_starts'), minutes=stat.get('minutes'), goals_against=stat.get('goals_against'),
                        goals_against_per90=stat.get('ga90'), shots_on_target_against=stat.get('sota'), saves=stat.get('saves'), save_percentage=stat.get('save_pct'),
                        wins=stat.get('wins'), draws=stat.get('draws') or stat.get('ties'), losses=stat.get('losses'), clean_sheets=stat.get('clean_sheets'),
                        clean_sheet_percentage=stat.get('clean_sheets_pct'), penalties_attempted=stat.get('pens_att'), penalties_allowed=stat.get('pens_allowed'),
                        penalties_saved=stat.get('pens_saved'), penalties_missed=stat.get('pens_missed'), post_shot_xg=stat.get('psxg')
                    )
                    db.add(gk_stat)
                else:
                    comp_stat = CompetitionStats(
                        player_id=player_id, season=stat.get('season', ''), competition_name=stat.get('competition_name', ''), competition_type=stat.get('competition_type', ''),
                        games=stat.get('games'), games_starts=stat.get('games_starts'), minutes=stat.get('minutes'), goals=stat.get('goals'),
                        assists=stat.get('assists'), penalty_goals=stat.get('penalty_goals'), xg=stat.get('xg'), npxg=stat.get('npxg'),
                        xa=stat.get('xa'), yellow_cards=stat.get('yellow_cards'), red_cards=stat.get('red_cards')
                    )
                    db.add(comp_stat)
                saved_count += 1
            except Exception as e: logger.error(f"❌ Error saving stat: {e}")
            
        db.commit()
        logger.info(f"✅ Saved {saved_count} competition stats")
        return saved_count
    except Exception as e:
        logger.error(f"❌ DB Error in competition stats: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

async def sync_match_logs_for_season(scraper: FBrefPlaywrightScraper, player_info: dict, season: str) -> int:
    """Sync match logs for a specific season (Safe for Port 6543)."""
    player_id = player_info['id']
    player_name = player_info['name']
    api_id = player_info.get('api_id')
    
    logger.info(f"📋 Syncing match logs for {player_name} ({season})")
    
    # --- FAZA 1: API ---
    try:
        match_logs = await scraper.get_player_match_logs(api_id, player_name, season)
    except Exception as e:
        logger.error(f"Scraper error: {e}")
        return 0
        
    if not match_logs:
        logger.warning(f"⚠️ No match logs found for {season}")
        return 0
    
    # --- FAZA 2: BAZA ---
    db = SessionLocal()
    try:
        year_start = int(season.split('-')[0])
        year_end = year_start + 1
        season_start = date(year_start, 7, 1)
        season_end = date(year_end, 6, 30)
        
        db.query(PlayerMatch).filter(PlayerMatch.player_id == player_id, PlayerMatch.match_date >= season_start, PlayerMatch.match_date <= season_end).delete(synchronize_session=False)
        
        saved_count = 0
        skipped_duplicates = 0
        
        for match_data in match_logs:
            try:
                match_date_str = match_data.get('match_date')
                match_date = date.today()
                if match_date_str:
                    try: match_date = datetime.strptime(match_date_str, '%Y-%m-%d').date()
                    except: pass
                
                match = PlayerMatch(
                    player_id=player_id, match_date=match_date, competition=match_data.get('competition', '')[:100], round=match_data.get('round', '')[:50],
                    venue=match_data.get('venue', '')[:50], opponent=match_data.get('opponent', '')[:100], result=match_data.get('result', '')[:20],
                    minutes_played=match_data.get('minutes_played', 0) or 0, goals=match_data.get('goals', 0) or 0, assists=match_data.get('assists', 0) or 0,
                    shots=match_data.get('shots', 0) or 0, shots_on_target=match_data.get('shots_on_target', 0) or 0, xg=float(match_data.get('xg', 0.0) or 0.0),
                    xa=float(match_data.get('xa', 0.0) or 0.0), passes_completed=match_data.get('passes_completed', 0) or 0, passes_attempted=match_data.get('passes_attempted', 0) or 0,
                    touches=match_data.get('touches', 0) or 0, yellow_cards=match_data.get('yellow_cards', 0) or 0, red_cards=match_data.get('red_cards', 0) or 0
                )
                db.add(match)
                # Opcjonalnie flush tutaj jeśli chcesz łapać błędy pojedynczo, 
                # ale dla wydajności commit na koniec jest lepszy.
                # db.flush() 
                saved_count += 1
            except Exception as e:
                if 'uq_player_match' in str(e) or 'UNIQUE constraint' in str(e): skipped_duplicates += 1
                else: logger.error(f"❌ Row error: {e}")

        db.commit()
        if skipped_duplicates > 0: logger.info(f"⚠️ Skipped {skipped_duplicates} duplicate matches")
        logger.info(f"✅ Saved {saved_count} matches for {season}")
        return saved_count
    except Exception as e:
        logger.error(f"❌ DB Error matchlogs: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

async def main():
    parser = argparse.ArgumentParser(description='Sync full player data (competition stats + match logs)')
    parser.add_argument('player_name', help='Player name to sync')
    parser.add_argument('--seasons', nargs='*', help='Specific seasons to sync match logs')
    parser.add_argument('--all-seasons', action='store_true', help='Sync match logs for ALL seasons')
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info(f"FULL SYNC: {args.player_name}")
    logger.info("=" * 80)
    
    player_info = {}
    db_temp = SessionLocal()
    try:
        player = db_temp.query(Player).filter(Player.name.ilike(f"%{args.player_name}%")).first()
        if not player:
            logger.error(f"❌ Player not found: {args.player_name}")
            sys.exit(1)
        player_info = {'id': player.id, 'name': player.name, 'api_id': player.api_id}
        logger.info(f"✅ Found player: {player.name} (ID: {player.id})")
    finally:
        db_temp.close() # SESJA ZAMKNIĘTA

    async with FBrefPlaywrightScraper(headless=True, rate_limit_seconds=12.0) as scraper:
        logger.info("\n" + "=" * 80)
        logger.info("STEP 1: Competition Stats")
        logger.info("=" * 80)
        comp_count = await sync_competition_stats(scraper, player_info)
        
        logger.info("\n" + "=" * 80)
        logger.info("STEP 2: Match Logs")
        logger.info("=" * 80)
        reset_sequences_if_needed()
        
        seasons_to_sync = []
        if args.all_seasons:
            db_check = SessionLocal()
            try:
                stats = db_check.query(CompetitionStats.season).filter(CompetitionStats.player_id == player_info['id']).distinct().all()
                all_seasons = set(s[0] for s in stats if s[0])
                seasons_to_sync = sorted(all_seasons, reverse=True)
            finally: db_check.close()
            logger.info(f"📅 Found {len(seasons_to_sync)} seasons to sync")
        elif args.seasons: seasons_to_sync = args.seasons
        else: seasons_to_sync = ["2025-2026"]
            
        total_matches = 0
        for season in seasons_to_sync:
            matches = await sync_match_logs_for_season(scraper, player_info, season)
            total_matches += matches
            
        logger.info("\n" + "=" * 80)
        logger.info("STEP 3: Aggregation & Fixes")
        logger.info("=" * 80)
        logger.info("🔄 Aggregating competition stats from match logs...")
        sync_competition_stats_from_matches(player_info['id'])
        logger.info("🔧 Fixing missing minutes...")
        fix_missing_minutes_from_matchlogs(player_info['id'])
        
        logger.info("\n" + "=" * 80)
        logger.info(f"✅ SYNC COMPLETE")
        logger.info(f"   Competition Stats: {comp_count}")
        logger.info(f"   Match Logs: {total_matches}")
        logger.info("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())



