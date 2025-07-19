"""TrainingPeaks API client."""

from typing import Dict, Any, List, Optional
import httpx
from .auth import TrainingPeaksAuth
from .config import get_config


class TrainingPeaksClient:
    """Client for interacting with TrainingPeaks API."""
    
    def __init__(self, auth: TrainingPeaksAuth):
        self.auth = auth
        self.config = get_config()
        self.base_url = self.config.api_base_url
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        token = await self.auth.get_valid_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_athlete_profile(self) -> Dict[str, Any]:
        """Get the authenticated athlete's profile information."""
        return await self._make_request("GET", "/v1/athlete")
    
    async def get_athlete_zones(self) -> Dict[str, Any]:
        """Get the authenticated athlete's training zones."""
        return await self._make_request("GET", "/v1/athlete/zones")
    
    async def get_workouts(
        self, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get athlete's workouts within a date range."""
        params = {"limit": limit}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        response = await self._make_request("GET", "/v1/athlete/workouts", params=params)
        return response.get("workouts", [])
    
    async def get_workout_details(self, workout_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific workout."""
        return await self._make_request("GET", f"/v1/athlete/workouts/{workout_id}")
    
    async def get_calendar_events(
        self, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get calendar events from athlete's TrainingPeaks calendar."""
        params = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        response = await self._make_request("GET", "/v1/athlete/calendar", params=params)
        return response.get("events", [])
    
    async def get_metrics(
        self, 
        metric_type: str,
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get metrics data (weight, HRV, steps, stress, sleep)."""
        params = {"type": metric_type}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        response = await self._make_request("GET", "/v1/athlete/metrics", params=params)
        return response.get("metrics", [])
    
    async def get_planned_workouts(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Get planned workouts up to 7 days in the future."""
        params = {"daysAhead": min(days_ahead, 7)}
        response = await self._make_request("GET", "/v1/athlete/planned-workouts", params=params)
        return response.get("workouts", [])