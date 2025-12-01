# ❓ FAQ - Matchlogs Scheduler

## Najczęściej Zadawane Pytania

### 🚀 Podstawowe

#### Q: Co to jest matchlogs scheduler?
**A:** Automatyczne zadanie, które raz w tygodniu (wtorek 7:00) synchronizuje szczegółowe statystyki z każdego meczu dla wszystkich graczy w bazie. Zbiera 23 różne pola danych na mecz.

#### Q: Czy to działa bez mojej interwencji?
**A:** Tak! Wystarczy ustawić `ENABLE_SCHEDULER=true` w `.env` i uruchomić backend. Scheduler będzie działał w tle 24/7.

#### Q: Ile to kosztuje?
**A:** $0! Działa za darmo na Render.com (free tier).

---

### ⏰ Harmonogram

#### Q: Kiedy dokładnie działa scheduler?
**A:** 
- **Stats Sync**: Poniedziałek i Czwartek o 6:00
- **Matchlogs Sync**: Wtorek o 7:00
- **Timezone**: Europe/Warsaw (konfigurowalne)

#### Q: Dlaczego wtorek o 7:00?
**A:** Bo daje to czas po synchronizacji statystyk w poniedziałek. Matchlogi są zazwyczaj dostępne dzień po meczu.

#### Q: Czy mogę zmienić godzinę?
**A:** Tak, ale musisz edytować `app/backend/main.py`. Szukaj `CronTrigger(day_of_week='tue', hour=7, ...)`.

---

### 🔧 Konfiguracja

#### Q: Jak włączyć scheduler?
**A:** 
```bash
# W pliku .env
ENABLE_SCHEDULER=true
```

#### Q: Czy muszę konfigurować email?
**A:** Nie! Email jest opcjonalny. Scheduler działa bez niego. Email to tylko monitoring.

#### Q: Jak sprawdzić czy scheduler działa?
**A:** 
```bash
curl http://localhost:8000/
```
Sprawdź sekcję `"scheduler"` w odpowiedzi.

---

### 📊 Dane

#### Q: Jakie dane są zbierane?
**A:** Dla każdego meczu: data, przeciwnik, wynik, minuty, gole, asysty, xG, xA, strzały, podania, dryblingi, odbiory, kartki i więcej (23 pola).

#### Q: Czy dane są zapisywane lokalnie?
**A:** Tak, w SQLite (plik `players.db`). Na Render używaj persistent disk.

#### Q: Jak długo przechowywane są dane?
**A:** Zawsze. Dane są zastępowane przy każdej synchronizacji (usuwa stare, dodaje nowe).

---

### 🕸️ Scraping

#### Q: Skąd pochodzą dane?
**A:** Z FBref.com - profesjonalnej strony ze statystykami piłkarskimi.

#### Q: Czy to legalne?
**A:** Tak, respektujemy ToS FBref - 12 sekund między requestami (rate limiting).

#### Q: Co jeśli FBref zmieni strukturę strony?
**A:** Scraper może przestać działać. Będzie trzeba zaktualizować kod w `fbref_playwright_scraper.py`.

---

### 📧 Email

#### Q: Jak skonfigurować email?
**A:** Zobacz `EMAIL_SETUP_GUIDE.md`. Dla Gmail użyj App Password.

#### Q: Dlaczego nie dostaje email?
**A:** 
1. Sprawdź spam folder
2. Sprawdź konfigurację SMTP w `.env`
3. Dla Gmail użyj App Password (nie zwykłe hasło)
4. Zobacz logi: `⚠️ Email not configured`

#### Q: Czy dostanę email po każdej synchronizacji?
**A:** Tak, jeśli email jest skonfigurowany:
- **Zielony header** dla stats sync (Pon/Czw)
- **Niebieski header** dla matchlogs sync (Wtorek)

---

### 🐛 Problemy

