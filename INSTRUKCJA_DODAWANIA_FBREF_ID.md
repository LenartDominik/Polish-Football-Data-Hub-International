# 📝 Instrukcja Dodawania FBref ID

**Data:** 2025-11-25  
**Graczy bez FBref ID:** 19

---

## 🎯 Cel

Dodać FBref ID dla 19 graczy, którzy nie mogą być synchronizowani automatycznie.

---

## 📋 Lista Graczy Bez FBref ID

### Do znalezienia:

1. **Radosław Żelazny** - AS Roma
2. **Jakub Zieliński** - Wolfsburg (GK)
3. **Cezary Miszta** - Rio Ave (GK)
4. **Karol Linetty** - Kocaelispor (MF)
5. **Mateusz Wieteska** - Kocaelispor (DF)
6. **Mateusz Lis** - Göztepe (GK)
7. **Albert Posiadała** - Samsunspor (GK)
8. **Jakub Moder** - Feyenoord (MF)
9. **Przemysław Tytoń** - Twente (GK)
10. **Paweł Bochniewicz** - Heerenveen (DF)
... i 9 innych

---

## 🔍 Jak Znaleźć FBref ID?

### Krok 1: Wyszukaj gracza na FBref

Idź na: https://fbref.com/en/search/search.fcgi

Wpisz nazwisko gracza, np.: **"Jakub Moder"**

### Krok 2: Otwórz profil gracza

Kliknij w nazwisko gracza z wyników wyszukiwania.

### Krok 3: Skopiuj ID z URL

URL będzie wyglądać tak:
```
https://fbref.com/en/players/XXXXXXXX/Jakub-Moder
                              ^^^^^^^^
                              TO JEST FBREF ID
```

**Przykład:**
```
https://fbref.com/en/players/8d78e732/Robert-Lewandowski
```
FBref ID = `8d78e732`

---

## 💾 Metoda 1: Ręczna Aktualizacja SQL (Prostsza)

### Krok 1: Otwórz bazę danych

```bash
cd polish-players-tracker
sqlite3 players.db
```

### Krok 2: Zaktualizuj gracza

```sql
-- Sprawdź ID gracza w bazie
SELECT id, name FROM players WHERE name LIKE '%Moder%';

-- Zaktualizuj FBref ID
UPDATE players SET api_id = 'xxxxxxxxx' WHERE id = 57;

-- Sprawdź czy zapisało się
SELECT id, name, api_id FROM players WHERE id = 57;

-- Wyjdź
.quit
```

### Przykład dla Jakuba Modera:

```sql
-- Znajdź ID gracza w bazie (np. 57)
SELECT id, name FROM players WHERE name = 'Jakub Moder';

-- Dodaj FBref ID (np. 'abc12345')
UPDATE players SET api_id = 'abc12345' WHERE id = 57;
```

---

## 🐍 Metoda 2: Python Script (Szybsza dla wielu)

### Krok 1: Stwórz plik `add_fbref_ids.py`

```python
import sqlite3

# Słownik: ID gracza w bazie -> FBref ID
fbref_ids = {
    7: 'xxxxxxxxx',   # Radosław Żelazny
    18: 'xxxxxxxxx',  # Jakub Zieliński
    48: 'xxxxxxxxx',  # Cezary Miszta
    52: 'xxxxxxxxx',  # Karol Linetty
    53: 'xxxxxxxxx',  # Mateusz Wieteska
    55: 'xxxxxxxxx',  # Mateusz Lis
    56: 'xxxxxxxxx',  # Albert Posiadała
    57: 'xxxxxxxxx',  # Jakub Moder
    58: 'xxxxxxxxx',  # Przemysław Tytoń
    59: 'xxxxxxxxx',  # Paweł Bochniewicz
    # ... dodaj resztę
}

conn = sqlite3.connect('players.db')
cursor = conn.cursor()

for player_id, fbref_id in fbref_ids.items():
    cursor.execute(
        'UPDATE players SET api_id = ? WHERE id = ?',
        (fbref_id, player_id)
    )
    print(f'✅ Zaktualizowano gracza ID {player_id}: api_id = {fbref_id}')

conn.commit()
conn.close()

print(f'\n✅ Zaktualizowano {len(fbref_ids)} graczy')
```

### Krok 2: Uruchom skrypt

```bash
cd polish-players-tracker
python add_fbref_ids.py
```

---

## 🔄 Metoda 3: Użyj Istniejącego Skryptu

Projekt ma już skrypt do dodawania graczy ręcznie!

### `quick_add_player.py`

