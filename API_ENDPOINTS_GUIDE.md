# 📚 API Endpoints Guide - Polish Players Tracker

## 📊 Data Source & Attribution

All player statistics are sourced from **[FBref.com](https://fbref.com/)** (Sports Reference LLC).

**Disclaimer:** This project is independent and not affiliated with FBref.com. For official statistics, visit [FBref.com](https://fbref.com/)

See `LICENSE` and `CREDITS.md` for full attribution details.

---

## 🌐 Dostęp do Dokumentacji

### Swagger UI (Interaktywna)
```
http://localhost:8000/docs
```
- Interaktywne testowanie API
- "Try it out" dla każdego endpointa
- Automatyczna walidacja
- Przykładowe requesty/responses
- **Zawiera FBref attribution** w opisie API

### ReDoc (Czytelna)
```
http://localhost:8000/redoc
```
- Czytelna dokumentacja
- Pełne schematy danych
- Exportable jako HTML
- **Zawiera FBref attribution** w opisie API

## 📋 Wszystkie Endpointy

### 🏠 Root & Health

#### `GET /`
Informacje o API, wersja, features, scheduler status, **FBref attribution**
```json
{
  "message": "🇵🇱 Welcome to Polish Players Tracker API",
  "version": "0.6.0",
  "data_source": {
    "name": "FBref.com",
    "provider": "Sports Reference LLC",
    "url": "https://fbref.com/",
    "attribution": "All player statistics sourced from FBref.com",
    "disclaimer": "This project is independent and not affiliated with FBref.com"
  },
  "scheduler": {
    "enabled": true,
    "stats_sync_schedule": "Monday & Thursday at 06:00",
    "matchlogs_sync_schedule": "Tuesday at 07:00",
    "next_stats_sync": "2025-01-27 06:00:00+01:00",
    "next_matchlogs_sync": "2025-01-28 07:00:00+01:00"
  }
}
```

#### `GET /health`
Health check dla monitoringu
```json
{
  "status": "ok",
  "timestamp": "2025-01-28T10:00:00",
  "scheduler_running": true
}
```

---

### 👤 Players

#### `GET /api/players`
Lista wszystkich graczy
- **Query params:**
  - `skip` (int): Offset dla paginacji
  - `limit` (int): Liczba wyników

#### `GET /api/players/{player_id}`
Szczegóły gracza
- **Path param:** `player_id` (int)
- **Response:** Pełne dane gracza + statystyki

#### `POST /api/players`
Dodaj nowego gracza
- **Body:**
```json
{
  "name": "Robert Lewandowski",
  "team": "FC Barcelona",
  "league": "La Liga",
  "position": "FW",
  "is_goalkeeper": false
}
```

#### `PUT /api/players/{player_id}`
Aktualizuj gracza
- **Path param:** `player_id` (int)
- **Body:** Dane do aktualizacji

#### `DELETE /api/players/{player_id}`
Usuń gracza
- **Path param:** `player_id` (int)

---

### 📊 Statistics

#### `GET /api/players/{player_id}/competition-stats`
Statystyki rozbite na rozgrywki
- **Path param:** `player_id` (int)
- **Response:** Liga, Puchary Europejskie, Reprezentacja

#### `GET /api/players/{player_id}/goalkeeper-stats`
Statystyki bramkarskie (tylko dla bramkarzy)
- **Path param:** `player_id` (int)
- **Response:** Obrony, czyste konta, save %

---

### 📋 Matchlogs (NOWE w v0.6.0)

#### `GET /api/matchlogs/{player_id}`
Wszystkie mecze gracza
- **Path param:** `player_id` (int)
- **Query params:**
  - `season` (str): Filtruj po sezonie (np. "2025-2026")
  - `competition` (str): Filtruj po rozgrywkach
  - `limit` (int): Liczba wyników
  - `offset` (int): Offset dla paginacji

**Przykład:**
```
GET /api/players/1/matches?season=2025-2026&limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "player_id": 1,
    "match_date": "2025-01-20",
    "competition": "La Liga",
    "opponent": "Real Madrid",
    "result": "W 2-1",
    "venue": "Home",
    "minutes_played": 90,
    "goals": 1,
    "assists": 1,
    "xg": 0.8,
    "xa": 0.5,
    "shots": 5,
    "shots_on_target": 3,
    "passes_completed": 45,
    "passes_attempted": 52,
    "tackles": 2,
    "yellow_cards": 0
  }
]
```

#### `GET /api/matchlogs/{player_id}/summary`
Podsumowanie statystyk z meczów
- **Path param:** `player_id` (int)
- **Query params:**
  - `season` (str): Filtruj po sezonie

**Response:**
```json
{
  "total_matches": 28,
  "total_goals": 25,
  "total_assists": 8,
  "total_minutes": 2340,
  "avg_goals_per_match": 0.89,
  "avg_assists_per_match": 0.29,
  "total_xg": 22.5,
  "total_xa": 7.2,
  "total_shots": 140,
  "shot_accuracy": 0.45,
  "pass_completion": 0.87
}
```

---

### ⚖️ Comparison

#### `GET /api/comparison/compare`
Porównaj dwóch graczy
- **Query params:**
  - `player1_id` (int): ID pierwszego gracza
  - `player2_id` (int): ID drugiego gracza

**Przykład:**
```
GET /api/comparison/compare?player1_id=1&player2_id=2
```

---

### 🏟️ Matches (Live - w budowie)

#### `GET /api/matches/live`
Mecze na żywo (feature w budowie)

---

## 🔧 Konfiguracja

### Włączenie Schedulera

Aby scheduler działał automatycznie:

```bash
# W pliku .env
ENABLE_SCHEDULER=true
SCHEDULER_TIMEZONE=Europe/Warsaw
```

### Email Notifications

```bash
# W pliku .env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=recipient@example.com
```

---

## 📅 Scheduler Jobs

### Job #1: Stats Sync
- **Trigger:** Poniedziałek i Czwartek o 6:00
- **Czas trwania:** ~20-30 minut (dla 100+ graczy)
- **Co robi:** Synchronizuje statystyki sezonowe
- **Email:** Wysyła raport z zielonym headerem

### Job #2: Matchlogs Sync (NOWY)
- **Trigger:** Wtorek o 7:00
- **Czas trwania:** ~20-30 minut (dla 100+ graczy)
- **Co robi:** Synchronizuje szczegółowe logi meczowe
- **Email:** Wysyła raport z niebieskim headerem

---

## 🧪 Testowanie API

### Przez Swagger UI

1. Otwórz: http://localhost:8000/docs
2. Znajdź endpoint (np. `GET /api/players`)
3. Kliknij "Try it out"
4. Wprowadź parametry
5. Kliknij "Execute"
6. Zobacz response

### Przez cURL

```bash
# Lista graczy
curl http://localhost:8000/api/players

# Pojedynczy gracz
curl http://localhost:8000/api/players/1

# Matchlogi gracza
curl http://localhost:8000/api/players/1/matches

# Scheduler status
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health
```

### Przez Python

```python
import requests

# Lista graczy
response = requests.get("http://localhost:8000/api/players")
players = response.json()

# Matchlogi
response = requests.get("http://localhost:8000/api/players/1/matches?limit=10")
matches = response.json()

# Scheduler info
response = requests.get("http://localhost:8000/")
info = response.json()
print(info["scheduler"])
```

---

## 📊 Schematy Danych

### Player Schema
```json
{
  "id": 1,
  "name": "Robert Lewandowski",
  "team": "FC Barcelona",
  "league": "La Liga",
  "position": "FW",
  "is_goalkeeper": false,
  "api_id": "8d78e732",
  "last_updated": "2025-01-28"
}
```

### CompetitionStats Schema
```json
{
  "id": 1,
  "player_id": 1,
  "season": "2025-2026",
  "competition_type": "LEAGUE",
  "competition_name": "La Liga",
  "games": 20,
  "goals": 18,
  "assists": 5,
  "xg": 16.5,
  "xa": 4.8,
  "minutes": 1800,
  "yellow_cards": 2,
  "red_cards": 0
}
```

### PlayerMatch Schema (matchlogs)
```json
{
  "id": 1,
  "player_id": 1,
  "match_date": "2025-01-20",
  "competition": "La Liga",
  "round": "Matchweek 20",
  "venue": "Home",
  "opponent": "Real Madrid",
  "result": "W 2-1",
  "minutes_played": 90,
  "goals": 1,
  "assists": 1,
  "shots": 5,
  "shots_on_target": 3,
  "xg": 0.8,
  "xa": 0.5,
  "passes_completed": 45,
  "passes_attempted": 52,
  "pass_completion_pct": 86.5,
  "key_passes": 3,
  "tackles": 2,
  "interceptions": 1,
  "blocks": 0,
  "touches": 65,
  "dribbles_completed": 4,
  "carries": 25,
  "fouls_committed": 1,
  "fouls_drawn": 3,
  "yellow_cards": 0,
  "red_cards": 0
}
```

---

## 🎯 Best Practices

### 1. Paginacja
Zawsze używaj `limit` i `offset` dla dużych list:
```
GET /api/players?limit=20&offset=0
```

### 2. Filtrowanie
Używaj query params do filtrowania:
```
GET /api/players/1/matches?season=2025-2026&competition=La Liga
```

### 3. Error Handling
API zwraca standardowe kody HTTP:
- `200` - OK
- `201` - Created
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

### 4. Rate Limiting
- Scheduler używa 12s między requestami do FBref
- API nie ma rate limitów (dla użytkowników)

---

## 🔗 Przydatne Linki

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **Root Info:** http://localhost:8000/

---

## 📚 Więcej Dokumentacji

- **README:** `README.md` - Main documentation (includes FBref attribution)
- **LICENSE:** `LICENSE` - MIT License + Data Attribution
- **CREDITS:** `CREDITS.md` - Full FBref attribution + tech stack
- **Matchlogs Scheduler:** `MATCHLOGS_SCHEDULER.md`
- **Quick Start:** `QUICKSTART_MATCHLOGS.md`
- **Email Setup:** `EMAIL_SETUP_GUIDE.md`
- **Deployment:** `RENDER_DEPLOYMENT.md`
- **Stack:** `STACK.md`

---

## 📊 Data Attribution

All player statistics in this API are sourced from **[FBref.com](https://fbref.com/)** (Sports Reference LLC).

**Our commitment:**
- ✅ Rate Limiting: 12-second delay between requests
- ✅ Clear Attribution: FBref credited in UI, API, and documentation
- ✅ Non-Commercial: Educational/portfolio project
- ✅ Respectful Scraping: Following best practices and ToS

**Disclaimer:** Independent project, not affiliated with FBref.com

---

**Version:** 0.6.0  
**Last Updated:** 2025-01-23 (FBref attribution added)

