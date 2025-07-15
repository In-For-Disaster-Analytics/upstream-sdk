"""
Unit tests for authentication module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from upstream.auth import AuthManager, TokenManager
from upstream.exceptions import AuthenticationError, NetworkError
from upstream.utils import ConfigManager


class TestTokenManager:
    """Test cases for TokenManager class."""
    
    def test_init(self):
        """Test token manager initialization."""
        manager = TokenManager()
        
        assert manager.access_token is None
        assert manager.refresh_token is None
        assert manager.expires_at is None
    
    def test_set_tokens(self):
        """Test setting tokens."""
        manager = TokenManager()
        
        manager.set_tokens(
            access_token="test-access-token",
            refresh_token="test-refresh-token",
            expires_in=3600
        )
        
        assert manager.access_token == "test-access-token"
        assert manager.refresh_token == "test-refresh-token"
        assert manager.expires_at is not None
    
    def test_set_tokens_without_expires_in(self):
        """Test setting tokens without expiration time."""
        manager = TokenManager()
        
        manager.set_tokens(access_token="test-access-token")
        
        assert manager.access_token == "test-access-token"
        assert manager.expires_at is not None
    
    def test_is_expired_no_token(self):
        """Test token expiration check with no token."""
        manager = TokenManager()
        
        assert manager.is_expired() is True
    
    def test_is_expired_valid_token(self):
        """Test token expiration check with valid token."""
        manager = TokenManager()
        future_time = datetime.now() + timedelta(hours=1)
        
        manager.access_token = "test-token"
        manager.expires_at = future_time
        
        assert manager.is_expired() is False
    
    def test_is_expired_expired_token(self):
        """Test token expiration check with expired token."""
        manager = TokenManager()
        past_time = datetime.now() - timedelta(hours=1)
        
        manager.access_token = "test-token"
        manager.expires_at = past_time
        
        assert manager.is_expired() is True
    
    def test_clear(self):
        """Test clearing tokens."""
        manager = TokenManager()
        manager.set_tokens("test-token", "test-refresh", 3600)
        
        manager.clear()
        
        assert manager.access_token is None
        assert manager.refresh_token is None
        assert manager.expires_at is None


class TestAuthManager:
    """Test cases for AuthManager class."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        config = Mock(spec=ConfigManager)
        config.username = "test_user"
        config.password = "test_pass"
        config.base_url = "https://test.example.com"
        config.timeout = 30
        return config
    
    def test_init(self, mock_config):
        """Test auth manager initialization."""
        manager = AuthManager(mock_config)
        
        assert manager.config == mock_config
        assert manager.token_manager is not None
        assert manager.session is not None
    
    @patch('upstream.auth.requests.Session')
    def test_authenticate_success(self, mock_session_class, mock_config):
        """Test successful authentication."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "refresh_token": "test-refresh-token",
            "expires_in": 3600
        }
        mock_response.raise_for_status.return_value = None
        
        # Setup mock session
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        manager = AuthManager(mock_config)
        manager.authenticate()
        
        # Verify authentication call
        mock_session.post.assert_called_once_with(
            "https://test.example.com/auth/login",
            json={
                "username": "test_user",
                "password": "test_pass"
            }
        )
        
        # Verify token is set
        assert manager.token_manager.access_token == "test-access-token"
    
    @patch('upstream.auth.requests.Session')
    def test_authenticate_invalid_credentials(self, mock_session_class, mock_config):
        """Test authentication with invalid credentials."""
        # Setup mock response for 401 error
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("HTTP 401 Error")
        
        # Setup mock session
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        manager = AuthManager(mock_config)
        
        with pytest.raises(AuthenticationError, match="Invalid username or password"):
            manager.authenticate()
    
    @patch('upstream.auth.requests.Session')
    def test_authenticate_missing_credentials(self, mock_session_class):
        """Test authentication with missing credentials."""
        config = Mock(spec=ConfigManager)
        config.username = None
        config.password = "test_pass"
        config.base_url = "https://test.example.com"
        config.timeout = 30
        
        manager = AuthManager(config)
        
        with pytest.raises(AuthenticationError, match="Username and password are required"):
            manager.authenticate()
    
    @patch('upstream.auth.requests.Session')
    def test_authenticate_no_access_token(self, mock_session_class, mock_config):
        """Test authentication response without access token."""
        # Setup mock response without access token
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Login successful"}
        mock_response.raise_for_status.return_value = None
        
        # Setup mock session
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        manager = AuthManager(mock_config)
        
        with pytest.raises(AuthenticationError, match="No access token received"):
            manager.authenticate()
    
    @patch('upstream.auth.requests.Session')
    def test_refresh_token_success(self, mock_session_class, mock_config):
        """Test successful token refresh."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "new-access-token",
            "expires_in": 3600
        }
        mock_response.raise_for_status.return_value = None
        
        # Setup mock session
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        manager = AuthManager(mock_config)
        manager.token_manager.refresh_token = "test-refresh-token"
        
        manager.refresh_token()
        
        # Verify refresh call
        mock_session.post.assert_called_with(
            "https://test.example.com/auth/refresh",
            json={"refresh_token": "test-refresh-token"}
        )
        
        # Verify token is updated
        assert manager.token_manager.access_token == "new-access-token"
    
    @patch('upstream.auth.requests.Session')
    def test_refresh_token_no_refresh_token(self, mock_session_class, mock_config):
        """Test token refresh without refresh token."""
        # Setup mock for full authentication
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "refresh_token": "test-refresh-token",
            "expires_in": 3600
        }
        mock_response.raise_for_status.return_value = None
        
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        manager = AuthManager(mock_config)
        
        # Should fall back to full authentication
        manager.refresh_token()
        
        # Verify full authentication was called
        mock_session.post.assert_called_with(
            "https://test.example.com/auth/login",
            json={
                "username": "test_user",
                "password": "test_pass"
            }
        )
    
    def test_get_headers_valid_token(self, mock_config):
        """Test getting headers with valid token."""
        manager = AuthManager(mock_config)
        manager.token_manager.access_token = "test-token"
        manager.token_manager.expires_at = datetime.now() + timedelta(hours=1)
        
        headers = manager.get_headers()
        
        expected_headers = {
            "Authorization": "Bearer test-token",
            "Content-Type": "application/json"
        }
        assert headers == expected_headers
    
    def test_get_headers_no_token(self, mock_config):
        """Test getting headers without token."""
        manager = AuthManager(mock_config)
        
        with pytest.raises(AuthenticationError, match="No valid access token available"):
            manager.get_headers()
    
    def test_is_authenticated_true(self, mock_config):
        """Test authentication status check when authenticated."""
        manager = AuthManager(mock_config)
        manager.token_manager.access_token = "test-token"
        manager.token_manager.expires_at = datetime.now() + timedelta(hours=1)
        
        assert manager.is_authenticated() is True
    
    def test_is_authenticated_false(self, mock_config):
        """Test authentication status check when not authenticated."""
        manager = AuthManager(mock_config)
        
        assert manager.is_authenticated() is False
    
    @patch('upstream.auth.requests.Session')
    def test_logout_success(self, mock_session_class, mock_config):
        """Test successful logout."""
        # Setup mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        
        # Setup mock session
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        manager = AuthManager(mock_config)
        manager.token_manager.access_token = "test-token"
        manager.token_manager.expires_at = datetime.now() + timedelta(hours=1)
        
        manager.logout()
        
        # Verify logout call
        mock_session.post.assert_called_once()
        
        # Verify tokens are cleared
        assert manager.token_manager.access_token is None
    
    @patch('upstream.auth.requests.Session')
    def test_logout_request_fails(self, mock_session_class, mock_config):
        """Test logout when request fails."""
        # Setup mock session to raise exception
        mock_session = Mock()
        mock_session.post.side_effect = Exception("Network error")
        mock_session_class.return_value = mock_session
        
        manager = AuthManager(mock_config)
        manager.token_manager.access_token = "test-token"
        
        # Should not raise exception, just clear tokens
        manager.logout()
        
        # Verify tokens are still cleared despite error
        assert manager.token_manager.access_token is None