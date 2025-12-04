# 🏢 Commercial Deployment Guide

## Architektura dla aplikacji komercyjnej

### 📊 Stack rekomendowany:

```
┌─────────────────────────────────────────────────────────┐
│                    USERS / CLIENTS                       │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
┌──────────────────┐            ┌──────────────────┐
│  Streamlit Cloud │            │   Custom Domain  │
│    (Frontend)    │            │   (Optional)     │
│  streamlit.app   │            │  players.com     │
└──────────────────┘            └──────────────────┘
          │                               │
          └───────────────┬───────────────┘
                          ▼
                ┌──────────────────┐
                │   Render.com     │
                │  Backend API     │
                │   (FastAPI)      │
                │  + Scheduler     │
                └──────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
┌──────────────────┐            ┌──────────────────┐
│   Supabase       │            │  SendGrid API    │
│  PostgreSQL DB   │            │  (Email)         │
│  (Managed)       │            │                  │
└──────────────────┘            └──────────────────┘
```

---

## 🗄️ Option 1: PostgreSQL na Supabase (POLECAM!)

### Dlaczego Supabase?
- ✅ **Darmowy tier**: 500 MB storage, unlimited API requests
- ✅ **PostgreSQL managed** - nie musisz zarządzać serwerem
- ✅ **Automatyczne backupy**
- ✅ **Connection pooling** - szybkie połączenia
- ✅ **Dashboard** - SQL editor, logs, metrics
- ✅ **API REST + GraphQL** (opcjonalnie)
- ✅ **Real-time subscriptions** (dla live updates)

### Setup (10 minut):

#### 1. Utwórz projekt na Supabase

1. Zarejestruj się: https://supabase.com
2. Create New Project:
   - **Name**: polish-players-tracker
   - **Database Password**: [wygeneruj mocne hasło]
   - **Region**: Frankfurt (najbliżej Polski)
   - **Plan**: Free

#### 2. Pobierz connection string

W Supabase Dashboard:
1. Settings → Database
2. Connection string → URI (for psycopg2)

Przykład:
```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

#### 3. Zaktualizuj .env

```env
# PostgreSQL (Supabase) - JEDYNA WSPIERANA BAZA:
DATABASE_URL=postgresql://postgres.xxxxx:[PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres

# Nowy (Supabase PostgreSQL):
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

#### 4. Dodaj psycopg2 do requirements.txt

```txt
# Dodaj na końcu requirements.txt:
psycopg2-binary==2.9.9
```

Zainstaluj:
```bash
pip install psycopg2-binary
```

#### 5. Uruchom migracje

```bash
# Utwórz tabele w PostgreSQL
alembic upgrade head
```

#### 6. Migruj dane (jeśli masz istniejące)

**Opcja A: Export/Import przez Alembic**
```bash
# Export ze SQLite
python -c "from app.backend.database import SessionLocal; from app.backend.models.player import Player; import json; db = SessionLocal(); players = db.query(Player).all(); print(json.dumps([{'name': p.name, 'team': p.team, 'league': p.league, 'position': p.position, 'nationality': p.nationality} for p in players], indent=2))" > players_backup.json

# Import do PostgreSQL (zmień DATABASE_URL w .env na PostgreSQL)
# Dodaj graczy przez quick_add_player.py lub API
```

**Opcja B: Użyj pgloader (dla dużych danych)**
```bash
# Zainstaluj pgloader (Linux/Mac)
# Ubuntu: sudo apt-get install pgloader
# Mac: brew install pgloader

# Migruj
pgloader sqlite://players.db postgresql://[connection-string]
```

---

## 🗄️ Option 2: PostgreSQL na Railway

### Dlaczego Railway?
- ✅ **$5 darmowego kredytu** miesięcznie
- ✅ **PostgreSQL + Backend w jednym miejscu**
- ✅ **Automatyczne backupy**
- ✅ **Prosty interface**

### Setup:

1. Zarejestruj się: https://railway.app
2. New Project → Provision PostgreSQL
3. Pobierz `DATABASE_URL` z Settings → Variables
4. Użyj w `.env`

---

## 🗄️ Option 3: PostgreSQL na Render.com

