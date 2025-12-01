# Bugfix: Wyświetlanie wszystkich meczów europejskich (Champions Lg + Europa Lg)

## Problem
Sebastian Szymański nie miał wyświetlonych meczów z kwalifikacji Ligi Mistrzów (Champions Lg) w sezonie 2025-26. W kolumnie "European Cups" oraz w tabeli "Season Statistics History" pokazywały się tylko mecze z Europy League.

## Przyczyna
FBref agreguje mecze z różnych rozgrywek europejskich (Champions League kwalifikacje → Europa League faza grupowa) w jednej linii w tabeli `competition_stats`. Gdy drużyna spada z kwalifikacji Champions League do Europa League, FBref pokazuje to jako jeden wpis "Europa Lg" w tabeli zagregowanej.

Natomiast w `player_matches` (matchlogs) każdy mecz jest osobno:
- **Champions Lg**: 4 mecze (kwalifikacje, sierpień 2025)
- **Europa Lg**: 5 meczów (faza grupowa, wrzesień-listopad 2025)

Frontend używał tylko danych z `competition_stats`, co powodowało brak wyświetlenia meczów z kwalifikacji.

## Rozwiązanie

### 1. Nowa funkcja agregująca dla kolumny European Cups
**Dodano funkcję `get_european_stats_from_matches()`** w `streamlit_app.py`:
   - Agreguje wszystkie mecze europejskie z `player_matches` (Champions Lg, Europa Lg, Conf Lg)
   - **Filtruje po sezonie (lipiec-czerwiec)**
   - **Wykluczą mecze z 0 minut** (minutes_played > 0)
   - Sumuje statystyki: mecze, minuty, gole, asysty, xG, xA
   - Zwraca dict z zagregowanymi danymi

### 2. Nowa funkcja dla tabeli Season Statistics History
**Dodano funkcję `get_european_history_by_competition()`** w `streamlit_app.py`:
   - Grupuje mecze europejskie z `player_matches` po sezonie I rozgrywkach
   - **Wykluczą mecze z 0 minut** (minutes_played > 0)
   - Zwraca osobne wiersze dla Champions Lg, Europa Lg, Conf Lg
   - Format zgodny z `competition_stats` (DataFrame z kolumnami: season, competition_type, competition_name, games, goals, assists, etc.)

### 3. Zaktualizowano kolumnę "European Cups"
   - **Priorytet**: dane z `player_matches` (jeśli dostępne) - pokazuje KAŻDĄ rozgrywkę osobno
   - **Fallback**: dane z `competition_stats` (dla starszych sezonów bez matchlogs)
   - **Wyświetla osobne wiersze** dla każdej rozgrywki europejskiej (Champions Lg, Europa Lg, Conf Lg)
   - Format: każda rozgrywka ma własny wiersz z boldem (np. **Champions Lg**)

### 4. Zaktualizowano tabelę "Season Statistics History"
   - Usuwa zagregowane wpisy EUROPEAN_CUP z `competition_stats`
   - Dodaje szczegółowe wiersze z `player_matches` (osobno Champions Lg, Europa Lg, etc.)
   - Dzięki temu każda rozgrywka europejska ma swój osobny wiersz w tabeli - tak jak u Świderskiego

### 5. Zaktualizowano sekcję Details
   - Używa zagregowanych danych z `player_matches` gdy dostępne
   - Pokazuje pełne statystyki (starty, minuty, xG, xA, per 90)

## Wynik
Dla Sebastiana Szymańskiego (sezon 2025-26):

### Kolumna European Cups:
- **Przed**: 1 wiersz "Europa Lg" (4 mecze, 179 minut, 1 gol) - brak Champions Lg
- **Po**: **2 osobne wiersze** dla każdej rozgrywki:
  - **Champions Lg**: 4 mecze, 0 goli, 1 asysta, 360 minut (kwalifikacje)
  - **Europa Lg**: 4 mecze, 1 gol, 0 asyst, 179 minut (faza ligowa - tylko zagrane)
  - **RAZEM**: 8 meczów zagranych, 1 gol, 1 asysta, 539 minut

### Tabela Season Statistics History:
- **Przed**: 1 wiersz "Europa Lg" (4 mecze, 179 minut, 1 gol) - brak Champions Lg
- **Po**: **2 osobne wiersze**:
  - "Champions Lg": 4 mecze, 0 goli, 1 asysta, 360 minut
  - "Europa Lg": 4 mecze, 1 gol, 0 asyst, 179 minut
  - **RAZEM**: 8 meczów zagranych (wykluczono mecze z 0 minut)

## Pliki zmienione
- `app/frontend/streamlit_app.py`:
  - Dodano funkcję `get_european_stats_from_matches()` (linie 121-170)
  - Dodano funkcję `get_european_history_by_competition()` (linie 172-243)
  - Zaktualizowano kolumnę 2 (European Cups) - linie 484-648
  - Zaktualizowano tabelę Season Statistics History - linie 1165-1179

## Testowanie

### Test 1: Kolumna European Cups
1. Uruchom backend: `python -m uvicorn app.backend.main:app --reload`
2. Uruchom frontend: `streamlit run app/frontend/streamlit_app.py`
3. Wyszukaj "Szymański"
4. Sprawdź kolumnę "European Cups (2025-2026)":
   - ✅ Powinny być **2 osobne wiersze** (nie 1 zagregowany)
   - ✅ **Champions Lg**: 4 Games, 0 Goals, 1 Assist
   - ✅ **Europa Lg**: 5 Games, 1 Goal, 0 Assists
5. Rozwiń "Details" w European Cups:
   - ✅ Powinny być **2 sekcje** (Champions Lg + Europa Lg) oddzielone poziomą linią
   - ✅ Champions Lg: 360 minut, breakdown statystyk
   - ✅ Europa Lg: 179 minut, breakdown statystyk

### Test 2: Tabela Season Statistics History
1. Przewiń w dół do sekcji "Season Statistics History (All Competitions)"
2. Sprawdź wiersze dla sezonu 2025-2026:
   - ✅ Powinien być wiersz "Champions Lg": 4 mecze, 360 minut, 0 goli, 1 asysta
   - ✅ Powinien być wiersz "Europa Lg": 5 meczów, 179 minut, 1 gol, 0 asyst
   - ✅ Format podobny jak u Świderskiego (osobne wiersze dla każdej rozgrywki)

## Uwagi
- Rozwiązanie działa również dla innych graczy z wieloma rozgrywkami europejskimi
- Automatycznie obsługuje Conference League (Conf Lg)
- Dla sezonów bez matchlogs używa fallback do `competition_stats`
- **Matchlogi muszą być zsynchronizowane**: `python sync_match_logs.py "Player Name"`
- Rozwiązanie nie wpływa na bramkarzy (używają `goalkeeper_stats`)
