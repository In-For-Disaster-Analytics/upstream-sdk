"""
Main client class for the Upstream SDK.

This module provides the primary interface for interacting with the Upstream API
and CKAN data platform using the OpenAPI client.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, BinaryIO

from upstream_api_client import MeasurementCreateResponse, MeasurementIn
from upstream_api_client.models import CampaignsIn, StationCreate
from upstream_api_client.models.aggregated_measurement import AggregatedMeasurement
from upstream_api_client.models.campaign_create_response import CampaignCreateResponse
from upstream_api_client.models.get_campaign_response import GetCampaignResponse
from upstream_api_client.models.get_station_response import GetStationResponse
from upstream_api_client.models.list_campaigns_response_pagination import (
    ListCampaignsResponsePagination,
)
from upstream_api_client.models.list_measurements_response_pagination import (
    ListMeasurementsResponsePagination,
)
from upstream_api_client.models.list_stations_response_pagination import (
    ListStationsResponsePagination,
)
from upstream_api_client.models.measurement_update import MeasurementUpdate
from upstream_api_client.models.station_create_response import StationCreateResponse

from upstream.ckan import CKANIntegration

from .auth import AuthManager
from .campaigns import CampaignManager
from .ckan_api import CkanApiManager
from .data import DataUploader
from .measurements import MeasurementManager
from .pods import PodsManager
from .sensor_variables import SensorVariableManager
from .sensors import SensorManager
from .stations import StationManager
from .user_roles import UserRoleManager
from .utils import ConfigManager, get_logger

logger = get_logger(__name__)


class UpstreamClient:
    """Main client class for interacting with the Upstream API."""

    ckan: Optional[CKANIntegration]



    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        ckan_url: Optional[str] = None,
        ckan_organization: Optional[str] = None,
        config_file: Optional[Union[str, Path]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Upstream client.

        Args:
            username: Username for authentication
            password: Password for authentication
            base_url: Base URL for the Upstream API
            ckan_url: URL for CKAN integration
            ckan_organization: CKAN organization name
            config_file: Path to configuration file
            **kwargs: Additional configuration options

        Raises:
            ConfigurationError: If required configuration is missing
        """
        # Load configuration from file if provided
        if config_file:
            config = ConfigManager.from_file(config_file)
        else:
            config = ConfigManager(
                username=username,
                password=password,
                base_url=base_url,
                ckan_url=ckan_url,
                ckan_organization=ckan_organization,
                **kwargs,
            )
        # Initialize authentication manager
        self.auth_manager = AuthManager(config)

        # Initialize component managers
        self.campaigns = CampaignManager(self.auth_manager)
        self.stations = StationManager(self.auth_manager)
        self.sensors = SensorManager(self.auth_manager)
        self.measurements = MeasurementManager(self.auth_manager)
        self.data = DataUploader(self.auth_manager)
        self.sensor_variables = SensorVariableManager(self.auth_manager)
        self.ckan_api = CkanApiManager(self.auth_manager)
        self.pods = PodsManager(self.auth_manager)
        self.user_roles = UserRoleManager(self.auth_manager)

        # Initialize CKAN integration if URL provided
        if config.ckan_url:
            self.ckan = CKANIntegration(
                ckan_url=config.ckan_url, config=config.to_dict()
            )
        else:
            self.ckan = None

        logger.info("Upstream client initialized successfully")

    @classmethod
    def from_config(cls, config_file: Union[str, Path]) -> "UpstreamClient":
        """Create client from configuration file.

        Args:
            config_file: Path to configuration file (JSON or YAML)

        Returns:
            Configured UpstreamClient instance
        """
        return cls(config_file=config_file)

    @classmethod
    def from_environment(cls) -> "UpstreamClient":
        """Create client from environment variables.

        Environment variables:
        - UPSTREAM_USERNAME: Username for authentication
        - UPSTREAM_PASSWORD: Password for authentication
        - UPSTREAM_BASE_URL: Base URL for the Upstream API
        - CKAN_URL: URL for CKAN integration
        - CKAN_ORGANIZATION: CKAN organization name

        Returns:
            Configured UpstreamClient instance
        """
        return cls(
            username=os.environ.get("UPSTREAM_USERNAME"),
            password=os.environ.get("UPSTREAM_PASSWORD"),
            base_url=os.environ.get("UPSTREAM_BASE_URL"),
            ckan_url=os.environ.get("CKAN_URL"),
            ckan_organization=os.environ.get("CKAN_ORGANIZATION"),
        )

    def authenticate(self) -> bool:
        """Test authentication with the API.

        Returns:
            True if authentication successful, False otherwise
        """
        return self.auth_manager.authenticate()

    def create_campaign(self, campaign_in: CampaignsIn) -> CampaignCreateResponse:
        """Create a new monitoring campaign.

        Args:
            campaign_in: CampaignsIn model instance

        Returns:
            Created Campaign object
        """
        return self.campaigns.create(campaign_in)

    def get_campaign(self, campaign_id: int) -> GetCampaignResponse:
        """Get campaign by ID.

        Args:
            campaign_id: Campaign ID

        Returns:
            Campaign object
        """
        return self.campaigns.get(campaign_id)

    def list_campaigns(self, **kwargs: Any) -> ListCampaignsResponsePagination:
        """List all campaigns.

        Args:
            **kwargs: Additional filtering parameters

        Returns:
            List of Campaign objects
        """
        return self.campaigns.list(**kwargs)

    def create_station(
        self, campaign_id: int, station_create: StationCreate
    ) -> StationCreateResponse:
        """Create a new monitoring station.

        Args:
            campaign_id: ID of the campaign
            station_create: StationCreate model instance

        Returns:
            Created Station object
        """
        return self.stations.create(campaign_id, station_create)

    def get_station(self, station_id: int, campaign_id: int) -> GetStationResponse:
        """Get station by ID.

        Args:
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            Station object
        """
        return self.stations.get(station_id, campaign_id)

    def list_stations(
        self, campaign_id: int, **kwargs: Any
    ) -> ListStationsResponsePagination:
        """List stations for a campaign.

        Args:
            campaign_id: Campaign ID to filter by
            **kwargs: Additional filtering parameters

        Returns:
            List of Station objects
        """
        return self.stations.list(campaign_id=campaign_id, **kwargs)

    def upload_csv_data(
        self,
        campaign_id: int,
        station_id: int,
        sensors_file: Union[str, Path],
        measurements_file: Union[str, Path],
        tapis_token: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Upload sensor data from CSV files.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file
            **kwargs: Additional upload parameters

        Returns:
            Upload result dictionary
        """
        return self.data.upload_csv_data(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_file,
            measurements_file=measurements_file,
            tapis_token=tapis_token,
            **kwargs,
        )

    def get_campaign_permissions(self, campaign_id: int) -> Dict[str, Any]:
        """Get permissions for a campaign."""
        return self.campaigns.get_permissions(campaign_id)

    def publish_campaign(
        self,
        campaign_id: int,
        cascade: bool = True,
        force: bool = False,
        organization: Optional[str] = None,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Publish a campaign."""
        return self.campaigns.publish(
            campaign_id=campaign_id,
            cascade=cascade,
            force=force,
            organization=organization,
            tapis_token=tapis_token,
        )

    def unpublish_campaign(
        self,
        campaign_id: int,
        cascade: bool = True,
        force: bool = False,
        organization: Optional[str] = None,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Unpublish a campaign."""
        return self.campaigns.unpublish(
            campaign_id=campaign_id,
            cascade=cascade,
            force=force,
            organization=organization,
            tapis_token=tapis_token,
        )

    def publish_station(
        self,
        campaign_id: int,
        station_id: int,
        cascade: bool = False,
        force: bool = False,
        organization: Optional[str] = None,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Publish a station."""
        return self.stations.publish(
            campaign_id=campaign_id,
            station_id=station_id,
            cascade=cascade,
            force=force,
            organization=organization,
            tapis_token=tapis_token,
        )

    def unpublish_station(
        self,
        campaign_id: int,
        station_id: int,
        cascade: bool = False,
        force: bool = False,
        organization: Optional[str] = None,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Unpublish a station."""
        return self.stations.unpublish(
            campaign_id=campaign_id,
            station_id=station_id,
            cascade=cascade,
            force=force,
            organization=organization,
            tapis_token=tapis_token,
        )

    def publish_sensor(
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
        return self.sensors.publish(
            campaign_id=campaign_id,
            station_id=station_id,
            sensor_id=sensor_id,
            cascade=cascade,
            force=force,
            organization=organization,
            tapis_token=tapis_token,
        )

    def unpublish_sensor(
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
        return self.sensors.unpublish(
            campaign_id=campaign_id,
            station_id=station_id,
            sensor_id=sensor_id,
            cascade=cascade,
            force=force,
            organization=organization,
            tapis_token=tapis_token,
        )

    def export_sensors_csv(
        self,
        campaign_id: int,
        station_id: int,
        output: Optional[BinaryIO] = None,
    ) -> Optional[str]:
        """Export sensors for a station as CSV."""
        return self.stations.export_sensors_csv(
            campaign_id=campaign_id, station_id=station_id, output=output
        )

    def export_measurements_csv(
        self,
        campaign_id: int,
        station_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        output: Optional[BinaryIO] = None,
    ) -> Optional[str]:
        """Export measurements for a station as CSV."""
        return self.stations.export_measurements_csv(
            campaign_id=campaign_id,
            station_id=station_id,
            start_date=start_date,
            end_date=end_date,
            output=output,
        )

    def list_sensor_variables(self) -> List[str]:
        """List available sensor variables."""
        return self.sensor_variables.list()

    def list_ckan_organizations(self, tapis_token: Optional[str] = None) -> List[Dict[str, Any]]:
        """List CKAN organizations available to the current user."""
        return self.ckan_api.list_organizations(tapis_token=tapis_token)

    def create_pod_bundle(
        self,
        base: str,
        pg_user: str,
        pg_password: str,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a pod bundle."""
        return self.pods.create_bundle(
            base=base,
            pg_user=pg_user,
            pg_password=pg_password,
            tapis_token=tapis_token,
        )

    def list_user_roles(self) -> List[Dict[str, Any]]:
        """List user roles (admin only)."""
        return self.user_roles.list_roles()

    def upsert_user_role(self, username: str, role: str) -> Dict[str, Any]:
        """Create or update a user role (admin only)."""
        return self.user_roles.upsert_role(username=username, role=role)

    def delete_user_role(self, username: str) -> bool:
        """Delete a user role (admin only)."""
        return self.user_roles.delete_role(username=username)

    def get_measurements_geojson(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_measurement_value: Optional[float] = None,
        max_measurement_value: Optional[float] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        downsample_threshold: Optional[int] = None,
        tapis_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get sensor measurements as GeoJSON."""
        return self.measurements.get_geojson(
            campaign_id=campaign_id,
            station_id=station_id,
            sensor_id=sensor_id,
            start_date=start_date,
            end_date=end_date,
            min_measurement_value=min_measurement_value,
            max_measurement_value=max_measurement_value,
            limit=limit,
            page=page,
            downsample_threshold=downsample_threshold,
            tapis_token=tapis_token,
        )

    def upload_sensor_measurement_files(
        self,
        campaign_id: int,
        station_id: int,
        sensors_file: Union[str, Path, bytes, Tuple[str, bytes]],
        measurements_file: Union[str, Path, bytes, Tuple[str, bytes]],
        chunk_size: int = 1000,
    ) -> Dict[str, object]:
        """Upload sensor and measurement CSV files to process and store data in the database.

        This method uses the direct API endpoint for processing sensor and measurement files.
        Measurements are uploaded in chunks to avoid HTTP timeouts with large files.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: File path, bytes, or tuple (filename, bytes) containing sensor metadata
            measurements_file: File path, bytes, or tuple (filename, bytes) containing measurement data
            chunk_size: Number of measurement lines per chunk (default: 1000)

        Returns:
            Response from the upload API containing processing results

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
        return self.sensors.upload_csv_files(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_file,
            measurements_file=measurements_file,
            chunk_size=chunk_size,
        )

    def create_measurement(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        measurement_in: MeasurementIn,
    ) -> MeasurementCreateResponse:
        """Create a new measurement.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            measurement_in: MeasurementIn model instance

        Returns:
            Created Measurement instance
        """
        return self.measurements.create(
            campaign_id, station_id, sensor_id, measurement_in
        )

    def list_measurements(
        self, campaign_id: int, station_id: int, sensor_id: int, **kwargs: Any
    ) -> ListMeasurementsResponsePagination:
        """List measurements for a sensor.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            **kwargs: Additional filtering parameters (start_date, end_date, min_measurement_value, etc.)

        Returns:
            List of Measurement instances
        """
        return self.measurements.list(campaign_id, station_id, sensor_id, **kwargs)

    def get_measurements_with_confidence_intervals(
        self, campaign_id: int, station_id: int, sensor_id: int, **kwargs: Any
    ) -> List[AggregatedMeasurement]:
        """Get sensor measurements with confidence intervals for visualization.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            **kwargs: Additional filtering parameters (interval, interval_value, start_date, etc.)

        Returns:
            List of AggregatedMeasurement instances with confidence intervals
        """
        return self.measurements.get_with_confidence_intervals(
            campaign_id, station_id, sensor_id, **kwargs
        )

    def update_measurement(
        self,
        campaign_id: int,
        station_id: int,
        sensor_id: int,
        measurement_id: int,
        measurement_update: MeasurementUpdate,
    ) -> MeasurementCreateResponse:
        """Update a measurement.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID
            measurement_id: Measurement ID
            measurement_update: MeasurementUpdate model instance

        Returns:
            Updated Measurement instance
        """
        return self.measurements.update(
            campaign_id, station_id, sensor_id, measurement_id, measurement_update
        )

    def delete_measurements(
        self, campaign_id: int, station_id: int, sensor_id: int
    ) -> bool:
        """Delete all measurements for a sensor.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensor_id: Sensor ID

        Returns:
            True if deletion successful
        """
        return self.measurements.delete(campaign_id, station_id, sensor_id)

    def upload_chunked_csv_data(
        self,
        campaign_id: int,
        station_id: int,
        sensors_file: Union[str, Path],
        measurements_file: Union[str, Path],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Upload large sensor data from CSV files in chunks.

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file
            **kwargs: Additional upload parameters

        Returns:
            Upload result dictionary
        """
        return self.data.upload_chunked_csv_data(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_file,
            measurements_file=measurements_file,
            **kwargs,
        )

    def validate_files(
        self, sensors_file: Union[str, Path], measurements_file: Union[str, Path]
    ) -> Dict[str, Any]:
        """Validate CSV files without uploading.

        Args:
            sensors_file: Path to sensors CSV file
            measurements_file: Path to measurements CSV file

        Returns:
            Validation result dictionary
        """
        return self.data.validate_files(sensors_file, measurements_file)

    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get information about a CSV file.

        Args:
            file_path: Path to CSV file

        Returns:
            File information dictionary
        """
        return self.data.get_file_info(file_path)

    def publish_to_ckan(
        self,
        campaign_id: int,
        station_id: int,
        organization: Optional[str] = None,
        cascade: bool = False,
        force: bool = False,
        tapis_token: Optional[str] = None,
        dataset_metadata: Optional[Dict[str, Any]] = None,
        resource_metadata: Optional[Dict[str, Any]] = None,
        custom_tags: Optional[List[str]] = None,
        auto_publish: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Publish station data to CKAN via the Upstream API (pods).

        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            organization: Optional CKAN organization to publish into
            cascade: Whether to cascade publish to child resources
            force: Whether to force publish even if parent is unpublished
            tapis_token: Tapis access token required for CKAN operations
            dataset_metadata: Not supported via API publish (ignored)
            resource_metadata: Not supported via API publish (ignored)
            custom_tags: Not supported via API publish (ignored)
            auto_publish: Not supported via API publish (ignored)
            **kwargs: Additional parameters (ignored)

        Returns:
            Publish response from the Upstream API

        Examples:
            Basic usage:
            >>> client.publish_to_ckan(
            ...     campaign_id=123,
            ...     station_id=456,
            ...     organization="upstream",
            ...     tapis_token="...jwt..."
            ... )
        """
        ignored_fields = {
            "dataset_metadata": dataset_metadata,
            "resource_metadata": resource_metadata,
            "custom_tags": custom_tags,
            "auto_publish": auto_publish,
            "kwargs": kwargs,
        }
        if any(value for key, value in ignored_fields.items() if key != "auto_publish") or (
            "auto_publish" in ignored_fields and auto_publish is False
        ):
            logger.warning(
                "publish_to_ckan now uses the Upstream API publish endpoint. "
                "Custom CKAN metadata parameters are ignored."
            )

        return self.publish_station(
            campaign_id=campaign_id,
            station_id=station_id,
            cascade=cascade,
            force=force,
            organization=organization,
            tapis_token=tapis_token,
        )

    def logout(self) -> None:
        """Logout and invalidate authentication."""
        self.auth_manager.logout()
        logger.info("Client logged out successfully")

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration.

        Returns:
            Configuration dictionary
        """
        return self.auth_manager.config.to_dict()

    def is_authenticated(self) -> bool:
        """Check if currently authenticated.

        Returns:
            True if authenticated with valid token
        """
        return self.auth_manager.is_authenticated()

    def refresh_token(self) -> bool:
        """Refresh authentication token.

        Returns:
            True if refresh successful
        """
        return self.auth_manager.refresh_token()
