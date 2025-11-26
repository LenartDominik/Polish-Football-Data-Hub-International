"""
PostgreSQL Configuration Helper
Pomocnik do konfiguracji PostgreSQL dla komercyjnego deploymentu
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

def test_postgresql_connection(database_url: str = None):
    """
    Test PostgreSQL connection
    
    Args:
        database_url: PostgreSQL connection string
                      Format: postgresql://user:password@host:port/database
    """
    if not database_url:
        database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("💡 Set it in .env file:")
        print("   DATABASE_URL=postgresql://user:password@host:port/database")
        return False
    
    print("🔍 Testing PostgreSQL connection...")
    print(f"📍 Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'localhost'}")
    
    try:
        # Create engine with connection pooling disabled for test
        engine = create_engine(
            database_url,
            poolclass=NullPool,
            echo=False
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"📊 PostgreSQL version: {version[:50]}...")
            
            # Check if tables exist
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result]
            
            if tables:
                print(f"📋 Found {len(tables)} tables:")
                for table in tables:
                    print(f"   - {table}")
            else:
                print("⚠️  No tables found. Run migrations:")
                print("   alembic upgrade head")
            
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check DATABASE_URL format:")
        print("   postgresql://user:password@host:port/database")
        print("2. Check if PostgreSQL server is running")
        print("3. Check if firewall allows connection")
        print("4. Check username/password")
        return False


def migrate_sqlite_to_postgresql(sqlite_path: str = "players.db", postgres_url: str = None):
    """
    Migrate data from SQLite to PostgreSQL
    
    Args:
        sqlite_path: Path to SQLite database file
        postgres_url: PostgreSQL connection string
    """
    print("🔄 Starting migration from SQLite to PostgreSQL...")
    
    if not os.path.exists(sqlite_path):
        print(f"❌ SQLite database not found: {sqlite_path}")
        return False
    
    if not postgres_url:
        postgres_url = os.getenv("DATABASE_URL")
    
    if not postgres_url:
        print("❌ DATABASE_URL not set")
        return False
    
    try:
        from app.backend.models.player import Player
        from app.backend.models.competition_stats import CompetitionStats
        from app.backend.models.goalkeeper_stats import GoalkeeperStats
        from sqlalchemy.orm import sessionmaker
        
        # SQLite connection
        sqlite_engine = create_engine(f"sqlite:///{sqlite_path}")
        SQLiteSession = sessionmaker(bind=sqlite_engine)
        sqlite_db = SQLiteSession()
        
        # PostgreSQL connection
        postgres_engine = create_engine(postgres_url)
        PostgresSession = sessionmaker(bind=postgres_engine)
        postgres_db = PostgresSession()
        
        # Migrate players
        print("\n📊 Migrating players...")
        players = sqlite_db.query(Player).all()
        print(f"   Found {len(players)} players")
        
        for player in players:
            # Check if player exists in PostgreSQL
            existing = postgres_db.query(Player).filter(
                Player.name == player.name
            ).first()
            
            if not existing:
                postgres_db.add(Player(
                    name=player.name,
                    team=player.team,
                    league=player.league,
                    position=player.position,
                    nationality=player.nationality,
                    api_id=player.api_id,
                    last_updated=player.last_updated
                ))
        
        postgres_db.commit()
        print(f"   ✅ Migrated {len(players)} players")
        
        # Migrate competition stats
        print("\n📊 Migrating competition stats...")
        stats = sqlite_db.query(CompetitionStats).all()
        print(f"   Found {len(stats)} competition stats records")
        
        for stat in stats:
            postgres_db.add(CompetitionStats(
                player_id=stat.player_id,
                season=stat.season,
                competition_type=stat.competition_type,
                competition_name=stat.competition_name,
                games=stat.games,
                games_starts=stat.games_starts,
                minutes=stat.minutes,
                goals=stat.goals,
                assists=stat.assists,
                xg=stat.xg,
                xa=stat.xa,
                yellow_cards=stat.yellow_cards,
                red_cards=stat.red_cards
            ))
        
        postgres_db.commit()
        print(f"   ✅ Migrated {len(stats)} competition stats")
        
        # Migrate goalkeeper stats
        print("\n📊 Migrating goalkeeper stats...")
        gk_stats = sqlite_db.query(GoalkeeperStats).all()
        print(f"   Found {len(gk_stats)} goalkeeper stats records")
        
        for stat in gk_stats:
            postgres_db.add(GoalkeeperStats(
                player_id=stat.player_id,
                season=stat.season,
                competition_type=stat.competition_type,
                competition_name=stat.competition_name,
                games=stat.games,
                games_starts=stat.games_starts,
                minutes=stat.minutes,
                goals_against=stat.goals_against,
                goals_against_per90=stat.goals_against_per90,
                shots_on_target_against=stat.shots_on_target_against,
                saves=stat.saves,
                save_percentage=stat.save_percentage,
                clean_sheets=stat.clean_sheets,
                clean_sheet_percentage=stat.clean_sheet_percentage,
                wins=stat.wins,
                draws=stat.draws,
                losses=stat.losses,
                penalties_attempted=stat.penalties_attempted,
                penalties_allowed=stat.penalties_allowed,
                penalties_saved=stat.penalties_saved,
                penalties_missed=stat.penalties_missed,
                post_shot_xg=stat.post_shot_xg
            ))
        
        postgres_db.commit()
        print(f"   ✅ Migrated {len(gk_stats)} goalkeeper stats")
        
        print("\n✅ Migration completed successfully!")
        print(f"📊 Total records migrated:")
        print(f"   - {len(players)} players")
        print(f"   - {len(stats)} competition stats")
        print(f"   - {len(gk_stats)} goalkeeper stats")
        
        sqlite_db.close()
        postgres_db.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_backup(database_url: str = None, output_file: str = "backup.sql"):
    """
    Create PostgreSQL backup using pg_dump
    
    Args:
        database_url: PostgreSQL connection string
        output_file: Output backup file path
    """
    if not database_url:
        database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not set")
        return False
    
    print(f"💾 Creating backup to {output_file}...")
    
    # Parse connection string
    # Format: postgresql://user:password@host:port/database
    import re
    match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', database_url)
    
    if not match:
        print("❌ Invalid DATABASE_URL format")
        return False
    
    user, password, host, port, database = match.groups()
    
    # Use pg_dump
    import subprocess
    
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    cmd = [
        'pg_dump',
        '-h', host,
        '-p', port,
        '-U', user,
        '-d', database,
        '-f', output_file,
        '--no-owner',
        '--no-acl'
    ]
    
    try:
        subprocess.run(cmd, env=env, check=True)
        print(f"✅ Backup created: {output_file}")
        return True
    except FileNotFoundError:
        print("❌ pg_dump not found. Install PostgreSQL client tools:")
        print("   Ubuntu: sudo apt-get install postgresql-client")
        print("   Mac: brew install postgresql")
        print("   Windows: Install from https://www.postgresql.org/download/")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Backup failed: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    print("🐘 PostgreSQL Configuration Helper")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            # Test connection
            test_postgresql_connection()
            
        elif command == "migrate":
            # Migrate from SQLite
            sqlite_path = sys.argv[2] if len(sys.argv) > 2 else "players.db"
            migrate_sqlite_to_postgresql(sqlite_path)
            
        elif command == "backup":
            # Create backup
            output = sys.argv[2] if len(sys.argv) > 2 else "backup.sql"
            create_backup(output_file=output)
            
        else:
            print(f"❌ Unknown command: {command}")
            print("\nAvailable commands:")
            print("  python config_postgres.py test          - Test PostgreSQL connection")
            print("  python config_postgres.py migrate       - Migrate from SQLite to PostgreSQL")
            print("  python config_postgres.py backup        - Create PostgreSQL backup")
    else:
        # Interactive mode
        print("\n1. Test PostgreSQL connection")
        print("2. Migrate from SQLite to PostgreSQL")
        print("3. Create PostgreSQL backup")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == "1":
            test_postgresql_connection()
        elif choice == "2":
            sqlite_path = input("SQLite database path (default: players.db): ") or "players.db"
            migrate_sqlite_to_postgresql(sqlite_path)
        elif choice == "3":
            output = input("Backup file name (default: backup.sql): ") or "backup.sql"
            create_backup(output_file=output)
        elif choice == "4":
            print("👋 Bye!")
        else:
            print("❌ Invalid option")
