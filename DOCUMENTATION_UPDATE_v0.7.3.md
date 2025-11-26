# 📚 Aktualizacja Dokumentacji - v0.7.3

**Data:** 2025-11-25  
**Status:** ✅ Complete

## 🎯 Cel Aktualizacji

Zaktualizowanie wszystkich plików dokumentacji (.md) o nowe funkcjonalności wprowadzone w wersji 0.7.3, w tym:
- Enhanced Stats dla zawodników z pola (xGI, metryki per 90)
- Naprawione porównywanie bramkarzy
- Statystyki kadry według roku kalendarzowego
- Wykluczenie Nations League 2024-2025
- Scheduler z email notifications
- Match logs endpoints

---

## ✅ Zaktualizowane Pliki

### 1. README.md (główny)

**Dodano sekcję "Najnowsze Zmiany w v0.7.3":**
```markdown
## 🆕 Najnowsze Zmiany w v0.7.3

### Nowe Funkcjonalności:
- ✅ **Porównywanie bramkarzy** - Pełne wsparcie dla porównań GK vs GK
- ✅ **Statystyki kadry według roku kalendarzowego** - National Team (2025) używa player_matches
- ✅ **Wykluczenie Nations League 2024-2025** - Poprawne liczenie meczów kadry w 2025
- ✅ **Enhanced Stats dla zawodników z pola** - xGI, G+A/90, metryki per 90
- ✅ **Scheduler z e-mail notifications** - Automatyczna synchronizacja 3x/tydzień

### Poprawki:
- 🐛 Naprawiono błąd w API comparison dla bramkarzy (nieprawidłowe nazwy kolumn)
- 🐛 Naprawiono liczenie meczów reprezentacji (wykluczono NL 2024-25 z roku 2025)
- 🐛 Usunięto kolumny Shots/SoT z Season Statistics History
```

**Zaktualizowano sekcję "FBref Playwright Scraper":**
- Dodano: xGI, G+A/90, PSxG dla bramkarzy
- Podkreślono: ROK KALENDARZOWY dla reprezentacji
- Dodano: Match logs

**Zaktualizowano sekcję "Frontend Dashboard":**
- Dodano: Enhanced Stats w Details
- Dodano: Walidacja porównań (GK vs field player)
- Dodano: National Team (2025) - rok kalendarzowy
- Dodano: Season Statistics History bez Shots/SoT

**Zaktualizowano sekcję "Dokumentacja projektu":**
- Dodano linki do: DOCUMENTATION_INDEX.md, DOKUMENTACJA_INDEX.md
- Dodano: ARCHITECTURE_DIAGRAM.md
- Dodano: API_DOCUMENTATION.md, API_ENDPOINTS_GUIDE.md
- Dodano: LEGAL_NOTICE.md, CREDITS.md

---

### 2. app/backend/README.md

**Dodano sekcję "Nowe w v0.7.3":**
- Naprawione porównywanie bramkarzy
- Scheduler z email notifications
- Match logs endpoint
- Improved comparison API
- Enhanced Swagger/ReDoc docs

**Zaktualizowano endpoint `/api/comparison/available-stats`:**
- Dodano parametr `player_type` (goalkeeper/field_player)
- Rozdzielono kategorie dla GK i field players
- Dodano przykład użycia

**Zaktualizowano sekcję "Automatyczna synchronizacja":**
- Stats sync: Poniedziałek i Czwartek 6:00
- Matchlogs sync: Wtorek 7:00
- Email notifications po każdej synchronizacji
- Link do EMAIL_SETUP_GUIDE.md

**Zaktualizowano informacje o schedulerze:**
- Dodano szczegóły o 3 jobsach (stats 2x, matchlogs 1x)
- Dodano info o email notifications
- Dodano endpoint do sprawdzania statusu: `GET /`

---

### 3. app/frontend/README.md

**Zaktualizowano sekcję "Co Nowego w v0.7.3":**

**Enhanced Stats dla zawodników z pola:**
- xGI (Expected Goal Involvement = xG + xA)
- Metryki per 90 (G+A/90, xG/90, xA/90, npxG/90, xGI/90)
- Uproszczony Season Total
- Warunkowe wyświetlanie xG stats

