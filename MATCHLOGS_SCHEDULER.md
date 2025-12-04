# 📋 Matchlogs Scheduler - Dokumentacja

## 🎯 Przegląd

Automatyczna synchronizacja szczegółowych logów meczowych dla wszystkich graczy w bazie danych. Scheduler został dodany do systemu automatyzacji Polish Football Data Hub International.

## ⏰ Harmonogram

### Synchronizacja Statystyk (istniejąca)
- **Dni:** Poniedziałek i Czwartek
- **Godzina:** 06:00 (strefa czasowa: Europe/Warsaw)
- **Częstotliwość:** 2x w tygodniu
- **Cel:** Aktualizacja podstawowych statystyk graczy po meczach weekendowych i LM

### Synchronizacja Matchlogs (NOWA)
- **Dzień:** Wtorek
- **Godzina:** 07:00 (strefa czasowa: Europe/Warsaw)
- **Częstotliwość:** 1x w tygodniu
- **Cel:** Szczegółowe logi meczowe dla każdego gracza

## 🔧 Funkcje

### 1. `sync_player_matchlogs(scraper, db, player, season)`
Synchronizuje logi meczowe dla pojedynczego gracza.

**Parametry:**
- `scraper`: Instancja FBrefPlaywrightScraper
- `db`: Sesja bazy danych
- `player`: Obiekt Player
- `season`: Sezon (domyślnie: "2025-2026")

**Zwraca:**
- Liczba zsynchronizowanych meczów

**Funkcjonalność:**
- Pobiera FBref ID gracza
- Pobiera logi meczowe za pomocą Playwright scraper
- Usuwa istniejące matchlogi dla gracza
- Zapisuje nowe dane do tabeli `player_matches`

### 2. `scheduled_sync_matchlogs()`
Zaplanowane zadanie do synchronizacji matchlogs dla wszystkich graczy.

**Funkcjonalność:**
- Pobiera wszystkich graczy z bazy
- Filtruje graczy posiadających FBref ID
- Synchronizuje matchlogi z rate limiting 12s
- Wysyła powiadomienie email po zakończeniu
- Loguje szczegółowe informacje o przebiegu

### 3. `send_matchlogs_notification_email(synced, failed, total, total_matches, duration_minutes, failed_players)`
Wysyła powiadomienie email po synchronizacji matchlogs.

**Email zawiera:**
- Liczbę zsynchronizowanych graczy
- Całkowitą liczbę meczów
- Czas trwania synchronizacji
- Listę graczy, którzy nie zostali zsynchronizowani
- Formatowanie HTML z kolorami

## 📊 Dane Zbierane

Dla każdego meczu gracza:
- **Podstawowe:** Data, przeciwnik, wynik, miejsce (dom/wyjazd)
- **Czas gry:** Minuty rozegrane
- **Gole i asysty:** Goals, assists, xG, xA
- **Strzały:** Shots, shots on target
- **Podania:** Completed, attempted, completion %, key passes
- **Obrona:** Tackles, interceptions, blocks
- **Akcje:** Touches, dribbles, carries, fouls
- **Kartki:** Yellow cards, red cards

## 🚀 Aktywacja

### Włączenie Schedulera

W pliku `.env`:
```bash
ENABLE_SCHEDULER=true
```

### Konfiguracja Email (opcjonalna)

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=notification-recipient@example.com
```

## 📝 Logi

Scheduler loguje:
- Start i koniec synchronizacji
- Postęp dla każdego gracza
- Liczbę znalezionych meczów
- Błędy i ostrzeżenia
- Podsumowanie wyników

Przykład:
```
============================================================
📋 SCHEDULED MATCHLOGS SYNC - Starting automatic match logs synchronization
⏰ Time: 2025-01-28 07:00:00
============================================================

📋 Found 120 players with FBref ID to sync match logs
⏱️ Estimated time: ~24.0 minutes (12s rate limit)

[1/120] 📋 Syncing match logs: Robert Lewandowski
  📊 Found 28 matches
  ✅ Saved 28 matches
✅ Successfully synced 28 matches for Robert Lewandowski

...

============================================================
✅ SCHEDULED MATCHLOGS SYNC COMPLETE
📊 Results: 118 players synced, 3240 total matches, 2 failed out of 120 total
⏱️ Duration: 24.3 minutes
============================================================
```

## 🔍 API Endpoints

Po synchronizacji dane są dostępne przez:

- `GET /api/players/{player_id}/matches` - Wszystkie mecze gracza
- `GET /api/players/{player_id}/matches?season=2025-2026` - Mecze z sezonu
- `GET /api/players/{player_id}/matches?limit=10` - Ostatnie 10 meczów
- `GET /api/players/{player_id}/matches/summary` - Podsumowanie statystyk

## 🎯 Rate Limiting

- **Czas między requestami:** 12 sekund
- **Zgodność:** FBref Terms of Service
- **Szacowany czas:** ~12s × liczba graczy / 60 = minuty

Dla 120 graczy: ~24 minuty

## 🐛 Troubleshooting

### Scheduler nie startuje
```bash
# Sprawdź logi
tail -f logs/app.log

# Upewnij się że zmienna środowiskowa jest ustawiona
echo $ENABLE_SCHEDULER
```

### Matchlogi nie są synchronizowane
1. Sprawdź czy gracz ma FBref ID (`api_id` lub `fbref_id`)
2. Sprawdź logi dla konkretnego gracza
3. Przetestuj manualnie: `python sync_match_logs.py "Player Name"`

### Email nie jest wysyłany
1. Sprawdź konfigurację SMTP w `.env`
2. Sprawdź logi: `⚠️ Email not configured - skipping notification`
3. Dla Gmail użyj App Password zamiast zwykłego hasła

## 📈 Monitoring

### Health Check Endpoint
```bash
curl http://localhost:8000/health
```

Odpowiedź:
```json
{
  "status": "ok",
  "timestamp": "2025-01-28T07:00:00",
  "scheduler_running": true
}
```

### Root Endpoint
```bash
curl http://localhost:8000/
```

Zwraca informacje o schedulerze:
```json
{
  "scheduler": {
    "enabled": true,
    "stats_sync_schedule": "Monday & Thursday at 06:00 (Europe/Warsaw)",
    "matchlogs_sync_schedule": "Tuesday at 07:00 (Europe/Warsaw)",
    "next_stats_sync": "2025-01-27 06:00:00+01:00",
    "next_matchlogs_sync": "2025-01-28 07:00:00+01:00"
  }
}
```

## 🔄 Manualna Synchronizacja

Aby zsynchronizować matchlogi dla pojedynczego gracza:

```bash
cd polish-players-tracker
python sync_match_logs.py "Robert Lewandowski"
python sync_match_logs.py "Michał Helik" --season 2024-2025
```

## 💡 Best Practices

1. **Rate Limiting:** Nie zmieniaj wartości 12s - to zapewnia zgodność z FBref ToS
2. **Email Notifications:** Konfiguruj email dla monitorowania produkcji
3. **Logi:** Regularnie sprawdzaj logi dla błędów
4. **Baza danych:** Używaj persistent storage (Render Disk) dla produkcji
5. **Timezone:** Domyślna strefa Europe/Warsaw - zmień w `.env` jeśli potrzeba

## 🎉 Podsumowanie

Matchlogs scheduler automatycznie zbiera szczegółowe dane meczowe dla wszystkich graczy raz w tygodniu, umożliwiając głęboką analizę wydajności i trendów. System jest w pełni zintegrowany z istniejącym schedulere'm statystyk i systemem powiadomień email.
