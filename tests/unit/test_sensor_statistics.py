"""
Unit tests for sensor statistics update functionality.
"""

from unittest.mock import Mock, patch

import pytest
from upstream_api_client.models import (
    ForceUpdateSensorStatisticsResponse,
    UpdateSensorStatisticsResponse,
)
from upstream_api_client.rest import ApiException

from upstream.auth import AuthManager
from upstream.exceptions import APIError, ValidationError
from upstream.sensors import SensorManager


class TestSensorStatisticsUpdate:
    """Test sensor statistics update functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.auth_manager = Mock(spec=AuthManager)
        self.auth_manager.config = Mock()
        self.sensor_manager = SensorManager(self.auth_manager)

    def test_force_update_statistics_success(self):
        """Test successful force update of all sensor statistics."""
        # Mock the API client and response
        mock_api_client = Mock()
        mock_sensors_api = Mock()
        mock_response = Mock(spec=ForceUpdateSensorStatisticsResponse)
        mock_response.success = True
        mock_response.message = "Statistics updated successfully"

        mock_sensors_api.force_update_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_statistics_post.return_value = mock_response

        with patch.object(
            self.auth_manager, "get_api_client"
        ) as mock_get_client, patch(
            "upstream.sensors.SensorsApi", return_value=mock_sensors_api
        ):
            mock_get_client.return_value.__enter__.return_value = mock_api_client

            result = self.sensor_manager.force_update_statistics(
                campaign_id=123, station_id=456
            )

            assert result == mock_response
            mock_sensors_api.force_update_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_statistics_post.assert_called_once_with(
                campaign_id=123, station_id=456
            )

    def test_force_update_statistics_validation_error(self):
        """Test validation errors for force update statistics."""
        # Test missing campaign_id
        with pytest.raises(ValidationError, match="Campaign ID is required"):
            self.sensor_manager.force_update_statistics(
                campaign_id=None, station_id=456
            )

        # Test missing station_id
        with pytest.raises(ValidationError, match="Station ID is required"):
            self.sensor_manager.force_update_statistics(
                campaign_id=123, station_id=None
            )

        # Test zero campaign_id
        with pytest.raises(ValidationError, match="Campaign ID is required"):
            self.sensor_manager.force_update_statistics(
                campaign_id=0, station_id=456
            )

        # Test zero station_id
        with pytest.raises(ValidationError, match="Station ID is required"):
            self.sensor_manager.force_update_statistics(
                campaign_id=123, station_id=0
            )

    def test_force_update_statistics_api_error_404(self):
        """Test API error handling for 404 (station not found)."""
        mock_api_client = Mock()
        mock_sensors_api = Mock()
        mock_api_exception = ApiException(status=404, reason="Not Found")
        mock_sensors_api.force_update_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_statistics_post.side_effect = mock_api_exception

        with patch.object(
            self.auth_manager, "get_api_client"
        ) as mock_get_client, patch(
            "upstream.sensors.SensorsApi", return_value=mock_sensors_api
        ):
            mock_get_client.return_value.__enter__.return_value = mock_api_client

            with pytest.raises(APIError, match="Station not found: 456"):
                self.sensor_manager.force_update_statistics(
                    campaign_id=123, station_id=456
                )

    def test_force_update_statistics_api_error_generic(self):
        """Test API error handling for generic errors."""
        mock_api_client = Mock()
        mock_sensors_api = Mock()
        mock_api_exception = ApiException(status=500, reason="Internal Server Error")
        mock_sensors_api.force_update_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_statistics_post.side_effect = mock_api_exception

        with patch.object(
            self.auth_manager, "get_api_client"
        ) as mock_get_client, patch(
            "upstream.sensors.SensorsApi", return_value=mock_sensors_api
        ):
            mock_get_client.return_value.__enter__.return_value = mock_api_client

            with pytest.raises(
                APIError, match="Failed to force update sensor statistics"
            ):
                self.sensor_manager.force_update_statistics(
                    campaign_id=123, station_id=456
                )

    def test_force_update_single_sensor_statistics_success(self):
        """Test successful force update of single sensor statistics."""
        # Mock the API client and response
        mock_api_client = Mock()
        mock_sensors_api = Mock()
        mock_response = Mock(spec=UpdateSensorStatisticsResponse)
        mock_response.success = True
        mock_response.message = "Sensor statistics updated successfully"

        mock_sensors_api.force_update_single_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_statistics_post.return_value = mock_response

        with patch.object(
            self.auth_manager, "get_api_client"
        ) as mock_get_client, patch(
            "upstream.sensors.SensorsApi", return_value=mock_sensors_api
        ):
            mock_get_client.return_value.__enter__.return_value = mock_api_client

            result = self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=123, station_id=456, sensor_id=789
            )

            assert result == mock_response
            mock_sensors_api.force_update_single_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_statistics_post.assert_called_once_with(
                campaign_id=123, station_id=456, sensor_id=789
            )

    def test_force_update_single_sensor_statistics_validation_error(self):
        """Test validation errors for force update single sensor statistics."""
        # Test missing campaign_id
        with pytest.raises(ValidationError, match="Campaign ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=None, station_id=456, sensor_id=789
            )

        # Test missing station_id
        with pytest.raises(ValidationError, match="Station ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=123, station_id=None, sensor_id=789
            )

        # Test missing sensor_id
        with pytest.raises(ValidationError, match="Sensor ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=123, station_id=456, sensor_id=None
            )

        # Test zero values
        with pytest.raises(ValidationError, match="Campaign ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=0, station_id=456, sensor_id=789
            )

        with pytest.raises(ValidationError, match="Station ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=123, station_id=0, sensor_id=789
            )

        with pytest.raises(ValidationError, match="Sensor ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=123, station_id=456, sensor_id=0
            )

    def test_force_update_single_sensor_statistics_api_error_404(self):
        """Test API error handling for 404 (sensor not found)."""
        mock_api_client = Mock()
        mock_sensors_api = Mock()
        mock_api_exception = ApiException(status=404, reason="Not Found")
        mock_sensors_api.force_update_single_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_statistics_post.side_effect = mock_api_exception

        with patch.object(
            self.auth_manager, "get_api_client"
        ) as mock_get_client, patch(
            "upstream.sensors.SensorsApi", return_value=mock_sensors_api
        ):
            mock_get_client.return_value.__enter__.return_value = mock_api_client

            with pytest.raises(APIError, match="Sensor not found: 789"):
                self.sensor_manager.force_update_single_sensor_statistics(
                    campaign_id=123, station_id=456, sensor_id=789
                )

    def test_force_update_single_sensor_statistics_api_error_generic(self):
        """Test API error handling for generic errors."""
        mock_api_client = Mock()
        mock_sensors_api = Mock()
        mock_api_exception = ApiException(status=500, reason="Internal Server Error")
        mock_sensors_api.force_update_single_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_statistics_post.side_effect = mock_api_exception

        with patch.object(
            self.auth_manager, "get_api_client"
        ) as mock_get_client, patch(
            "upstream.sensors.SensorsApi", return_value=mock_sensors_api
        ):
            mock_get_client.return_value.__enter__.return_value = mock_api_client

            with pytest.raises(
                APIError, match="Failed to force update sensor statistics"
            ):
                self.sensor_manager.force_update_single_sensor_statistics(
                    campaign_id=123, station_id=456, sensor_id=789
                )

    def test_force_update_statistics_generic_exception(self):
        """Test generic exception handling for force update statistics."""
        mock_api_client = Mock()
        mock_sensors_api = Mock()
        mock_sensors_api.force_update_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_statistics_post.side_effect = Exception(
            "Unexpected error"
        )

        with patch.object(
            self.auth_manager, "get_api_client"
        ) as mock_get_client, patch(
            "upstream.sensors.SensorsApi", return_value=mock_sensors_api
        ):
            mock_get_client.return_value.__enter__.return_value = mock_api_client

            with pytest.raises(
                APIError, match="Failed to force update sensor statistics"
            ):
                self.sensor_manager.force_update_statistics(
                    campaign_id=123, station_id=456
                )

    def test_force_update_single_sensor_statistics_generic_exception(self):
        """Test generic exception handling for force update single sensor statistics."""
        mock_api_client = Mock()
        mock_sensors_api = Mock()
        mock_sensors_api.force_update_single_sensor_statistics_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_statistics_post.side_effect = Exception(
            "Unexpected error"
        )

        with patch.object(
            self.auth_manager, "get_api_client"
        ) as mock_get_client, patch(
            "upstream.sensors.SensorsApi", return_value=mock_sensors_api
        ):
            mock_get_client.return_value.__enter__.return_value = mock_api_client

            with pytest.raises(
                APIError, match="Failed to force update sensor statistics"
            ):
                self.sensor_manager.force_update_single_sensor_statistics(
                    campaign_id=123, station_id=456, sensor_id=789
                )