# ✅ Frontend Testing Checklist - Goalkeeper Comparison Fix

## 🎯 Cel testowania
Sprawdzenie czy porównywanie bramkarzy działa poprawnie w interfejsie Streamlit.

---

## 📋 Przed rozpoczęciem testów

### 1. Upewnij się że backend działa
```powershell
# Terminal 1: Backend
cd polish-players-tracker
python -m uvicorn app.backend.main:app --reload --port 8000
```
✅ Backend powinien być dostępny na: http://localhost:8000

### 2. Uruchom frontend Streamlit
```powershell
# Terminal 2: Frontend
cd polish-players-tracker
streamlit run app/frontend/streamlit_app.py --server.port 8501
```
✅ Frontend powinien być dostępny na: http://localhost:8501

---

## 🧪 Test 1: Porównanie dwóch bramkarzy

### Kroki:
1. ✅ Otwórz http://localhost:8501
2. ✅ Przejdź do strony **"⚖️ Compare Players"** (w menu po lewej)
3. ✅ W "Select first player" wybierz: **Wojciech Szczęsny** (Barcelona)
4. ✅ W "Select second player" wybierz: **Łukasz Skorupski** (Bologna)

### Oczekiwany rezultat:
- ✅ Powinien pojawić się niebieski komunikat: **"🧤 Comparing goalkeepers"**
- ✅ Powinny być dostępne **4 kolumny** statystyk:
  - **Goalkeeper Stats**: Saves, Save %, Clean Sheets, Goals Against, etc.
  - **Penalties**: Penalties Attempted, Saved, Allowed, Missed
  - **Performance**: Wins, Draws, Losses
  - **General**: Matches, Games Started, Minutes Played

### Kontynuacja testu:
5. ✅ Zaznacz przynajmniej 3 statystyki (np. Saves, Clean Sheets, Save %)
6. ✅ Kliknij przycisk **"Compare Players"**

### Oczekiwany rezultat:
- ✅ Powinien pojawić się **Radar Chart** z porównaniem
- ✅ Powinien pojawić się **Bar Chart** z porównaniem
- ✅ Powinna pojawić się **tabela** z surowymi danymi
- ✅ Dane powinny zawierać statystyki bramkarskie (saves, clean_sheets, etc.)

---

## 🧪 Test 2: Porównanie dwóch zawodników z pola

### Kroki:
1. ✅ Na tej samej stronie wybierz: **Robert Lewandowski** (Barcelona)
2. ✅ Wybierz drugiego: **Piotr Zieliński** (Inter)

### Oczekiwany rezultat:
- ✅ Powinien pojawić się niebieski komunikat: **"⚽ Comparing field players"**
- ✅ Powinny być dostępne **3 kolumny** statystyk:
  - **Offensive**: Goals, Assists, xG, xA, Shots, etc.
  - **Defensive**: Yellow Cards, Red Cards
  - **General**: Matches, Games Started, Minutes Played

### Kontynuacja testu:
3. ✅ Zaznacz statystyki (np. Goals, Assists, xG)
4. ✅ Kliknij **"Compare Players"**

### Oczekiwany rezultat:
- ✅ Wykresy i tabela z danymi ofensywnymi

---

## 🧪 Test 3: Próba porównania bramkarza z zawodnikiem z pola

### Kroki:
1. ✅ Wybierz: **Wojciech Szczęsny** (bramkarz)
2. ✅ Wybierz: **Robert Lewandowski** (napastnik)

### Oczekiwany rezultat:
- ❌ Powinien pojawić się **czerwony komunikat błędu**:
  ```
  ⚠️ You cannot compare goalkeepers with field players! 
  Please select two goalkeepers or two field players.
  ```
- ❌ Aplikacja powinna się **zatrzymać** i nie pokazywać sekcji wyboru statystyk
- ❌ Przycisk "Compare Players" **nie powinien być dostępny**

---

## 🎨 Wizualna weryfikacja

### Sprawdź czy widoczne są następujące elementy:

#### Dla bramkarzy (🧤):
- [ ] Info box z tekstem "🧤 Comparing goalkeepers"
- [ ] 4 kolumny checkboxów
- [ ] Statystyki specyficzne dla bramkarzy (Saves, Clean Sheets, Save %)
- [ ] Statystyki rzutów karnych
- [ ] Statystyki wyniku (Wins, Draws, Losses)

#### Dla zawodników z pola (⚽):
- [ ] Info box z tekstem "⚽ Comparing field players"
- [ ] 3 kolumny checkboxów
- [ ] Statystyki ofensywne (Goals, Assists, xG, xA)
- [ ] Statystyki defensywne (Yellow Cards, Red Cards)

#### Dla nieprawidłowego porównania (❌):
- [ ] Czerwony komunikat błędu
- [ ] Brak dalszych opcji wyboru
- [ ] Aplikacja zatrzymana

---

## 📊 Przykładowe dane do weryfikacji

### Wojciech Szczęsny (sezon 2025-26):
- Matches: 6
- Saves: 15
- Save %: 63.0%
- Clean Sheets: 0
- Goals Against: 11
- Penalties Saved: 1

### Robert Lewandowski (sezon 2025-26):
- Matches: ~15-20
- Goals: 8+
- Assists: kilka
- xG: wartość dodatnia

---

## ✅ Kryteria akceptacji

Test jest **PASSED** jeśli:
- ✅ Bramkarze mogą być porównywani z bramkarzami
- ✅ Zawodnicy z pola mogą być porównywani z zawodnikami z pola
- ✅ Porównywanie mieszane jest **zablokowane** z odpowiednim komunikatem
- ✅ Statystyki wyświetlane są prawidłowo dla każdego typu gracza
- ✅ Wykresy i tabele działają poprawnie
- ✅ Nie ma błędów w konsoli przeglądarki

---

## 🐛 Zgłaszanie problemów

Jeśli coś nie działa:
1. Sprawdź logi backendu (terminal z uvicorn)
2. Sprawdź logi frontendu (terminal ze streamlit)
3. Sprawdź konsolę przeglądarki (F12)
4. Sprawdź czy oba serwery działają:
   - Backend: http://localhost:8000/health
   - Frontend: http://localhost:8501

---

## 📝 Notatki testowe

Miejsce na Twoje uwagi podczas testowania:

```
Data testu: __________
Tester: __________

Test 1 (Bramkarze):        [ ] PASS  [ ] FAIL
Test 2 (Zawodnicy z pola): [ ] PASS  [ ] FAIL  
Test 3 (Mieszany):         [ ] PASS  [ ] FAIL

Uwagi:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```
