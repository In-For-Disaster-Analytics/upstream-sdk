"""
Authentication manager for Upstream SDK.
"""

import time
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta

import requests

from .exceptions import AuthenticationError, NetworkError
from .utils import ConfigManager

logger = logging.getLogger(__name__)


class TokenManager:
    """Manages authentication tokens and refresh logic."""
    
    def __init__(self) -> None:
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.expires_at: Optional[datetime] = None
    
    def set_tokens(
        self,
        access_token: str,
        refresh_token: Optional[str] = None,
        expires_in: Optional[int] = None,
    ) -> None:
        """
        Set authentication tokens.
        
        Args:
            access_token: Access token
            refresh_token: Refresh token
            expires_in: Token expiration time in seconds
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        
        if expires_in:
            self.expires_at = datetime.now() + timedelta(seconds=expires_in)
        else:
            # Default to 1 hour if not specified
            self.expires_at = datetime.now() + timedelta(hours=1)
    
    def is_expired(self) -> bool:
        """Check if current token is expired."""
        if not self.access_token or not self.expires_at:
            return True
        
        # Consider token expired 5 minutes before actual expiration
        return datetime.now() >= (self.expires_at - timedelta(minutes=5))
    
    def clear(self) -> None:
        """Clear all tokens."""
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None


class AuthManager:
    """
    Manages authentication with the Upstream API.
    
    Handles token acquisition, refresh, and automatic re-authentication.
    """
    
    def __init__(self, config: ConfigManager) -> None:
        """
        Initialize authentication manager.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.token_manager = TokenManager()
        self.session = requests.Session()
        self.session.timeout = config.timeout
    
    def authenticate(self) -> None:
        """
        Authenticate with the Upstream API.
        
        Raises:
            AuthenticationError: If authentication fails
        """
        if not self.config.username or not self.config.password:
            raise AuthenticationError("Username and password are required")
        
        auth_url = f"{self.config.base_url}/auth/login"
        
        auth_data = {
            "username": self.config.username,
            "password": self.config.password,
        }
        
        try:
            response = self.session.post(auth_url, json=auth_data)
            response.raise_for_status()
            
            auth_response = response.json()
            
            # Extract tokens from response
            access_token = auth_response.get("access_token")
            refresh_token = auth_response.get("refresh_token")
            expires_in = auth_response.get("expires_in")
            
            if not access_token:
                raise AuthenticationError("No access token received")
            
            self.token_manager.set_tokens(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
            )
            
            logger.info("Successfully authenticated with Upstream API")
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Authentication request failed: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise AuthenticationError("Invalid username or password")
            else:
                raise AuthenticationError(f"Authentication failed: {e}")
    
    def refresh_token(self) -> None:
        """
        Refresh the authentication token.
        
        Raises:
            AuthenticationError: If token refresh fails
        """
        if not self.token_manager.refresh_token:
            # No refresh token available, need to re-authenticate
            self.authenticate()
            return
        
        refresh_url = f"{self.config.base_url}/auth/refresh"
        
        refresh_data = {
            "refresh_token": self.token_manager.refresh_token,
        }
        
        try:
            response = self.session.post(refresh_url, json=refresh_data)
            response.raise_for_status()
            
            refresh_response = response.json()
            
            access_token = refresh_response.get("access_token")
            refresh_token = refresh_response.get("refresh_token")
            expires_in = refresh_response.get("expires_in")
            
            if not access_token:
                raise AuthenticationError("No access token received during refresh")
            
            self.token_manager.set_tokens(
                access_token=access_token,
                refresh_token=refresh_token or self.token_manager.refresh_token,
                expires_in=expires_in,
            )
            
            logger.info("Successfully refreshed authentication token")
            
        except requests.exceptions.RequestException as e:
            # Token refresh failed, try full re-authentication
            logger.warning(f"Token refresh failed: {e}. Attempting re-authentication.")
            self.authenticate()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                # Refresh token expired, need to re-authenticate
                logger.warning("Refresh token expired. Re-authenticating.")
                self.authenticate()
            else:
                raise AuthenticationError(f"Token refresh failed: {e}")
    
    def get_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary of headers including authorization
        """
        # Check if token needs refresh
        if self.token_manager.is_expired():
            self.refresh_token()
        
        if not self.token_manager.access_token:
            raise AuthenticationError("No valid access token available")
        
        return {
            "Authorization": f"Bearer {self.token_manager.access_token}",
            "Content-Type": "application/json",
        }
    
    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        return (
            self.token_manager.access_token is not None
            and not self.token_manager.is_expired()
        )
    
    def logout(self) -> None:
        """
        Logout and clear authentication tokens.
        """
        # Optionally, call logout endpoint if available
        logout_url = f"{self.config.base_url}/auth/logout"
        
        try:
            headers = self.get_headers()
            response = self.session.post(logout_url, headers=headers)
            response.raise_for_status()
            logger.info("Successfully logged out from Upstream API")
        except Exception as e:
            logger.warning(f"Logout request failed: {e}")
        
        # Clear tokens regardless of logout request result
        self.token_manager.clear()
        logger.info("Authentication tokens cleared")