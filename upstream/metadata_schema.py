"""
Custom metadata schema management for the Upstream API.

Metadata schema fields define extra, admin-configurable fields for a given
scope (campaign, station, or sensor) — e.g. a required "instrument_type"
field on sensors. This mirrors the backend's MetadataSchemaCreate/Update
schemas: only `scope`, `key`, `label`, and `field_type` are required to
create a field; every other attribute is optional with a server-side default.
"""

from typing import Any, Dict, Optional, cast

from .auth import AuthManager
from .exceptions import ValidationError
from .http import request_json
from .utils import get_logger

logger = get_logger(__name__)


class MetadataSchemaManager:
    """Manage custom metadata schema fields via the Upstream API."""

    def __init__(self, auth_manager: AuthManager) -> None:
        self.auth_manager = auth_manager

    def list_schema(
        self, scope: Optional[str] = None, active_only: bool = False
    ) -> Dict[str, Any]:
        """List metadata schema fields, optionally filtered to one scope
        (campaign, station, sensor) and/or active fields only."""
        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url("/api/v1/metadata-schema")
        params: Dict[str, Any] = {}
        if scope is not None:
            params["scope"] = scope
        if active_only:
            params["active_only"] = active_only
        return cast(
            Dict[str, Any],
            request_json(
                "GET",
                url,
                headers=headers,
                params=params or None,
                timeout=self.auth_manager.config.timeout,
                verify=self.auth_manager.config.request_verify,
            ),
        )

    def get_schema(self, schema_id: int) -> Dict[str, Any]:
        if not schema_id:
            raise ValidationError("Schema ID is required", field="schema_id")
        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url(f"/api/v1/metadata-schema/{schema_id}")
        return cast(
            Dict[str, Any],
            request_json(
                "GET",
                url,
                headers=headers,
                timeout=self.auth_manager.config.timeout,
                verify=self.auth_manager.config.request_verify,
            ),
        )

    def create_schema(
        self,
        scope: str,
        key: str,
        label: str,
        field_type: str,
        required: bool = False,
        help_text: Optional[str] = None,
        units: Optional[str] = None,
        ckan_field: Optional[str] = None,
        ckan_mode: str = "extra",
        order_index: int = 0,
        active: bool = True,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a metadata schema field. `field_type` is one of: string,
        number, date, enum, bool, json."""
        if not scope:
            raise ValidationError("Scope is required", field="scope")
        if not key:
            raise ValidationError("Key is required", field="key")
        if not label:
            raise ValidationError("Label is required", field="label")
        if not field_type:
            raise ValidationError("Field type is required", field="field_type")

        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url("/api/v1/metadata-schema")
        payload = {
            "scope": scope,
            "key": key,
            "label": label,
            "field_type": field_type,
            "required": required,
            "help_text": help_text,
            "units": units,
            "ckan_field": ckan_field,
            "ckan_mode": ckan_mode,
            "order_index": order_index,
            "active": active,
            "options": options,
        }
        return cast(
            Dict[str, Any],
            request_json(
                "POST",
                url,
                headers=headers,
                json=payload,
                timeout=self.auth_manager.config.timeout,
                verify=self.auth_manager.config.request_verify,
            ),
        )

    def update_schema(self, schema_id: int, **fields: Any) -> Dict[str, Any]:
        """Partially update a metadata schema field. Accepts any subset of
        MetadataSchemaCreate's fields (scope, key, label, field_type,
        required, help_text, units, ckan_field, ckan_mode, order_index,
        active, options) — only fields passed are sent."""
        if not schema_id:
            raise ValidationError("Schema ID is required", field="schema_id")
        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url(f"/api/v1/metadata-schema/{schema_id}")
        return cast(
            Dict[str, Any],
            request_json(
                "PATCH",
                url,
                headers=headers,
                json=fields,
                timeout=self.auth_manager.config.timeout,
                verify=self.auth_manager.config.request_verify,
            ),
        )

    def delete_schema(self, schema_id: int) -> None:
        if not schema_id:
            raise ValidationError("Schema ID is required", field="schema_id")
        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url(f"/api/v1/metadata-schema/{schema_id}")
        request_json(
            "DELETE",
            url,
            headers=headers,
            timeout=self.auth_manager.config.timeout,
            verify=self.auth_manager.config.request_verify,
        )