```python
# Otwórz plik: polish-players-tracker/quick_add_player.py
# Zmodyfikuj na górze:

player_data = {
    'name': 'Jakub Moder',
    'team': 'Feyenoord',
    'league': 'Eredivisie',
    'position': 'Midfielder',
    'is_goalkeeper': False,
    'api_id': 'XXXXXXXX'  # <- DODAJ FBREF ID TUTAJ
}
```

Uruchom:
```bash
python quick_add_player.py
```

---

## 📝 Przykład Krok po Kroku: Jakub Moder

### 1. Znajdź na FBref:
```
https://fbref.com/en/search/search.fcgi?search=Jakub+Moder
```

### 2. Otwórz profil, skopiuj ID z URL:
```
https://fbref.com/en/players/abc12345/Jakub-Moder
                              ^^^^^^^^
```

### 3. Zaktualizuj w bazie:
```sql
sqlite3 players.db
UPDATE players SET api_id = 'abc12345' WHERE name = 'Jakub Moder';
.quit
```

### 4. Synchronizuj:
```bash
python sync_playwright.py "Jakub Moder"
```

### 5. Sprawdź w aplikacji:
```
http://localhost:8501/
# Wyszukaj "Moder" - powinien mieć statystyki!
```

---

## ⚡ Szybki Szablon SQL (dla wszystkich 19)

```sql
-- Otwórz bazę
sqlite3 players.db

-- Dodaj wszystkie FBref ID na raz (wypełnij ID-ki):

UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 7;   -- Radosław Żelazny
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 18;  -- Jakub Zieliński
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 48;  -- Cezary Miszta
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 52;  -- Karol Linetty
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 53;  -- Mateusz Wieteska
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 55;  -- Mateusz Lis
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 56;  -- Albert Posiadała
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 57;  -- Jakub Moder
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 58;  -- Przemysław Tytoń
UPDATE players SET api_id = 'xxxxxxxx' WHERE id = 59;  -- Paweł Bochniewicz
-- ... dodaj resztę 9 graczy

-- Sprawdź ile zaktualizowano
SELECT COUNT(*) FROM players WHERE api_id IS NOT NULL AND api_id != '';

-- Wyjdź
.quit
```

---

## 🎯 Workflow

1. **Znajdź FBref ID** (10 graczy = ~10 minut)
2. **Dodaj do bazy** (SQL lub Python)
3. **Synchronizuj** (`python sync_all_playwright.py`)
4. **Sprawdź w aplikacji** (http://localhost:8501)

---

## 📊 Weryfikacja

### Sprawdź ile graczy ma FBref ID:

```sql
sqlite3 players.db
SELECT COUNT(*) FROM players WHERE api_id IS NOT NULL AND api_id != '';
.quit
```

**Przed:** 79  
**Po dodaniu 19:** 98 ✅

---

## ⚠️ Ważne Uwagi

### 1. Format FBref ID:
- 8 znaków alfanumerycznych
- Przykład: `8d78e732`
- **NIE:** pełny URL

### 2. Nie dla wszystkich może być dostępny:
- Młodzi gracze (rezerwy)
- Gracze bez meczów w statystykach FBref
- **Rozwiązanie:** Pomiń tych graczy lub usuń z bazy

### 3. Po dodaniu FBref ID:
- Musisz zsynchronizować gracza: `python sync_playwright.py "Imię Nazwisko"`
- LUB czekać na automatyczną synchronizację (scheduler)

---

## 🚀 Po Dodaniu Wszystkich ID

```bash
# Synchronizuj wszystkich graczy
python sync_all_playwright.py

# Czas: ~16 minut (98 graczy × 12s)

# Sprawdź w aplikacji
streamlit run app/frontend/streamlit_app.py
```

---

## ✅ Checklist

- [ ] Znaleźć FBref ID dla 19 graczy
- [ ] Dodać ID do bazy (SQL lub Python)
- [ ] Zweryfikować: `SELECT COUNT(*) FROM players WHERE api_id IS NOT NULL`
- [ ] Synchronizować: `python sync_all_playwright.py`
- [ ] Sprawdzić w aplikacji: http://localhost:8501

---

## 💡 Porady

**Najszybsza metoda:**
1. Otwórz https://fbref.com w jednej karcie
2. Otwórz `sqlite3 players.db` w terminalu
3. Dla każdego gracza:
   - Wyszukaj na FBref → skopiuj ID z URL
   - `UPDATE players SET api_id = 'xxx' WHERE id = YY;`
4. Zamknij: `.quit`
5. Synchronizuj: `python sync_all_playwright.py`

**Czas:** ~20 minut dla 19 graczy

---

**Powodzenia! 🚀**

Jeśli masz problem z konkretnym graczem - daj znać!
