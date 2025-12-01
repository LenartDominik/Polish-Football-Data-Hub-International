# Bug Fix: Season Total & Minutes in Season Statistics History

## Problem Description

Użytkownik zgłosił dwa problemy:

1. **Season Total (2025-2026) - źle zlicza mecze**
   - Przykład: Szymański pokazuje 25 games, ale powinien mieć więcej (brakuje Champions League)
   
2. **Season Statistics History - minuty pokazują 0**
   - Wiele wierszy w tabeli historycznej ma 0 minut mimo że są mecze

## Root Cause Analysis

### Problem 1: Brakujące mecze w Season Total

**Przyczyna:** FBref nie zawsze zwraca wszystkie rozgrywki europejskie w tabelach statystyk (`stats_standard_intl_cup`). 

Przykład Szymańskiego:
- `competition_stats`: Europa Lg (4 mecze, 179 minut)
- `player_matches`: Europa Lg (5 mecze, 179 minut) + **Champions Lg (4 mecze, 360 minut)**
- **Brakujące:** Champions League (4 mecze, 360 minut)

FBref scraper pobiera dane z tabel:
- `stats_standard_dom_lg` - liga krajowa
- `stats_standard_dom_cup` - puchary krajowe  
- `stats_standard_intl_cup` - rozgrywki europejskie
- `stats_standard_nat_tm` - reprezentacja

**Jednak Champions League czasami nie jest w `stats_standard_intl_cup`**, więc nie trafia do `competition_stats`.

### Problem 2: Minuty = 0 w Season Statistics History

**Przyczyna 1:** FBref nie zawsze zwraca kolumnę `minutes` w tabelach statystyk (zależy od ligi/sezonu).

**Przyczyna 2:** Funkcja `fix_missing_minutes_from_matchlogs()` używała prostego `ILIKE` do dopasowania nazw rozgrywek, co nie działało dla różnych wariantów nazw:
- `competition_stats`: "Europa Lg" 
- `player_matches`: "Europa League" lub "UEFA Europa League"

**Przyczyna 3:** Funkcja działa tylko po sync gracza, nie naprawia starych danych.

## Solution Implemented

### Fix 1: Season Total - dodanie brakujących danych europejskich

**Plik:** `polish-players-tracker/app/frontend/streamlit_app.py` (linia ~953)

Dodano kod który:
1. Sprawdza czy `player_matches` ma więcej meczów europejskich niż `competition_stats`
2. Jeśli tak - dodaje brakujące mecze, minuty, gole i asysty do Season Total

```python
# KROK 2.5: Add missing European cup data from player_matches
# Sometimes FBref doesn't include all European competitions in competition_stats
if not matches_df.empty and 'player_id' in matches_df.columns:
    euro_stats = get_european_stats_from_matches(row['id'], matches_df, '2025')
    if euro_stats:
        euro_comps_in_comp_stats = comp_stats_2526[comp_stats_2526['competition_type'] == 'EUROPEAN_CUP']
        games_in_comp_stats = euro_comps_in_comp_stats['games'].sum() if not euro_comps_in_comp_stats.empty else 0
        
        if euro_stats['games'] > games_in_comp_stats:
            games_diff = euro_stats['games'] - games_in_comp_stats
            minutes_diff = euro_stats['minutes'] - (euro_comps_in_comp_stats['minutes'].sum() if not euro_comps_in_comp_stats.empty else 0)
            
            total_games += games_diff
            total_minutes += minutes_diff
            total_goals += max(0, euro_stats['goals'] - (euro_comps_in_comp_stats['goals'].sum() if not euro_comps_in_comp_stats.empty else 0))
            total_assists += max(0, euro_stats['assists'] - (euro_comps_in_comp_stats['assists'].sum() if not euro_comps_in_comp_stats.empty else 0))
```

### Fix 2: Season Statistics History - pokazywanie "N/A" dla brakujących minut

**Plik:** `polish-players-tracker/app/frontend/streamlit_app.py` (linia ~1368)

**Problem:** Starsze sezony mają 0 minut w `competition_stats`, ponieważ:
- Match logs są pobierane TYLKO dla bieżącego sezonu (2025-2026)
- FBref nie zawsze zwraca minuty w tabelach statystyk dla starszych sezonów
- Pokazywanie "0" jest mylące - sugeruje że gracz nie grał, a nie że brakuje danych

**Rozwiązanie:** Pokazuj "N/A" zamiast "0" gdy są mecze ale brak minut:

```python
# Special handling for minutes: Show "N/A" for 0 minutes when games > 0
if 'minutes' in season_display.columns:
    mask_missing_minutes = (season_display['minutes'] == 0) & (season_display['games'] > 0)
    season_display['minutes'] = season_display['minutes'].astype(int).astype(str)
    season_display.loc[mask_missing_minutes, 'minutes'] = 'N/A'
```

