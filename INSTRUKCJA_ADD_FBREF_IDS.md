# 🚀 Instrukcja: Dodawanie FBref ID (add_fbref_ids.py)

**Data:** 2025-11-25  
**Script:** `add_fbref_ids.py`

---

## 🎯 Cel

Ułatwienie dodawania FBref ID dla 19 graczy bez api_id w bazie danych.

---

## 📝 Instrukcja Krok po Kroku

### Krok 1: Znajdź FBref ID dla graczy

1. **Idź na FBref:**
   ```
   https://fbref.com/en/search/search.fcgi
   ```

2. **Wyszukaj gracza** (np. "Jakub Moder")

3. **Otwórz profil gracza**

4. **Skopiuj ID z URL:**
   ```
   https://fbref.com/en/players/abc12345/Jakub-Moder
                                ^^^^^^^^
                                TO JEST ID (8 znaków)
   ```

---

### Krok 2: Edytuj plik `add_fbref_ids.py`

Otwórz plik i znajdź słownik `fbref_ids` (linie ~20-55):

```python
fbref_ids = {
    # Format: player_id_in_database: 'fbref_id'
    
    # ========== PRIORITY 1: Main Squad Players ==========
    57: 'abc12345',  # Jakub Moder (Feyenoord, MF) - WPISZ ID TUTAJ
    52: 'def67890',  # Karol Linetty (Kocaelispor, MF) - WPISZ ID TUTAJ
    # ... itd.
}
```

**Przykład - przed:**
```python
57: '',  # Jakub Moder (Feyenoord, MF)
```

**Przykład - po:**
```python
57: 'abc12345',  # Jakub Moder (Feyenoord, MF)
```

---

### Krok 3: Uruchom script

```bash
cd polish-players-tracker
python add_fbref_ids.py
```

---

## 📊 Co Robi Script?

### 1. Sprawdza bazę danych
```
🔧 FBref ID Update Script
================================================================================

📊 Status:
   ✅ FBref IDs filled: 5
   ⚠️  FBref IDs missing: 14
```

### 2. Pokazuje co zostanie zaktualizowane
```
🔄 Ready to update 5 player(s):

    57. Jakub Moder                    → abc12345
    52. Karol Linetty                  → def67890
    53. Mateusz Wieteska               → ghi11111
    ...
```

### 3. Pyta o potwierdzenie
```
Continue? (yes/no): yes
```

### 4. Aktualizuje bazę danych
```
🔄 Updating database...

   ✅ Jakub Moder                    (ID: 57) → abc12345
   ✅ Karol Linetty                  (ID: 52) → def67890
   ✅ Mateusz Wieteska               (ID: 53) → ghi11111
```

### 5. Pokazuje wynik i następne kroki
```
✅ Update Complete!
================================================================================

📊 Results:
   ✅ Updated: 5
   ❌ Errors: 0
   ⚠️  Still missing: 14

🔄 Next Steps:

   1. Synchronize updated players:
      # Removed - use scheduler on Render (automatic sync Mon/Thu/Tue)

   2. Or synchronize individual players:
      python sync_player_full.py "Jakub Moder" --all-seasons
      python sync_player_full.py "Karol Linetty" --all-seasons
      
   3. Check the frontend:
      streamlit run app/frontend/streamlit_app.py
```

---

## 🎯 Lista Graczy (Priorytet)

### Priority 1: Main Squad Players (5)
- **57** - Jakub Moder (Feyenoord, MF)
- **52** - Karol Linetty (Kocaelispor, MF)
- **53** - Mateusz Wieteska (Kocaelispor, DF)
- **59** - Paweł Bochniewicz (Heerenveen, DF)
- **60** - Szymon Włodarczyk (Excelsior, FW)

### Priority 2: Goalkeepers (6)
- **48** - Cezary Miszta (Rio Ave, GK)
- **55** - Mateusz Lis (Göztepe, GK)
- **56** - Albert Posiadała (Samsunspor, GK)
- **58** - Przemysław Tytoń (Twente, GK)
- **61** - Filip Bednarek (Sparta Rotterdam, GK)
- **18** - Jakub Zieliński (Wolfsburg, GK, U19) - może nie mieć

### Priority 3: Other Players (4)
- **105** - Karol Angielski (AEK Larnaca, FW)
- **104** - Piotr Parzyszek (KuPS, FW)
- **102** - Miłosz Trojak (Ulsan HD, DF)
- **82** - Bartosz Szywała (Slavia Praga)
- **92** - Daniel Baran (FC Dallas)
- **83** - Eryk Łukaszka (FK Bodø/Glimt II) - może nie mieć

### Priority 4: Youth/Uncertain (2)
- **7** - Radosław Żelazny (AS Roma) - młodzieżówka?
- **103** - Jan Ziółkowski (Roma, DF) - młodzieżówka?