### Dlaczego Render PostgreSQL?
- ✅ **Backend i DB w jednym miejscu**
- ✅ **Darmowy tier**: 90 dni free, potem $7/miesiąc
- ✅ **Persistent storage**

### Setup:

1. Render Dashboard → New → PostgreSQL
2. Pobierz **Internal Database URL**
3. W `render.yaml` zamień SQLite na PostgreSQL:

```yaml
databases:
  - name: polish-players-db
    plan: free
    region: frankfurt

services:
  - type: web
    name: polish-players-backend
    env: python
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: polish-players-db
          property: connectionString
```

---

## 🎨 Streamlit Cloud Deployment

### Setup (10 minut):

#### 1. Przygotuj repozytorium

Struktura dla Streamlit Cloud:
```
polish-players-tracker/
├── streamlit_app.py           # Główny plik (MUSI być w root!)
├── requirements-streamlit.txt # Zależności dla Streamlit
├── .streamlit/
│   └── config.toml           # Konfiguracja Streamlit
└── pages/
    └── 2_⚖️_compare_players.py
```

#### 2. Przenieś streamlit_app.py do root

```bash
# Skopiuj z app/frontend/ do root
cp app/frontend/streamlit_app.py streamlit_app.py

# Zaktualizuj importy w streamlit_app.py
```

#### 3. Utwórz requirements-streamlit.txt

```txt
streamlit==1.51.0
pandas==2.3.3
plotly==5.18.0
requests==2.32.5
```

#### 4. Utwórz .streamlit/config.toml

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

#### 5. Deploy na Streamlit Cloud

1. Push do GitHub (jeśli jeszcze nie)
2. Zarejestruj się: https://share.streamlit.io
3. New app:
   - **Repository**: your-repo
   - **Branch**: main
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.11

4. **Advanced settings** → Secrets:
```toml
# Backend API URL
BACKEND_API_URL = "https://your-backend.onrender.com"
```

5. Deploy! ✨

#### 6. Zaktualizuj streamlit_app.py - użyj BACKEND_API_URL

```python
import streamlit as st
import os

# Backend API URL (Streamlit Cloud secrets lub .env lokalnie)
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# Użyj w requestach
response = requests.get(f"{BACKEND_API_URL}/api/players")
```

---

## 💰 Koszty miesięczne (komercyjny deployment)

### Opcja 1: Minimalna (Start-up)

| Serwis | Plan | Koszt |
|--------|------|-------|
| **Render** (Backend + Scheduler) | Free | $0 |
| **Supabase** (PostgreSQL 500 MB) | Free | $0 |
| **Streamlit Cloud** (Frontend) | Free | $0 |
| **SendGrid** (Email 100/dzień) | Free | $0 |
| **Custom Domain** (opcjonalnie) | GoDaddy | ~$12/rok |
| **TOTAL** | | **$0-1/miesiąc** ✅ |

**Limity:**
- ✅ Do **10,000 użytkowników/miesiąc**
- ✅ 500 MB bazy danych (wystarczy dla 1000+ graczy)
- ✅ Scheduler działa 24/7

---

### Opcja 2: Małe/Średnie (Scale-up)

| Serwis | Plan | Koszt |
|--------|------|-------|
| **Render** (Backend) | Starter | $7/miesiąc |
| **Supabase** (PostgreSQL 8 GB) | Pro | $25/miesiąc |
| **Streamlit Cloud** | Team | $0 (lub $250/miesiąc dla wielu apps) |
| **SendGrid** (Email 40k/dzień) | Essentials | $19.95/miesiąc |
| **Custom Domain** | | ~$1/miesiąc |
| **TOTAL** | | **~$52/miesiąc** |

**Features:**
- ✅ Do **100,000+ użytkowników/miesiąc**
- ✅ 8 GB bazy danych
- ✅ Priorytetowy support
- ✅ Custom branding

---

### Opcja 3: Enterprise (Duża skala)

