"""
Sync players who don't have data in competition_stats or goalkeeper_stats tables.
This script finds players who were never synced with the new Playwright scraper.
"""
import sqlite3
import subprocess
import time
from datetime import datetime

def get_missing_players():
    """Get list of players without data in new tables."""
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    
    query = """
        SELECT p.id, p.name, p.team, p.league, p.position
        FROM players p
        WHERE NOT EXISTS (
            SELECT 1 FROM competition_stats cs WHERE cs.player_id = p.id
        )
        AND NOT EXISTS (
            SELECT 1 FROM goalkeeper_stats gs WHERE gs.player_id = p.id
        )
        ORDER BY p.name
    """
    
    cursor.execute(query)
    players = cursor.fetchall()
    conn.close()
    
    return players

def main():
    print("=" * 80)
    print("SYNC MISSING PLAYERS - Playwright Scraper")
    print("=" * 80)
    
    players = get_missing_players()
    
    if not players:
        print("\n✅ All players already have data in competition_stats/goalkeeper_stats!")
        return
    
    print(f"\n⚠️ Found {len(players)} players without data in new tables:")
    print("\nPlayers to sync:")
    for player_id, name, team, league, position in players[:10]:  # Show first 10
        print(f"  • {name:30} ({team}, {league})")
    
    if len(players) > 10:
        print(f"  ... and {len(players) - 10} more")
    
    print("\n" + "=" * 80)
    print("OPTIONS:")
    print("=" * 80)
    print("1. Sync ALL missing players (takes ~2-3 hours)")
    print("2. Sync specific player")
    print("3. List all missing players")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n⚠️ This will sync ALL missing players. This takes time!")
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            print(f"\nStarting sync of {len(players)} players...")
            print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            success = 0
            failed = 0
            
            for i, (player_id, name, team, league, position) in enumerate(players, 1):
                print(f"\n[{i}/{len(players)}] Syncing: {name}")
                
                try:
                    result = subprocess.run(
                        ['python', 'sync_playwright.py', name, '--all-seasons'],
                        capture_output=True,
                        text=True,
                        timeout=300  # 5 minutes per player
                    )
                    
                    if result.returncode == 0:
                        print(f"  ✅ Success")
                        success += 1
                    else:
                        print(f"  ❌ Failed")
                        failed += 1
                        
                except subprocess.TimeoutExpired:
                    print(f"  ⏱️ Timeout (skipped)")
                    failed += 1
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    failed += 1
                
                # Rate limiting - wait between players
                if i < len(players):
                    print("  ⏳ Waiting 12 seconds...")
                    time.sleep(12)
            
            print("\n" + "=" * 80)
            print("SYNC COMPLETE")
            print("=" * 80)
            print(f"Success: {success}")
            print(f"Failed: {failed}")
            print(f"Total: {len(players)}")
            print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    elif choice == "2":
        print("\nAvailable players:")
        for i, (player_id, name, team, league, position) in enumerate(players, 1):
            print(f"{i:3}. {name:30} ({team})")
        
        try:
            idx = int(input("\nEnter player number: ").strip()) - 1
            if 0 <= idx < len(players):
                player_id, name, team, league, position = players[idx]
                print(f"\nSyncing: {name}")
                subprocess.run(['python', 'sync_playwright.py', name, '--all-seasons'])
            else:
                print("Invalid number")
        except ValueError:
            print("Invalid input")
    
    elif choice == "3":
        print("\n" + "=" * 80)
        print("ALL MISSING PLAYERS:")
        print("=" * 80)
        for i, (player_id, name, team, league, position) in enumerate(players, 1):
            print(f"{i:3}. {name:30} ({team:25}, {league:20})")
    
    elif choice == "4":
        print("\nExiting...")
    
    else:
        print("\nInvalid choice")

if __name__ == "__main__":
    main()
