# 📚 API Documentation - Polish Players Tracker

## 🌐 API Endpoints

### Base URL
- **Development:** `http://localhost:8000`
- **Production:** `https://your-app.onrender.com`

### Interactive Documentation
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## ⚖️ Legal Notice

**This API is for educational and non-commercial use only.**

- **Data Source:** FBref.com (© Sports Reference LLC)
- **Usage:** Educational and portfolio purposes only
- **NOT for commercial use** without proper licensing

See [LEGAL_NOTICE.md](LEGAL_NOTICE.md) for full details.

---

## 🔐 Authentication

**Current:** No authentication required (public API)

**Future (if commercial):**
```http
X-API-Key: your-api-key-here
```

---

## 📊 Endpoints

### 🏥 Health Check

**GET** `/health`

Check if API is running and database is connected.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "0.7.3"
}
```

---

### 👥 Players

#### Get All Players

**GET** `/api/players`

Get list of all Polish players.

**Query Parameters:**
- `limit` (int, optional): Max number of results (default: 100)
- `offset` (int, optional): Pagination offset (default: 0)
- `position` (string, optional): Filter by position (GK, DF, MF, FW)
- `team` (string, optional): Filter by team name

**Example:**
```http
GET /api/players?limit=10&position=FW
```

**Response:**
```json
{
  "total": 85,
  "players": [
    {
      "id": 1,
      "name": "Robert Lewandowski",
      "position": "FW",
      "team": "Barcelona",
      "nationality": "Poland",
      "fbref_id": "8d78e732",
      "created_at": "2025-11-20T10:00:00Z"
    }
  ]
}
```

---

#### Get Player by ID

**GET** `/api/players/{player_id}`

Get detailed information about a specific player.

**Path Parameters:**
- `player_id` (int, required): Player ID

**Example:**
```http
GET /api/players/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Robert Lewandowski",
  "position": "FW",
  "team": "Barcelona",
  "nationality": "Poland",
  "fbref_id": "8d78e732",
  "season_stats": {
    "2025-2026": {
      "league": {
        "games": 15,
        "goals": 12,
        "assists": 5,
        "xg": 10.5,
        "xa": 3.2
      }
    }
  }
}
```

---

### 📊 Statistics

#### Get Player Statistics

**GET** `/api/stats/{player_id}`

Get comprehensive statistics for a player.

**Query Parameters:**
- `season` (string, optional): Filter by season (e.g., "2025-2026")
- `competition_type` (string, optional): LEAGUE, EUROPEAN_CUPS, DOMESTIC_CUPS, NATIONAL_TEAM

**Example:**
```http
GET /api/stats/1?season=2025-2026&competition_type=LEAGUE
```

**Response:**
```json
{
  "player_id": 1,
  "player_name": "Robert Lewandowski",
  "season": "2025-2026",
  "statistics": [
    {
      "competition_type": "LEAGUE",
      "competition_name": "La Liga",
      "games": 15,
      "games_starts": 14,
      "minutes": 1260,
      "goals": 12,
      "assists": 5,
      "xg": 10.5,
      "xa": 3.2,
      "npxg": 9.8,
      "yellow_cards": 2,
      "red_cards": 0
    }
  ],
  "data_attribution": "Statistics © FBref.com (Sports Reference LLC)"
}
```

---

#### Get Competition Stats

**GET** `/api/competition-stats`

Get statistics grouped by competition.

**Query Parameters:**
- `player_id` (int, required): Player ID
- `season` (string, optional): Filter by season

**Response:**
```json
{
  "player_id": 1,
  "season": "2025-2026",
  "league_stats": {
    "games": 15,
    "goals": 12,
    "assists": 5
  },
  "european_cups": {
    "games": 8,
    "goals": 6,
    "assists": 2
  },
  "domestic_cups": {
    "games": 3,
    "goals": 2,
    "assists": 1
  },
  "national_team": {
    "games": 8,
    "goals": 5,
    "assists": 3
  }
}
```

---

### 🏆 Matches

#### Get Player Matches

**GET** `/api/matches/{player_id}`

Get individual match data for a player.

**Query Parameters:**
- `season` (string, optional): Filter by season
- `competition` (string, optional): Filter by competition
- `limit` (int, optional): Max results (default: 50)

**Example:**
```http
GET /api/matches/1?season=2025-2026&limit=10
```

**Response:**
```json
{
  "player_id": 1,
  "matches": [
    {
      "match_date": "2025-11-17",
      "opponent": "Real Madrid",
      "competition": "La Liga",
      "minutes_played": 90,
      "goals": 2,
      "assists": 1,
      "xg": 1.8,
      "xa": 0.9
    }
  ],
  "data_attribution": "Match data © FBref.com"
}
```

---

### ⚖️ Comparison

#### Compare Players

**POST** `/api/comparison`

Compare statistics of multiple players.

**Request Body:**
```json
{
  "player_ids": [1, 2],
  "season": "2025-2026",
  "metrics": ["goals", "assists", "xg", "xa"]
}
```

**Response:**
```json
{
  "comparison": [
    {
      "player_id": 1,
      "name": "Robert Lewandowski",
      "goals": 12,
      "assists": 5,
      "xg": 10.5,
      "xa": 3.2
    },
    {
      "player_id": 2,
      "name": "Piotr Zieliński",
      "goals": 4,
      "assists": 8,
      "xg": 3.2,
      "xa": 6.5
    }
  ]
}
```

---

## 📈 Advanced Metrics

### xGI (Expected Goal Involvement)

**Formula:** `xGI = xG + xA`

Represents total expected contribution to goals (both scoring and assisting).

### Per 90 Metrics

All per 90 metrics are calculated as:
```
metric_per_90 = (metric_value / minutes_played) * 90
```

**Available:**
- `goals_per_90`
- `assists_per_90`
- `xg_per_90`
- `xa_per_90`
- `npxg_per_90`
- `xgi_per_90`

---

## 🚨 Error Responses

### 404 Not Found
```json
{
  "detail": "Player not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["query", "limit"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 📊 Data Attribution

**All statistics in API responses are sourced from:**
- **FBref.com** (© Sports Reference LLC)
- **URL:** https://fbref.com/

**Usage Terms:**
- Educational and non-commercial use only
- See [LEGAL_NOTICE.md](LEGAL_NOTICE.md) for full terms

---

## 🔄 Rate Limiting

**Current:** No rate limiting (free tier)

**Recommended usage:**
- Max 100 requests/minute
- Cache responses when possible

**Future (if commercial):**
- Free tier: 100 requests/hour
- Paid tier: 10,000 requests/hour

---

## 📝 Changelog

### v0.7.3 (Current)
- ✅ Enhanced stats (xGI, per 90 metrics)
- ✅ Legal compliance added
- ✅ Updated documentation

### v0.7.0
- Added xG/xA statistics
- Added per 90 metrics
- Enhanced player details

---

## 🐛 Known Issues

1. **Cold Start:** First request after 15min inactivity may take 30-60s (Render free tier)
2. **xG Data:** Not available for all leagues/seasons
3. **Nations League 2024-2025:** Excluded from 2025 national team stats (matches were in 2024)

---

## 📞 Support

**Issues:** https://github.com/your-username/polish-players-tracker/issues  
**Email:** your-email@example.com

---

## 📚 Related Documentation

- [LEGAL_NOTICE.md](LEGAL_NOTICE.md) - Legal terms and data attribution
- [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md) - Deployment guide
- [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - System architecture
- [README.md](README.md) - Project overview

---

**Last Updated:** 25.11.2025  
**Version:** 0.7.3  
**Status:** ✅ Production Ready (Non-Commercial)
