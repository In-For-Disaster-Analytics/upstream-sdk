"""
Sensor management module for the Upstream SDK using OpenAPI client.

This module handles retrieval and management of sensors
using the generated OpenAPI client.
"""

from typing import Optional, Any

from upstream_api_client.api import SensorsApi
from upstream_api_client.models import (
    SensorUpdate,
    GetSensorResponse,
    SensorCreateResponse,
    ListSensorsResponsePagination
)
from upstream_api_client.rest import ApiException

from .auth import AuthManager
from .exceptions import APIError, ValidationError
from .utils import get_logger

logger = get_logger(__name__)


class SensorManager:
    """
    Manages sensor operations using the OpenAPI client.
    """

    def __init__(self, auth_manager: AuthManager) -> None:
        """
        Initialize sensor manager.

        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager

    def get(self, sensor_id: str, station_id: str, campaign_id: str) -> GetSensorResponse:
        """
        Get sensor by ID.

        Args:
            sensor_id: Sensor ID
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            Sensor instance

        Raises:
            ValidationError: If IDs are invalid
            APIError: If sensor not found or retrieval fails
        """
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            sensor_id_int = int(sensor_id)
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.get_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_get(
                    sensor_id=sensor_id_int,
                    station_id=station_id_int,
                    campaign_id=campaign_id_int
                )

                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid ID format: sensor_id={sensor_id}, station_id={station_id}, campaign_id={campaign_id}") from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404)
            else:
                raise APIError(f"Failed to get sensor: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to get sensor: {e}")

    def list(
        self,
        campaign_id: str,
        station_id: str,
        limit: int = 100,
        page: int = 1,
        **kwargs: Any,
    ) -> ListSensorsResponsePagination:
        """
        List sensors for a station.

        Args:
            campaign_id: Campaign ID to filter by
            station_id: Station ID to filter by
            limit: Maximum number of sensors to return
            page: Page number for pagination
            **kwargs: Additional filtering parameters (variable_name, units, alias, etc.)

        Returns:
            List of Sensor instances

        Raises:
            ValidationError: If campaign_id or station_id is invalid
            APIError: If listing fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")

        try:
            campaign_id_int = int(campaign_id)
            station_id_int = int(station_id)

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.list_sensors_api_v1_campaigns_campaign_id_stations_station_id_sensors_get(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    limit=limit,
                    page=page,
                    **kwargs
                )

                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid ID format: campaign_id={campaign_id}, station_id={station_id}") from exc
        except ApiException as e:
            raise APIError(f"Failed to list sensors: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to list sensors: {e}")

    def update(self, sensor_id: str, station_id: str, campaign_id: str, sensor_update: SensorUpdate) -> SensorCreateResponse:
        """
        Update sensor.

        Args:
            sensor_id: Sensor ID
            station_id: Station ID
            campaign_id: Campaign ID
            sensor_update: SensorUpdate model instance

        Returns:
            Updated Sensor instance

        Raises:
            ValidationError: If IDs are invalid or sensor_update is not a SensorUpdate
            APIError: If update fails
        """
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not isinstance(sensor_update, SensorUpdate):
            raise ValidationError("sensor_update must be a SensorUpdate instance", field="sensor_update")

        try:
            sensor_id_int = int(sensor_id)
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_patch(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    sensor_id=sensor_id_int,
                    sensor_update=sensor_update
                )

                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid ID format: sensor_id={sensor_id}, station_id={station_id}, campaign_id={campaign_id}") from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404) from e
            elif e.status == 422:
                raise ValidationError(f"Sensor validation failed: {e}") from e
            else:
                raise APIError(f"Failed to update sensor: {e}", status_code=e.status) from e
        except Exception as e:
            raise APIError(f"Failed to update sensor: {e}") from e

    def delete(self, sensor_id: str, station_id: str, campaign_id: str) -> bool:
        """
        Delete sensor.

        Args:
            sensor_id: Sensor ID
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            True if deletion successful

        Raises:
            ValidationError: If IDs are invalid
            APIError: If deletion fails
        """
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            sensor_id_int = int(sensor_id)
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                sensors_api.delete_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_delete(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int
                )

                logger.info(f"Deleted sensor: {sensor_id}")
                return True

        except ValueError as exc:
            raise ValidationError(f"Invalid ID format: sensor_id={sensor_id}, station_id={station_id}, campaign_id={campaign_id}") from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404)
            else:
                raise APIError(f"Failed to delete sensor: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to delete sensor: {e}")