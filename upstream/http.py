"""
HTTP helpers for Upstream SDK.
"""

from typing import Any, Dict, Optional, Union

import requests

from .exceptions import APIError, NetworkError


def request_json(
    method: str,
    url: str,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    verify: Optional[Union[bool, str]] = None,
) -> Any:
    """Perform an HTTP request and return JSON content."""
    request_kwargs: Dict[str, Any] = {
        "headers": headers,
        "params": params,
        "json": json,
        "timeout": timeout,
    }
    if verify is not None:
        request_kwargs["verify"] = verify

    try:
        response = requests.request(method, url, **request_kwargs)
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
