"""
Authentication manager for Upstream SDK using OpenAPI client.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import requests
from upstream_api_client import ApiClient, Configuration
from upstream_api_client.rest import ApiException

from .exceptions import AuthenticationError, ConfigurationError, NetworkError
from .utils import ConfigManager

logger = logging.getLogger(__name__)


class AuthManager:
    """
    Manages authentication with the Upstream API using OpenAPI client.
    """

    def __init__(self, config: ConfigManager) -> None:
        """
        Initialize authentication manager.

        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.configuration = Configuration(host=config.base_url)
        self.api_client: Optional[ApiClient] = None
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.tapis_access_token: Optional[str] = None
        self.tapis_refresh_token: Optional[str] = None
        self.tapis_expires_at: Optional[int] = None
        self.username: Optional[str] = None
        self.role: Optional[str] = None

        # Validate configuration
        if not config.username or not config.password:
            raise ConfigurationError("Username and password are required")

    def authenticate(self) -> bool:
        """
        Authenticate with the Upstream API.

        Returns:
            True if authentication successful

        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            if self.config.username is None or self.config.password is None:
                raise AuthenticationError("Username and password are required")

            url = self._build_url("/api/v1/token")
            payload = {
                "username": self.config.username,
                "password": self.config.password,
                "grant_type": "password",
            }
            response = requests.post(url, data=payload, timeout=self.config.timeout)

            if response.status_code == 401:
                raise AuthenticationError("Invalid username or password")
            if response.status_code == 422:
                raise AuthenticationError("Authentication request validation failed")
            if response.status_code >= 400:
                raise AuthenticationError(
                    f"Authentication failed: {response.status_code} {response.text}"
                )

            data = response.json()

            # Store token information
            self.access_token = data.get("access_token")
            if not self.access_token:
                raise AuthenticationError("Authentication response missing access token")
            self.configuration.access_token = self.access_token

            # Additional auth context (optional)
            self.tapis_access_token = data.get("tapis_access_token")
            self.tapis_refresh_token = data.get("tapis_refresh_token")
            self.tapis_expires_at = data.get("tapis_expires_at")
            self.username = data.get("username") or self.config.username
            self.role = data.get("role")

            # Calculate expiration time (default to 1 hour if not provided)
            expires_in = data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            logger.info("Successfully authenticated with Upstream API")
            return True

        except requests.RequestException as e:
            raise NetworkError(f"Authentication request failed: {e}") from e
        except ApiException as e:
            raise AuthenticationError(f"Authentication failed: {e}") from e
        except Exception as e:
            raise NetworkError(f"Authentication request failed: {e}") from e

    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated with a valid token.

        Returns:
            True if authenticated with valid token
        """
        if not self.access_token or not self.token_expires_at:
            return False

        # Consider token expired if it expires within 5 minutes
        buffer_time = timedelta(minutes=5)
        return datetime.now() < (self.token_expires_at - buffer_time)

    def get_api_client(self) -> ApiClient:
        """
        Get authenticated API client.

        Returns:
            Configured API client with authentication

        Raises:
            AuthenticationError: If not authenticated
        """
        if not self.is_authenticated():
            if not self.authenticate():
                raise AuthenticationError("Failed to authenticate")

        return ApiClient(self.configuration)

    def get_headers(
        self,
        include_tapis_token: bool = False,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Get authentication headers for direct requests.

        Returns:
            Dictionary of headers including authorization
        """
        if not self.is_authenticated():
            if not self.authenticate():
                raise AuthenticationError("Failed to authenticate")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        if include_tapis_token:
            token_value = tapis_token or self.tapis_access_token
            if token_value:
                headers["X-TAPIS-TOKEN"] = token_value
        return headers

    def get_tapis_token(self) -> Optional[str]:
        """Return the cached Tapis access token if available."""
        return self.tapis_access_token

    def _build_url(self, path: str) -> str:
        base = (self.config.base_url or "").rstrip("/")
        if not path.startswith("/"):
            path = "/" + path
        return f"{base}{path}"

    def build_url(self, path: str) -> str:
        """Public wrapper for building absolute URLs."""
        return self._build_url(path)

    def refresh_token(self) -> bool:
        """
        Refresh authentication token.

        Returns:
            True if refresh successful
        """
        # For now, just re-authenticate
        # TODO: Implement proper token refresh if supported by API
        try:
            return self.authenticate()
        except Exception as e:
            logger.warning(f"Token refresh failed: {e}")
            return False

    def logout(self) -> None:
        """
        Logout and clear authentication tokens.
        """
        self.access_token = None
        self.token_expires_at = None
        self.configuration.access_token = None
        logger.info("Successfully logged out")
