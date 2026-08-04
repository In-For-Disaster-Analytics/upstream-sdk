"""
Note management for the Upstream API.

Notes can be attached at four scopes — campaign, station, sensor, and
measurement — each with its own list/create endpoints. Campaign- and
station-scoped notes additionally expose a `/locations` endpoint for
plotting any note with an independent location (currently only ever
populated on measurement notes) on a coverage map. Update and delete
are scope-prefixed in the URL but operate on a note by its own id.
"""

from typing import Any, Dict, Optional, cast

from .auth import AuthManager
from .exceptions import ValidationError
from .http import request_json
from .utils import get_logger

logger = get_logger(__name__)


class NoteManager:
    """Manage campaign, station, sensor, and measurement notes via the Upstream API."""

    def __init__(self, auth_manager: AuthManager) -> None:
        self.auth_manager = auth_manager

    def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        headers = self.auth_manager.get_headers()
        url = self.auth_manager.build_url(path)
        return request_json(
            method,
            url,
            headers=headers,
            json=json,
            timeout=self.auth_manager.config.timeout,
            verify=self.auth_manager.config.request_verify,
        )

    # -- campaign-scoped ---------------------------------------------------

    def list_campaign_notes(self, campaign_id: int) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        return cast(
            Dict[str, Any],
            self._request("GET", f"/api/v1/campaigns/{campaign_id}/notes"),
        )

    def create_campaign_note(self, campaign_id: int, content: str) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not content:
            raise ValidationError("Content is required", field="content")
        return cast(
            Dict[str, Any],
            self._request(
                "POST",
                f"/api/v1/campaigns/{campaign_id}/notes",
                json={"content": content},
            ),
        )

    def list_campaign_note_locations(self, campaign_id: int) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        return cast(
            Dict[str, Any],
            self._request("GET", f"/api/v1/campaigns/{campaign_id}/notes/locations"),
        )

    def update_campaign_note(
        self, campaign_id: int, note_id: int, content: str
    ) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not note_id:
            raise ValidationError("Note ID is required", field="note_id")
        if not content:
            raise ValidationError("Content is required", field="content")
        return cast(
            Dict[str, Any],
            self._request(
                "PATCH",
                f"/api/v1/campaigns/{campaign_id}/notes/{note_id}",
                json={"content": content},
            ),
        )

    def delete_campaign_note(self, campaign_id: int, note_id: int) -> None:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not note_id:
            raise ValidationError("Note ID is required", field="note_id")
        self._request("DELETE", f"/api/v1/campaigns/{campaign_id}/notes/{note_id}")

    # -- station-scoped ------------------------------------------------------

    def list_station_notes(self, campaign_id: int, station_id: int) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        return cast(
            Dict[str, Any],
            self._request(
                "GET",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}/notes",
            ),
        )

    def create_station_note(
        self, campaign_id: int, station_id: int, content: str
    ) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not content:
            raise ValidationError("Content is required", field="content")
        return cast(
            Dict[str, Any],
            self._request(
                "POST",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}/notes",
                json={"content": content},
            ),
        )

    def list_station_note_locations(
        self, campaign_id: int, station_id: int
    ) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        return cast(
            Dict[str, Any],
            self._request(
                "GET",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
                "/notes/locations",
            ),
        )

    def update_station_note(
        self, campaign_id: int, station_id: int, note_id: int, content: str
    ) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not note_id:
            raise ValidationError("Note ID is required", field="note_id")
        if not content:
            raise ValidationError("Content is required", field="content")
        return cast(
            Dict[str, Any],
            self._request(
                "PATCH",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
                f"/notes/{note_id}",
                json={"content": content},
            ),
        )

    def delete_station_note(
        self, campaign_id: int, station_id: int, note_id: int
    ) -> None:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not note_id:
            raise ValidationError("Note ID is required", field="note_id")
        self._request(
            "DELETE",
            f"/api/v1/campaigns/{campaign_id}/stations/{station_id}/notes/{note_id}",
        )

    # -- sensor-scoped -------------------------------------------------------

    def list_sensor_notes(
        self, campaign_id: int, station_id: int, sensor_id: int
    ) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        return cast(
            Dict[str, Any],
            self._request(
                "GET",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
                f"/sensors/{sensor_id}/notes",
            ),
        )

    def create_sensor_note(
        self, campaign_id: int, station_id: int, sensor_id: int, content: str
    ) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not content:
            raise ValidationError("Content is required", field="content")
        return cast(
            Dict[str, Any],
            self._request(
                "POST",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
                f"/sensors/{sensor_id}/notes",
                json={"content": content},
            ),
        )

    def update_sensor_note(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        note_id: int,
        content: str,
    ) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not note_id:
            raise ValidationError("Note ID is required", field="note_id")
        if not content:
            raise ValidationError("Content is required", field="content")
        return cast(
            Dict[str, Any],
            self._request(
                "PATCH",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
                f"/sensors/{sensor_id}/notes/{note_id}",
                json={"content": content},
            ),
        )

    def delete_sensor_note(
        self, campaign_id: int, station_id: int, sensor_id: int, note_id: int
    ) -> None:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not note_id:
            raise ValidationError("Note ID is required", field="note_id")
        self._request(
            "DELETE",
            f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
            f"/sensors/{sensor_id}/notes/{note_id}",
        )

    # -- measurement-scoped (the only scope that carries its own location) --

    def list_measurement_notes(
        self, campaign_id: int, station_id: int, sensor_id: int, measurement_id: int
    ) -> Dict[str, Any]:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not measurement_id:
            raise ValidationError("Measurement ID is required", field="measurement_id")
        return cast(
            Dict[str, Any],
            self._request(
                "GET",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
                f"/sensors/{sensor_id}/measurements/{measurement_id}/notes",
            ),
        )

    def create_measurement_note(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        measurement_id: int,
        content: str,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a measurement note. `location` is WKT, e.g. "POINT(lon lat)" —
        independent of the measurement's own location, and only meaningful here
        (campaign/station/sensor notes have no location field)."""
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not measurement_id:
            raise ValidationError("Measurement ID is required", field="measurement_id")
        if not content:
            raise ValidationError("Content is required", field="content")
        payload: Dict[str, Any] = {"content": content}
        if location is not None:
            payload["location"] = location
        return cast(
            Dict[str, Any],
            self._request(
                "POST",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
                f"/sensors/{sensor_id}/measurements/{measurement_id}/notes",
                json=payload,
            ),
        )

    def update_measurement_note(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        measurement_id: int,
        note_id: int,
        content: str,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Full-replacement semantics for `location`, matching `content`: pass the
        desired location (WKT) or omit/None to clear it."""
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not measurement_id:
            raise ValidationError("Measurement ID is required", field="measurement_id")
        if not note_id:
            raise ValidationError("Note ID is required", field="note_id")
        if not content:
            raise ValidationError("Content is required", field="content")
        payload: Dict[str, Any] = {"content": content, "location": location}
        return cast(
            Dict[str, Any],
            self._request(
                "PATCH",
                f"/api/v1/campaigns/{campaign_id}/stations/{station_id}"
                f"/sensors/{sensor_id}/measurements/{measurement_id}/notes/{note_id}",
                json=payload,
            ),
        )

    def delete_measurement_note(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        measurement_id: int,
        note_id: int,
    ) -> None:
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not measurement_id:
            raise ValidationError("Measurement ID is required", field="measurement_id")
        if not note_id:
            raise ValidationError("Note ID is required", field="note_id")
        self._request(
            "DELETE",
            f"/api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}"
            f"/measurements/{measurement_id}/notes/{note_id}",
        )
