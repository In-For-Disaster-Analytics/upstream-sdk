"""
Exception classes for the Upstream SDK.

This module defines custom exception classes for different error conditions
that can occur when interacting with the Upstream API and CKAN platform.
"""

from typing import Optional, Any, Dict


class UpstreamError(Exception):
    """Base exception class for all Upstream SDK errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(UpstreamError):
    """Raised when authentication with the Upstream API fails."""
    
    def __init__(self, message: str = "Authentication failed", 
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, details)


class ValidationError(UpstreamError):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, details)
        self.field = field


class UploadError(UpstreamError):
    """Raised when data upload operations fail."""
    
    def __init__(self, message: str, 
                 upload_id: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, details)
        self.upload_id = upload_id


class APIError(UpstreamError):
    """Raised when API requests fail."""
    
    def __init__(self, message: str, 
                 status_code: Optional[int] = None,
                 response_data: Optional[Dict[str, Any]] = None,
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, details)
        self.status_code = status_code
        self.response_data = response_data or {}


class NetworkError(UpstreamError):
    """Raised when network operations fail."""
    
    def __init__(self, message: str = "Network operation failed",
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, details)


class ConfigurationError(UpstreamError):
    """Raised when SDK configuration is invalid."""
    
    def __init__(self, message: str, 
                 config_key: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, details)
        self.config_key = config_key


class RateLimitError(UpstreamError):
    """Raised when API rate limits are exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded",
                 retry_after: Optional[int] = None,
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, details)
        self.retry_after = retry_after