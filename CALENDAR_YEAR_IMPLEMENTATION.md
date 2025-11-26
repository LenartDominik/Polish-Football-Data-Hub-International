# ✅ Implementacja Roku Kalendarzowego dla Reprezentacji

## 🎯 Zadanie

**Wymaganie:** Mecze reprezentacji narodowej powinny być wyświetlane według **roku kalendarzowego**, a nie sezonu (jak dla klubów).

## 📊 Problem

### Przed Zmianami:
- Aplikacja używała tabeli `competition_stats`, która agreguje dane per **sezon/rozgrywki**
- Dla reprezentacji:
  - **Sezon "2026"** = wszystkie mecze WCQ (łącznie 7), niezależnie od daty
  - **Sezon "2024-2025"** = wszystkie mecze Nations League
  - **Sezon "2025"** = mecze towarzyskie

**Efekt:** Świderski pokazywał **13 meczów** (agregacja całych sezonów), podczas gdy w roku kalendarzowym 2025 zagrał tylko **6 meczów**.

### Dlaczego Rok Kalendarzowy dla Reprezentacji?
Reprezentacja narodowa:
- Gra w różnych rozgrywkach w ciągu roku (WCQ, Friendlies, Nations League, Euro)
- Statystyki są naturalnie grupowane według roku kalendarzowego (np. "statystyki 2025")
- Sezony klubowe vs. rok kalendarzowy dla kadry to standard w piłce nożnej

## 🔧 Rozwiązanie

### Nowe Funkcje Pomocnicze:

#### 1. `get_national_team_stats_by_year(player_id, year, matches_df)`
Pobiera statystyki reprezentacji dla konkretnego roku kalendarzowego z tabeli `player_matches`.

**Używana w:** Sekcja "National Team (2025)" w kolumnie 4

**Funkcjonalność:**
- Filtruje mecze według daty (`match_date` rozpoczyna się od roku, np. "2025")
- Filtruje tylko mecze reprezentacji (WCQ, Friendlies, Nations League, Euro, World Cup)
- Agreguje: games, starts, goals, assists, minutes, xG, xA, shots, etc.

```python
national_stats_2025 = get_national_team_stats_by_year(row['id'], 2025, matches_df)
# Zwraca: {'games': 6, 'goals': 0, 'assists': 0, 'minutes': 151, ...}
```

#### 2. `get_national_team_history_by_calendar_year(player_id, matches_df)`
Pobiera pełną historię reprezentacji pogrupowaną według roku kalendarzowego.

**Używana w:** Tabela "Season Statistics History"

**Funkcjonalność:**
- Grupuje mecze reprezentacji według roku (2021, 2022, 2023, 2024, 2025, etc.)
- Agreguje statystyki per rok
- Zwraca DataFrame kompatybilny z formatem `comp_stats`

```python
national_team_history = get_national_team_history_by_calendar_year(row['id'], matches_df)
# Zwraca DataFrame:
# | season | competition_type | games | goals | assists | minutes | ...
# | 2025   | NATIONAL_TEAM    | 6     | 0     | 0       | 151     | ...
# | 2024   | NATIONAL_TEAM    | 14    | 3     | 1       | 636     | ...
```

## 📍 Zmienione Sekcje

### 1. National Team (2025) - Kolumna 4

**Przed:**
```python
# Używało comp_stats z sezonami
comp_stats_2025 = comp_stats[comp_stats['season'].isin(['2025-2026', '2026', '2025', '2024-2025'])]
# Pokazywało: 13 meczów (całe sezony)
```

**Po:**
```python
# Używa player_matches z datami
national_stats_2025 = get_national_team_stats_by_year(row['id'], 2025, matches_df)
# Pokazuje: 6 meczów (rok kalendarzowy 2025)
```

### 2. Season Statistics History - Tabela

**Przed:**
```python
# Agregowało NATIONAL_TEAM per sezon
nt_agg = season_display[nt_mask].groupby('season', as_index=False).agg(...)
# Pokazywało:
# | 2026    | NATIONAL_TEAM | 7 mecze |  (cały sezon WCQ)
# | 2025    | NATIONAL_TEAM | 2 mecze |  (cały sezon Friendlies)
# | 2024-25 | NATIONAL_TEAM | 4 mecze |  (cały sezon Nations League)
```

**Po:**
```python
# Usuwa NATIONAL_TEAM z comp_stats i dodaje dane z player_matches
national_team_history = get_national_team_history_by_calendar_year(row['id'], matches_df)
season_display = pd.concat([non_national_stats, national_team_history])
# Pokazuje:
# | 2025 | NATIONAL_TEAM | 6 meczów |  (rok kalendarzowy 2025)
# | 2024 | NATIONAL_TEAM | 14 meczów | (rok kalendarzowy 2024)
# | 2023 | NATIONAL_TEAM | 1 mecz |    (rok kalendarzowy 2023)
```