| Serwis | Plan | Koszt |
|--------|------|-------|
| **AWS EC2** (Backend) | t3.medium | ~$30/miesiąc |
| **AWS RDS PostgreSQL** | db.t3.small | ~$25/miesiąc |
| **Cloudflare** (CDN + DDoS) | Pro | $20/miesiąc |
| **SendGrid** (Email unlimited) | Premier | $89.95/miesiąc |
| **Monitoring** (Datadog) | Pro | $15/miesiąc |
| **TOTAL** | | **~$180/miesiąc** |

**Features:**
- ✅ **Unlimited** users
- ✅ 99.99% uptime SLA
- ✅ Auto-scaling
- ✅ Advanced monitoring
- ✅ Dedykowany support

---

## 🔐 Bezpieczeństwo (dla aplikacji komercyjnej)

### 1. Environment Variables

**NIE commituj** do Git:
```env
DATABASE_URL=postgresql://...
SMTP_PASSWORD=...
SECRET_KEY=...
```

Używaj:
- **Render**: Environment Variables w Dashboard
- **Streamlit Cloud**: Secrets w Settings
- **Lokalnie**: `.env` (dodane do `.gitignore`)

### 2. API Authentication (opcjonalnie)

Dodaj API keys dla komercyjnego API:

```python
# app/backend/main.py
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

# Użyj w endpointach
@app.get("/api/players", dependencies=[Depends(get_api_key)])
def get_players():
    ...
```

### 3. Rate Limiting (dla API)

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.get("/api/players")
@limiter.limit("100/minute")
def get_players(request: Request):
    ...
```

### 4. HTTPS Only

Render/Streamlit automatycznie dodają HTTPS ✅

### 5. Database Backups

**Supabase**: Automatyczne daily backups ✅  
**Render**: Dodaj manual backup script  
**Railway**: Automatyczne backups ✅

---

## 📊 Monitoring & Analytics

### 1. Uptime Monitoring

**UptimeRobot** (darmowy):
1. Monitor: https://your-api.onrender.com/health
2. Alert email jeśli down

### 2. Error Tracking

**Sentry** (darmowy tier):
```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
)
```

### 3. Analytics

**Google Analytics** dla Streamlit:
```python
# W streamlit_app.py
import streamlit.components.v1 as components

components.html("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
""", height=0)
```

---

## 🚀 Custom Domain (opcjonalnie)

### Dla Streamlit Cloud:
1. Kup domenę (GoDaddy, Namecheap)
2. Streamlit Settings → Custom domain → Dodaj `players.com`
3. Ustaw CNAME w DNS:
   ```
   CNAME www your-app.streamlit.app
   ```

### Dla Render (Backend):
1. Render Settings → Custom domain
2. Dodaj `api.players.com`
3. Ustaw CNAME:
   ```
   CNAME api your-backend.onrender.com
   ```

---

## 📝 Deployment Checklist

### Przed deployment:

- [ ] PostgreSQL setup (Supabase/Railway/Render)
- [ ] Migracje uruchomione (`alembic upgrade head`)
- [ ] Dane zmigrowane (jeśli potrzeba)
- [ ] Backend deployed na Render
- [ ] Scheduler enabled (`ENABLE_SCHEDULER=true`)
- [ ] Email configured (SendGrid/Gmail)
- [ ] Streamlit app w root (`streamlit_app.py`)
- [ ] `requirements-streamlit.txt` created
- [ ] `.streamlit/config.toml` created
- [ ] Push do GitHub
- [ ] Streamlit Cloud deployment
- [ ] `BACKEND_API_URL` w Streamlit Secrets
- [ ] Test całego flow (frontend → backend → database)
- [ ] Monitoring setup (UptimeRobot)
- [ ] Custom domain (opcjonalnie)

---

## 🎉 Gotowe! Komercyjna aplikacja online!

**Co masz:**
- ✅ Backend API (Render) - 24/7, scheduler, email
- ✅ PostgreSQL (Supabase) - managed, backups
- ✅ Frontend (Streamlit Cloud) - interactive dashboard
- ✅ Custom domain (opcjonalnie)
- ✅ Monitoring & Analytics
- ✅ Bezpieczeństwo (HTTPS, secrets)

**Koszt**: $0-52/miesiąc (zależnie od skali)

---

**Pytania? Chcesz pomoc z konkretnym krokiem?** 🚀
