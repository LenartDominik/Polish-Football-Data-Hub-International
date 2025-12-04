# ?? Polish Football Data Hub International - Complete API Reference

**Version:** 0.7.4
**Base URL:** `http://localhost:8000` (development) or `https://your-domain.com` (production)

---

## ?? Table of Contents

1. [Players Endpoints](#players-endpoints)
2. [Comparison Endpoints](#comparison-endpoints)
3. [Match Logs Endpoints](#match-logs-endpoints)
4. [Root & Health Endpoints](#root--health-endpoints)

---

## ?? Players Endpoints

**Prefix:** `/api/players`
**Tag:** `players`

### GET /api/players

Lista wszystkich graczy w bazie danych.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Robert Lewandowski",
    "team": "Barcelona",
    "league": "La Liga",
    "position": "Forward",
    "age": 35,
    "nationality": "Poland",
    "is_goalkeeper": false
  }
]
```

### GET /api/players/{player_id}

Szczegó³y konkretnego gracza.

**Parameters:**
- `player_id` (path, integer, required) - ID gracza

**Response:** Obiekt gracza z pe³nymi danymi.

### GET /api/players/stats/competition

Wszystkie statystyki z tabeli `competition_stats`.

**Response:** Lista wszystkich rekordów competition_stats (Liga, Puchary, etc.)

### GET /api/players/stats/goalkeeper

Wszystkie statystyki z tabeli `goalkeeper_stats`.

**Response:** Lista wszystkich rekordów goalkeeper_stats (tylko bramkarze).

### GET /api/players/stats/matches

Wszystkie mecze z tabeli `player_matches`.

**Response:** Lista wszystkich meczów wszystkich graczy.

---

## ?? Comparison Endpoints

**Prefix:** `/api/comparison`
**Tag:** `comparison`

### GET /api/comparison/players/{player_id}/stats

Statystyki pojedynczego gracza (przydatne przed porównaniem).

**Parameters:**
- `player_id` (path, integer, required) - ID gracza
- `season` (query, string, optional) - Sezon (np. "2025-2026")

**Response:** Statystyki gracza z wszystkich rozgrywek w danym sezonie.

### GET /api/comparison/compare

Porównanie dwóch graczy.

**Parameters:**
- `player1_id` (query, integer, required) - ID pierwszego gracza
- `player2_id` (query, integer, required) - ID drugiego gracza
- `season` (query, string, optional) - Sezon do porównania
- `stats` (query, array[string], optional) - Lista statystyk do porównania

**Important:** 
- Bramkarze mog¹ byæ porównywani tylko z bramkarzami
- Zawodnicy pola mog¹ byæ porównywani tylko z zawodnikami pola

**Response:**
```json
{
  "player1": {
    "id": 5,
    "name": "Robert Lewandowski",
    "position": "Forward",
    "team": "Barcelona",
    "league": "La Liga",
    "matches": 20,
    "goals": 18,
    "assists": 7,
    "xG": 19.5,
    "xA": 6.8,
    "G+A_per_90": 1.28
  },
  "player2": {
    "id": 8,
    "name": "Piotr Zieliñski",
    "position": "Midfielder",
    "team": "Inter",
    "league": "Serie A",
    "matches": 22,
    "goals": 5,
    "assists": 8,
    "xG": 4.2,
    "xA": 7.1,
    "G+A_per_90": 0.59
  },
  "comparison_date": "2025-01-XX...",
  "player_type": "field_player"
}
```

### GET /api/comparison/available-stats

Lista dostêpnych statystyk do porównania.

**Parameters:**
- `player_type` (query, string, optional) - "goalkeeper" lub "field_player"

**Response:** Zwraca listê dostêpnych metryk dla danego typu gracza.

---

## ?? Match Logs Endpoints

**Prefix:** `/api/matchlogs`
**Tag:** `matchlogs`

### GET /api/matchlogs/{player_id}

Lista wszystkich meczów gracza z opcjonalnymi filtrami.

**Parameters:**
- `player_id` (path, integer, required) - ID gracza
- `season` (query, string, optional) - Filtr sezonu (np. "2025-2026")
- `competition` (query, string, optional) - Filtr rozgrywek (np. "La Liga")
- `limit` (query, integer, optional, default: 100) - Maksymalna liczba wyników

**Example:**
```bash
GET /api/matchlogs/5?season=2025-2026&competition=La%20Liga&limit=20
```

**Response:**
```json
{
  "player_id": 5,
  "player_name": "Robert Lewandowski",
  "total_matches": 20,
  "filters": {
    "season": "2025-2026",
    "competition": "La Liga"
  },
  "matches": [
    {
      "id": 123,
      "date": "2025-01-15",
      "competition": "La Liga",
      "round": "Matchweek 19",
      "venue": "Home",
      "opponent": "Real Madrid",
      "result": "W 3-1",
      "minutes_played": 90,
      "goals": 2,
      "assists": 1,
      "shots": 5,
      "shots_on_target": 4,
      "xg": 1.8,
      "xa": 0.4,
      "passes_completed": 45,
      "passes_attempted": 52,
      "pass_completion_pct": 86.5,
      "key_passes": 3,
      "tackles": 1,
      "interceptions": 0,
      "blocks": 0,
      "touches": 67,
      "dribbles_completed": 2,
      "carries": 35,
      "fouls_committed": 1,
      "fouls_drawn": 2,
      "yellow_cards": 0,
      "red_cards": 0
    }
  ]
}
```

### GET /api/matchlogs/{player_id}/stats

Statystyki agregowane (sumy i œrednie) z wszystkich meczów gracza.

**Parameters:**
- `player_id` (path, integer, required) - ID gracza
- `season` (query, string, optional) - Filtr sezonu
- `competition` (query, string, optional) - Filtr rozgrywek

**Example:**
```bash
GET /api/matchlogs/5/stats?season=2025-2026
```

**Response:**
```json
{
  "player_id": 5,
  "player_name": "Robert Lewandowski",
  "filters": {
    "season": "2025-2026",
    "competition": null
  },
  "summary": {
    "total_matches": 20,
    "total_minutes": 1755,
    "total_goals": 18,
    "total_assists": 7,
    "total_shots": 98,
    "total_shots_on_target": 67,
    "total_xg": 19.5,
    "total_xa": 6.8,
    "total_yellow_cards": 2,
    "total_red_cards": 0,
    "avg_minutes_per_match": 87.8,
    "avg_goals_per_match": 0.9,
    "avg_assists_per_match": 0.35
  }
}
```

### GET /api/matchlogs/match/{match_id}

Szczegó³owe informacje o pojedynczym meczu.

**Parameters:**
- `match_id` (path, integer, required) - ID meczu

**Example:**
```bash
GET /api/matchlogs/match/123
```

**Response:**
```json
{
  "match_id": 123,
  "player": {
    "id": 5,
    "name": "Robert Lewandowski",
    "team": "Barcelona"
  },
  "match_info": {
    "date": "2025-01-15",
    "competition": "La Liga",
    "round": "Matchweek 19",
    "venue": "Home",
    "opponent": "Real Madrid",
    "result": "W 3-1"
  },
  "performance": {
    "minutes_played": 90,
    "goals": 2,
    "assists": 1
  },
  "shooting": {
    "shots": 5,
    "shots_on_target": 4,
    "xg": 1.8
  },
  "passing": {
    "passes_completed": 45,
    "passes_attempted": 52,
    "pass_completion_pct": 86.5,
    "key_passes": 3,
    "xa": 0.4
  },
  "defense": {
    "tackles": 1,
    "interceptions": 0,
    "blocks": 0
  },
  "possession": {
    "touches": 67,
    "dribbles_completed": 2,
    "carries": 35
  },
  "discipline": {
    "fouls_committed": 1,
    "fouls_drawn": 2,
    "yellow_cards": 0,
    "red_cards": 0
  }
}
```

---

## ?? Root & Health Endpoints

### GET /

Welcome endpoint - informacje o API.

**Response:** Obiekt z opisem API, list¹ endpointów, informacjami o schedulerze.

### GET /health

Health check endpoint (do monitoringu).

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-01-XX...",
  "scheduler_running": true
}
```

---

## ?? Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## ?? Quick Test Commands

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. List all players
curl http://localhost:8000/api/players

# 3. Get specific player
curl http://localhost:8000/api/players/5

# 4. Compare two players
curl "http://localhost:8000/api/comparison/compare?player1_id=5&player2_id=8"

# 5. Get player matches
curl http://localhost:8000/api/matchlogs/5

# 6. Get match stats summary
curl http://localhost:8000/api/matchlogs/5/stats

# 7. Get specific match details
curl http://localhost:8000/api/matchlogs/match/123
```

---

## ?? Response Codes

- `200` - Success
- `404` - Resource not found (player, match, etc.)
- `400` - Bad request (e.g., comparing goalkeeper with field player)
- `500` - Internal server error

---

## ?? Common Use Cases

### Use Case 1: Get player season statistics
```bash
# Step 1: Get player ID
curl http://localhost:8000/api/players | jq '.[] | select(.name=="Robert Lewandowski")'

# Step 2: Get match logs for current season
curl "http://localhost:8000/api/matchlogs/5?season=2025-2026"

# Step 3: Get aggregated stats
curl "http://localhost:8000/api/matchlogs/5/stats?season=2025-2026"
```

### Use Case 2: Compare two strikers
```bash
# Compare Lewandowski (id=5) vs Pi¹tek (id=10)
curl "http://localhost:8000/api/comparison/compare?player1_id=5&player2_id=10&season=2025-2026"
```

### Use Case 3: Analyze specific match
```bash
# Get match details
curl http://localhost:8000/api/matchlogs/match/123
```

---

**Last Updated:** 2025-01-XX
**Version:** 0.7.4
