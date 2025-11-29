# Bugfix: PostgreSQL Sequence Desynchronization

## Problem
Podczas synchronizacji danych gracza za pomocą `sync_player_full.py` pojawiał się błąd:

```
psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "competition_stats_pkey"
DETAIL:  Key (id)=(543) already exists.
```

## Przyczyna
W PostgreSQL sekwencje auto-incrementu (sequences) nie są automatycznie resetowane po usunięciu rekordów z tabeli. Gdy skrypt:
1. Usuwa stare rekordy gracza (`DELETE FROM competition_stats WHERE player_id = X`)
2. Dodaje nowe rekordy
3. Sekwencja próbuje użyć ID, które już istnieje w bazie

## Rozwiązanie

### 1. Zmiany w skryptach synchronizacyjnych

Dodano funkcję `reset_sequences_if_needed()` do następujących skryptów:
- ✅ `sync_player_full.py` - pełna synchronizacja gracza
- ✅ `sync_match_logs.py` - synchronizacja match logs
- ✅ `sync_playwright.py` - główny skrypt synchronizacji

Funkcja automatycznie resetuje sekwencje PostgreSQL po usunięciu danych:

```python
def reset_sequences_if_needed(db):
    """Reset PostgreSQL sequences to avoid ID conflicts after bulk deletes"""
    try:
        db_url = str(db.bind.url)
        if 'postgresql' in db_url or 'postgres' in db_url:
            logger.info("🔧 Resetting PostgreSQL sequences...")
            db.execute(text("SELECT setval('competition_stats_id_seq', (SELECT COALESCE(MAX(id), 1) FROM competition_stats));"))
            db.execute(text("SELECT setval('goalkeeper_stats_id_seq', (SELECT COALESCE(MAX(id), 1) FROM goalkeeper_stats));"))
            db.execute(text("SELECT setval('player_matches_id_seq', (SELECT COALESCE(MAX(id), 1) FROM player_matches));"))
            db.commit()
            logger.info("✅ Sequences reset successfully")
    except Exception as e:
        logger.warning(f"⚠️ Could not reset sequences: {e}")
```

Ta funkcja jest wywoływana automatycznie po każdym usunięciu rekordów w `sync_competition_stats()`.

### 2. Narzędzie naprawcze: `fix_postgres_sequences.py`

Stworzono oddzielny skrypt do ręcznego resetowania sekwencji:

```bash
python fix_postgres_sequences.py
```

Ten skrypt można uruchomić w każdej chwili, jeśli pojawi się problem z sekwencjami.

## Jak korzystać

### Normalna synchronizacja (już naprawiona)

Wszystkie skrypty synchronizacyjne automatycznie resetują sekwencje:

```bash
# Pełna synchronizacja gracza (competition stats + match logs)
python sync_player_full.py "Karol Świderski" --all-seasons

# Synchronizacja match logs
python sync_match_logs.py "Robert Lewandowski" --season 2024-2025

# Główny skrypt synchronizacji (wszystkie gracze lub pojedynczy)
python sync_playwright.py --all-seasons
python sync_playwright.py --player "Zieliński"
```

Wszystkie skrypty automatycznie resetują sekwencje podczas działania.

### Ręczne resetowanie sekwencji (jeśli potrzebne)
```bash
python fix_postgres_sequences.py
```

## Dodatkowe zmiany

1. **Import SQLAlchemy text()**: Dodano `from sqlalchemy import text` do obsługi surowych zapytań SQL
2. **Flush po delete**: Dodano `db.flush()` po operacji `delete()` dla prawidłowego oczyszczenia sesji
3. **Automatyczna detekcja**: Skrypt wykrywa automatycznie, czy używany jest PostgreSQL

## Testowanie

Problem został przetestowany i rozwiązany:
- ✅ Synchronizacja Świderskiego działa poprawnie
- ✅ 35 competition stats zsynchronizowanych bez błędów
- ✅ Sekwencje automatycznie resetowane podczas operacji

## Uwagi techniczne

- Rozwiązanie działa tylko dla PostgreSQL (SQLite nie ma tego problemu)
- Sekwencje są resetowane do `MAX(id) + 1` z każdej tabeli
- Nie wpływa na inne operacje bazodanowe
- Kompatybilne z istniejącymi skryptami synchronizacji

## Data naprawy
Styczeń 2025
