# Test Plan: Sebastian Szymański - European Cups Display

## Co zostało naprawione?
Szymański grał w **dwóch różnych rozgrywkach europejskich** w sezonie 2025-26:
1. **Champions League** (kwalifikacje) - sierpień 2025
2. **Europa League** (faza grupowa) - wrzesień-listopad 2025

Poprzednio aplikacja pokazywała tylko Europa League (5 meczów), teraz pokazuje **wszystkie 9 meczów** z obu rozgrywek.

---

## Instrukcje testowania

### Krok 1: Upewnij się, że backend działa
```powershell
cd polish-players-tracker
python -m uvicorn app.backend.main:app --reload
```
Backend powinien działać na `http://localhost:8000`

### Krok 2: Uruchom frontend (w nowym terminalu)
```powershell
cd polish-players-tracker
streamlit run app/frontend/streamlit_app.py
```
Frontend otworzy się na `http://localhost:8501`

### Krok 3: Wyszukaj Szymańskiego
1. W polu "Player Search" wpisz: **Szymański**
2. Kliknij na kartę gracza (powinna być rozwinięta automatycznie)

---

## Test 1: Kolumna "European Cups (2025-2026)" ✅

### Oczekiwany wynik:
```
🌍 European Cups (2025-2026)

**Champions Lg**
Games: 4
Goals: 0
Assists: 1

**Europa Lg**
Games: 4
Goals: 1
Assists: 0
```

### Co sprawdzić:
- ✅ **Dwa osobne wiersze** dla Champions Lg i Europa Lg (nie jeden zagregowany)
- ✅ Champions Lg: **4 mecze**, 0 goli, 1 asysta
- ✅ Europa Lg: **4 mecze**, 1 gol, 0 asyst (wykluczono 1 mecz z 0 minut)
- ✅ **Razem: 8 meczów zagranych**, 1 gol, 1 asysta

### Details (rozwiń expander):
```
### Champions Lg
⏱️ Minutes: 360
🎯 Goals: 0
🅰️ Assists: 1
⚡ G+A / 90: 0.25
---

### Europa Lg
⏱️ Minutes: 179
🎯 Goals: 1
🅰️ Assists: 0
⚡ G+A / 90: 0.50
---
```
(Mecze z 0 minut są automatycznie wykluczane)

---

## Test 2: Tabela "Season Statistics History (All Competitions)" ✅

Przewiń w dół do tabeli historii statystyk.

### Oczekiwany wynik dla sezonu 2025-2026:
Powinny być **DWIE osobne linie** dla rozgrywek europejskich:

| Season    | Type         | Competition   | Games | Goals | Assists | xG  | xA  | Minutes |
|-----------|--------------|---------------|-------|-------|---------|-----|-----|---------|
| 2025-2026 | EUROPEAN_CUP | Champions Lg  | 4     | 0     | 1       | 0.0 | 0.0 | 360     |
| 2025-2026 | EUROPEAN_CUP | Europa Lg     | 5     | 1     | 0       | 0.1 | 0.4 | 179     |
| 2025-2026 | LEAGUE       | Süper Lig     | 12    | 1     | 0       | ... | ... | 415     |

### Co sprawdzić:
- ✅ **Champions Lg** - osobny wiersz (4 mecze, 0 goli, 1 asysta, 360 minut)
- ✅ **Europa Lg** - osobny wiersz (4 mecze, 1 gol, 0 asyst, 179 minut)
- ✅ **RAZEM: 8 meczów zagranych** w sezonie 2025-2026 (mecze z 0 minut wykluczono)
- ✅ Format podobny jak u Świderskiego (każda rozgrywka osobno)

---

## Test 3: Porównanie ze Świderskim (opcjonalnie)

Wyszukaj "Świderski" i sprawdź, czy jego tabela wygląda podobnie (osobne wiersze dla każdej rozgrywki europejskiej).

---

## Troubleshooting

### Problem: "No matches played" w European Cups
**Przyczyna**: Matchlogi nie zostały zsynchronizowane.

**Rozwiązanie**:
```powershell
cd polish-players-tracker
python sync_match_logs.py "Sebastian Szymański" --season 2025-2026
```

### Problem: Nadal pokazuje tylko Europa Lg
**Przyczyna**: Cache w Streamlit.

**Rozwiązanie**:
1. W prawym górnym rogu Streamlit kliknij "⋮" (menu)
2. Wybierz "Clear cache"
3. Odśwież stronę (F5)

### Problem: Backend nie odpowiada
**Rozwiązanie**:
```powershell
# Sprawdź czy backend działa
Invoke-WebRequest -Uri "http://localhost:8000/api/players/" -UseBasicParsing
```
Jeśli dostaniesz błąd, uruchom ponownie backend.

---

## Oczekiwane wyniki po naprawie

✅ Kolumna European Cups: **9 meczów** (Champions Lg + Europa Lg)  
✅ Tabela History: **2 osobne wiersze** dla Champions Lg i Europa Lg  
✅ Szczegóły pokazują **539 minut** łącznie  

---

**Data testu**: 2025-01-XX
**Tester**: [Twoje imię]
**Status**: [ ] PASSED / [ ] FAILED