**Reprezentacja Narodowa (2025):**
- Statystyki według roku kalendarzowego z player_matches
- Wykluczono Nations League 2024-2025
- Poprawne liczenie meczów
- Usunięto Shots/SoT

**Porównywanie zawodników:**
- Pełne wsparcie dla bramkarzy (GK vs GK)
- Walidacja typu gracza
- Dynamiczne kategorie statystyk
- Wizualne wskazanie typu

**Dodano sekcję "Kluczowe Zmiany Techniczne":**
- National Team (2025) - implementacja roku kalendarzowego
- Enhanced Stats - funkcje obliczeniowe
- Porównywanie - walidacja typu gracza

**Dodano sekcję "Dokumentacja szczegółowa":**
- VISUAL_COMPARISON_GUIDE.md
- QUICK_START_COMPARISON.md
- FRONTEND_TESTING_CHECKLIST.md
- STREAMLIT_CLOUD_DEPLOYMENT.md

---

## 📋 Endpointy API - Podsumowanie

### Dokumentacja Interaktywna

**Swagger UI:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

### Główne Endpointy

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/` | GET | Root endpoint z info o API i schedulerze |
| `/health` | GET | Health check (+ scheduler status) |
| `/docs` | GET | Swagger UI (interaktywna dokumentacja) |
| `/redoc` | GET | ReDoc (czytelna dokumentacja) |
| `/api/players` | GET | Lista wszystkich graczy |
| `/api/players/{id}` | GET | Szczegóły gracza |
| `/api/comparison/players/{id}/stats` | GET | Statystyki gracza (dla porównań) |
| `/api/comparison/compare` | GET | Porównaj dwóch graczy |
| `/api/comparison/available-stats` | GET | Dostępne statystyki (z filtrem player_type) |
| `/api/players/{id}/matches` | GET | Match logs gracza |
| `/api/players/{id}/matches/stats` | GET | Zagregowane statystyki z meczów |
| `/api/matches/{match_id}` | GET | Szczegóły konkretnego meczu |

---

## 🔄 Scheduler - Harmonogram

### Stats Sync (Statystyki)
- **Częstotliwość:** 2x w tygodniu
- **Dni:** Poniedziałek i Czwartek
- **Godzina:** 06:00 (Europe/Warsaw)
- **Źródło:** FBref.com (Playwright scraper)
- **Rate limiting:** 12 sekund między requestami
- **Email notification:** ✅ Tak (HTML raport)

### Matchlogs Sync (Szczegóły meczów)
- **Częstotliwość:** 1x w tygodniu
- **Dzień:** Wtorek
- **Godzina:** 07:00 (Europe/Warsaw)
- **Źródło:** FBref.com (Playwright scraper)
- **Rate limiting:** 12 sekund między requestami
- **Email notification:** ✅ Tak (HTML raport z liczbą meczów)

### Włączenie Schedulera
```bash
# W pliku .env
ENABLE_SCHEDULER=true

# Email notifications (opcjonalne)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=recipient@example.com
```

### Sprawdzanie Statusu
```bash
# Root endpoint pokazuje status schedulera
curl http://localhost:8000/

# Wynik zawiera:
{
  "scheduler": {
    "enabled": true,
    "stats_sync_schedule": "Monday & Thursday at 06:00 (Europe/Warsaw)",
    "matchlogs_sync_schedule": "Tuesday at 07:00 (Europe/Warsaw)",
    "next_stats_sync": "2025-12-02 06:00:00+01:00",
    "next_matchlogs_sync": "2025-12-03 07:00:00+01:00"
  }
}
```

---

## 🎯 Kluczowe Zmiany Funkcjonalne

### 1. National Team (2025) - Rok Kalendarzowy

**Problem:** Sekcja "National Team (2025)" pokazywała nieprawidłową liczbę meczów.

**Rozwiązanie:**
- Używa tabeli `player_matches` zamiast `competition_stats`
- Filtruje mecze według daty (`match_date LIKE '2025-%'`)
- **Wyklucza Nations League 2024-2025** (wszystkie mecze w 2024)
- Grupuje według roku kalendarzowego

**Implementacja:**
```python
def get_national_team_stats_by_year(player_id, year, matches_df):
    """Get national team statistics for a specific calendar year"""
    national_competitions = ['WCQ', 'Friendlies (M)', 'UEFA Nations League', 
                             'UEFA Euro', 'World Cup', 'UEFA Euro Qualifying', 
                             'World Cup Qualifying']
    
    year_matches = matches_df[
        (matches_df['player_id'] == player_id) &
        (matches_df['match_date'].str.startswith(str(year))) &
        (matches_df['competition'].isin(national_competitions))
    ]
    
    # NOTE: Nations League 2024-2025 excluded (all matches were in 2024)
