# 🤖 Scheduler - Status i Monitoring

## 📊 Sprawdzanie Statusu Schedulera

### 1. **Health Check Endpoint**

Podstawowe info o schedulerem:

```bash
curl https://your-backend.onrender.com/health
```

**Odpowiedź:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00",
  "scheduler_running": true
}
```

---

### 2. **API Root Endpoint** (szczegółowe info)

Pełna informacja o schedulerem i następnych synchronizacjach:

```bash
curl https://your-backend.onrender.com/
```

**Odpowiedź zawiera:**
```json
{
  "scheduler": {
    "enabled": true,
    "stats_sync_schedule": "Monday & Thursday at 06:00 (Europe/Warsaw)",
    "matchlogs_sync_schedule": "Tuesday at 07:00 (Europe/Warsaw)",
    "next_stats_sync": "2024-01-18 06:00:00+01:00",
    "next_matchlogs_sync": "2024-01-16 07:00:00+01:00"
  }
}
```

---

## ⚙️ Konfiguracja Schedulera na Renderze

### Wymagane Zmienne Środowiskowe

W **Render Dashboard** → Twój backend → **Environment**:

#### **Podstawowe (wymagane)**
```
ENABLE_SCHEDULER=true
SCHEDULER_TIMEZONE=Europe/Warsaw
DATABASE_URL=postgresql://postgres.xxx:password@...
```

#### **Email Notifications (opcjonalne, ale zalecane)**
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=recipient@example.com
```

**💡 Uwaga:** Bez konfiguracji email, scheduler będzie działał, ale nie będzie wysyłał powiadomień.

---

## 📅 Harmonogram Synchronizacji

### **Stats Sync** (statystyki graczy)
- **Kiedy:** Poniedziałek i Czwartek o **06:00** (Europe/Warsaw)
- **Dlaczego:** 
  - Poniedziałek - po meczach weekendowych
  - Czwartek - po meczach Ligi Mistrzów (środa)
- **Czas trwania:** ~20-40 minut (zależnie od liczby graczy)
- **Rate limiting:** 12 sekund między graczami

### **Matchlogs Sync** (szczegóły meczów)
- **Kiedy:** Wtorek o **07:00** (Europe/Warsaw)
- **Dlaczego:** Daje czas na aktualizację stats w poniedziałek
- **Czas trwania:** ~30-60 minut (zależnie od liczby graczy i meczów)
- **Rate limiting:** 12 sekund między graczami

---

## 📧 Email Notifications

### Co otrzymasz po zakończeniu sync?

#### **Stats Sync Email**
```
Subject: 🤖 Scheduler Sync Complete: 25/28 Players Synced

Polish Players Tracker - Scheduled Sync Report
============================================================

Status: ✅ SUCCESS

Players Synced: 25/28 (89.3%)
Failed: 3
Duration: 32.5 minutes

Failed Players:
- Jan Kowalski
- Piotr Nowak
- Adam Zieliński
```

#### **Matchlogs Sync Email**
```
Subject: 📋 Matchlogs Sync Complete: 150 Matches from 25/28 Players

Polish Players Tracker - Matchlogs Sync Report
============================================================

Status: ✅ SUCCESS

Players Synced: 25/28 (89.3%)
Total Matches Synced: 150
Failed: 3
Duration: 45.2 minutes
```

### Kiedy NIE dostaniesz emaila?

- Email nie jest skonfigurowany (brak SMTP_* zmiennych)
- SMTP credentials są nieprawidłowe
- W logach zobaczysz: `⚠️ Email not configured - skipping notification`

---

## 🔍 Monitoring w Render Logs

### Co szukać w logach?

#### **Scheduler Start (przy uruchomieniu backendu)**
```
🚀 Aplikacja startuje...
📅 Initializing scheduler...
✅ Scheduler uruchomiony
📅 Stats sync schedule: Thursday & Monday at 06:00 (Europe/Warsaw)
📅 Matchlogs sync schedule: Tuesday at 07:00 (Europe/Warsaw)
📅 Next stats sync: 2024-01-18 06:00:00+01:00
📅 Next matchlogs sync: 2024-01-16 07:00:00+01:00
```

#### **Podczas Synchronizacji Stats**
```
============================================================
🤖 SCHEDULED SYNC STARTED
============================================================
📊 Total players to sync: 28

[1/28] 🔄 Syncing: Robert Lewandowski
✅ Successfully synced: Robert Lewandowski

[2/28] 🔄 Syncing: Wojciech Szczęsny
✅ Successfully synced: Wojciech Szczęsny

...

============================================================
✅ SCHEDULED SYNC COMPLETE
📊 Results: 25 synced, 3 failed out of 28 total
⏱️ Duration: 32.5 minutes
============================================================
```

#### **Podczas Synchronizacji Matchlogs**
```
============================================================
📋 SCHEDULED MATCHLOGS SYNC STARTED
============================================================
📊 Total players to sync match logs: 28

[1/28] 📋 Syncing match logs: Robert Lewandowski
✅ Successfully synced 8 matches for Robert Lewandowski

...

============================================================
✅ SCHEDULED MATCHLOGS SYNC COMPLETE
📊 Results: 25 players synced, 150 total matches, 3 failed out of 28 total
⏱️ Duration: 45.2 minutes
============================================================
```

