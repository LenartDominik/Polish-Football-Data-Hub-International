# 🎯 Podsumowanie komend synchronizacji - Grudzień 2025

> **Aktualne na grudzień 2025** | Obecny sezon: **2025-2026**

## 🚀 **Najważniejsze zmiany:**

### ✅ **Naprawiono `sync_playwright.py` → `sync_player.py`**
- **Przed:** Tylko competition stats (duplikował spotkania)
- **Teraz:** Competition stats + match logs (bez duplikatów)
- **Przemianowano** dla lepszej czytelności

### ✅ **Zaktualizowano dokumentację**
- 25+ plików .md zaktualizowanych
- README.md, instrukcje, przewodniki
- API docs (/docs, /redoc) - już aktualne

---

## 📋 **WSZYSTKIE DOSTĘPNE KOMENDY**

### **1. Synchronizacja gracza - obecny sezon (GŁÓWNA)**
```powershell
python sync_player.py "Jakub Kamiński"
```
**✅ Zwraca:** Competition stats + match logs dla sezonu 2025-2026

### **2. Synchronizacja gracza - konkretny sezon**
```powershell
python sync_player.py "Jakub Kamiński" --season=2024-2025
```
**✅ Zwraca:** Competition stats + match logs dla wybranego sezonu

### **3. Pełna synchronizacja (wszystkie sezony)**
```powershell
python sync_player_full.py "Jakub Kamiński"
```
**✅ Zwraca:** Competition stats + match logs ze wszystkich sezonów kariery

### **4. Tylko match logs**
```powershell
python sync_match_logs.py "Jakub Kamiński"
```
**✅ Zwraca:** Tylko szczegółowe match logs dla obecnego sezonu

### **5. Wszystkie sezony gracza (tylko competition stats)**
```powershell
python sync_player.py "Jakub Kamiński" --all-seasons
```
**✅ Zwraca:** Competition stats ze wszystkich sezonów (bez match logs)

### **6. Wszyscy gracze (obecny sezon)**
```powershell
python sync_all_playwright.py
```
**✅ Zwraca:** Competition stats + match logs dla wszystkich graczy (sezon 2025-2026)

### **7. Wszyscy gracze (wszystkie sezony)**
```powershell
python sync_all_playwright.py --all-seasons
```
**⚠️ Uwaga:** Bardzo czasochłonne (2-3h)

---

## 🎯 **Kiedy której użyć?**

| Sytuacja | Komenda | Czas |
|----------|---------|------|
| **Codzienna aktualizacja** | `sync_player.py "Nazwisko"` | ~15s |
| **Sprawdzenie konkretnego sezonu** | `sync_player.py "Nazwisko" --season=2024-2025` | ~15s |
| **Nowy gracz w bazie** | `sync_player_full.py "Nazwisko"` | ~60s |
| **Szybkie sprawdzenie meczów** | `sync_match_logs.py "Nazwisko"` | ~15s |
| **Aktualizacja całej bazy** | `sync_all_playwright.py` | ~20 min |

---

## 🔧 **Opcje dodatkowe**

```powershell
# Zobacz co się dzieje w przeglądarce
python sync_player.py "Nazwisko" --visible

# Używaj FBref ID zamiast wyszukiwania
python sync_player.py "Nazwisko" --use-id
```

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