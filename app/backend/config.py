from __future__ import annotations
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=False)

class Settings:
    def __init__(self) -> None:
        # Baza danych - Supabase PostgreSQL (wymagane w .env)                                                       │
        self.database_url: str = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise ValueError(
            "❌ DATABASE_URL not found in environment variables!\n"
            "Please set DATABASE_URL in .env file.\n"
            "Example:\n"
            "  DATABASE_URL=postgresql://postgres.xxx:password@aws-1-eu-west-1.pooler.supabase.com:6543/postgres\n"
            "See SUPABASE_GUIDE.md for setup instructions."
        )
        
        # Ustawienia synchronizacji
        self.sync_daily_hour: int = int(os.getenv("SYNC_DAILY_HOUR", "6"))

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

