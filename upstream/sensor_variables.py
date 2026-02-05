"""
Sensor variable lookups via the Upstream API.
"""

from typing import List

from .auth import AuthManager
from .http import request_json
from .utils import get_logger

logger = get_logger(__name__)


class SensorVariableManager:
    """List sensor variable names available in the system."""

    def __init__(self, auth_manager: AuthManager) -> None:
        self.auth_manager = auth_manager

    def list(self) -> List[str]:
        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url("/api/v1/sensor_variables")
        response = request_json(
            "GET", url, headers=headers, timeout=self.auth_manager.config.timeout
        )
        return response or []
