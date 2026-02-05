"""
Unit tests for sensor statistics update functionality.
"""

from unittest.mock import Mock, patch

import pytest

from upstream.auth import AuthManager
from upstream.exceptions import APIError, ValidationError
from upstream.sensors import SensorManager


class TestSensorStatisticsUpdate:
    """Test sensor statistics update functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.auth_manager = Mock(spec=AuthManager)
        self.auth_manager.config = Mock()
        self.auth_manager.config.timeout = 30
        self.auth_manager.get_headers.return_value = {"Authorization": "Bearer token"}
        self.auth_manager.build_url.side_effect = lambda path: f"http://test{path}"
        self.sensor_manager = SensorManager(self.auth_manager)

    def test_force_update_statistics_success(self):
        """Test successful force update of all sensor statistics."""
        mock_response = {"success": True, "message": "Statistics updated successfully"}

        with patch("upstream.sensors.request_json", return_value=mock_response) as mock_request:
            result = self.sensor_manager.force_update_statistics(
                campaign_id=123, station_id=456
            )

            assert result == mock_response
            mock_request.assert_called_once()

    def test_force_update_statistics_validation_error(self):
        """Test validation errors for force update statistics."""
        with pytest.raises(ValidationError, match="Campaign ID is required"):
            self.sensor_manager.force_update_statistics(
                campaign_id=None, station_id=456
            )

        with pytest.raises(ValidationError, match="Station ID is required"):
            self.sensor_manager.force_update_statistics(
                campaign_id=123, station_id=None
            )

        with pytest.raises(ValidationError, match="Campaign ID is required"):
            self.sensor_manager.force_update_statistics(
                campaign_id=0, station_id=456
            )

        with pytest.raises(ValidationError, match="Station ID is required"):
            self.sensor_manager.force_update_statistics(
                campaign_id=123, station_id=0
            )

    def test_force_update_statistics_api_error_404(self):
        """Test API error handling for 404 (station not found)."""
        with patch(
            "upstream.sensors.request_json",
            side_effect=APIError("not found", status_code=404),
        ):
            with pytest.raises(APIError, match="Station not found: 456"):
                self.sensor_manager.force_update_statistics(
                    campaign_id=123, station_id=456
                )

    def test_force_update_statistics_api_error_generic(self):
        """Test API error handling for generic errors."""
        with patch(
            "upstream.sensors.request_json",
            side_effect=APIError("server error", status_code=500),
        ):
            with pytest.raises(
                APIError, match="Failed to force update sensor statistics"
            ):
                self.sensor_manager.force_update_statistics(
                    campaign_id=123, station_id=456
                )

    def test_force_update_single_sensor_statistics_success(self):
        """Test successful force update of single sensor statistics."""
        mock_response = {
            "success": True,
            "message": "Sensor statistics updated successfully",
        }

        with patch("upstream.sensors.request_json", return_value=mock_response) as mock_request:
            result = self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=123, station_id=456, sensor_id=789
            )

            assert result == mock_response
            mock_request.assert_called_once()

    def test_force_update_single_sensor_statistics_validation_error(self):
        """Test validation errors for force update single sensor statistics."""
        with pytest.raises(ValidationError, match="Campaign ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=None, station_id=456, sensor_id=789
            )

        with pytest.raises(ValidationError, match="Station ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=123, station_id=None, sensor_id=789
            )

        with pytest.raises(ValidationError, match="Sensor ID is required"):
            self.sensor_manager.force_update_single_sensor_statistics(
                campaign_id=123, station_id=456, sensor_id=None
            )

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
        with patch(
            "upstream.sensors.request_json",
            side_effect=APIError("not found", status_code=404),
        ):
            with pytest.raises(APIError, match="Sensor not found: 789"):
                self.sensor_manager.force_update_single_sensor_statistics(
                    campaign_id=123, station_id=456, sensor_id=789
                )

    def test_force_update_single_sensor_statistics_api_error_generic(self):
        """Test API error handling for generic errors."""
        with patch(
            "upstream.sensors.request_json",
            side_effect=APIError("server error", status_code=500),
        ):
            with pytest.raises(
                APIError, match="Failed to force update sensor statistics"
            ):
                self.sensor_manager.force_update_single_sensor_statistics(
                    campaign_id=123, station_id=456, sensor_id=789
                )

    def test_force_update_statistics_generic_exception(self):
        """Test generic exception handling for force update statistics."""
        with patch(
            "upstream.sensors.request_json",
            side_effect=Exception("Unexpected error"),
        ):
            with pytest.raises(
                APIError, match="Failed to force update sensor statistics: Unexpected error"
            ):
                self.sensor_manager.force_update_statistics(
                    campaign_id=123, station_id=456
                )

    def test_force_update_single_sensor_statistics_generic_exception(self):
        """Test generic exception handling for force update single sensor statistics."""
        with patch(
            "upstream.sensors.request_json",
            side_effect=Exception("Unexpected error"),
        ):
            with pytest.raises(
                APIError, match="Failed to force update sensor statistics: Unexpected error"
            ):
                self.sensor_manager.force_update_single_sensor_statistics(
                    campaign_id=123, station_id=456, sensor_id=789
                )
