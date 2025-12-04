# 🚀 Deployment na Render.com

## Krok po kroku - Deployment backendu z schedulerem na Render

### 📋 Przygotowanie (5 minut)

#### 1. Utwórz konto na Render.com
- Przejdź na: https://render.com
- Zarejestruj się (możesz użyć GitHub)
- **Plan: FREE** (wystarczy dla schedulera!)

#### 2. Podłącz repozytorium GitHub
- Utwórz repo na GitHub (jeśli jeszcze nie masz)
- Push projektu:
```bash
cd polish-players-tracker
git init
git add .
git commit -m "Initial commit for Render deployment"
git remote add origin [YOUR-GITHUB-REPO-URL]
git push -u origin main
```

---

### 🎯 Deployment (10 minut)

#### 1. Utwórz nowy Web Service na Render

1. Zaloguj się na Render.com
2. Kliknij **"New +"** → **"Web Service"**
3. Wybierz swoje repozytorium GitHub
4. Konfiguracja:
   - **Name**: `polish-players-backend`
   - **Region**: `Frankfurt` (najbliżej Polski)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
     ```
   - **Start Command**:
     ```bash
     uvicorn app.backend.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: **Free**

#### 2. Dodaj zmienne środowiskowe

W sekcji **Environment Variables** dodaj:

```
ENABLE_SCHEDULER=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=twoj-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_FROM=twoj-email@gmail.com
EMAIL_TO=gdzie-wyslac@gmail.com
```

#### 3. Dodaj Persistent Disk dla bazy danych

**WAŻNE**: Używamy Supabase PostgreSQL (darmowe!) - dane są bezpieczne w chmurze.

1. W ustawieniach serwisu przejdź do **"Disks"**
2. Kliknij **"Add Disk"**
3. Konfiguracja:
   - **Name**: `database`
   - **Mount Path**: `/app/data`
   - **Size**: `1 GB` (wystarczy)

4. **Zmodyfikuj config.py** aby używał ścieżki `/app/data/players.db`:

W pliku `app/backend/config.py` zmień:
```python
# Stara wersja
DATABASE_URL = "sqlite:///./players.db"

# Nowa wersja (dla Render)
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////app/data/players.db")
```

#### 4. Deploy!

1. Kliknij **"Create Web Service"**
2. Render zacznie budować aplikację (~5-10 minut)
3. Poczekaj aż status będzie: **"Live"** ✅

---

### ✅ Weryfikacja

#### 1. Sprawdź czy backend działa

Otwórz URL swojego serwisu (np. `https://polish-players-backend.onrender.com`):

```bash
curl https://polish-players-backend.onrender.com/health
# Odpowiedź: {"status":"ok"}
```

#### 2. Sprawdź logi schedulera

W Render Dashboard:
- Przejdź do **"Logs"**
- Szukaj:
```
✅ Scheduler uruchomiony
📅 Sync schedule: Thursday & Monday at 06:00
```

#### 3. Test końcowy

Scheduler będzie działał:
- **Poniedziałek 6:00** (UTC - czyli 7:00 czasu polskiego zimą, 8:00 latem!)
- **Czwartek 6:00** (UTC)

**UWAGA**: Render używa czasu UTC!

---

### ⚠️ Ważne informacje o planie FREE

#### Limity:
- ✅ **Zawsze włączony** (nie usypia się podczas wykonywania scheduled tasks)
- ✅ **750 godzin/miesiąc** (wystarczy dla 24/7!)
- ✅ **100 GB bandwidth/miesiąc**
- ❌ **Custom domain** - tylko `*.onrender.com`
- ⚠️ **Cold start** - po 15 min bez requestów może się "uśpić" (ale scheduler go obudzi!)

#### Rate limiting:
- Playwright + 12 sekund rate limit = bezpieczne! ✅
- 98 graczy × ~20 minut = OK dla Render

---

### 🔧 Troubleshooting

#### Problem: Baza danych się resetuje po redeploy
**Rozwiązanie**: Upewnij się że persistent disk jest poprawnie zamontowany w `/app/data`

#### Problem: Playwright nie działa
**Rozwiązanie**: Sprawdź czy build command zawiera:
```bash
playwright install chromium && playwright install-deps chromium
```

#### Problem: Scheduler nie działa
**Rozwiązanie**: Sprawdź w logach czy `ENABLE_SCHEDULER=true` jest ustawione

#### Problem: Timezone (scheduler włącza się o złej porze)
**Rozwiązanie**: Render używa UTC. Dodaj do `.env`:
```python
SCHEDULER_TIMEZONE=Europe/Warsaw
```
I zmodyfikuj `main.py` aby używał tego timezone.

---

### 💰 Koszt

**Plan FREE**: $0/miesiąc
- Backend działa 24/7 ✅
- Scheduler synchronizuje automatycznie ✅
- ✅ **PostgreSQL (Supabase)**: Dane są bezpieczne w chmurze z automatycznymi backupami
- ✅ **ROZWIĄZANIE**: Użyj Supabase PostgreSQL (też DARMOWE!)

**Supabase PostgreSQL**: $0/miesiąc (darmowe NA ZAWSZE)
- 500 MB storage (wystarczy dla setek graczy)
- Automatyczne backupy
- Działa z Render + Streamlit Cloud
- 📖 Instrukcja: [SUPABASE_MIGRATION_GUIDE.md](SUPABASE_MIGRATION_GUIDE.md)

**Plan Starter** ($7/miesiąc) - opcjonalnie, jeśli potrzebujesz:
- Szybszy cold start
- Więcej mocy obliczeniowej

---

### 📊 Monitoring

Render Dashboard pokazuje:
- ✅ **Logi** w czasie rzeczywistym
- ✅ **Metryki** (CPU, RAM, requests)
- ✅ **Deploy history**
- ✅ **Health checks**

---

### 🎉 Gotowe!

Teraz Twoja aplikacja:
- ✅ Działa 24/7 w chmurze
- ✅ Scheduler synchronizuje graczy 2x w tygodniu
- ✅ Nie musisz trzymać komputera włączonego
- ✅ Automatyczne deploye z GitHub
- ✅ Darmowe! ($0/miesiąc)

---

### 📧 Email notifications

Po każdej synchronizacji (Pon/Czw 6:00 UTC) dostaniesz email z raportem!

---

## ❓ Problemy?

Jeśli coś nie działa:
1. Sprawdź logi w Render Dashboard
2. Sprawdź czy zmienne środowiskowe są ustawione
3. Sprawdź czy persistent disk jest zamontowany
4. Sprawdź build logs

---

## 🚀 Następne kroki

1. Deploy aplikacji na Render
2. Czekaj do Poniedziałku/Czwartku 6:00 UTC
3. Sprawdź email z raportem!

**Gotowe do deploymentu!** 🎉
