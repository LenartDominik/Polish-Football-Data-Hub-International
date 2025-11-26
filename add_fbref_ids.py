"""
Script to add FBref IDs for players without api_id in the database.

Usage:
    1. Find FBref IDs on https://fbref.com for each player
    2. Fill in the fbref_ids dictionary below
    3. Run: python add_fbref_ids.py

Author: Polish Football Data Hub International
Date: 2025-11-25
"""

import sqlite3
from pathlib import Path

# ============================================================================
# STEP 1: Fill in FBref IDs for each player
# ============================================================================
# To find FBref ID:
# 1. Go to https://fbref.com/en/search/search.fcgi
# 2. Search for player name
# 3. Open player profile
# 4. Copy ID from URL: https://fbref.com/en/players/XXXXXXXX/Player-Name
#                                                    ^^^^^^^^
#                                                    This is FBref ID

fbref_ids = {
    # Format: player_id_in_database: 'fbref_id'
    
    # ========== PRIORITY 1: Main Squad Players ==========
    57: '',  # Jakub Moder (Feyenoord, MF) - Eredivisie
    52: '',  # Karol Linetty (Kocaelispor, MF) - Süper Lig
    53: '',  # Mateusz Wieteska (Kocaelispor, DF) - Süper Lig
    59: '',  # Paweł Bochniewicz (Heerenveen, DF) - Eredivisie
    60: '',  # Szymon Włodarczyk (Excelsior, FW) - Eredivisie
    
    # ========== PRIORITY 2: Goalkeepers ==========
    48: '',  # Cezary Miszta (Rio Ave, GK) - Primeira Liga
    55: '',  # Mateusz Lis (Göztepe, GK) - Süper Lig
    56: '',  # Albert Posiadała (Samsunspor, GK) - Süper Lig
    58: '',  # Przemysław Tytoń (Twente, GK) - Eredivisie
    61: '',  # Filip Bednarek (Sparta Rotterdam, GK) - Eredivisie
    18: '',  # Jakub Zieliński (Wolfsburg, GK) - U19 Youth (może nie mieć)
    
    # ========== PRIORITY 3: Other Players ==========
    105: '',  # Karol Angielski (AEK Larnaca, FW) - Cyprus
    104: '',  # Piotr Parzyszek (KuPS, FW) - Finland
    102: '',  # Miłosz Trojak (Ulsan HD, DF) - K League
    82: '',   # Bartosz Szywała (Slavia Praga, ?) - Chance Liga
    92: '',   # Daniel Baran (FC Dallas, ?) - MLS
    83: '',   # Eryk Łukaszka (FK Bodø/Glimt II, ?) - Eliteserien (może nie mieć)
    
    # ========== PRIORITY 4: Youth/Uncertain ==========
    7: '',    # Radosław Żelazny (AS Roma, ?) - Serie A (młodzieżówka?)
    103: '',  # Jan Ziółkowski (Roma, DF) - Serie A (młodzieżówka?)
}

# ============================================================================
# Database Configuration
# ============================================================================
DB_PATH = Path(__file__).parent / 'players.db'

# ============================================================================
# Main Script
# ============================================================================

def check_database():
    """Check if database exists"""
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        print("   Make sure you're running this script from the project root directory.")
        return False
    return True


def get_player_info(cursor, player_id):
    """Get player information from database"""
    cursor.execute(
        'SELECT id, name, team, position, league FROM players WHERE id = ?',
        (player_id,)
    )
    return cursor.fetchone()


def update_fbref_id(cursor, player_id, fbref_id):
    """Update FBref ID for a player"""
    cursor.execute(
        'UPDATE players SET api_id = ? WHERE id = ?',
        (fbref_id, player_id)
    )


def main():
    print("=" * 80)
    print("🔧 FBref ID Update Script")
    print("=" * 80)
    print()
    
    # Check database
    if not check_database():
        return
    
    # Count how many IDs to add
    filled_ids = {k: v for k, v in fbref_ids.items() if v}
    empty_ids = {k: v for k, v in fbref_ids.items() if not v}
    
    print(f"📊 Status:")
    print(f"   ✅ FBref IDs filled: {len(filled_ids)}")
    print(f"   ⚠️  FBref IDs missing: {len(empty_ids)}")
    print()
    
    if not filled_ids:
        print("❌ No FBref IDs provided!")
        print()
        print("📝 Instructions:")
        print("   1. Open this file: add_fbref_ids.py")
        print("   2. Find FBref IDs on https://fbref.com")
        print("   3. Fill in the fbref_ids dictionary (lines 20-55)")
        print("   4. Run this script again")
        print()
        print("Example:")
        print("   57: 'abc12345',  # Jakub Moder")
        return
    
    # Confirm before updating
    print(f"🔄 Ready to update {len(filled_ids)} player(s):")
    print()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Show what will be updated
    for player_id, fbref_id in filled_ids.items():
        player_info = get_player_info(cursor, player_id)
        if player_info:
            pid, name, team, position, league = player_info
            pos = position if position else '?'
            team_name = team if team else '?'
            print(f"   {pid:3d}. {name:30s} → {fbref_id}")
        else:
            print(f"   ⚠️  Player ID {player_id} not found in database")
    
    print()
    response = input("Continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("❌ Cancelled.")
        conn.close()
        return
    
    # Update database
    print()
    print("🔄 Updating database...")
    print()
    
    updated_count = 0
    error_count = 0
    
    for player_id, fbref_id in filled_ids.items():
        try:
            player_info = get_player_info(cursor, player_id)
            if player_info:
                pid, name, team, position, league = player_info
                update_fbref_id(cursor, player_id, fbref_id)
                print(f"   ✅ {name:30s} (ID: {pid}) → {fbref_id}")
                updated_count += 1
            else:
                print(f"   ❌ Player ID {player_id} not found")
                error_count += 1
        except Exception as e:
            print(f"   ❌ Error updating player ID {player_id}: {e}")
            error_count += 1
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print()
    print("=" * 80)
    print("✅ Update Complete!")
    print("=" * 80)
    print()
    print(f"📊 Results:")
    print(f"   ✅ Updated: {updated_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   ⚠️  Still missing: {len(empty_ids)}")
    print()
    
    if updated_count > 0:
        print("🔄 Next Steps:")
        print()
        print("   1. Synchronize updated players:")
        print("      python sync_all_playwright.py")
        print()
        print("   2. Or synchronize individual players:")
        for player_id in filled_ids.keys():
            cursor = sqlite3.connect(DB_PATH).cursor()
            player_info = get_player_info(cursor, player_id)
            if player_info:
                _, name, _, _, _ = player_info
                print(f'      python sync_playwright.py "{name}"')
        print()
        print("   3. Check the frontend:")
        print("      streamlit run app/frontend/streamlit_app.py")
        print()
    
    if empty_ids:
        print("⚠️  Still need to add FBref IDs for:")
        cursor = sqlite3.connect(DB_PATH).cursor()
        for player_id in empty_ids.keys():
            player_info = get_player_info(cursor, player_id)
            if player_info:
                pid, name, team, position, league = player_info
                print(f"   {pid:3d}. {name}")
        print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
