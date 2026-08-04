"""
Unit tests for custom metadata schema management (MetadataSchemaManager).
"""

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from upstream.auth import AuthManager
from upstream.exceptions import ValidationError
from upstream.metadata_schema import MetadataSchemaManager
from upstream.utils import ConfigManager

pytestmark = pytest.mark.unit


@pytest.fixture
def schema_manager():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.portals.tapis.io",
    )
    auth_manager = AuthManager(config)
    # Pre-seed a cached token so get_headers() doesn't attempt a real
    # network authentication call — mirrors an already-logged-in session.
    auth_manager.access_token = "fake-token"
    auth_manager.token_expires_at = datetime.now() + timedelta(hours=1)
    return MetadataSchemaManager(auth_manager)


def test_list_schema_no_filters(schema_manager):
    with patch("upstream.metadata_schema.request_json") as mock_request:
        mock_request.return_value = {"items": []}
        schema_manager.list_schema()

    _, kwargs = mock_request.call_args
    assert kwargs["params"] is None


def test_list_schema_with_filters(schema_manager):
    with patch("upstream.metadata_schema.request_json") as mock_request:
        mock_request.return_value = {"items": []}
        schema_manager.list_schema(scope="station", active_only=True)

    _, kwargs = mock_request.call_args
    assert kwargs["params"] == {"scope": "station", "active_only": True}


def test_get_schema_requires_id(schema_manager):
    with pytest.raises(ValidationError):
        schema_manager.get_schema(None)


def test_create_schema_requires_required_fields(schema_manager):
    with pytest.raises(ValidationError):
        schema_manager.create_schema(
            scope="", key="instrument_type", label="Instrument", field_type="string"
        )


def test_create_schema(schema_manager):
    with patch("upstream.metadata_schema.request_json") as mock_request:
        mock_request.return_value = {"id": 1, "scope": "sensor"}
        result = schema_manager.create_schema(
            scope="sensor",
            key="instrument_type",
            label="Instrument Type",
            field_type="string",
            required=True,
        )

    assert result == {"id": 1, "scope": "sensor"}
    args, kwargs = mock_request.call_args
    assert args[0] == "POST"
    assert args[1].endswith("/api/v1/metadata-schema")
    assert kwargs["json"]["scope"] == "sensor"
    assert kwargs["json"]["key"] == "instrument_type"
    assert kwargs["json"]["required"] is True
    assert kwargs["json"]["ckan_mode"] == "extra"  # default preserved


def test_update_schema_sends_only_passed_fields(schema_manager):
    with patch("upstream.metadata_schema.request_json") as mock_request:
        mock_request.return_value = {"id": 1, "active": False}
        schema_manager.update_schema(1, active=False)

    args, kwargs = mock_request.call_args
    assert args[0] == "PATCH"
    assert args[1].endswith("/api/v1/metadata-schema/1")
    assert kwargs["json"] == {"active": False}


def test_delete_schema(schema_manager):
    with patch("upstream.metadata_schema.request_json") as mock_request:
        mock_request.return_value = None
        schema_manager.delete_schema(1)

    args, _ = mock_request.call_args
    assert args[0] == "DELETE"
    assert args[1].endswith("/api/v1/metadata-schema/1")


def test_delete_schema_requires_id(schema_manager):
    with pytest.raises(ValidationError):
        schema_manager.delete_schema(None)
