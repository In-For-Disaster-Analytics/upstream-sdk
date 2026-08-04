"""
Unit tests for note management (NoteManager).
"""

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from upstream.auth import AuthManager
from upstream.exceptions import ValidationError
from upstream.notes import NoteManager
from upstream.utils import ConfigManager

pytestmark = pytest.mark.unit


@pytest.fixture
def note_manager():
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
    return NoteManager(auth_manager)


def test_list_campaign_notes(note_manager):
    with patch("upstream.notes.request_json") as mock_request:
        mock_request.return_value = {"items": [], "total": 0}
        result = note_manager.list_campaign_notes(1)

    assert result == {"items": [], "total": 0}
    args, kwargs = mock_request.call_args
    assert args[0] == "GET"
    assert args[1].endswith("/api/v1/campaigns/1/notes")


def test_create_campaign_note_requires_content(note_manager):
    with pytest.raises(ValidationError):
        note_manager.create_campaign_note(1, "")


def test_create_campaign_note(note_manager):
    with patch("upstream.notes.request_json") as mock_request:
        mock_request.return_value = {"id": 42}
        result = note_manager.create_campaign_note(1, "Deployed new sensor")

    assert result == {"id": 42}
    args, kwargs = mock_request.call_args
    assert args[0] == "POST"
    assert args[1].endswith("/api/v1/campaigns/1/notes")
    assert kwargs["json"] == {"content": "Deployed new sensor"}


def test_list_campaign_note_locations(note_manager):
    with patch("upstream.notes.request_json") as mock_request:
        mock_request.return_value = {"items": [], "total": 0}
        note_manager.list_campaign_note_locations(1)

    args, _ = mock_request.call_args
    assert args[1].endswith("/api/v1/campaigns/1/notes/locations")


def test_create_station_note_requires_station_id(note_manager):
    with pytest.raises(ValidationError):
        note_manager.create_station_note(1, None, "content")


def test_update_station_note(note_manager):
    with patch("upstream.notes.request_json") as mock_request:
        mock_request.return_value = {"id": 5, "content": "updated"}
        note_manager.update_station_note(1, 2, 5, "updated")

    args, kwargs = mock_request.call_args
    assert args[0] == "PATCH"
    assert args[1].endswith("/api/v1/campaigns/1/stations/2/notes/5")
    assert kwargs["json"] == {"content": "updated"}


def test_delete_sensor_note(note_manager):
    with patch("upstream.notes.request_json") as mock_request:
        mock_request.return_value = None
        note_manager.delete_sensor_note(1, 2, 3, 9)

    args, _ = mock_request.call_args
    assert args[0] == "DELETE"
    assert args[1].endswith(
        "/api/v1/campaigns/1/stations/2/sensors/3/notes/9"
    )


def test_create_measurement_note_with_location(note_manager):
    with patch("upstream.notes.request_json") as mock_request:
        mock_request.return_value = {"id": 7}
        note_manager.create_measurement_note(
            1, 2, 3, 4, "plume traced upwind", location="POINT(10.1 20.2)"
        )

    args, kwargs = mock_request.call_args
    assert args[0] == "POST"
    assert args[1].endswith(
        "/api/v1/campaigns/1/stations/2/sensors/3/measurements/4/notes"
    )
    assert kwargs["json"] == {
        "content": "plume traced upwind",
        "location": "POINT(10.1 20.2)",
    }


def test_create_measurement_note_without_location_omits_field(note_manager):
    with patch("upstream.notes.request_json") as mock_request:
        mock_request.return_value = {"id": 8}
        note_manager.create_measurement_note(1, 2, 3, 4, "no location")

    _, kwargs = mock_request.call_args
    assert kwargs["json"] == {"content": "no location"}


def test_update_measurement_note_clears_location_with_none(note_manager):
    with patch("upstream.notes.request_json") as mock_request:
        mock_request.return_value = {"id": 8}
        note_manager.update_measurement_note(1, 2, 3, 4, 8, "still here", location=None)

    _, kwargs = mock_request.call_args
    # Full-replacement semantics: explicit None must still be sent to clear it.
    assert kwargs["json"] == {"content": "still here", "location": None}


def test_delete_measurement_note_requires_measurement_id(note_manager):
    with pytest.raises(ValidationError):
        note_manager.delete_measurement_note(1, 2, 3, None, 9)
