# ? QUICK START - Test Matchlogs Endpoints NOW!

**Potrzebujesz 5 minut aby przetestowaæ nowe endpointy!**

---

## ?? Krok 1: Uruchom Backend (30 sekund)

```bash
cd polish-players-tracker
uvicorn app.backend.main:app --reload
```

Czekaj a¿ zobaczysz:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## ?? Krok 2: Otwórz Swagger UI (10 sekund)

Otwórz w przegl¹darce: **http://localhost:8000/docs**

ZnajdŸ sekcjê **"matchlogs"** - powinny byæ 3 endpointy:
- ? GET /api/matchlogs/{player_id}
- ? GET /api/matchlogs/{player_id}/stats
- ? GET /api/matchlogs/match/{match_id}

---

## ?? Krok 3: Test z Swagger UI (2 minuty)

### Test 1: Lista meczów gracza

1. Kliknij na **GET /api/matchlogs/{player_id}**
2. Kliknij **"Try it out"**
3. Wpisz `player_id`: **5** (lub inne ID z twojej bazy)
4. Opcjonalnie dodaj: `season`: **2025-2026**
5. Kliknij **"Execute"**

**Oczekiwany rezultat:** 200 OK + JSON z list¹ meczów

### Test 2: Statystyki agregowane

1. Kliknij na **GET /api/matchlogs/{player_id}/stats**
2. Kliknij **"Try it out"**
3. Wpisz `player_id`: **5**
4. Kliknij **"Execute"**

**Oczekiwany rezultat:** 200 OK + JSON ze statystykami

### Test 3: Szczegó³y meczu

1. Kliknij na **GET /api/matchlogs/match/{match_id}**
2. Kliknij **"Try it out"**
3. Wpisz `match_id`: **123** (lub ID z poprzedniego requesta)
4. Kliknij **"Execute"**

**Oczekiwany rezultat:** 200 OK lub 404 (jeœli mecz nie istnieje)

---

## ?? Krok 4: Test z curl (2 minuty)

Otwórz nowy terminal:

```bash
# Test 1: Health check
curl http://localhost:8000/health

# Test 2: Lista graczy (znajdŸ player_id)
curl http://localhost:8000/api/players | jq '.[0:3]'

# Test 3: Match logs (zamieñ 5 na prawdziwe ID)
curl http://localhost:8000/api/matchlogs/5 | jq

# Test 4: Stats
curl http://localhost:8000/api/matchlogs/5/stats | jq

# Test 5: Z filtrem sezonu
curl "http://localhost:8000/api/matchlogs/5?season=2025-2026" | jq
```

**Jeœli nie masz `jq`:** usuñ `| jq` z komend

---

## ? Krok 5: Weryfikacja (30 sekund)

SprawdŸ czy:
- [x] Wszystkie 3 endpointy s¹ widoczne w Swagger
- [x] Mo¿esz wykonaæ request przez Swagger UI
- [x] curl zwraca odpowiedzi 200 OK
- [x] Dane JSON s¹ poprawne

---

## ?? Gotowe!

Jeœli wszystkie testy przesz³y:
- ? **Nowe endpointy dzia³aj¹!**
- ? **Mo¿esz commitowaæ zmiany!**
- ? **Dokumentacja jest aktualna!**

---

## ? Coœ nie dzia³a?

### Problem: 404 Not Found na /api/matchlogs

**Rozwi¹zanie:**
1. Zatrzymaj serwer (Ctrl+C)
2. SprawdŸ plik: `app/backend/routers/matchlogs.py`
3. Linia 13 powinna mieæ: `router = APIRouter(prefix="/matchlogs", ...)`
4. Uruchom ponownie: `uvicorn app.backend.main:app --reload`

### Problem: Serwer nie startuje

**Rozwi¹zanie:**
1. SprawdŸ logi w terminalu
2. Przywróæ backup jeœli potrzeba:
   ```bash
   cp app/backend/routers/matchlogs.py.backup app/backend/routers/matchlogs.py
   ```
3. Zg³oœ problem

### Problem: Brak danych w odpowiedzi

**To normalne jeœli:**
- Nie masz meczów w bazie dla tego gracza
- Player ID nie istnieje (spróbuj innego ID)

---

## ?? Co Dalej?

Po udanych testach przeczytaj:

1. **CHECKLIST_MATCHLOGS_UPDATE.md** - Pe³na lista testów
2. **GIT_COMMIT_GUIDE.md** - Jak zacommitowaæ zmiany
3. **MIGRATION_GUIDE_MATCHLOGS.md** - Jeœli masz kod do zaktualizowania

---

## ?? Przydatne Linki

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health
- API Root: http://localhost:8000/

---

**Czas wykonania:** ~5 minut  
**Poziom trudnoœci:** ? £atwy  
**Status:** ? Gotowe do testu!