#### Q: Scheduler nie startuje
**A:**
1. Sprawdź `ENABLE_SCHEDULER=true` w `.env`
2. Sprawdź logi: `⏸️ Scheduler disabled`
3. Restartuj backend

#### Q: Matchlogi nie są synchronizowane
**A:**
1. Sprawdź czy gracz ma FBref ID (`api_id` lub `fbref_id`)
2. Jeśli nie ma: `python sync_player.py "Nazwa Gracza"`
3. Sprawdź logi dla szczegółów błędu

#### Q: Synchronizacja trwa wieczność
**A:** To normalne! Dla 100+ graczy: ~20-30 minut (rate limiting 12s).

#### Q: Niektórzy gracze nie są synchronizowani
**A:** 
1. Sprawdź email notification - lista failed players
2. Sprawdź logi backendu
3. Spróbuj manualnie: `python sync_match_logs.py "Nazwa"`

---

### 🌐 API

#### Q: Jak zobaczyć matchlogi gracza?
**A:**
```bash
curl http://localhost:8000/api/players/1/matches
```

#### Q: Jak filtrować po sezonie?
**A:**
```bash
curl http://localhost:8000/api/players/1/matches?season=2025-2026
```

#### Q: Gdzie jest dokumentacja API?
**A:** 
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Plik: `API_ENDPOINTS_GUIDE.md`

---

### ☁️ Deployment

#### Q: Czy działa na Render.com?
**A:** Tak! Zobacz `RENDER_DEPLOYMENT.md` dla instrukcji.

#### Q: Czy muszę płacić za Render?
**A:** Nie! Free tier wystarcza (750h/miesiąc).

#### Q: Jak sprawdzić czy scheduler działa na Render?
**A:** Otwórz URL swojego API + `/health` w przeglądarce.

---

### 💾 Baza Danych

#### Q: Gdzie są przechowywane matchlogi?
**A:** W tabeli `player_matches` w SQLite.

#### Q: Jak eksportować dane?
**A:** 
```bash
# Przez API
curl http://localhost:8000/api/players/1/matches > matches.json

# Bezpośrednio z bazy
sqlite3 players.db "SELECT * FROM player_matches;"
```

#### Q: Czy mogę użyć PostgreSQL zamiast SQLite?
**A:** Tak, zmień `DATABASE_URL` w `.env`. SQLAlchemy wspiera PostgreSQL.

---

### 🔄 Synchronizacja

#### Q: Czy mogę uruchomić sync manualnie?
**A:** Tak!
```bash
python sync_match_logs.py "Robert Lewandowski"
```

#### Q: Czy mogę zsynchronizować wszystkich graczy teraz?
**A:** Tak, ale to zajmie ~20-30 minut:
```bash
# Będzie trzeba napisać prosty skrypt lub poczekać na scheduler
```

#### Q: Co jeśli synchronizacja nie powiedzie się?
**A:** Sprawdź email notification (lista failed players) i logi. Spróbuj ponownie dla konkretnego gracza.

---

### ⚡ Wydajność

#### Q: Dlaczego rate limiting 12 sekund?
**A:** To respektuje Terms of Service FBref. Nie zmieniaj tej wartości!

#### Q: Czy mogę przyspieszyć synchronizację?
**A:** Nie. 12s to minimum zgodne z ToS. Szybsza synchronizacja = ban z FBref.

#### Q: Ile zajmuje pamięci?
**A:** ~100-200MB RAM dla backendu + Playwright. Free tier Render (512MB) wystarcza.

---

### 🎯 Features

#### Q: Czy jest dashboard do oglądania matchlogs?
**A:** Nie w v0.6.0. To jest planowane na przyszłość. Na razie: API + Swagger UI.

#### Q: Czy mogę porównać matchlogi dwóch graczy?
**A:** Nie bezpośrednio. Możesz pobrać dane przez API i porównać samodzielnie.

#### Q: Czy są statystyki trendów?
**A:** Nie w v0.6.0. Endpoint `summary` daje podstawowe agregacje.

