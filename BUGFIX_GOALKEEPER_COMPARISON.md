# Bugfix: Goalkeeper Comparison API

## 🐛 Problem
Porównywanie bramkarzy z bramkarzami nie działało, ponieważ API comparison używało niepoprawnych nazw kolumn z tabeli `goalkeeper_stats`. Powodowało to błędy przy próbie porównania dwóch bramkarzy.

## ✅ Rozwiązanie

### 1. Backend API (`app/backend/routers/comparison.py`)

**Naprawione nazwy kolumn w zapytaniu SQL dla bramkarzy:**
- ~~`gs.minutes_played`~~ → `gs.minutes` ✅
- ~~`gs.penalties_faced`~~ → `gs.penalties_attempted` ✅
- Usunięto nieistniejące kolumny: `yellow_cards`, `red_cards`
- Dodano brakujące kolumny:
  - `goals_against_per90`
  - `clean_sheet_percentage`
  - `wins`, `draws`, `losses`
  - `penalties_missed`
  - `post_shot_xg`

**Zaktualizowany endpoint `/available-stats` dla bramkarzy:**
- Dodano wszystkie dostępne statystyki bramkarskie
- Pogrupowano w logiczne kategorie:
  - `goalkeeper_specific`: saves, save_percentage, clean_sheets, goals_against, etc.
  - `penalties`: penalties_attempted, penalties_saved, penalties_allowed, penalties_missed
  - `performance`: wins, draws, losses
  - `general`: matches, games_starts, minutes_played

### 2. Frontend (`app/frontend/pages/2_⚖️_compare_players.py`)

**Dodano walidację typu gracza:**
- Automatyczne wykrywanie czy gracz jest bramkarzem czy zawodnikiem z pola
- Blokada porównywania bramkarzy z zawodnikami z pola
- Komunikat błędu: "⚠️ You cannot compare goalkeepers with field players!"

**Dynamiczne wyświetlanie statystyk:**
- Dla bramkarzy: 4 kolumny (Goalkeeper Stats, Penalties, Performance, General)
- Dla zawodników z pola: 3 kolumny (Offensive, Defensive, General)
- Automatyczne pobieranie odpowiednich statystyk z API

**Wizualne wskazanie typu:**
- 🧤 "Comparing goalkeepers" dla bramkarzy
- ⚽ "Comparing field players" dla zawodników z pola

## 🧪 Testy

Wszystkie testy przeszły pomyślnie:

✅ **Test 1**: Porównanie dwóch bramkarzy - DZIAŁA
✅ **Test 2**: Porównanie dwóch zawodników z pola - DZIAŁA  
✅ **Test 3**: Porównanie bramkarz + zawodnik z pola - POPRAWNIE ZABLOKOWANE (HTTP 400)
✅ **Test 4**: Endpoint `/available-stats?player_type=goalkeeper` - DZIAŁA

## 📊 Przykładowe statystyki bramkarskie

Porównanie: **Wojciech Szczęsny** vs **Łukasz Skorupski**

| Statystyka | Szczęsny | Skorupski |
|------------|----------|-----------|
| Matches | 6 | ? |
| Saves | 15 | ? |
| Save % | 63.0% | ? |
| Clean Sheets | 0 | ? |
| Goals Against | 11 | ? |
| Penalties Saved | 1 | ? |
| Wins | 4 | ? |

## 🎯 Rezultat

- ✅ Bramkarze mogą być porównywani z bramkarzami
- ✅ Zawodnicy z pola mogą być porównywani z zawodnikami z pola
- ✅ System blokuje nieprawidłowe porównania
- ✅ Wszystkie statystyki bramkarskie są dostępne
- ✅ Frontend automatycznie dostosowuje się do typu gracza

## 📝 Pliki zmodyfikowane

1. `app/backend/routers/comparison.py` - Naprawione zapytania SQL i endpoint `/available-stats`
2. `app/frontend/pages/2_⚖️_compare_players.py` - Dodana walidacja i dynamiczne wyświetlanie statystyk

---

**Data**: 2025
**Wersja**: 0.7.3+
**Status**: ✅ Naprawione i przetestowane
