# ?? Migration Guide: Matchlogs Endpoints v0.7.3 õ v0.7.4

**?? BREAKING CHANGE ALERT** - Ten dokument pomoøe Ci zaktualizowaÊ kod uøywajπcy starych endpointÛw matchlogs.

---

## ?? Quick Reference Table

| Co siÍ zmieni≥o | Stary endpoint (v0.7.3) | Nowy endpoint (v0.7.4) |
|----------------|-------------------------|------------------------|
| Lista meczÛw gracza | `GET /api/players/{id}/matches` | `GET /api/matchlogs/{id}` |
| Statystyki meczowe | `GET /api/players/{id}/matches/stats` | `GET /api/matchlogs/{id}/stats` |
| SzczegÛ≥y meczu | `GET /api/players/matches/{id}` | `GET /api/matchlogs/match/{id}` |

---

## ?? Python Migration Examples

### Example 1: Basic Request

**PRZED (v0.7.3):**
```python
import requests

API_URL = "http://localhost:8000"
player_id = 5

# Pobierz mecze gracza
response = requests.get(f"{API_URL}/api/players/{player_id}/matches")
matches = response.json()
```

**PO (v0.7.4):**
```python
import requests

API_URL = "http://localhost:8000"
player_id = 5

# Pobierz mecze gracza
response = requests.get(f"{API_URL}/api/matchlogs/{player_id}")
matches = response.json()
```

### Example 2: With Filters

**PRZED:**
```python
# Pobierz mecze z filtrem sezonu
params = {"season": "2025-2026", "limit": 20}
response = requests.get(
    f"{API_URL}/api/players/{player_id}/matches",
    params=params
)
```

**PO:**
```python
# Pobierz mecze z filtrem sezonu
params = {"season": "2025-2026", "limit": 20}
response = requests.get(
    f"{API_URL}/api/matchlogs/{player_id}",
    params=params
)
```

### Example 3: Match Stats Summary

**PRZED:**
```python
# Pobierz podsumowanie statystyk
response = requests.get(
    f"{API_URL}/api/players/{player_id}/matches/summary"
)
stats = response.json()
```

**PO:**
```python
# Pobierz podsumowanie statystyk
response = requests.get(
    f"{API_URL}/api/matchlogs/{player_id}/stats"
)
stats = response.json()
```

### Example 4: Match Details

**PRZED:**
```python
# Pobierz szczegÛ≥y meczu
match_id = 123
response = requests.get(
    f"{API_URL}/api/players/matches/{match_id}"
)
match = response.json()
```

**PO:**
```python
# Pobierz szczegÛ≥y meczu
match_id = 123
response = requests.get(
    f"{API_URL}/api/matchlogs/match/{match_id}"
)
match = response.json()
```

---

## ?? Streamlit/Frontend Migration

### api_client.py

**PRZED:**
```python
def get_player_matches(player_id, season=None, competition=None):
    """Pobiera listÍ meczÛw gracza"""
    params = {}
    if season:
        params['season'] = season
    if competition:
        params['competition'] = competition
    
    response = requests.get(
        f"{API_URL}/api/players/{player_id}/matches",
        params=params
    )
    return response.json()

def get_match_stats_summary(player_id):
    """Pobiera statystyki agregowane"""
    response = requests.get(
        f"{API_URL}/api/players/{player_id}/matches/summary"
    )
    return response.json()
```

**PO:**
```python
def get_player_matches(player_id, season=None, competition=None):
    """Pobiera listÍ meczÛw gracza"""
    params = {}
    if season:
        params['season'] = season
    if competition:
        params['competition'] = competition
    
    response = requests.get(
        f"{API_URL}/api/matchlogs/{player_id}",
        params=params
    )
    return response.json()

def get_match_stats_summary(player_id, season=None):
    """Pobiera statystyki agregowane"""
    params = {}
    if season:
        params['season'] = season
    
    response = requests.get(
        f"{API_URL}/api/matchlogs/{player_id}/stats",
        params=params
    )
    return response.json()

def get_match_details(match_id):
    """Pobiera szczegÛ≥y pojedynczego meczu"""
    response = requests.get(
        f"{API_URL}/api/matchlogs/match/{match_id}"
    )
    return response.json()
```

---

## ?? JavaScript/TypeScript Migration

### Example: Fetch API

**PRZED:**
```javascript
// Get player matches
async function getPlayerMatches(playerId, season = null) {
  const params = new URLSearchParams();
  if (season) params.append('season', season);
  
  const response = await fetch(
    `${API_URL}/api/players/${playerId}/matches?${params}`
  );
  return await response.json();
}
```

