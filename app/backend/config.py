from __future__ import annotations
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=False)

class Settings:
    def __init__(self) -> None:
        # Baza danych
        # Dla Render.com: używaj /app/data/players.db (persistent disk)
        # Lokalnie: używaj ./players.db
        default_db = "sqlite:///./players.db"
        
        # Jeśli jesteśmy na Render (sprawdź czy katalog /app/data istnieje)
        if os.path.exists("/app/data"):
            default_db = "sqlite:////app/data/players.db"
        
        self.database_url: str = (
            os.getenv("DATABASE_URL") or os.getenv("database_url") or default_db
        )
        
        # Ustawienia synchronizacji
        self.sync_daily_hour: int = int(os.getenv("SYNC_DAILY_HOUR", "6"))
        self.sync_live_interval_minutes: int = int(os.getenv("SYNC_LIVE_INTERVAL_MINUTES", "5"))
        
        # Timezone dla schedulera (domyślnie Europe/Warsaw)
        self.scheduler_timezone: str = os.getenv("SCHEDULER_TIMEZONE", "Europe/Warsaw")

        # --- NOWA SEKCJA: Konfiguracja Email (SMTP) ---
        self.smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
        # Port musi być liczbą (int), domyślnie 587 dla TLS
        self.smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
        # User i Hasło zazwyczaj nie mają wartości domyślnej - jeśli brak w .env, będą puste
        self.smtp_user: str = os.getenv("SMTP_USER", "")
        self.smtp_password: str = os.getenv("SMTP_PASSWORD", "")
        
        self.email_from: str = os.getenv("EMAIL_FROM", "")
        self.email_to: str = os.getenv("EMAIL_TO", "")

settings = Settings()

