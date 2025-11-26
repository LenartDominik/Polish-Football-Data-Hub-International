# 🚀 Quick Start - Matchlogs Scheduler

## ⚡ 3-minutowy start

### 1️⃣ Włącz Scheduler

Dodaj do `.env`:
```bash
ENABLE_SCHEDULER=true
```

### 2️⃣ Uruchom Backend

```bash
cd polish-players-tracker
python -m uvicorn app.backend.main:app --reload
```

### 3️⃣ Sprawdź Status

Otwórz: http://localhost:8000/

Szukaj sekcji:
```json
{
  "scheduler": {
    "enabled": true,
    "matchlogs_sync_schedule": "Tuesday at 07:00 (Europe/Warsaw)",
    "next_matchlogs_sync": "2025-01-28 07:00:00+01:00"
  }
}
```

✅ Jeśli widzisz powyższe - scheduler jest gotowy!

## 🧪 Test Manualny (opcjonalnie)

Jeśli nie chcesz czekać do wtorku, przetestuj ręcznie:

```bash
python sync_match_logs.py "Robert Lewandowski"
```

Powinieneś zobaczyć:
```
============================================================
SYNC MATCH LOGS: Robert Lewandowski
Season: 2025-2026
============================================================
✅ Found player: Robert Lewandowski (ID: 1)
📊 Found 28 matches
✅ Saved 28 matches for Robert Lewandowski
============================================================
✅ SUCCESS: Synced 28 matches
============================================================
```

## 📧 Email Notifications (opcjonalnie)

Dodaj do `.env`:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=twoj-email@gmail.com
SMTP_PASSWORD=twoje-app-password
EMAIL_FROM=twoj-email@gmail.com
EMAIL_TO=odbiorca@example.com
```

💡 **Dla Gmail:** Użyj App Password zamiast zwykłego hasła
   (Google Account → Security → 2-Step Verification → App passwords)

## 📊 Sprawdź Dane

### API Endpoint
```bash
# Wszystkie mecze gracza
curl http://localhost:8000/api/players/1/matches

# Ostatnie 10 meczów
curl http://localhost:8000/api/players/1/matches?limit=10

# Podsumowanie
curl http://localhost:8000/api/players/1/matches/summary
```

### Swagger UI
Otwórz: http://localhost:8000/docs

Znajdź endpoint: `GET /api/players/{player_id}/matches`

Kliknij "Try it out" i testuj!

## ⏰ Kiedy Działa Scheduler?

| Job | Dni | Godzina | Co robi |
|-----|-----|---------|---------|
| **Stats Sync** | Poniedziałek, Czwartek | 06:00 | Synchronizuje statystyki graczy |
| **Matchlogs Sync** | **Wtorek** | **07:00** | Synchronizuje szczegółowe logi meczów |

## 🐛 Problem? Sprawdź:

### Scheduler nie działa
```bash
# Sprawdź logi
tail -f logs/app.log

# Upewnij się że ENABLE_SCHEDULER=true
echo $ENABLE_SCHEDULER
```

### Brak matchlogs
```bash
# Sprawdź czy gracz ma FBref ID
curl http://localhost:8000/api/players/1

# Jeśli api_id lub fbref_id jest puste:
python sync_playwright.py "Nazwa Gracza"
```

### Email nie przychodzi
1. Sprawdź konfigurację SMTP w `.env`
2. Dla Gmail użyj App Password
3. Sprawdź spam folder
4. Scheduler działa bez emaila - to opcjonalne!

## 🎉 Gotowe!

Twój system automatycznie będzie:
- 📊 Pobierać statystyki 2x w tygodniu (pon/czw)
- 📋 Pobierać matchlogi 1x w tygodniu (wt)
- 📧 Wysyłać raporty email
- ⚡ Respektować rate limiting (12s)

**Więcej informacji:** Zobacz `MATCHLOGS_SCHEDULER.md` dla pełnej dokumentacji.

---

**Made with ❤️ for Polish football fans**
