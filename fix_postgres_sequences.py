"""
Fix PostgreSQL sequence desynchronization issues
Run this if you encounter "duplicate key value violates unique constraint" errors

Usage: python fix_postgres_sequences.py
"""
import sys
sys.path.append('.')

from sqlalchemy import text
from app.backend.database import SessionLocal

def fix_sequences():
    """Reset all PostgreSQL sequences to match current max IDs"""
    db = SessionLocal()
    try:
        # Check if we're using PostgreSQL
        db_url = str(db.bind.url)
        if 'postgresql' not in db_url and 'postgres' not in db_url:
            print("ℹ️  Not using PostgreSQL - sequences don't need fixing")
            return
        
        print("🔧 Fixing PostgreSQL sequences...")
        
        # Fix competition_stats sequence
        result = db.execute(text("SELECT setval('competition_stats_id_seq', (SELECT COALESCE(MAX(id), 1) FROM competition_stats));"))
        seq_value = list(result)[0][0]
        print(f"✅ competition_stats_id_seq reset to: {seq_value}")
        
        # Fix goalkeeper_stats sequence
        result = db.execute(text("SELECT setval('goalkeeper_stats_id_seq', (SELECT COALESCE(MAX(id), 1) FROM goalkeeper_stats));"))
        seq_value = list(result)[0][0]
        print(f"✅ goalkeeper_stats_id_seq reset to: {seq_value}")
        
        # Fix player_matches sequence
        result = db.execute(text("SELECT setval('player_matches_id_seq', (SELECT COALESCE(MAX(id), 1) FROM player_matches));"))
        seq_value = list(result)[0][0]
        print(f"✅ player_matches_id_seq reset to: {seq_value}")
        
        # Fix players sequence
        result = db.execute(text("SELECT setval('players_id_seq', (SELECT COALESCE(MAX(id), 1) FROM players));"))
        seq_value = list(result)[0][0]
        print(f"✅ players_id_seq reset to: {seq_value}")
        
        db.commit()
        print("\n🎉 All sequences fixed successfully!")
        print("\nYou can now run your sync commands without errors.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_sequences()