### Fix 3: Poprawione dopasowanie nazw rozgrywek

**Plik:** `polish-players-tracker/sync_player.py` (funkcja `fix_missing_minutes_from_matchlogs`, linia ~129)

Dodano mapowanie popularnych wariantów nazw rozgrywek:

```python
# Map common variations
comp_mappings = {
    'europa lg': ['europa lg', 'europa league', 'uefa europa league'],
    'champions lg': ['champions lg', 'champions league', 'uefa champions league'],
    'conf lg': ['conf lg', 'conference league', 'uefa conference league'],
    'süper lig': ['süper lig', 'super lig'],
    'serie a': ['serie a'],
    'la liga': ['la liga', 'laliga'],
    'premier league': ['premier league'],
    'bundesliga': ['bundesliga'],
}

# Find matches for this competition (try multiple name variations)
search_terms = [stat.competition_name]
for key, variations in comp_mappings.items():
    if key in comp_name_lower:
        search_terms = variations
        break

matches = []
for term in search_terms:
    term_matches = db.query(PlayerMatch).filter(
        PlayerMatch.player_id == player.id,
        PlayerMatch.match_date >= season_start,
        PlayerMatch.match_date <= season_end,
        PlayerMatch.competition.ilike(f"%{term}%")
    ).all()
    matches.extend(term_matches)

# Remove duplicates
matches = list({m.id: m for m in matches}.values())
```

Ta sama poprawka została zastosowana dla goalkeeper stats.

## Testing

**Test case: Sebastian Szymański (2025-2026)**

### Przed naprawą:
```
COMPETITION_STATS:
  Liga: 12 games, 415 min
  Europa Lg: 4 games, 179 min
  National Team: 9 games, 613 min
  TOTAL: 25 games, 1207 min

PLAYER_MATCHES:
  Liga: 12 games, 415 min
  Europa Lg: 5 games, 179 min
  Champions Lg: 4 games, 360 min  ← MISSING!
  National Team: 5 games, 298 min
  TOTAL: 26 games, 1252 min
```

### Po naprawie (frontend):
Season Total powinien pokazać:
- **26 games** (zamiast 25)
- Poprawne minuty z uwzględnieniem Champions League

### Season Statistics History:
Tabela już używa funkcji `get_european_history_by_competition()` która agreguje bezpośrednio z `player_matches`, więc pokazuje oddzielne wiersze dla:
- Champions Lg
- Europa Lg
- Conference Lg

## Known Limitations

1. **Stare sezony - brak match logs:** 
   - Scraper pobiera match logs TYLKO dla bieżącego sezonu (domyślnie 2025-2026)
   - Starsze sezony pokazują "N/A" dla minut jeśli FBref nie zwrócił danych w tabelach statystyk
   - Aby uzyskać pełne dane historyczne, trzeba by pobierać match logs dla każdego sezonu osobno (bardzo czasochłonne)

2. **FBref data completeness:** 
   - Jeśli FBref nie ma danych w tabelach statystyk ani w match logs, nie możemy ich uzupełnić
   - Niektóre ligi/sezony mogą nie mieć pełnych danych o minutach

3. **National Team:** 
   - Minuty reprezentacji mogą być niepoprawne jeśli `competition_stats` agreguje dane inaczej niż `player_matches` (np. calendar year vs season)

## Recommendations

1. **Re-sync gracza** żeby odświeżyć dane dla bieżącego sezonu:
   ```bash
   python sync_player.py "Player Name"
   ```

2. **Starsze sezony pokazują "N/A"** dla minut - to normalne zachowanie:
   - FBref nie zawsze zwraca minuty w tabelach statystyk
   - Pobieranie match logs dla wszystkich sezonów byłoby bardzo czasochłonne
   - "N/A" oznacza brakujące dane, a nie 0 minut rozegranych

3. **Używaj `--all-seasons`** TYLKO jeśli chcesz odświeżyć wszystkie dane statystyczne:
   ```bash
   python sync_player.py "Player Name" --all-seasons
   ```
   ⚠️ To NIE pobierze match logs dla starszych sezonów - tylko odświeży `competition_stats`

4. Sprawdź logi po sync - funkcja `fix_missing_minutes_from_matchlogs` pokaże ile rekordów naprawiła dla bieżącego sezonu.

## Files Modified

1. `polish-players-tracker/app/frontend/streamlit_app.py` - dodano agregację z player_matches dla Season Total
2. `polish-players-tracker/sync_player.py` - poprawiono dopasowanie nazw w `fix_missing_minutes_from_matchlogs`

## Date
2025-12-01
