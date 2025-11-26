# FBref xG Data Limitation - Dokumentacja Problemu

## Problem
Dla niektórych graczy (np. Karol Świderski) statystyki Expected Goals (xG, npxG, xA) są wyświetlane jako `None`, podczas gdy dla innych (np. Robert Lewandowski) działają poprawnie.

## Analiza Przyczyny

### Testy wykonane:
1. **Karol Świderski (Super League - Turcja):**
   - Liga domowa: Super League - xG=None, npxG=None, xA=None ❌
   - Conference League: xG=0.7, npxG=0.7, xA=0.1 ✅

2. **Robert Lewandowski (La Liga - Hiszpania):**
   - Liga domowa: La Liga - xG=27.1, npxG=24.0, xA=2.3 ✅
   - Copa del Rey: xG=None, npxG=None, xA=None ❌
   - Champions League: xG=10.4, npxG=8.0, xA=1.5 ✅

### Wnioski:
**FBref NIE udostępnia danych Expected (xG, npxG, xA) dla wszystkich lig.**

Dane Expected są dostępne tylko dla:
- ✅ **Top 5 europejskich lig:** Premier League, La Liga, Bundesliga, Serie A, Ligue 1
- ✅ **Rozgrywki europejskie:** Champions League, Europa League, Conference League
- ❌ **Inne ligi:** Super League (Turcja), Ekstraklasa (Polska), MLS (częściowo), itp.
- ❌ **Puchary krajowe:** Copa del Rey, FA Cup, itp.

### Sprawdzone tabele na FBref:
1. `stats_expected_dom_lg` - Tabela Expected (preferowana) - **NIE ISTNIEJE dla Super League**
2. `stats_shooting_dom_lg` - Tabela Shooting (fallback) - **ISTNIEJE, ale kolumny xG/npxG są PUSTE**

## Rozwiązanie Zastosowane

### Kod zmodyfikowany:
Plik: `app/backend/services/fbref_playwright_scraper.py`

**Dodano:**
1. **Fallback do tabeli Shooting:** Jeśli tabela `stats_expected_dom_lg` nie istnieje lub jest pusta, kod próbuje pobrać dane z `stats_shooting_dom_lg`
2. **Nową metodę `_parse_shooting_table()`:** Parsuje dane xG/npxG z tabeli shooting (gdzie czasem są dostępne)
3. **Walidację wartości:** Sprawdza czy wartości xG/npxG są > 0 przed użyciem (aby nie nadpisywać pustymi wartościami)
4. **Fallback dla wszystkich typów rozgrywek:**
   - Domestic League (`stats_shooting_dom_lg`)
   - Domestic Cups (`stats_shooting_dom_cup`)
   - International Cups (`stats_shooting_intl_cup`)

**Algorytm pobierania danych:**
```
1. Szukaj tabeli Expected (stats_expected_*)
   ├─ Jeśli znaleziono → użyj danych
   └─ Jeśli nie znaleziono:
      └─ Szukaj tabeli Shooting (stats_shooting_*)
         ├─ Jeśli znaleziono i ma wartości > 0 → użyj danych
         └─ Jeśli nie znaleziono lub puste → zostaw None
```

**Wynik:**
- Kod próbuje pobrać dane z dwóch źródeł (Expected table → Shooting table)
- Jeśli oba źródła są puste/niedostępne, wartość pozostaje jako `None`
- `None` oznacza "dane niedostępne dla tej ligi" (nie mylić z wartością 0.0)

## Ograniczenia

### Nie można naprawić w 100%:
Dla lig, które nie mają danych xG na FBref (jak Super League), **NIE MA sposobu** na pobranie tych danych z FBref.

### Możliwe alternatywy:
1. **Inne źródła danych:**
   - Understat.com (tylko top 5 lig)
   - SofaScore API (wymaga klucza API)
   - Fotmob (trudny scraping)

2. **Oszacowanie xG:**
   - Proste przybliżenie na podstawie strzałów/celnych strzałów
   - Bardzo niedokładne, nie zalecane

3. **Akceptacja ograniczenia:**
   - Wyświetlać `None` lub "N/A" w interfejsie
   - Dodać informację: "xG dostępne tylko dla top 5 lig + rozgrywki europejskie"

## Rekomendacja

**Zalecam pozostawienie wartości jako `None` i dodanie informacji w UI:**

```python
if xg is None:
    display_text = "N/A (dane niedostępne dla tej ligi)"
```

**Dla użytkownika:**
"Statystyki Expected (xG, npxG, xA) są dostępne tylko dla:
- Premier League, La Liga, Bundesliga, Serie A, Ligue 1
- Champions League, Europa League, Conference League"

## Status
✅ Kod zaktualizowany z fallbackiem do tabeli shooting
⚠️ Ograniczenie ze strony FBref - nie można naprawić w pełni
📝 Dokumentacja problemu utworzona