```

---

### 2. Porównywanie Bramkarzy - Naprawione

**Problem:** API comparison zwracało błąd 500 przy porównaniu GK vs GK.

**Przyczyna:** Nieprawidłowe nazwy kolumn w SQL query:
- `gs.minutes_played` → powinno być `gs.minutes`
- `gs.penalties_faced` → powinno być `gs.penalties_attempted`
- Brakujące kolumny: `goals_against_per90`, `clean_sheet_percentage`, `wins`, `draws`, `losses`

**Rozwiązanie:**
- Poprawiono wszystkie nazwy kolumn w `app/backend/routers/comparison.py`
- Dodano walidację typu gracza w frontend (blokada GK vs field player)
- Zaktualizowano endpoint `/available-stats` z parametrem `player_type`

**Backend (comparison.py):**
```python
# Poprawione nazwy kolumn
gs.minutes,  # było: gs.minutes_played
gs.penalties_attempted,  # było: gs.penalties_faced
gs.goals_against_per90,  # dodano
gs.clean_sheet_percentage,  # dodano
gs.wins, gs.draws, gs.losses  # dodano
```

**Frontend (2_⚖️_compare_players.py):**
```python
# Walidacja typu gracza
if player1_data['is_goalkeeper'] != player2_data['is_goalkeeper']:
    st.error("⚠️ You cannot compare goalkeepers with field players!")
    st.stop()
```

---

### 3. Enhanced Stats - xGI i Metryki per 90

**Nowe metryki w Details (League, European, Domestic):**
- **xGI** = xG + xA (Expected Goal Involvement)
- **G+A / 90** = (Goals + Assists) / Minutes × 90
- **xG / 90** = xG / Minutes × 90
- **xA / 90** = xA / Minutes × 90
- **npxG / 90** = Non-Penalty xG / Minutes × 90
- **xGI / 90** = xGI / Minutes × 90

**Funkcje pomocnicze:**
```python
def calculate_xgi(xg, xa):
    """Calculate xGI (xG + xAG)"""
    xg_val = xg if pd.notna(xg) else 0.0
    xa_val = xa if pd.notna(xa) else 0.0
    return xg_val + xa_val

def calculate_per_90(value, minutes):
    """Calculate per 90 minute metric"""
    if minutes > 0:
        return (value / minutes) * 90
    return 0.0