**PO:**
```javascript
// Get player matches
async function getPlayerMatches(playerId, season = null) {
  const params = new URLSearchParams();
  if (season) params.append('season', season);
  
  const response = await fetch(
    `${API_URL}/api/matchlogs/${playerId}?${params}`
  );
  return await response.json();
}
```

### Example: Axios

**PRZED:**
```javascript
import axios from 'axios';

// Get match stats
const getMatchStats = async (playerId) => {
  const response = await axios.get(
    `${API_URL}/api/players/${playerId}/matches/summary`
  );
  return response.data;
};
```

**PO:**
```javascript
import axios from 'axios';

// Get match stats
const getMatchStats = async (playerId) => {
  const response = await axios.get(
    `${API_URL}/api/matchlogs/${playerId}/stats`
  );
  return response.data;
};
```

---

## ?? Find & Replace Commands

### Unix/Linux/Mac (grep + sed)

```bash
# Find all occurrences
grep -r "/api/players/.*/matches" .

# Replace in all files (backup first!)
find . -type f -name "*.py" -exec sed -i.bak 's|/api/players/\([^/]*\)/matches|/api/matchlogs/\1|g' {} +
```

### Windows (PowerShell)

```powershell
# Find all occurrences
Get-ChildItem -Recurse -Include *.py | Select-String "/api/players/.*?/matches"

# Replace in all Python files
Get-ChildItem -Recurse -Include *.py | ForEach-Object {
    (Get-Content $_.FullName) `
        -replace '/api/players/(\d+)/matches/summary', '/api/matchlogs/$1/stats' `
        -replace '/api/players/(\d+)/matches', '/api/matchlogs/$1' `
        -replace '/api/players/matches/(\d+)', '/api/matchlogs/match/$1' |
    Set-Content $_.FullName
}
```

### VS Code (Find & Replace with Regex)

1. OtwÛrz Find & Replace (Ctrl+H)
2. W≥πcz regex (Alt+R)
3. Uøyj tych wzorcÛw:

**Pattern 1:**
- Find: `/api/players/(\d+)/matches/summary`
- Replace: `/api/matchlogs/$1/stats`

**Pattern 2:**
- Find: `/api/players/(\d+)/matches`
- Replace: `/api/matchlogs/$1`

**Pattern 3:**
- Find: `/api/players/matches/(\d+)`
- Replace: `/api/matchlogs/match/$1`

---

## ? Testing Checklist

Po aktualizacji kodu, przetestuj:

- [ ] Pobieranie listy meczÛw dzia≥a
- [ ] Filtry (season, competition, limit) dzia≥ajπ poprawnie
- [ ] Statystyki agregowane sπ zwracane
- [ ] SzczegÛ≥y pojedynczego meczu dzia≥ajπ
- [ ] Obs≥uga b≥ÍdÛw (404) dzia≥a poprawnie
- [ ] Frontend wyúwietla dane poprawnie

---

## ?? Common Mistakes

### Mistake 1: Stary nawyk w URL

```python
# ? èLE - stary URL
response = requests.get(f"/api/players/{player_id}/matches")

# ? DOBRZE - nowy URL
response = requests.get(f"/api/matchlogs/{player_id}")
```

### Mistake 2: Zapomnienie o nowej úcieøce dla match details

```python
# ? èLE
response = requests.get(f"/api/players/matches/{match_id}")

# ? DOBRZE - nowa úcieøka
response = requests.get(f"/api/matchlogs/match/{match_id}")
```

### Mistake 3: Stary endpoint dla statystyk

```python
# ? èLE - "summary" juø nie istnieje
response = requests.get(f"/api/matchlogs/{player_id}/summary")

# ? DOBRZE - teraz to "stats"
response = requests.get(f"/api/matchlogs/{player_id}/stats")
```

---

## ?? Need Help?

1. **Check Swagger UI:** http://localhost:8000/docs
2. **Read Documentation:**
   - `README_MATCHLOGS_UPDATE.md` - szczegÛ≥y zmian
   - `API_COMPLETE_REFERENCE.md` - pe≥na dokumentacja
3. **Test with curl:**
   ```bash
   curl http://localhost:8000/api/matchlogs/5
   ```

---

## ?? Response Format Changes

**Dobra wiadomoúÊ:** Format odpowiedzi siÍ NIE zmieni≥! 

Tylko URL siÍ zmieni≥, struktura JSON pozosta≥a taka sama:

```json
{
  "player_id": 5,
  "player_name": "Robert Lewandowski",
  "total_matches": 20,
  "matches": [...]
}
```

---

**Last Updated:** 2025-01-XX  
**Version:** 0.7.4  
**Prepared by:** Rovo Dev
