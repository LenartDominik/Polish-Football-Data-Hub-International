# 🚀 Migracja SQLite → Supabase PostgreSQL

## 📌 Dlaczego Supabase?
- ✅ **Darmowe NA ZAWSZE** (500 MB storage, 2 GB transfer/mies, 50k API requests/day)
- ✅ PostgreSQL (prawdziwa baza dla produkcji)
- ✅ Automatyczne backupy
- ✅ Dashboard do przeglądania danych
- ✅ Hosting w Europie dostępny
- ✅ Działa z Render + Streamlit Cloud

---

## 🎯 SZYBKI START (15 minut)

### Krok 1: Utwórz konto Supabase (2 min)

1. Idź na: **https://supabase.com**
2. Kliknij **"Start your project"**
3. Zaloguj się przez GitHub (najszybsze)

### Krok 2: Utwórz nowy projekt (3 min)

1. Kliknij **"New Project"**
2. Wypełnij:
   - **Name**: `polish-players-tracker`
   - **Database Password**: Wygeneruj silne hasło (ZAPISZ JE!)
   - **Region**: `Europe (Frankfurt)` lub `Europe (London)`
   - **Plan**: Free ($0/month)
3. Kliknij **"Create new project"** (poczekaj ~2 min na setup)

### Krok 3: Skopiuj Connection String (1 min)

1. W dashboardzie Supabase → **Settings** (⚙️ ikona w lewym menu)
2. Kliknij **Database**
3. Przewiń w dół do **"Connection string"**
4. Wybierz zakładkę **"URI"**
5. Skopiuj connection string (wygląda tak):
   ```
   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
   ```
6. **ZAMIEŃ** `[YOUR-PASSWORD]` na swoje hasło z Kroku 2!

### Krok 4: Eksportuj dane z SQLite (2 min)

```powershell
# W folderze polish-players-tracker
python migrate_sqlite_to_postgres.py export
```

To utworzy plik `sqlite_export.sql`

### Krok 5: Uruchom migracje Alembic na Supabase (3 min)

1. **Dodaj DATABASE_URL do .env**:
   ```bash
   # W pliku .env
   DATABASE_URL=postgresql://postgres.xxxxx:TWOJE_HASLO@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
   ```

2. **Uruchom migracje** (tworzy tabele):
   ```powershell
   alembic upgrade head
   ```

### Krok 6: Importuj dane (2 min)

```powershell
python migrate_sqlite_to_postgres.py import
```

### Krok 7: Sprawdź czy działa (1 min)

```powershell
# Uruchom backend
python -m uvicorn app.backend.main:app --reload

# Otwórz: http://localhost:8000/docs
# Sprawdź endpoint /api/players/
```

---

## 🔧 Konfiguracja Render

### Dodaj DATABASE_URL w Render Dashboard:

1. Idź do: **render.com** → Twój serwis
2. **Environment** → **Add Environment Variable**
3. Dodaj:
   - **Key**: `DATABASE_URL`
   - **Value**: Twój Supabase connection string
   - Kliknij **Save Changes**

4. Render automatycznie zrestartuje serwis z nową bazą! ✅

---

## 🎨 Konfiguracja Streamlit Cloud

### Dodaj DATABASE_URL w Streamlit Secrets:

1. Idź do: **streamlit.io/cloud** → Twoja aplikacja
2. **Settings** → **Secrets**
3. Dodaj:
   ```toml
   DATABASE_URL = "postgresql://postgres.xxxxx:HASLO@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
   ```
4. Kliknij **Save** → Streamlit zrestartuje app

---

## 📊 Supabase Dashboard - Co możesz robić

### Table Editor (przeglądanie danych):
- **Database** → **Tables** → wybierz tabelę (np. `players`)
- Możesz przeglądać, edytować, filtrować dane w GUI

### SQL Editor (zapytania):
- **SQL Editor** → wpisz zapytanie:
  ```sql
  SELECT name, position, team_name, goals, assists 
  FROM players 
  ORDER BY goals DESC 
  LIMIT 10;
  ```

### Backupy:
- **Database** → **Backups** → codzienne automatyczne backupy!

---

## 🔍 Weryfikacja po migracji

### Sprawdź liczbę graczy:
```sql
SELECT COUNT(*) FROM players;
```

### Sprawdź przykładowe dane:
```sql
SELECT * FROM players LIMIT 5;
```

### Sprawdź tabele:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

Powinny być:
- `players`
- `season_stats`
- `player_matches`
- `goalkeeper_stats`
- `competition_stats`
- `alembic_version`

---

## ⚠️ Troubleshooting

### Problem: "connection timeout"
**Rozwiązanie**: Używasz connection pooler? Zmień port 6543 → 5432 dla direct connection

### Problem: "password authentication failed"
**Rozwiązanie**: Upewnij się, że zamieniłeś `[YOUR-PASSWORD]` w connection string!

### Problem: "SSL required"
**Rozwiązanie**: Dodaj `?sslmode=require` na końcu connection string:
```
postgresql://...postgres?sslmode=require
```

---

## 💰 Limity Free Tier

- **Storage**: 500 MB
- **Database size**: unlimited rows (w ramach 500 MB)
- **Bandwidth**: 2 GB/miesiąc
- **API Requests**: 50,000/dzień

Twoja aplikacja zmieści się bez problemu! 🎉

---

## 🎓 Dalsze kroki

Po migracji:
1. ✅ Usuń `players.db` z repozytorium (dodaj do .gitignore)
2. ✅ Zaktualizuj README.md z instrukcjami Supabase
3. ✅ Przetestuj scheduler na Render
4. ✅ Przetestuj frontend na Streamlit Cloud

---

## 📞 Pomoc

Jeśli coś nie działa:
1. Sprawdź logi Render: Dashboard → Logs
2. Sprawdź connection string (czy hasło jest poprawne?)
3. Sprawdź czy migracje Alembic się wykonały: `alembic current`

---

**🎉 Gotowe! Masz teraz prawdziwą bazę PostgreSQL w chmurze - za darmo, na zawsze!**
