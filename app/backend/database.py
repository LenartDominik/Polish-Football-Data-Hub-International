from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import re

# Ensure we use a synchronous DBAPI driver for SQLAlchemy's sync engine.
# If the DATABASE_URL contains an async driver like '+aiosqlite', replace
# it with the synchronous SQLite driver portion so create_engine uses the
# standard DBAPI and doesn't attempt async IO (which triggers greenlet errors).
database_url = settings.database_url
if not database_url:
    raise ValueError(
        "? DATABASE_URL not configured!\n"
        "Please set DATABASE_URL in your .env file.\n"
        "Example: DATABASE_URL=postgresql://user:pass@host:port/db\n"
        "See SUPABASE_GUIDE.md for setup instructions."
    )

# DEBUG: Log connection string format (without password)
def mask_password(url: str) -> str:
    """Mask password in connection string for logging"""
    return re.sub(r'://([^:]+):([^@]+)@', r'://\1:****@', url)

print(f"[DATABASE] Connection URL format: {mask_password(database_url)}")

# Extract and log connection details
if database_url.startswith(('postgresql', 'postgres')):
    match = re.search(r'://([^:]+):([^@]+)@([^:]+):(\d+)/(.+?)(\?|$)', database_url)
    if match:
        username, _, host, port, dbname = match.groups()[:5]
        print(f"[DATABASE] User: {username}")
        print(f"[DATABASE] Host: {host}")
        print(f"[DATABASE] Port: {port}")
        print(f"[DATABASE] Database: {dbname}")
        
        # Check for Transaction Pooler issues
        if port == "6543" and username == "postgres":
            print("⚠️  [DATABASE] WARNING: Using Transaction Pooler (port 6543) with username 'postgres'")
            print("⚠️  [DATABASE] Transaction Pooler usually requires format: postgres.PROJECT_REF")
            print("⚠️  [DATABASE] If authentication fails, check your DATABASE_URL format")
if "+aiosqlite" in database_url:
    database_url = database_url.replace("+aiosqlite", "")

# Detect database type
is_sqlite = database_url.startswith("sqlite")
is_postgresql = database_url.startswith("postgresql") or database_url.startswith("postgres")

# Create engine with appropriate settings
if is_sqlite:
    # SQLite-specific settings
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}  # tylko dla SQLite
    )
elif is_postgresql:
    # PostgreSQL-specific settings
    # Check if using Supabase Transaction Pooler (port 6543 - needs prepared statements disabled)
    connect_args = {}
    if "6543" in database_url or ("supabase.com" in database_url and "pooler" in database_url):
        # Disable prepared statements for Supabase Transaction Pooling (psycopg2)
        # This is required because Transaction Pooler doesn't support PREPARE statements
        connect_args = {"options": "-c statement_timeout=30000"}
    
    engine = create_engine(
        database_url,
        pool_pre_ping=True,  # Test connection before using
        pool_size=10,        # Connection pool size
        max_overflow=20,     # Max connections above pool_size
        echo=False,          # Set to True for SQL debugging
        connect_args=connect_args,
        # Disable statement caching for Transaction Pooler compatibility
        execution_options={"statement_cache_size": 0} if "6543" in database_url else {}
    )
else:
    # Default (other databases)
    engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


