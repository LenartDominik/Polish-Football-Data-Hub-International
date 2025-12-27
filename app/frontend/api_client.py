"""API Client for Polish Players Tracker
Handles all communication with the FastAPI backend.
"""
import requests
import pandas as pd
from typing import Optional, List, Dict, Any
import streamlit as st
import os


class APIClient:
    """Client for communicating with the FastAPI backend"""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize API client with base URL"""
        if base_url is None:
            # Try to get from Streamlit secrets first, then environment, then default
            try:
                # Streamlit Cloud: read from secrets
                base_url = st.secrets.get("BACKEND_API_URL", None)
            except (AttributeError, FileNotFoundError):
                # Not in Streamlit Cloud or secrets not configured
                base_url = None
            
            # Fallback to environment variable
            if base_url is None:
                base_url = os.getenv("API_BASE_URL", None)
            
            # Final fallback to localhost
            if base_url is None:
                base_url = "http://localhost:8000"
        
        self.base_url = base_url.rstrip("/")
        self.timeout = 60  # seconds (increased for Cloud cold starts)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make HTTP request to API with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            st.error(f"? Cannot connect to API at {self.base_url}. Make sure the backend is running.")
            st.info("?? Start backend with: `python -m uvicorn app.backend.main:app --reload`")
            return None
        except requests.exceptions.Timeout:
            st.error(f"?? Request timeout after {self.timeout}s")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"? API Error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            st.error(f"? Unexpected error: {str(e)}")
            return None
    
    # ===== PLAYERS ENDPOINTS =====
    
    def get_all_players(self, name: Optional[str] = None, team: Optional[str] = None, league: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> pd.DataFrame:
        """Get players from API with optional filters and pagination"""
        params = {}
        if name:
            params['name'] = name
        if team:
            params['team'] = team
        if league:
            params['league'] = league
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        
        data = self._make_request("GET", "/api/players/", params=params if params else None)
        if data is None:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        return df
    
    def get_player(self, player_id: int) -> Optional[Dict]:
        """Get single player by ID"""
        return self._make_request("GET", f"/api/players/{player_id}")
    
    # ===== STATS ENDPOINTS =====
    
    def get_all_competition_stats(self) -> pd.DataFrame:
        """Get all competition stats (use cautiously; heavy). Prefer filtered methods below."""
        data = self._make_request("GET", "/api/players/stats/competition")
        if data is None:
            return pd.DataFrame()
        return pd.DataFrame(data)

    def get_competition_stats(self, player_id: int, season: Optional[str] = None, competition_type: Optional[str] = None, limit: Optional[int] = 100) -> pd.DataFrame:
        """Get competition stats filtered for a single player (and optional season/type)"""
        params = {'player_id': player_id}
        if season:
            params['season'] = season
        if competition_type:
            params['competition_type'] = competition_type
        if limit is not None:
            params['limit'] = limit
        data = self._make_request("GET", "/api/players/stats/competition", params=params)
        if data is None:
            return pd.DataFrame()
        return pd.DataFrame(data)
    
    def get_all_goalkeeper_stats(self) -> pd.DataFrame:
        """Get all goalkeeper stats (use cautiously; heavy). Prefer filtered methods below."""
        data = self._make_request("GET", "/api/players/stats/goalkeeper")
        if data is None:
            return pd.DataFrame()
        return pd.DataFrame(data)

    def get_goalkeeper_stats(self, player_id: int, season: Optional[str] = None, competition_type: Optional[str] = None, limit: Optional[int] = 100) -> pd.DataFrame:
        """Get goalkeeper stats filtered for a single player (and optional season/type)"""
        params = {'player_id': player_id}
        if season:
            params['season'] = season
        if competition_type:
            params['competition_type'] = competition_type
        if limit is not None:
            params['limit'] = limit
        data = self._make_request("GET", "/api/players/stats/goalkeeper", params=params)
        if data is None:
            return pd.DataFrame()
        return pd.DataFrame(data)
    
    def get_all_matches(self) -> pd.DataFrame:
        """Get all player matches"""
        data = self._make_request("GET", "/api/players/stats/matches")
        if data is None:
            return pd.DataFrame()
        return pd.DataFrame(data)
    
    # ===== COMPARISON ENDPOINTS =====
    
    def get_player_stats(self, player_id: int) -> Dict[str, pd.DataFrame]:
        """Get all stats for a player (competition_stats, goalkeeper_stats, player_matches)"""
        data = self._make_request("GET", f"/api/comparison/players/{player_id}/stats")
        if data is None:
            return {
                'competition_stats': pd.DataFrame(),
                'goalkeeper_stats': pd.DataFrame(),
                'player_matches': pd.DataFrame()
            }
        
        return {
            'competition_stats': pd.DataFrame(data.get('competition_stats', [])),
            'goalkeeper_stats': pd.DataFrame(data.get('goalkeeper_stats', [])),
            'player_matches': pd.DataFrame(data.get('player_matches', []))
        }
    
    # ===== MATCHLOGS ENDPOINTS =====
    
    def get_player_matches(
        self, 
        player_id: int,
        competition: Optional[str] = None,
        season: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = 100
    ) -> pd.DataFrame:
        """Get matches for a player with optional filters; returns just the matches list.
        The backend returns { 'matches': [...] }, so we extract that for a compact DataFrame.
        """
        params = {}
        if competition:
            params['competition'] = competition
        if season:
            params['season'] = season
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if limit:
            params['limit'] = limit
        
        data = self._make_request("GET", f"/api/matchlogs/{player_id}", params=params)
        if data is None:
            return pd.DataFrame()
        
        matches = data.get('matches', []) if isinstance(data, dict) else data
        df = pd.DataFrame(matches)
        
        # Add player_id column (needed for get_season_total_stats_by_date_range)
        if not df.empty:
            df['player_id'] = data.get('player_id', player_id) if isinstance(data, dict) else player_id
        
        # Normalize date column name for downstream code expecting 'match_date'
        if 'date' in df.columns and 'match_date' not in df.columns:
            df = df.rename(columns={'date': 'match_date'})
        return df


# Global API client instance
@st.cache_resource
def get_api_client(api_url=None) -> APIClient:
    """Get cached API client instance"""
    if api_url is not None:
        return APIClient(api_url)
    
    # Priority order:
    # 1. Streamlit secrets (for Streamlit Cloud)
    # 2. Environment variables (for local/Render)
    # 3. Default localhost
    
    api_url_env = None
    
    # Try Streamlit secrets first
    try:
        api_url_env = st.secrets.get("BACKEND_API_URL", None)
        if api_url_env:
            return APIClient(api_url_env)
    except (AttributeError, FileNotFoundError):
        pass
    
    # Try environment variables
    api_url_env = os.getenv("API_BASE_URL")
    if api_url_env:
        return APIClient(api_url_env)
    
    # Default to localhost
    return APIClient("http://localhost:8000")