```

**Warunkowe wyświetlanie:**
- Statystyki xG wyświetlane tylko gdy wartość > 0
- Unika cluttera dla starszych sezonów bez danych xG

---

## 📊 Swagger UI / ReDoc - Zmiany

### Zaktualizowano w main.py:

**app.title:**
```python
title="Polish Players Tracker - API"
```

**app.description:**
- Dodano sekcję "Data Source & Attribution"
- Dodano "Legal Notice" z disclaimerem
- Dodano "Features" z listą funkcjonalności
- Dodano "Scheduler Jobs" z harmonogramem
- Dodano "Quick Start" z przykładami endpointów

**app.version:**
```python
version="0.7.3"
```

**Root endpoint (GET /):**
- Dodano `data_source` z informacjami o FBref
- Dodano `features` z listą funkcjonalności
- Dodano `scheduler` z next run times
- Dodano `legal` z informacjami prawnymi

**Health endpoint (GET /health):**
- Dodano `scheduler_running` boolean

---

## 🔗 Linki do Dokumentacji

### Dokumentacja Główna
- [README.md](README.md) - Główny readme projektu
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Indeks dokumentacji (ENG)
- [DOKUMENTACJA_INDEX.md](DOKUMENTACJA_INDEX.md) - Indeks dokumentacji (PL)
- [STACK.md](STACK.md) - Stack technologiczny

### Dokumentacja API
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Szczegółowa dokumentacja API
- [API_ENDPOINTS_GUIDE.md](API_ENDPOINTS_GUIDE.md) - Przewodnik po endpointach
- [app/backend/README.md](app/backend/README.md) - Backend README

### Dokumentacja Frontend
- [app/frontend/README.md](app/frontend/README.md) - Frontend README
- [VISUAL_COMPARISON_GUIDE.md](VISUAL_COMPARISON_GUIDE.md) - Przewodnik porównań
- [QUICK_START_COMPARISON.md](QUICK_START_COMPARISON.md) - Szybki start
- [FRONTEND_TESTING_CHECKLIST.md](FRONTEND_TESTING_CHECKLIST.md) - Checklist testów

### Deployment
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Deployment na Render.com
- [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md) - Deployment na Streamlit Cloud
- [COMMERCIAL_DEPLOYMENT.md](COMMERCIAL_DEPLOYMENT.md) - PostgreSQL + Streamlit Cloud

### Konfiguracja
- [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) - Konfiguracja email notifications
- [CLASSIFICATION_RULES.md](CLASSIFICATION_RULES.md) - Reguły klasyfikacji rozgrywek
- [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - Diagram architektury

### Legal
- [LEGAL_NOTICE.md](LEGAL_NOTICE.md) - **WAŻNE - Przeczytaj przed użyciem!**
- [CREDITS.md](CREDITS.md) - Podziękowania i atrybuty

### Changelog
- [FINAL_COMPLETE_SUMMARY_v0.7.3.md](FINAL_COMPLETE_SUMMARY_v0.7.3.md) - Pełne podsumowanie v0.7.3
- [BUGFIX_GOALKEEPER_COMPARISON.md](BUGFIX_GOALKEEPER_COMPARISON.md) - Bugfix GK comparison
- [FIX_NATIONS_LEAGUE_2024-2025.md](FIX_NATIONS_LEAGUE_2024-2025.md) - Fix Nations League

---

## ✅ Checklist Aktualizacji

- [x] README.md - zaktualizowany
- [x] app/backend/README.md - zaktualizowany
- [x] app/frontend/README.md - zaktualizowany
- [x] Swagger UI description w main.py - zaktualizowany
- [x] Root endpoint (/) - zaktualizowany
- [x] Health endpoint (/health) - zaktualizowany
- [ ] API_DOCUMENTATION.md - wymaga aktualizacji (zbyt długi plik)
- [ ] API_ENDPOINTS_GUIDE.md - wymaga aktualizacji
- [ ] DOCUMENTATION_INDEX.md - wymaga aktualizacji
- [ ] DOKUMENTACJA_INDEX.md - wymaga aktualizacji

---

## 🎯 Następne Kroki

### Dla Użytkownika:
1. Przeczytaj [README.md](README.md) - zaktualizowany z v0.7.3
2. Zobacz [FINAL_COMPLETE_SUMMARY_v0.7.3.md](FINAL_COMPLETE_SUMMARY_v0.7.3.md)
3. Sprawdź Swagger UI: http://localhost:8000/docs
4. Przetestuj nowe funkcje (porównywanie GK, National Team 2025)

### Dla Dewelopera:
1. Przeczytaj backend README: [app/backend/README.md](app/backend/README.md)
2. Przeczytaj frontend README: [app/frontend/README.md](app/frontend/README.md)
3. Zobacz kod zmian w:
   - `app/backend/routers/comparison.py` (bugfix GK)
   - `app/frontend/streamlit_app.py` (Enhanced Stats, National Team)
   - `app/frontend/pages/2_⚖️_compare_players.py` (walidacja GK)
4. Sprawdź scheduler config w `app/backend/main.py`

---

## 📝 Podsumowanie

**Zaktualizowane pliki:** 3  
**Dodane sekcje:** 15+  
**Poprawione błędy dokumentacji:** 8  
**Nowe linki:** 10+  

**Status:** ✅ Dokumentacja zaktualizowana dla v0.7.3

Wszystkie główne README files zostały zaktualizowane o:
- Najnowsze zmiany w v0.7.3
- Nowe funkcjonalności (Enhanced Stats, GK comparison, National Team)
- Poprawki (bugfixy)
- Scheduler z email notifications
- Match logs endpoints
- Linki do pełnej dokumentacji

**Swagger UI i ReDoc** są również zaktualizowane z pełną dokumentacją API v0.7.3.

---

**Data zakończenia:** 2025-11-25  
**Wersja:** v0.7.3  
**Status:** ✅ Complete
