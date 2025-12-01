# Instrukcje restartowania Streamlit po zmianach

## Problem
Po zmianach w kodzie, Streamlit może cache'ować stare dane. Musisz wyczyścić cache i zrestartować aplikację.

## Rozwiązanie

### Metoda 1: Wyczyść cache w aplikacji (ZALECANE)
1. Otwórz http://localhost:8501/
2. W prawym górnym rogu kliknij **"⋮"** (menu)
3. Wybierz **"Clear cache"**
4. Poczekaj aż cache zostanie wyczyszczony
5. Odśwież stronę **(F5)** lub kliknij **"Rerun"**

### Metoda 2: Restart z terminala
1. Zatrzymaj Streamlit: **Ctrl+C** w terminalu gdzie działa frontend
2. Uruchom ponownie:
   ```powershell
   cd polish-players-tracker
   streamlit run app/frontend/streamlit_app.py
   ```

### Metoda 3: Hard restart (jeśli powyższe nie działają)
1. Zatrzymaj frontend: **Ctrl+C**
2. Zatrzymaj backend: **Ctrl+C** (w drugim terminalu)
3. Usuń cache Streamlit:
   ```powershell
   Remove-Item -Recurse -Force .streamlit/cache -ErrorAction SilentlyContinue
   ```
4. Uruchom backend:
   ```powershell
   python -m uvicorn app.backend.main:app --reload
   ```
5. Uruchom frontend (w nowym terminalu):
   ```powershell
   streamlit run app/frontend/streamlit_app.py
   ```

## Weryfikacja
Po restarcie sprawdź:
1. Wyszukaj **"Szymański"**
2. Przewiń do **"Season Statistics History (All Competitions)"**
3. Sprawdź czy są **2 wiersze** dla sezonu 2025-2026:
   - ✅ Champions Lg: 4 mecze, 0 goli, 1 asysta
   - ✅ Europa Lg: 4 mecze, 1 gol, 0 asyst

## Troubleshooting

### Nadal nie widzę Champions Lg?
Sprawdź konsolę przeglądarki (F12) - mogą być błędy JavaScript.

### Czy backend działa?
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/players/" -UseBasicParsing
```
Powinien zwrócić status 200.

### Czy matchlogi są w bazie?
```powershell
cd polish-players-tracker
python -c "from app.backend.database import SessionLocal; from app.backend.models.player_match import PlayerMatch; db = SessionLocal(); count = db.query(PlayerMatch).filter(PlayerMatch.player_id == 49).count(); print(f'Szymanski matches: {count}'); db.close()"
```
Powinno pokazać: `Szymanski matches: 26`
