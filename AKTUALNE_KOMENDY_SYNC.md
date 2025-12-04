# 🚀 Aktualny przewodnik po komendach synchronizacji

> **Stan na grudzień 2025** - Obecny sezon: **2025-2026**

## 📋 **Dostępne komendy**

### **1. Pełna synchronizacja - wszystkie sezony**
```powershell
python sync_player_full.py "Jakub Kamiński" --all-seasons
```
**Co robi:** Competition stats + match logs ze wszystkich sezonów kariery

### **2. Tylko match logs - obecny sezon**
```powershell
python sync_match_logs.py "Jakub Kamiński"
```
**Co robi:** Tylko szczegółowe match logs dla obecnego sezonu (2025-2026)

---

## 📊 **Porównanie komend**

| Komenda | Competition Stats | Match Logs | Sezony | Czas |
|---------|------------------|------------|--------|------|
| `sync_player_full.py "Nazwisko" --all-seasons` | ✅ | ✅ | Wszystkie | ~60s |
| `sync_match_logs.py "Nazwisko"` | ❌ | ✅ | Obecny | ~15s |

---

## 🎯 **Które użyć kiedy?**

### **Nowy gracz - pełne dane:**
```powershell
python sync_player_full.py "Nowy Gracz" --all-seasons
```

### **Aktualizacja istniejącego gracza:**
```powershell
python sync_player_full.py "Lewandowski" --all-seasons
```

### **Tylko sprawdzenie ostatnich meczów:**
```powershell
python sync_match_logs.py "Lewandowski"
```

---

## ⚠️ **Ważne informacje**

- **Obecny sezon**: 2025-2026 (lipiec 2025 - czerwiec 2026)
- **Poprzedni sezon**: 2024-2025 (lipiec 2024 - czerwiec 2025)
- **Domyślny sezon**: Zawsze obecny (2025-2026)
- **Rate limit**: 12 sekund między requestami do FBref
- **Automatyczna synchronizacja**: Scheduler na Render (Pon/Czw 6:00, Wt 7:00)

---

## 🤖 **Automatyczna synchronizacja (Scheduler)**

Backend na Render automatycznie synchronizuje wszystkich graczy:
- **Stats sync:** Poniedziałek i Czwartek o 6:00
- **Matchlogs sync:** Wtorek o 7:00
- **Email powiadomienia:** Po każdej synchronizacji

**Nie musisz ręcznie synchronizować** - scheduler robi to automatycznie!

---

**💡 Tip:** Do codziennych aktualizacji użyj schedulera (automatyczny). Ręcznie synchronizuj tylko nowych graczy lub gdy potrzebujesz natychmiastowej aktualizacji!