from api_client import APIClient
import pandas as pd
import os

# Mock streamlit secrets for local test if needed, or rely on localhost default
client = APIClient("http://localhost:8000")

print("--- Testing API Client ---")
try:
    # 1. Get Players to find Lewandowski
    print("Fetching players...")
    players_df = client.get_all_players()
    
    if players_df.empty:
        print("❌ No players returned!")
        exit()
        
    lewy = players_df[players_df['name'].str.contains("Lewandowski", case=False)]
    
    if lewy.empty:
        print("❌ Lewandowski not found in players list")
        exit()
        
    pid = lewy.iloc[0]['id']
    print(f"✅ Found Lewandowski: ID {pid}")
    
    # 2. Get Competition Stats
    print(f"Fetching competition stats for ID {pid}...")
    stats_df = client.get_competition_stats(pid)
    
    if stats_df.empty:
        print("⚠️ Returned DataFrame is empty!")
    else:
        print(f"✅ Got {len(stats_df)} rows")
        print("\nColumns:", stats_df.columns.tolist())
        print("\nSeason filter check:")
        filters = ['2025-2026', '2025', '2025/2026']
        print(f"Filters: {filters}")
        
        # Normalize checks
        stats_df['season_str'] = stats_df['season'].astype(str).str.strip()
        stats_df['type_str'] = stats_df['competition_type'].astype(str).str.strip().str.upper()
        
        matches = stats_df[stats_df['season_str'].isin(filters)]
        print(f"\nMatching Rows for 2025-2026: {len(matches)}")
        print(matches[['season', 'competition_name', 'competition_type']].to_string())

except Exception as e:
    print(f"❌ Error: {e}")
