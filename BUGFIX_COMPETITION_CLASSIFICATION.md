# BUGFIX: Competition Type Classification

## Data: 2025-01-XX
## Wersja: 0.7.4

## Problem
1. **"Conf Lg"** (Conference League) był klasyfikowany jako `LEAGUE` zamiast `EUROPEAN_CUP`
2. **"Leagues Cup"** miał niespójną klasyfikację - czasem `DOMESTIC_CUP`, czasem `EUROPEAN_CUP`
   - Poprawna klasyfikacja: `LEAGUE` (rozgrywki międzynarodowe MLS vs Liga MX, nie puchar krajowy)

## Przyczyna
Funkcja `get_competition_type()` w trzech plikach:
- `app/backend/main.py`
- `sync_competition_stats.py`
- `sync_playwright.py`

Miała problemy:
1. Brak "conf lg" w liście rozgrywek europejskich
2. "leagues cup" błędnie w liście pucharów krajowych
3. Słowo "euro" dopasowywało "Europa Lg" do reprezentacji zamiast pucharów europejskich

## Rozwiązanie

### 1. Dodano "conf lg" do rozgrywek europejskich
```python
# European club competitions
if any(keyword in comp_lower for keyword in [
    'champions league', 'europa league', 'conference league', 
    'uefa', 'champions lg', 'europa lg', 'conf lg', 'ucl', 'uel', 'uecl'  # <-- dodano 'conf lg'
]):
    return "EUROPEAN_CUP"
```

### 2. Usunięto "leagues cup" z pucharów krajowych
```python
# Domestic cups
if any(keyword in comp_lower for keyword in [
    'copa del rey', 'copa', 'pokal', 'coupe', 'coppa',
    'fa cup', 'league cup', 'efl', 'carabao',
    'dfb-pokal', 'dfl-supercup', 'supercoca', 'supercoppa',
    'u.s. open cup'  # <-- usunięto 'leagues cup'
]):
    return "DOMESTIC_CUP"
```

### 3. Zmieniono kolejność sprawdzania (NATIONAL_TEAM przed EUROPEAN_CUP)
```python
# National team (CHECK FIRST - before UEFA competitions)
if any(keyword in comp_lower for keyword in [
    'national team', 'reprezentacja', 'international',
    'friendlies', 'wcq', 'world cup', 'uefa euro', 'copa américa'  # <-- 'uefa euro' zamiast 'euro'
]):
    return "NATIONAL_TEAM"
```

### 4. Zaktualizowano istniejące dane w bazie
```
Wykonano skrypt: tmp_rovodev_fix_db_classifications.py
- CompetitionStats: 33 rekordy naprawione
- GoalkeeperStats: 4 rekordy naprawione
- Łącznie: 37 rekordów zaktualizowanych
```

## Pliki zmienione
- ✅ `polish-players-tracker/app/backend/main.py` - funkcja `get_competition_type()`
- ✅ `polish-players-tracker/sync_competition_stats.py` - funkcja `get_competition_type()`
- ✅ `polish-players-tracker/sync_playwright.py` - funkcja `get_competition_type()`

## Testy
Wszystkie testy przeszły pomyślnie:
- ✅ "Conf Lg" -> EUROPEAN_CUP
- ✅ "Conference League" -> EUROPEAN_CUP
- ✅ "Leagues Cup" -> LEAGUE
- ✅ "Europa Lg" -> EUROPEAN_CUP (nie NATIONAL_TEAM)
- ✅ "Champions Lg" -> EUROPEAN_CUP
- ✅ "Friendlies (M)" -> NATIONAL_TEAM
- ✅ "WCQ" -> NATIONAL_TEAM
- ✅ "World Cup" -> NATIONAL_TEAM
- ✅ "UEFA Euro" -> NATIONAL_TEAM
- ✅ "Copa del Rey" -> DOMESTIC_CUP
- ✅ "La Liga" -> LEAGUE

## Wpływ
Po tej zmianie:
- Świderski i inni gracze z Conference League będą mieli poprawną klasyfikację
- Leagues Cup nie będzie błędnie klasyfikowane jako puchar krajowy
- Wszystkie mecze reprezentacji będą poprawnie rozpoznawane
- Europa League nie będzie mylona z meczami reprezentacji

## Weryfikacja
Aby zweryfikować poprawność, sprawdź gracza Świderski:
```bash
# W przyszłości po synchronizacji
SELECT competition_name, competition_type 
FROM competition_stats 
WHERE player_id = (SELECT id FROM players WHERE name LIKE '%Świderski%');
```

Oczekiwany wynik:
- "Conf Lg" powinno mieć `competition_type = 'EUROPEAN_CUP'`
