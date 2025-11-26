# 🏆 Competition Classification Rules

## 📋 Overview

This document explains how competitions are classified in the Polish Players Tracker system.

---

## 🎯 Competition Types

### 1. **LEAGUE** (Liga krajowa)
League competitions in each country.

**Examples:**
- Bundesliga (Germany)
- La Liga (Spain)
- Serie A (Italy)
- Premier League (England)
- Ligue 1 (France)
- Ekstraklasa (Poland)
- MLS (USA)

---

### 2. **DOMESTIC_CUP** (Puchary krajowe)
National cup competitions and supercups.

**Examples:**
- 🇩🇪 DFB-Pokal, DFL-Supercup
- 🇪🇸 Copa del Rey, Supercopa de España
- 🇮🇹 Coppa Italia, Supercoppa
- 🇬🇧 FA Cup, EFL Cup (Carabao Cup)
- 🇫🇷 Coupe de France
- 🇺🇸 U.S. Open Cup, Leagues Cup

**Important:** These are checked FIRST in the scraper to avoid conflicts with European competitions.

---

### 3. **EUROPEAN_CUP** (Puchary europejskie)
UEFA club competitions and international tournaments.

**Examples:**
- Champions League (UCL)
- Europa League (UEL)
- Europa Conference League (UECL)
- UEFA Super Cup
- Club World Cup

---

### 4. **NATIONAL_TEAM** (Reprezentacja narodowa)
International matches for national teams.

**Examples:**
- World Cup (WC)
- World Cup Qualifying (WCQ)
- UEFA Euro
- UEFA Euro Qualifying
- UEFA Nations League
- Friendlies

---

## 🔧 Scraper Logic

### Priority Order (IMPORTANT!)

The scraper checks competition types in this order:

1. **DOMESTIC_CUP** (checked first)
2. **EUROPEAN_CUP** (checked second)
3. **NATIONAL_TEAM** (checked third)
4. **LEAGUE** (default if no match)

**Why this order?**
- Some competitions have "Cup" in the name (e.g., "FA Cup", "Copa del Rey")
- If we check European keywords first, they might match "Cup" and be misclassified
- By checking domestic cups FIRST, we ensure correct classification

### Keyword Lists

#### Domestic Cup Keywords (checked first):
```python
domestic_cup_keywords = [
    'copa del rey', 'copa', 'pokal', 'coupe', 'coppa',
    'fa cup', 'league cup', 'efl', 'carabao',
    'dfb-pokal', 'dfl-supercup', 'supercopa', 'supercoppa',
    'u.s. open cup', 'leagues cup'
]
```

#### European Cup Keywords:
```python
european_keywords = [
    'champions', 'europa', 'uefa', 'conference',
    'champions lg', 'europa lg', 'ucl', 'uel', 'uecl',
    'european', 'cup winners', 'super cup', 'club world cup'
]
```

---

## 📊 Display in Streamlit App

### Column Layout:

```
[Column 1]          [Column 2]           [Column 3]            [Column 4]
League Stats        European Cups        Domestic Cups         National Team
(2025-2026)         (2025-2026)          (2025-2026)           (2025)
─────────────────   ──────────────────   ──────────────────    ─────────────────
Bundesliga          Champions League     DFB-Pokal             WCQ
La Liga             Europa League        Copa del Rey          Friendlies
Serie A             Conference League    Coppa Italia          Nations League
Premier League      Super Cup            FA Cup                Euro Qualifying
```

### Season Statistics Table:

Shows all competitions with their correct type:
- Liga → "League"
- Puchary europejskie → "European Cup"
- Puchary krajowe → "Domestic Cup"
- Reprezentacja → "National Team"

---

## ✅ Verification

Run this command to verify all classifications are correct:

```bash
python verify_domestic_cups.py
```

Expected output:
```
✅ NO CUPS WRONGLY CLASSIFIED AS LEAGUE
✅ Total DOMESTIC_CUP records: 69
✅ VERIFICATION PASSED
```

---

## 🔄 Historical Fixes

### January 2025 Fix #2 (Season 2025-2026)
- **Issue:** 4 domestic cup records in 2025-2026 were classified as LEAGUE
- **Affected:** DFB-Pokal (2 players), EFL Cup (2 players)
- **Root Cause:** Bug in `sync_playwright.py` line 133 - DOMESTIC_CUP was converted to LEAGUE
- **Fixed:** Updated conversion logic and `get_competition_type()` function
- **Solution:** Added DOMESTIC_CUP handling in both sync_playwright.py and main.py
- **Script:** `fix_domestic_cups_2025.py`

### January 2025 Fix #1
- **Issue:** 29 domestic cup records were classified as LEAGUE
- **Fixed:** Updated database and scraper priority order
- **Solution:** Check domestic cups FIRST before European competitions

### November 2024 Fix  
- **Issue:** National team data not displaying
- **Fixed:** Added proper enum conversion
- **Solution:** Updated CompetitionType enum handling in models

---

## 🎯 Best Practices

### For Developers:

1. **Always check domestic cups FIRST** in classification logic
2. **Use specific keywords** (e.g., "copa del rey" not just "copa")
3. **Test with multiple players** from different leagues
4. **Run verification script** after database changes

### For Maintenance:

1. **After scraper changes:** Run full sync and verification
2. **New competition added:** Update keyword lists
3. **Classification error found:** Check scraper priority order

---

## 📝 Files Involved

### Scraper:
- `app/backend/services/fbref_playwright_scraper.py` (Lines 321-338, 464-478)

### Sync Scripts:
- `sync_playwright.py` (Competition type conversion)

### Verification:
- `verify_domestic_cups.py` (Classification verification)

### Models:
- `app/backend/models/competition_stats.py` (CompetitionType enum)
- `app/backend/models/goalkeeper_stats.py` (CompetitionType enum)

---

**Last Updated:** January 2025  
**Status:** ✅ All classifications working correctly