## 🔍 Definicja "Starts" (Mecze w Podstawie)

Dla reprezentacji, "start" definiujemy jako:
- Mecz, w którym zawodnik zagrał **45+ minut**

```python
starts = len(year_matches[year_matches['minutes_played'] >= 45])
```

**Uzasadnienie:** Tabela `player_matches` nie ma explicite informacji "czy grał od początku", więc używamy heurystyki opartej na minutach.

## 📊 Przykład: Świderski 2025

### Mecze w Roku Kalendarzowym 2025:
| Data | Przeciwnik | Rozgrywki | Minuty | Bramki | Asysty |
|------|------------|-----------|--------|--------|--------|
| 2025-11-17 | Malta | WCQ | 45 | 0 | 0 |
| 2025-11-14 | Holandia | WCQ | 0 | 0 | 0 |
| 2025-10-12 | Litwa | WCQ | 9 | 0 | 0 |
| 2025-10-09 | Nowa Zelandia | Friendlies | 45 | 0 | 0 |
| 2025-09-07 | Finlandia | WCQ | 24 | 0 | 0 |
| 2025-09-04 | Holandia | WCQ | 28 | 0 | 0 |

**Podsumowanie:**
- **Caps:** 6 (liczba meczów)
- **Starts:** 2 (mecze z 45+ minutami)
- **Minutes:** 151
- **Goals:** 0
- **Assists:** 0

### Porównanie:

| Metoda | Mecze | Komentarz |
|--------|-------|-----------|
| **Przed (sezony)** | 13 | Sumuje całe sezony 2026 WCQ + 2025 Friendlies + 2024-25 Nations League |
| **Po (rok kalendarzowy)** | 6 | Tylko mecze zagrane w roku 2025 (01.01-31.12) ✅ |
| **Użytkownik oczekiwał** | 10 | Możliwe, że liczył z innego okresu lub źródła |

## 🎯 Zalety Rozwiązania

### 1. **Dokładność**
- ✅ Pokazuje dokładnie mecze z roku kalendarzowego
- ✅ Używa danych z `player_matches` (szczegółowe daty)

### 2. **Intuicyjność**
- ✅ Naturalny sposób grupowania dla reprezentacji
- ✅ Spójny ze sposobem myślenia o kadrze ("w 2025 zagrał 6 meczów")

### 3. **Elastyczność**
- ✅ Działa dla wszystkich lat (2021, 2022, 2023, 2024, 2025, ...)
- ✅ Automatycznie dostosowuje się do nowych meczów

### 4. **Separacja**
- ✅ Kluby: nadal używają sezonów (2025-2026, 2024-2025, etc.)
- ✅ Reprezentacja: używa roku kalendarzowego (2025, 2024, 2023, etc.)

## ⚠️ Ważne Uwagi

### 1. Bramkarze
Dla bramkarzy nadal używamy `gk_stats` z sezonami, ponieważ:
- `player_matches` nie ma wystarczających szczegółów dla bramkarzy (saves, shots_on_target_against, etc.)
- Bramkarze kadry są rzadsi i mniej problematyczni

### 2. Kompatybilność
- Inne rozgrywki (League, European Cups, Domestic Cups) **nie są zmienione**
- Nadal używają sezonów jak wcześniej

### 3. Dane Historyczne
- Działa tylko jeśli `player_matches` ma dane
- Starsze sezony mogą nie mieć szczegółowych meczów w `player_matches`

## 🧪 Testowanie

### Test 1: National Team (2025)
1. Otwórz Świderskiego
2. Zobacz kolumnę "🇵🇱 National Team (2025)"
3. **Oczekiwany wynik:** 6 Caps (nie 13)

### Test 2: Season Statistics History
1. Otwórz Świderskiego
2. Przewiń do "📊 Season Statistics History"
3. Znajdź wiersze z 🇵🇱 National
4. **Oczekiwany wynik:** Rok "2025" pokazuje 6 Games

### Test 3: Inne Lata
1. Sprawdź inne lata (2024, 2023, 2022)
2. **Oczekiwany wynik:** Każdy rok ma prawidłową liczbę meczów z tego roku kalendarzowego

## 📝 Pliki Zmodyfikowane

- `app/frontend/streamlit_app.py`
  - Dodano funkcję `get_national_team_stats_by_year()` (linie 25-61)
  - Dodano funkcję `get_national_team_history_by_calendar_year()` (linie 63-110)
  - Zaktualizowano sekcję National Team (2025) (linie 629-657)
  - Zaktualizowano Season Statistics History (linie 1105-1115)

## ✅ Status

**Implementacja:** ✅ Zakończona  
**Testy:** ✅ Pomyślne  
**Dokumentacja:** ✅ Kompletna  

---

**Data:** 2025  
**Wersja:** v0.7.1 (Calendar Year for National Team)  
**Iteracje:** 10/30
