"""
Upstream API CKAN proxy endpoints.
"""

from typing import Any, Dict, List, Optional

from .auth import AuthManager
from .exceptions import ValidationError
from .http import request_json
from .utils import get_logger

logger = get_logger(__name__)


class CkanApiManager:
    """Access CKAN-related endpoints exposed by the Upstream API."""

    def __init__(self, auth_manager: AuthManager) -> None:
        self.auth_manager = auth_manager

    def list_organizations(
        self, tapis_token: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        token_value = tapis_token or self.auth_manager.get_tapis_token()
        if not token_value:
            raise ValidationError("Tapis access token is required", field="tapis_token")

        headers = self.auth_manager.get_headers(
            include_tapis_token=True, tapis_token=token_value
        )
        url = self.auth_manager.build_url("/api/v1/ckan/organizations")
        response = request_json(
            "GET", url, headers=headers, timeout=self.auth_manager.config.timeout
        )
        return response or []
