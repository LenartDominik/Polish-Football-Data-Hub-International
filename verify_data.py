from app.backend.database import SessionLocal
from app.backend.models.competition_stats import CompetitionStats
from app.backend.models.player import Player
from app.backend.models.player_match import PlayerMatch
from sqlalchemy import func

def verify_lewandowski():
    db = SessionLocal()
    try:
        player = db.query(Player).filter(Player.name.ilike("%Lewandowski%")).first()
        if not player:
            print("❌ Player Lewandowski not found")
            return

        print(f"✅ Player: {player.name} (ID: {player.id})")
        
        # 1. Check Matches (Source of Truth)
        matches = db.query(PlayerMatch).filter(
            PlayerMatch.player_id == player.id,
            PlayerMatch.match_date >= '2025-07-01'
        ).order_by(PlayerMatch.match_date.desc()).all()
        
        print(f"\n📊 Match Logs (Season 2025-26): Found {len(matches)} matches")
        if matches:
            print(f"   Latest Match: {matches[0].match_date} vs {matches[0].opponent} ({matches[0].competition})")
            total_goals = sum(m.goals or 0 for m in matches)
            total_assists = sum(m.assists or 0 for m in matches)
            print(f"   Total Calculated from Matches: {total_goals} Goals, {total_assists} Assists")
        else:
            print("   ⚠️ No matches found for current season!")

        # 2. Check Competition Stats (Aggregated Data)
        stats = db.query(CompetitionStats).filter(
            CompetitionStats.player_id == player.id,
            CompetitionStats.season.in_(['2025-2026', '2025', '2025/2026'])
        ).all()
        
        print(f"\n🏆 Competition Stats Table:")
        if not stats:
            print("   ⚠️ No competition stats found for 2025-2026")
        for s in stats:
            print(f"   ► [{s.competition_type}] '{s.competition_name}' (Season: {s.season})")
            print(f"       Games: {s.games} | Goals: {s.goals} | Assists: {s.assists} | Mins: {s.minutes}")
            print(f"       Last Updated: (check DB timestamp if available)")

    except Exception as e:
        with open("verify_error.txt", "w", encoding="utf-8") as f:
            f.write(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    # Redirect stdout to a file manually
    with open("verify_output.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        verify_lewandowski()

