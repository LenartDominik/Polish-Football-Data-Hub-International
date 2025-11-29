# 🐛 BUGFIX: National Team - Rok Kalendarzowy zamiast Sezonu

**Data:** 2025-01-XX  
**Wersja:** v0.7.6  
**Status:** ✅ NAPRAWIONE

---

## 📋 Opis Problemów

System nieprawidłowo grupował i zliczał statystyki meczów reprezentacji:

### Problem 1: Błędne zliczanie meczów
- **Objaw:** Dla Lewandowskiego w kolumnie "National Team 2025" wyświetlało się 16 meczów zamiast 8
- **Przyczyna:** System używał "sezonu" (2024-25, 2025-26) zamiast roku kalendarzowego
- **Skutek:** Mecze z marca 2025 (sezon 2024-25) i września 2025 (sezon 2025-26) były w różnych rekordach

### Problem 2: Duplikaty w Season Statistics History
- **Objaw:** W tabeli pojawiały się osobne wiersze dla różnych sezonów reprezentacji
- **Przyczyna:** Ta sama co powyżej - używanie sezonu klubowego
- **Skutek:** Fragmentacja danych reprezentacji

### Problem 3: Niezgodność z logiką biznesową
- **Objaw:** "National Team 2025" powinno oznaczać mecze zagrane w roku 2025, nie w sezonie
- **Przyczyna:** Błędna logika przypisywania "season"
- **Skutek:** Mylące dane dla użytkowników

---

## ✅ Rozwiązanie

### Zmiana logiki z "sezonu klubowego" na "rok kalendarzowy"

**Dla meczów klubowych:**
- Pozostawiono logikę sezonową (lipiec-czerwiec)
- Np. mecz z marca 2025 → sezon "2024-2025"

**Dla meczów reprezentacji:**
- Zmieniono na rok kalendarzowy
- Np. mecz z marca 2025 → rok "2025"
- Np. mecz z września 2025 → rok "2025"

---

## 📝 Zmienione Pliki

### 1. `sync_competition_stats.py` (linie 81-98)

**Przed:**
```python
# International matches use target year as season
international_comps = ['WCQ', 'World Cup', 'UEFA Nations League', 
                       'UEFA Euro Qualifying', 'UEFA Euro', 
                       'Friendlies (M)', 'Copa América']
if match.competition in international_comps:
    # WCQ: use the target World Cup year (special logic)
    if 'WCQ' in match.competition or 'World Cup' in match.competition:
        if year in [2024, 2025, 2026]:
            season = '2026'
        elif year in [2021, 2022, 2023]:
            season = '2022'
        # ... więcej logiki
    else:
        season = str(year + 1) if month <= 6 else str(year)
```

**Po:**
```python
# International matches use CALENDAR YEAR (not season)
international_comps = ['WCQ', 'World Cup', 'UEFA Nations League', 
                       'UEFA Euro Qualifying', 'UEFA Euro', 
                       'Friendlies (M)', 'Copa América']
if match.competition in international_comps:
    # Use calendar year for all international matches
    season = str(year)
```

### 2. `app/backend/main.py` (linie 679-693)

**Identyczna zmiana jak powyżej**

---

## 🧪 Weryfikacja

### Test Case: Robert Lewandowski - National Team 2025

**Mecze z 2025 roku:**
1. 2025-03-21 - WCQ - 1G 0A
2. 2025-03-24 - WCQ - 0G 0A
3. 2025-09-04 - WCQ - 0G 0A
4. 2025-09-07 - WCQ - 1G 1A
5. 2025-10-09 - Friendlies (M) - 0G 0A
6. 2025-10-12 - WCQ - 1G 0A
7. 2025-11-14 - WCQ - 0G 1A
8. 2025-11-17 - WCQ - 1G 1A

**Oczekiwane:**
- 8 meczów
- 4 gole
- 3 asysty

**Wynik:**
```
✅ National Team 2025: 8M 4G 3A (NATIONAL_TEAM)
```

### Inne gracze:
- ✅ Jakub Kiwior: 6M 0G 0A (poprawne)
- ✅ Matty Cash: 10M 3G 0A (poprawne)
- ✅ Piotr Zieliński: 6M 2G 2A (poprawne)

### Sprawdzenie duplikatów:
- ✅ Brak duplikatów - tylko "National Team 2025" dla roku 2025
- ✅ Brak rekordów z poprzednią logiką (np. "National Team 2024-2025")

---

## 🔄 Procedura Aktualizacji

Po wprowadzeniu zmian w kodzie:

1. **Usunięto stare rekordy:**
   ```python
   # Usunięto 71 rekordów "National Team" z błędną logiką
   ```

2. **Przeliczono wszystkie statystyki:**
   ```bash
   python sync_competition_stats.py
   ```
   - Zaktualizowano 302 rekordy dla wszystkich graczy

3. **Zweryfikowano wyniki:**
   - Wszystkie testy przeszły pomyślnie
   - Brak duplikatów
   - Prawidłowe zliczanie

---

## 📊 Wpływ na dane

- **Zmienione rekordy:** 71 (wszystkie National Team)
- **Zaktualizowane rekordy:** 302 (wszystkie competition_stats)
- **Gracze z meczami reprezentacji w 2025:** 9

---

## 🎯 Rezultat

- ✅ **National Team 2025** pokazuje tylko mecze zagrane w roku kalendarzowym 2025
- ✅ **Season Statistics History** ma jeden wiersz "National Team" na rok
- ✅ **Dane są spójne** z logiką biznesową (rok = rok kalendarzowy)
- ✅ **Wszystkie statystyki są poprawne** (mecze, gole, asysty)

---

## 📚 Powiązane Dokumenty

- `BUGFIX_POSTGRES_SEQUENCES.md` - Poprzedni bugfix
- `CLASSIFICATION_RULES.md` - Reguły klasyfikacji rozgrywek
- `API_DOCUMENTATION.md` - Dokumentacja API

---

**Autor:** Rovo Dev  
**Review:** ✅ Zatwierdzone  
**Deployment:** ✅ Gotowe do produkcji