---

## ⚡ Szybki Workflow

### Opcja A: Dodaj wszystkie naraz (20 min)

1. Znajdź wszystkie 19 ID na FBref (~15 min)
2. Wpisz do `add_fbref_ids.py` (~3 min)
3. Uruchom script (~1 min)
4. Synchronizuj: `# Removed - use scheduler on Render (automatic sync Mon/Thu/Tue)` (~16 min)

**Total: ~36 minut**

---

### Opcja B: Dodaj tylko priorytetowe (10 min)

1. Znajdź 5 ID (Priority 1) na FBref (~5 min)
2. Wpisz do `add_fbref_ids.py` (~2 min)
3. Uruchom script (~1 min)
4. Synchronizuj tylko tych 5: (~2 min)
   ```bash
   python sync_player_full.py "Jakub Moder" --all-seasons
   python sync_player_full.py "Karol Linetty" --all-seasons
   # ... etc
   ```

**Total: ~10 minut**

---

## ⚠️ Ważne Uwagi

### 1. Format FBref ID:
✅ **Poprawny:** `'abc12345'` (8 znaków, w cudzysłowie)  
❌ **Błędny:** `abc12345` (bez cudzysłowu)  
❌ **Błędny:** `'https://fbref.com/en/players/abc12345/Player'` (pełny URL)

### 2. Niektórzy gracze mogą nie mieć FBref ID:
- Młodzieżówka bez meczów
- Rezerwy bez występów
- **Rozwiązanie:** Zostaw puste `''` - script pominie

### 3. Po dodaniu ID:
- **MUSISZ** zsynchronizować gracza: `python sync_player_full.py "Imię Nazwisko" --all-seasons`
- LUB czekać na automatyczną synchronizację (scheduler)

---

## 🧪 Testowanie

### Test 1: Dry run (bez wypełnionych ID)
```bash
python add_fbref_ids.py
```

**Oczekiwany wynik:**
```
❌ No FBref IDs provided!

📝 Instructions:
   1. Open this file: add_fbref_ids.py
   ...
```

### Test 2: Dodaj 1 gracza
```python
fbref_ids = {
    57: 'abc12345',  # Jakub Moder
}
```

```bash
python add_fbref_ids.py
```

**Oczekiwany wynik:**
```
✅ Updated: 1
```

### Test 3: Sprawdź w bazie
```bash
sqlite3 players.db
SELECT id, name, api_id FROM players WHERE id = 57;
.quit
```

**Oczekiwany wynik:**
```
57|Jakub Moder|abc12345
```

---

## 🔧 Troubleshooting

### Problem: "Database not found"
```
❌ Database not found: polish-players-tracker/players.db
```

**Rozwiązanie:**
```bash
# Upewnij się, że jesteś w głównym katalogu projektu
cd polish-players-tracker
python add_fbref_ids.py
```

---

### Problem: "Player ID not found"
```
⚠️  Player ID 999 not found in database
```

**Rozwiązanie:**
- Sprawdź czy ID gracza jest poprawne
- Użyj SQL aby zobaczyć wszystkich graczy:
```bash
sqlite3 players.db
SELECT id, name FROM players WHERE api_id IS NULL OR api_id = '';
.quit
```

---

### Problem: Błędny format ID
```python
# ❌ BŁĄD
57: abc12345,  # Brak cudzysłowu

# ✅ POPRAWNIE
57: 'abc12345',  # Z cudzysłowem
```

---

## 📖 Przykład Pełnego Workflow

```bash
# 1. Znajdź FBref ID
# Idź na https://fbref.com
# Wyszukaj "Jakub Moder"
# URL: https://fbref.com/en/players/abc12345/Jakub-Moder
# Skopiuj: abc12345

# 2. Edytuj plik
nano add_fbref_ids.py
# Zmień linię 29:
# 57: 'abc12345',  # Jakub Moder

# 3. Uruchom script
python add_fbref_ids.py
# Wpisz: yes

# 4. Synchronizuj
python sync_player_full.py "Jakub Moder" --all-seasons

# 5. Sprawdź w aplikacji
streamlit run app/frontend/streamlit_app.py
# Wyszukaj "Moder" - powinien mieć statystyki!
```

---

## ✅ Checklist

- [ ] Stworzyłem plik `add_fbref_ids.py` w głównym katalogu
- [ ] Znalazłem FBref ID na https://fbref.com
- [ ] Edytowałem słownik `fbref_ids` w pliku
- [ ] Uruchomiłem script: `python add_fbref_ids.py`
- [ ] Script zaktualizował bazę danych
- [ ] Zsynchronizowałem graczy: `# Removed - use scheduler on Render (automatic sync Mon/Thu/Tue)`
- [ ] Sprawdziłem w aplikacji: http://localhost:8501

---

**Powodzenia! 🚀**
