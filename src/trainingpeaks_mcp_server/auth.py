"""OAuth authentication for TrainingPeaks API."""

import time
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import httpx
from .config import get_config


class TrainingPeaksAuth:
    """Handle OAuth authentication with TrainingPeaks API."""
    
    def __init__(self):
        self.config = get_config()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.expires_at: Optional[float] = None
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate the authorization URL for OAuth flow."""
        params = {
            "client_id": self.config.client_id,
            "response_type": "code",
            "redirect_uri": self.config.redirect_uri,
            "scope": self.config.scopes,
        }
        if state:
            params["state"] = state
        
        return f"{self.config.auth_url}?{urlencode(params)}"
    
    async def exchange_code_for_token(self, authorization_code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        data = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "code": authorization_code,
            "redirect_uri": self.config.redirect_uri,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.config.token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            self._store_token_data(token_data)
            return token_data
    
    async def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh the access token using refresh token."""
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        
        data = {
            "grant_type": "refresh_token",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "refresh_token": self.refresh_token,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.config.token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            self._store_token_data(token_data)
            return token_data
    
    def _store_token_data(self, token_data: Dict[str, Any]) -> None:
        """Store token data from API response."""
        self.access_token = token_data.get("access_token")
        self.refresh_token = token_data.get("refresh_token")
        
        expires_in = token_data.get("expires_in")
        if expires_in:
            self.expires_at = time.time() + expires_in
    
    def is_token_expired(self) -> bool:
        """Check if the current access token is expired."""
        if not self.expires_at:
            return True
        return time.time() >= self.expires_at - 300  # 5 minute buffer
    
    async def get_valid_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        if not self.access_token or self.is_token_expired():
            if self.refresh_token:
                await self.refresh_access_token()
            else:
                raise ValueError("No valid token available. Please re-authenticate.")
        
        if not self.access_token:
            raise ValueError("Failed to obtain valid access token")
        
        return self.access_token
    
    def set_tokens(self, access_token: str, refresh_token: str, expires_in: int) -> None:
        """Manually set token data."""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = time.time() + expires_in