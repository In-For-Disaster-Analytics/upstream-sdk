"""
HTTP helpers for Upstream SDK.
"""

from typing import Any, Dict, Optional

import requests

from .exceptions import APIError, NetworkError


def request_json(
    method: str,
    url: str,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Any:
    """Perform an HTTP request and return JSON content."""
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise NetworkError(f"Request failed: {exc}") from exc

    if response.status_code >= 400:
        try:
            data = response.json()
        except ValueError:
            data = {"raw_body": response.text}
        raise APIError(
            message=f"API request failed: {response.status_code}",
            status_code=response.status_code,
            response_data=data,
        )

    if response.status_code == 204 or not response.text:
        return None

    try:
        return response.json()
    except ValueError:
        return response.text
