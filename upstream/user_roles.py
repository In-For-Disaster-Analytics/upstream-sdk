"""
User role management for the Upstream API.
"""

from typing import Any, Dict, List, cast

import requests

from .auth import AuthManager
from .exceptions import APIError, ValidationError
from .http import request_json
from .utils import get_logger

logger = get_logger(__name__)


class UserRoleManager:
    """Manage user roles via the Upstream API (admin only)."""

    def __init__(self, auth_manager: AuthManager) -> None:
        self.auth_manager = auth_manager

    def list_roles(self) -> List[Dict[str, Any]]:
        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url("/api/v1/user-roles")
        response = request_json(
            "GET", url, headers=headers, timeout=self.auth_manager.config.timeout
        )
        return cast(List[Dict[str, Any]], response or [])

    def upsert_role(self, username: str, role: str) -> Dict[str, Any]:
        if not username:
            raise ValidationError("Username is required", field="username")
        if not role:
            raise ValidationError("Role is required", field="role")

        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url(f"/api/v1/user-roles/{username}")
        payload = {"role": role}
        return cast(
            Dict[str, Any],
            request_json(
                "PUT",
                url,
                headers=headers,
                json=payload,
                timeout=self.auth_manager.config.timeout,
            ),
        )

    def delete_role(self, username: str) -> bool:
        if not username:
            raise ValidationError("Username is required", field="username")

        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url(f"/api/v1/user-roles/{username}")
        try:
            response = requests.delete(
                url, headers=headers, timeout=self.auth_manager.config.timeout
            )
        except requests.RequestException as exc:
            raise APIError(f"Failed to delete user role: {exc}") from exc

        if response.status_code == 204:
            return True
        if response.status_code == 404:
            raise APIError("User role not found", status_code=404)
        raise APIError(
            f"Failed to delete user role: {response.status_code}",
            status_code=response.status_code,
            response_data={"raw_body": response.text},
        )
