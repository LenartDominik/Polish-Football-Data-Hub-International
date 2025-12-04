# 🎯 Podsumowanie komend synchronizacji - Grudzień 2025

> **Aktualne na grudzień 2025** | Obecny sezon: **2025-2026**

## 🚀 **Najważniejsze zmiany:**

### ✅ **Uproszczono system synchronizacji**
- **Usunięto:** Stare, nieużywane skrypty (`sync_player.py`, `sync_all_playwright.py`, `quick_add_player.py`)
- **Pozostawiono:** Tylko 2 komendy + automatyczny scheduler
- **Czystszy projekt:** Bez zbędnych plików

### ✅ **Automatyczny scheduler**
- Synchronizacja wszystkich graczy 3x w tygodniu
- Email powiadomienia po każdej synchronizacji
- Cron-job.org budzi backend przed synchronizacją

---

## 📋 **DOSTĘPNE KOMENDY**

### **1. Pełna synchronizacja (wszystkie sezony)**
```powershell
python sync_player_full.py "Jakub Kamiński" --all-seasons
```
**✅ Zwraca:** Competition stats + match logs ze wszystkich sezonów kariery

### **2. Tylko match logs (obecny sezon)**
```powershell
python sync_match_logs.py "Jakub Kamiński"
```
**✅ Zwraca:** Tylko szczegółowe match logs dla obecnego sezonu

---

## 🤖 **Automatyczna synchronizacja (Scheduler)**

**Backend na Render automatycznie synchronizuje wszystkich graczy:**
- **Poniedziałek i Czwartek o 6:00** - pełne statystyki
- **Wtorek o 7:00** - match logs
- **Email powiadomienia** po każdej synchronizacji

**Cron-job.org budzi backend 5 minut przed synchronizacją:**
- **5:55 (Pon/Czw)** - wake-up przed stats sync
- **6:55 (Wt)** - wake-up przed matchlogs sync

**Nie musisz ręcznie synchronizować** - scheduler robi to automatycznie! 🎉

---

## 🎯 **Kiedy której użyć?**

| Sytuacja | Komenda | Czas |
|----------|---------|------|
| **Nowy gracz w bazie** | `sync_player_full.py "Nazwisko" --all-seasons` | ~60s |
| **Aktualizacja gracza** | `sync_player_full.py "Nazwisko" --all-seasons` | ~60s |
| **Szybkie sprawdzenie meczów** | `sync_match_logs.py "Nazwisko"` | ~15s |
| **Aktualizacja całej bazy** | **Scheduler (automatycznie!)** | ~20-30 min |

**💡 Zalecenie:** Używaj schedulera do regularnych aktualizacji. Ręcznie synchronizuj tylko nowych graczy lub gdy potrzebujesz natychmiastowej aktualizacji.

---

## 📊 **API Endpointy (Swagger UI)**

**Dostęp:** http://localhost:8000/docs

### **Players**
- `GET /api/players` - Lista wszystkich graczy
- `GET /api/players/{id}` - Szczegóły gracza

### **Matchlogs** 
- `GET /api/matchlogs/{player_id}` - Lista meczów gracza
- `GET /api/matchlogs/{player_id}/stats` - Statystyki z meczów
- `GET /api/matchlogs/match/{match_id}` - Szczegóły meczu

### **Comparison**
- `GET /api/comparison/compare` - Porównaj graczy
- `GET /api/comparison/players/{id}/stats` - Statystyki do porównania

### **Filtry API**
```bash
# Filtruj po sezonie
curl "http://localhost:8000/api/matchlogs/5?season=2025-2026"
curl "http://localhost:8000/api/matchlogs/5?season=2024-2025"

# Filtruj po rozgrywkach
curl "http://localhost:8000/api/matchlogs/5?competition=La%20Liga"
```

---

## ⚡ **Quick Start dla nowych użytkowników**

```powershell
# 1. Sprawdź czy API działa
curl http://localhost:8000/health

# 2. Znajdź gracza w bazie  
curl http://localhost:8000/api/players | findstr "Kamiński"

# 3. Zsynchronizuj gracza
python sync_player.py "Jakub Kamiński"

# 4. Sprawdź rezultaty
curl "http://localhost:8000/api/matchlogs/5?season=2025-2026"
```

---

## 🌟 **Najważniejsze informacje**

- **Obecny sezon:** 2025-2026 (lipiec 2025 - czerwiec 2026)
- **Rate limit:** 12 sekund między requestami FBref
- **Scheduler:** Automatyczna synchronizacja 2x w tygodniu
- **Dokumentacja:** /docs i /redoc już zaktualizowane
- **Główna komenda:** `python sync_player.py "Nazwisko"`

---

**💡 Pamiętaj:** Jeśli nie jesteś pewien, użyj `python sync_player.py "Nazwisko"` - to najczęściej używana komenda!