# 🚀 Aktualny przewodnik po komendach synchronizacji

> **Stan na grudzień 2025** - Obecny sezon: **2025-2026**

## 📋 **Szybkie komendy**

### **1. Pojedynczy gracz - obecny sezon**
```powershell
python sync_player.py "Jakub Kamiński"
```
**Co robi:** Competition stats + match logs dla sezonu 2025-2026

### **2. Pojedynczy gracz - konkretny sezon**
```powershell
python sync_player.py "Jakub Kamiński" --season=2024-2025
```
**Co robi:** Competition stats + match logs dla wybranego sezonu

### **3. Wszystkie sezony gracza**
```powershell
python sync_player_full.py "Jakub Kamiński"
```
**Co robi:** Competition stats + match logs ze wszystkich sezonów kariery

### **4. Tylko match logs**
```powershell
python sync_match_logs.py "Jakub Kamiński"
```
**Co robi:** Tylko szczegółowe match logs dla obecnego sezonu (2025-2026)

---

## 📊 **Porównanie komend**

| Komenda | Competition Stats | Match Logs | Sezony | Czas |
|---------|------------------|------------|--------|------|
| `sync_player.py "Nazwisko"` | ✅ | ✅ | Obecny (2025-2026) | ~15s |
| `sync_player.py "Nazwisko" --season=X` | ✅ | ✅ | Wybrany | ~15s |
| `sync_player.py "Nazwisko" --all-seasons` | ✅ | ❌ | Wszystkie | ~30-60s |
| `sync_player_full.py "Nazwisko"` | ✅ | ✅ | Wszystkie | ~60s |
| `sync_match_logs.py "Nazwisko"` | ❌ | ✅ | Obecny | ~15s |

---

## 🎯 **Które użyć kiedy?**

### **Codzienne aktualizacje:**
```powershell
python sync_player.py "Lewandowski"
```

### **Po przerwie reprezentacyjnej:**
```powershell
python sync_player.py "Lewandowski" --season=2024-2025  # eliminacje MŚ
python sync_player.py "Lewandowski"                     # obecny sezon
```

### **Nowy gracz - pełne dane:**
```powershell
python sync_player_full.py "Nowy Gracz"
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

---

## 🔧 **Opcje dodatkowe**

```powershell
# Zobacz przeglądarkę (debug)
python sync_player.py "Nazwisko" --visible

# Wszystkie gracze w bazie
python sync_all_playwright.py

# Wszystkie gracze - wszystkie sezony (ostrożnie!)
python sync_all_playwright.py --all-seasons
```

---

**💡 Tip:** Jeśli nie jesteś pewien, użyj `sync_player.py "Nazwisko"` - to najczęściej używana komenda!