"""
Pods management for the Upstream API.
"""

from typing import Any, Dict, Optional

from .auth import AuthManager
from .exceptions import ValidationError
from .http import request_json
from .utils import get_logger

logger = get_logger(__name__)


class PodsManager:
    """Manage pod bundles via the Upstream API."""

    def __init__(self, auth_manager: AuthManager) -> None:
        self.auth_manager = auth_manager

    def create_bundle(
        self,
        base: str,
        pg_user: str,
        pg_password: str,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not base:
            raise ValidationError("Base name is required", field="base")
        if not pg_user:
            raise ValidationError("Postgres username is required", field="pg_user")
        if not pg_password:
            raise ValidationError("Postgres password is required", field="pg_password")

        token_value = tapis_token or self.auth_manager.get_tapis_token()
        if not token_value:
            raise ValidationError("Tapis access token is required", field="tapis_token")

        headers = self.auth_manager.get_headers(
            include_tapis_token=True, tapis_token=token_value
        )
        url = self.auth_manager.build_url("/api/v1/pods/bundle")
        payload = {"base": base, "pg_user": pg_user, "pg_password": pg_password}
        return request_json(
            "POST",
            url,
            headers=headers,
            json=payload,
            timeout=self.auth_manager.config.timeout,
        )