#### **Scheduler Wyłączony**
```
🚀 Aplikacja startuje...
⏸️ Scheduler disabled (set ENABLE_SCHEDULER=true to enable)
```

---

## ❓ FAQ

### Czy scheduler zużywa free tier Render?

**Tak, ale mądrze:**
- Render Free Tier: 750h/miesiąc
- Backend działa 24/7: ~720h/miesiąc
- Synchronizacje: ~2h/tydzień (8h/miesiąc)
- **Total:** ~728h/miesiąc ✅ Mieści się w limicie!

### Czy mogę zmienić harmonogram?

**Tak!** Edytuj w `app/backend/main.py`:

```python
# Stats sync - zmień dzień/godzinę
scheduler.add_job(
    scheduled_sync_all_players,
    CronTrigger(day_of_week='thu,mon', hour=6, minute=0, timezone=timezone_str),
    ...
)

# Matchlogs sync - zmień dzień/godzinę
scheduler.add_job(
    scheduled_sync_matchlogs,
    CronTrigger(day_of_week='tue', hour=7, minute=0, timezone=timezone_str),
    ...
)
```

**Przykłady:**
- `day_of_week='mon,wed,fri'` - poniedziałek, środa, piątek
- `hour=8, minute=30` - 08:30
- `day='1,15'` - 1. i 15. dzień miesiąca

### Czy mogę ręcznie uruchomić sync?

**Tak!** Przez API:

**Manual Stats Sync (pojedynczy gracz):**
```bash
curl -X POST https://your-backend.onrender.com/api/players/1/sync
```

**Manual Matchlogs Sync (pojedynczy gracz):**
```bash
curl -X POST https://your-backend.onrender.com/api/players/1/sync-matchlogs
```

**Manual Full Sync (pojedynczy gracz):**
```bash
curl -X POST https://your-backend.onrender.com/api/players/1/sync-full
```

### Jak wyłączyć scheduler?

**W Render Dashboard:**
1. Environment → znajdź `ENABLE_SCHEDULER`
2. Zmień na `false`
3. Save Changes → Manual Deploy

Lub usuń zmienną całkowicie.

### Co jeśli sync failuje?

**Scheduler kontynuuje:**
- Loguje błędy dla konkretnych graczy
- Próbuje dalej z pozostałymi
- Wysyła email z listą failed players
- Następna synchronizacja odbędzie się zgodnie z harmonogramem

**W emailu zobaczysz:**
```
Failed Players:
- Jan Kowalski
- Piotr Nowak
```

**W logach:**
```
❌ Failed to sync player 'Jan Kowalski': 404 Not Found
```

---

## 🛠️ Troubleshooting

### Scheduler nie uruchamia się

**Sprawdź:**
1. Czy `ENABLE_SCHEDULER=true` w Render Environment?
2. Czy backend się w ogóle uruchomił? (sprawdź logi)
3. Czy `DATABASE_URL` jest poprawne?
4. Czy w logach jest: `⏸️ Scheduler disabled`?

### Email nie przychodzi

**Sprawdź:**
1. Czy wszystkie zmienne SMTP są ustawione?
2. Czy hasło to **App Password** (nie hasło do Gmail)?
3. Czy w logach jest: `⚠️ Email not configured - skipping notification`?
4. Sprawdź SPAM folder

**Gmail App Password:**
1. Google Account → Security → 2-Step Verification (włącz)
2. Security → App passwords → Generate
3. Użyj wygenerowanego hasła jako `SMTP_PASSWORD`

### Synchronizacja trwa za długo

**To normalne!**
- Rate limiting: 12 sekund między graczami
- 30 graczy × 12 sekund = 6 minut czystego czekania
- Plus scraping + zapisywanie do DB
- **Oczekiwany czas:** 20-60 minut

**⚠️ Nie skracaj rate limiting!** FBref może zablokować IP.

---

## 📚 Powiązane Dokumenty

- **TROUBLESHOOTING_DATABASE.md** - Problemy z połączeniem DB
- **RENDER_DEPLOYMENT.md** - Deployment setup
- **EMAIL_SETUP_GUIDE.md** - Szczegóły konfiguracji email
- **SCHEDULER_DOKUMENTACJA.md** - Techniczna dokumentacja schedulera

---

## ✅ Checklist: Scheduler Działa Poprawnie

- [ ] W logach przy starcie: `✅ Scheduler uruchomiony`
- [ ] W logach: `📅 Next stats sync: [data]`
- [ ] W logach: `📅 Next matchlogs sync: [data]`
- [ ] `/health` endpoint zwraca `"scheduler_running": true`
- [ ] `/` endpoint pokazuje `"enabled": true` i daty next sync
- [ ] Email przychodzi po każdej synchronizacji (jeśli skonfigurowany)
- [ ] Dane w bazie są aktualizowane automatycznie