---

### 📚 Dokumentacja

#### Q: Gdzie znajdę więcej informacji?
**A:**
- Quick start: `QUICKSTART_MATCHLOGS.md`
- Pełna docs: `MATCHLOGS_SCHEDULER.md`
- API: `API_ENDPOINTS_GUIDE.md`
- Email: `EMAIL_SETUP_GUIDE.md`
- Indeks: `DOKUMENTACJA_INDEX.md`

#### Q: Czy jest tutorial wideo?
**A:** Nie. Dokumentacja tekstowa jest bardzo szczegółowa.

---

### 🔐 Bezpieczeństwo

#### Q: Czy moje dane są bezpieczne?
**A:** Tak. Wszystko działa lokalnie lub na Twoim Render account. Żadne dane nie są wysyłane do osób trzecich (poza FBref do scrapingu).

#### Q: Co z App Password dla Gmail?
**A:** To bezpieczne. App Password ma ograniczone uprawnienia i może być odwołane w każdej chwili.

#### Q: Czy ktoś może zobaczyć moją bazę danych?
**A:** Nie, jeśli używasz Render. Baza jest prywatna dla Twojego service.

---

### 🛠️ Rozwój

#### Q: Czy mogę dodać własne pola do matchlogs?
**A:** Tak, ale musisz:
1. Edytować model `PlayerMatch` w `app/backend/models/player_match.py`
2. Stworzyć migrację Alembic
3. Zaktualizować scraper

#### Q: Czy mogę przyczynić się do projektu?
**A:** Tak! To open source. Fork na GitHub i submit PR.

#### Q: Gdzie zgłaszać bugi?
**A:** GitHub Issues (jeśli projekt jest na GitHub) lub bezpośrednio do maintainera.

---

### 💡 Wskazówki

#### Q: Jaki jest najlepszy workflow?
**A:**
1. Włącz scheduler (`ENABLE_SCHEDULER=true`)
2. Skonfiguruj email (opcjonalnie)
3. Deploy na Render.com
4. Sprawdzaj email raporty
5. Używaj API do analiz

#### Q: Jak zacząć od zera?
**A:**
1. Przeczytaj `README.md`
2. Przeczytaj `QUICKSTART_MATCHLOGS.md`
3. Uruchom backend lokalnie
4. Przetestuj przez Swagger UI
5. Deploy na Render

#### Q: Co jeśli coś nie działa?
**A:**
1. Sprawdź logi backendu
2. Zobacz `MATCHLOGS_SCHEDULER.md` → Troubleshooting
3. Zobacz FAQ (ten plik)
4. Szukaj w dokumentacji: `DOKUMENTACJA_INDEX.md`

---

## 🆘 Nie znalazłeś odpowiedzi?

### Sprawdź:
1. **Dokumentację:** `DOKUMENTACJA_INDEX.md` - indeks wszystkich docs
2. **Logi:** Backend console output
3. **Swagger UI:** http://localhost:8000/docs
4. **Email notification:** Szczegóły błędów

### Dalej problem?
1. Przeczytaj `MATCHLOGS_SCHEDULER.md` → Troubleshooting
2. Sprawdź GitHub Issues (jeśli projekt jest public)
3. Kontakt z maintainerem

---

## 🎉 Podsumowanie

**Most common issues:**
1. ❌ Scheduler disabled → `ENABLE_SCHEDULER=true`
2. ❌ Brak FBref ID → `python sync_player.py "Nazwa"`
3. ❌ Email nie działa → Użyj App Password dla Gmail
4. ❌ Długa synchronizacja → To normalne (12s rate limit)

**Most common questions answered!** ✅

---

**Wersja:** v0.6.0  
**Ostatnia aktualizacja:** 2025-01-28  
**Pytań w FAQ:** 50+

**Masz inne pytanie? Dodaj issue na GitHub!** 🚀
