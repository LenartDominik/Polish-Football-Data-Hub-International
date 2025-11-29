# ?? Matchlogs Endpoints Update - Dokumentacja Zmian

**Data:** 2025-01-XX
**Wersja:** 0.7.4

## ?? Cel Aktualizacji

Zmiana struktury endpointów match logs z `/api/players/{id}/matches` na `/api/matchlogs/{id}` 
dla lepszej organizacji i przejrzystoœci API.

## ?? Zmiany w Endpointach

### Przed (Stare œcie¿ki - DEPRECATED)
- ? `GET /api/players/{player_id}/matches`
- ? `GET /api/players/{player_id}/matches/summary`
- ? `GET /api/players/matches/{match_id}`

### Po (Nowe œcie¿ki - AKTUALNE)
- ? `GET /api/matchlogs/{player_id}`
- ? `GET /api/matchlogs/{player_id}/stats`
- ? `GET /api/matchlogs/match/{match_id}`

## ?? Szczegó³y Endpointów

### 1. GET /api/matchlogs/{player_id}

**Opis:** Pobiera listê wszystkich meczów gracza z opcjonalnymi filtrami.

**Parametry query:**
- `season` (optional) - Filtr po sezonie (np. "2025-2026")
- `competition` (optional) - Filtr po rozgrywkach (np. "La Liga")
- `limit` (optional, default: 100) - Maksymalna liczba wyników

**Przyk³ad:**
```bash
curl "http://localhost:8000/api/matchlogs/5?season=2025-2026&limit=20"
```

**OdpowiedŸ:**
```json
{
  "player_id": 5,
  "player_name": "Robert Lewandowski",
  "total_matches": 20,
  "filters": {
    "season": "2025-2026",
    "competition": null
  },
  "matches": [
    {
      "id": 123,
      "date": "2025-01-15",
      "competition": "La Liga",
      "opponent": "Real Madrid",
      "goals": 2,
      "assists": 1,
      "minutes_played": 90,
      "xg": 1.8,
      "xa": 0.4,
      ...
    }
  ]
}
```

### 2. GET /api/matchlogs/{player_id}/stats

**Opis:** Zwraca statystyki agregowane (sumy i œrednie) z wszystkich meczów.

**Parametry query:**
- `season` (optional) - Filtr po sezonie
- `competition` (optional) - Filtr po rozgrywkach

**Przyk³ad:**
```bash
curl "http://localhost:8000/api/matchlogs/5/stats?season=2025-2026"
```

**OdpowiedŸ:**
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
    "total_xg": 19.5,
    "total_xa": 6.8,
    "avg_minutes_per_match": 87.8,
    "avg_goals_per_match": 0.90,
    "avg_assists_per_match": 0.35
  }
}
```

### 3. GET /api/matchlogs/match/{match_id}

**Opis:** Pobiera szczegó³owe informacje o pojedynczym meczu.

**Parametry path:**
- `match_id` (required) - ID meczu

**Przyk³ad:**
```bash
curl "http://localhost:8000/api/matchlogs/match/123"
```

**OdpowiedŸ:**
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

## ?? Zmiany Techniczne

### Pliki Zmodyfikowane:

1. **`app/backend/routers/matchlogs.py`**
   - Zmiana prefixu routera z `/api/players` na `/matchlogs`
   - Aktualizacja œcie¿ek endpointów
   - Ulepszone docstringi dla dokumentacji Swagger

2. **`app/backend/main.py`**
   - Aktualizacja dokumentacji FastAPI/Swagger
   - Poprawka sekcji "Quick Start"
   - Zaktualizowane linki do endpointów

3. **`README.md`** (g³ówny)
   - Dodana sekcja Match Logs Endpoints
   - Zaktualizowane przyk³ady u¿ycia

4. **`app/backend/README.md`**
   - Zaktualizowane wszystkie œcie¿ki matchlogs
   - Dodane przyk³ady dla nowego endpointu `/match/{id}`

5. **`app/frontend/README.md`**
   - Dodana sekcja o korzystaniu z matchlogs API
   - Przyk³ady integracji w Python/requests

6. **`API_ENDPOINTS_GUIDE.md`**
   - Kompletna aktualizacja wszystkich przyk³adów
   - Zaktualizowane URLe w przyk³adach curl
   - Dodany endpoint `/match/{match_id}`

## ?? Testowanie

### Test endpointów:

```bash
# 1. Lista meczów gracza
curl http://localhost:8000/api/matchlogs/5

# 2. Statystyki agregowane
curl http://localhost:8000/api/matchlogs/5/stats

# 3. Szczegó³y meczu
curl http://localhost:8000/api/matchlogs/match/123

# 4. Z filtrami
curl "http://localhost:8000/api/matchlogs/5?season=2025-2026&competition=La%20Liga&limit=10"
```

### Sprawdzenie dokumentacji:

1. Otwórz http://localhost:8000/docs (Swagger UI)
2. SprawdŸ sekcjê "matchlogs" - powinny byæ 3 endpointy
3. Przetestuj ka¿dy endpoint w Swagger UI
4. SprawdŸ http://localhost:8000/redoc (ReDoc)

## ?? Kompatybilnoœæ Wsteczna

?? **BREAKING CHANGE** - Stare endpointy zosta³y usuniête.

Jeœli u¿ywa³eœ starych œcie¿ek, zaktualizuj swój kod:

```python
# Przed (NIEDZIA£AJ¥CE)
response = requests.get(f"{API_URL}/players/{player_id}/matches")

# Po (POPRAWNE)
response = requests.get(f"{API_URL}/matchlogs/{player_id}")
```

## ? Checklist Wdro¿enia

- [x] Zaktualizowany router matchlogs.py
- [x] Zaktualizowany main.py (Swagger docs)
- [x] Zaktualizowany g³ówny README.md
- [x] Zaktualizowany backend README.md
- [x] Zaktualizowany frontend README.md
- [x] Zaktualizowany API_ENDPOINTS_GUIDE.md
- [x] Dokumentacja Swagger/ReDoc
- [ ] Przetestowane wszystkie endpointy
- [ ] Zaktualizowany frontend (jeœli u¿ywa matchlogs)

## ?? Korzyœci

1. **Lepsza organizacja** - Matchlogs maj¹ w³asny namespace
2. **Przejrzystoœæ** - Œcie¿ki jasno pokazuj¹ przeznaczenie
3. **Spójnoœæ** - Wszystkie endpointy matchlogs pod jednym prefiksem
4. **£atwiejsza dokumentacja** - £atwiej grupowaæ w Swagger
5. **Skalowalnoœæ** - £atwiej dodawaæ nowe funkcje matchlogs

## ?? Wsparcie

W razie problemów sprawdŸ:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

---
**Autor:** Polish Players Tracker Team
**Kontakt:** Zobacz README.md
