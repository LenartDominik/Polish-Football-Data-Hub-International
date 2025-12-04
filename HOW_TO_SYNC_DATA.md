# 🔄 Jak Zsynchronizować Dane - Brakujące Mecze

## 🎯 Problem

W bazie danych brakuje **1 meczu WCQ** dla Lewandowskiego i Świderskiego w roku 2025.

**Aktualnie w bazie:**
- Lewandowski: 7 WCQ → powinno być 8
- Świderski: 7 WCQ → powinno być 8

**Potrzebna aktualizacja danych z FBref.**

---

## 🚀 Jak Zsynchronizować Dane

### Metoda 1: Pełna synchronizacja gracza (Zalecane)

```powershell
cd polish-players-tracker
python sync_player_full.py "Nazwisko Gracza" --all-seasons
```

Ten skrypt:
- Pobiera najnowsze dane z FBref
- Aktualizuje `competition_stats`
- Aktualizuje `player_matches`
- Synchronizuje wszystkie sezony kariery

### Metoda 2: Match Logs Sync (tylko mecze)

```bash
cd polish-players-tracker
python sync_match_logs.py "Nazwisko Gracza"
```

### Metoda 3: Automatyczna synchronizacja (najlepsze!)

Backend na Render automatycznie synchronizuje wszystkich graczy:
- **Poniedziałek i Czwartek o 6:00** - pełne statystyki
- **Wtorek o 7:00** - match logs
- **Email powiadomienia** po każdej synchronizacji

**Nie musisz nic robić - scheduler robi to za Ciebie!** 🤖

---

## ⏱️ Czas Wykonania

- **sync_player_full.py**: ~60 sekund (jeden gracz, wszystkie sezony)
- **sync_match_logs.py**: ~15 sekund (tylko mecze, jeden gracz)
- **Scheduler (automatyczny)**: ~20-30 minut (wszyscy gracze)

---

## ✅ Co Zostanie Zaktualizowane

### Tabele w bazie:
1. **competition_stats** - statystyki per sezon/rozgrywki
2. **player_matches** - szczegółowe mecze z datami
3. **season_stats** - statystyki sezonowe

### Dla reprezentacji:
- WCQ (Eliminacje MŚ 2026)
- Friendlies (Mecze towarzyskie)
- Inne rozgrywki reprezentacji

---

## 🔍 Po Synchronizacji - Weryfikacja

### Sprawdź Lewandowskiego:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('players.db')
query = """
SELECT season, competition_name, games
FROM competition_stats
WHERE player_id = 1
AND competition_type = 'NATIONAL_TEAM'
AND season = '2026'
"""
df = pd.read_sql_query(query, conn)
print(df)
conn.close()
```

**Oczekiwany wynik:** WCQ = 8 meczów

### Sprawdź Świderskiego:

```python
query = """
SELECT season, competition_name, games
FROM competition_stats
WHERE player_id = 72
AND competition_type = 'NATIONAL_TEAM'
AND season = '2026'
"""
```

**Oczekiwany wynik:** WCQ = 8 meczów

---

## 📊 Po Aktualizacji - Oczekiwane Wyniki w Aplikacji

### Lewandowski - National Team (2025):
- **Caps: 10** (8 WCQ + 2 Friendlies) *← zaktualizowane*

### Świderski - National Team (2025):
- **Caps: 10** (8 WCQ + 2 Friendlies) *← zaktualizowane*

---

## ⚠️ Uwagi

### 1. Wymagane Uprawnienia
Scraper potrzebuje dostępu do internetu i może wymagać:
- Playwright browsers zainstalowane
- Odpowiednie uprawnienia do zapisu w bazie

### 2. Czas Wykonania
Synchronizacja może zająć kilka minut. Poczekaj aż się zakończy.

### 3. Backup
Przed synchronizacją możesz zrobić backup bazy:
```bash
copy players.db players.db.backup
```

---

## 🐛 Jeśli Synchronizacja Nie Działa

### Problem 1: Brak Playwright
```bash
pip install playwright
playwright install
```

### Problem 2: Błędy scrapera
Sprawdź logi w:
- `sync_playwright_*.log`
- Konsola terminala

### Problem 3: Baza zablokowana
Zamknij aplikację Streamlit przed synchronizacją:
```bash
# W terminalu gdzie jest Streamlit naciśnij Ctrl+C
```

---

## 🎯 Alternatywne Rozwiązanie (Tymczasowe)

Jeśli nie możesz uruchomić synchronizacji, mogę:

1. **Ręcznie zmienić filtr** w aplikacji, żeby pokazywał liczby przybliżone
2. **Dodać komentarz** w aplikacji wyjaśniający rozbieżność
3. **Czekać** na Twoją synchronizację danych

**Które rozwiązanie preferujesz?**

---

## 📞 Co Dalej?

Po zsynchronizowaniu danych:
1. Uruchom aplikację ponownie
2. Sprawdź czy Lewandowski i Świderski mają po 10 meczów
3. Jeśli tak - problem rozwiązany! ✅
4. Jeśli nie - zgłoś mi szczegóły

---

**Status:** ⏳ Czeka na synchronizację danych
