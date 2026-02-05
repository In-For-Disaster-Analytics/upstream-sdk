"""
Sensor management module for the Upstream SDK using OpenAPI client.

This module handles retrieval and management of sensors
using the generated OpenAPI client.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from upstream_api_client.api import SensorsApi
from upstream_api_client.models import (
    GetSensorResponse,
    ListSensorsResponsePagination,
    SensorCreateResponse,
    SensorUpdate,
)
from upstream_api_client.rest import ApiException

from .auth import AuthManager
from .data import DataUploader
from .exceptions import APIError, ValidationError
from .http import request_json
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
        self.data_uploader = DataUploader(auth_manager)

    def get(
        self, sensor_id: int, station_id: int, campaign_id: int
    ) -> GetSensorResponse:
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

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.get_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_get(
                    sensor_id=sensor_id,
                    station_id=station_id,
                    campaign_id=campaign_id,
                )

                return response

        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404)
            else:
                raise APIError(f"Failed to get sensor: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to get sensor: {e}")

    def list(
        self,
        campaign_id: int,
        station_id: int,
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

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.list_sensors_api_v1_campaigns_campaign_id_stations_station_id_sensors_get(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    limit=limit,
                    page=page,
                    **kwargs,
                )

                return response

        except ApiException as e:
            raise APIError(f"Failed to list sensors: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to list sensors: {e}")

    def update(
        self,
        sensor_id: int,
        station_id: int,
        campaign_id: int,
        sensor_update: SensorUpdate,
    ) -> SensorCreateResponse:
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
            raise ValidationError(
                "sensor_update must be a SensorUpdate instance", field="sensor_update"
            )

        try:

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                response = sensors_api.partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_patch(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    sensor_update=sensor_update,
                )

                return response

        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404) from e
            elif e.status == 422:
                raise ValidationError(f"Sensor validation failed: {e}") from e
            else:
                raise APIError(
                    f"Failed to update sensor: {e}", status_code=e.status
                ) from e
        except Exception as e:
            raise APIError(f"Failed to update sensor: {e}") from e

    def delete(self, sensor_id: int, station_id: int, campaign_id: int) -> bool:
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

            with self.auth_manager.get_api_client() as api_client:
                sensors_api = SensorsApi(api_client)

                sensors_api.delete_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_delete(
                    campaign_id=campaign_id, station_id=station_id
                )

                logger.info(f"Deleted sensor: {sensor_id}")
                return True

        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404)
            else:
                raise APIError(f"Failed to delete sensor: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to delete sensor: {e}")

    def upload_csv_files(
        self,
        campaign_id: int,
        station_id: int,
        sensors_file: Union[str, Path, bytes, Tuple[str, bytes]],
        measurements_file: Union[str, Path, bytes, Tuple[str, bytes]],
        chunk_size: int = 1000,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload sensor and measurement CSV files to process and store data in the database.
        Measurements are uploaded in chunks to avoid HTTP timeouts with large files.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: File path, bytes, or tuple (filename, bytes) containing sensor metadata
            measurements_file: File path, bytes, or tuple (filename, bytes) containing measurement data
            chunk_size: Number of measurement lines per chunk (default: 1000)

        Returns:
            Response from the upload API containing processing results

        Raises:
            ValidationError: If IDs are invalid or files are not provided
            APIError: If upload fails

        CSV Format Requirements:

        Sensors CSV (sensors_file):
        - Header: alias,variablename,units,postprocess,postprocessscript
        - alias: Unique identifier for the sensor (used as column header in measurements)
        - variablename: Human-readable description of what the sensor measures
        - units: Measurement units (e.g., °C, %, hPa, m/s)
        - postprocess: Boolean flag indicating if post-processing is required
        - postprocessscript: Name of the post-processing script (if applicable)

        Measurements CSV (measurements_file):
        - Header: collectiontime,Lat_deg,Lon_deg,{sensor_aliases...}
        - collectiontime: Timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
        - Lat_deg: Latitude in decimal degrees
        - Lon_deg: Longitude in decimal degrees
        - Sensor columns: Each sensor alias from sensors.csv becomes a column header
        - Column names must exactly match the sensor aliases
        - Empty values are automatically handled

        File Requirements:
        - Maximum file size: 500 MB per file
        - Encoding: UTF-8
        - Timestamps should be in UTC or include timezone information
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensors_file:
            raise ValidationError("Sensors file is required", field="sensors_file")
        if not measurements_file:
            raise ValidationError(
                "Measurements file is required", field="measurements_file"
            )

        try:

            # Use DataUploader for file preparation and validation
            upload_file_sensors, measurements_chunks = self.data_uploader.prepare_files(
                campaign_id=campaign_id,
                station_id=station_id,
                sensors_file=sensors_file,
                measurements_file=measurements_file,
                chunk_size=chunk_size,
            )

            all_responses = []
            for i, chunk in enumerate(measurements_chunks):
                logger.info(
                    f"Uploading measurements chunk {i + 1}/{len(measurements_chunks)} ({len(chunk)} lines)"
                )

                response = self.data_uploader._post_upload(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_payload=upload_file_sensors,  # Always upload sensors file
                    measurements_payload=chunk,
                    tapis_token=tapis_token,
                )

                all_responses.append(response)

                logger.info(
                    f"Successfully uploaded {len(measurements_chunks)} measurement chunks for campaign {campaign_id}, station {station_id}"
                )
                return cast(Dict[str, Any], all_responses[-1]) if all_responses else {}

        except ApiException as e:
            if e.status == 422:
                raise ValidationError(f"File validation failed: {e}") from e
            else:
                raise APIError(
                    f"Failed to upload CSV files: {e}", status_code=e.status
                ) from e
        except Exception as e:
            raise APIError(f"Failed to upload CSV files: {e}") from e

    def force_update_statistics(
        self, campaign_id: int, station_id: int
    ) -> Dict[str, Any]:
        """
        Force update statistics for all sensors in a station.

        This method triggers a recalculation of statistics for all sensors
        associated with the specified station. Statistics include min/max values,
        averages, standard deviation, percentiles, and measurement counts.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID

        Returns:
            Response containing update status and processing information

        Raises:
            ValidationError: If IDs are invalid
            APIError: If statistics update fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")

        url = self.auth_manager.build_url(
            f"/api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/statistics"
        )
        headers = self.auth_manager.get_headers()
        try:
            response = request_json(
                "POST",
                url,
                headers=headers,
                timeout=self.auth_manager.config.timeout,
            )
            logger.info(
                "Force updated statistics for all sensors in station %s, campaign %s",
                station_id,
                campaign_id,
            )
            return response or {}
        except APIError as e:
            if e.status_code == 404:
                raise APIError(f"Station not found: {station_id}", status_code=404) from e
            raise APIError(
                f"Failed to force update sensor statistics: {e}",
                status_code=e.status_code,
            ) from e
        except Exception as e:
            raise APIError(f"Failed to force update sensor statistics: {e}") from e

    def force_update_single_sensor_statistics(
        self, campaign_id: int, station_id: int, sensor_id: int
    ) -> Dict[str, Any]:
        """
        Force update statistics for a single sensor.

        This method triggers a recalculation of statistics for a specific sensor.
        Statistics include min/max values, averages, standard deviation, percentiles,
        and measurement counts.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID

        Returns:
            Response containing update status and processing information

        Raises:
            ValidationError: If IDs are invalid
            APIError: If statistics update fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")

        url = self.auth_manager.build_url(
            f"/api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/statistics"
        )
        headers = self.auth_manager.get_headers()
        try:
            response = request_json(
                "POST",
                url,
                headers=headers,
                timeout=self.auth_manager.config.timeout,
            )
            logger.info(
                "Force updated statistics for sensor %s in station %s, campaign %s",
                sensor_id,
                station_id,
                campaign_id,
            )
            return response or {}
        except APIError as e:
            if e.status_code == 404:
                raise APIError(f"Sensor not found: {sensor_id}", status_code=404) from e
            raise APIError(
                f"Failed to force update sensor statistics: {e}",
                status_code=e.status_code,
            ) from e
        except Exception as e:
            raise APIError(f"Failed to force update sensor statistics: {e}") from e

    def publish(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        cascade: bool = False,
        force: bool = False,
        organization: Optional[str] = None,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Publish a sensor."""
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")

        include_tapis = bool(tapis_token or self.auth_manager.get_tapis_token())
        headers = self.auth_manager.get_headers(
            include_tapis_token=include_tapis, tapis_token=tapis_token
        )
        url = self.auth_manager.build_url(
            f"/api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/publish"
        )
        payload = {
            "cascade": cascade,
            "force": force,
            "organization": organization,
        }
        return request_json(
            "POST",
            url,
            headers=headers,
            json=payload,
            timeout=self.auth_manager.config.timeout,
        )

    def unpublish(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        cascade: bool = False,
        force: bool = False,
        organization: Optional[str] = None,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Unpublish a sensor."""
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not sensor_id:
            raise ValidationError("Sensor ID is required", field="sensor_id")

        include_tapis = bool(tapis_token or self.auth_manager.get_tapis_token())
        headers = self.auth_manager.get_headers(
            include_tapis_token=include_tapis, tapis_token=tapis_token
        )
        url = self.auth_manager.build_url(
            f"/api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/unpublish"
        )
        payload = {
            "cascade": cascade,
            "force": force,
            "organization": organization,
        }
        return request_json(
            "POST",
            url,
            headers=headers,
            json=payload,
            timeout=self.auth_manager.config.timeout,
        )
