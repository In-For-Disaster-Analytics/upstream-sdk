"""
Unit tests for UpstreamClient CKAN custom metadata functionality.
"""

from unittest.mock import Mock, patch
import pytest
from upstream.client import UpstreamClient

pytestmark = pytest.mark.unit


class TestUpstreamClientCKANMetadata:
    """Test UpstreamClient CKAN custom metadata functionality."""

    def test_publish_to_ckan_no_ckan_integration(self):
        """Test publish_to_ckan works without CKAN integration configured."""
        # Create client without CKAN integration by setting ckan to None
        client = UpstreamClient(
            username="test_user",
            password="test_pass",
            base_url="https://api.example.com"
        )
        # Manually set ckan to None to simulate no CKAN integration
        client.ckan = None

        with patch.object(client, "publish_station", return_value={"success": True}) as mock_publish:
            result = client.publish_to_ckan("campaign123", "station456")

        mock_publish.assert_called_once_with(
            campaign_id="campaign123",
            station_id="station456",
            cascade=False,
            force=False,
            organization=None,
            tapis_token=None,
        )
        assert result["success"] is True

    @patch("upstream.client.AuthManager")
    def test_publish_to_ckan_with_custom_metadata(self, mock_auth, caplog):
        """Test publish_to_ckan ignores custom metadata and routes to publish_station."""
        mock_auth_instance = Mock()
        mock_auth.return_value = mock_auth_instance

        mock_config = Mock()
        mock_config.ckan_url = "http://test-ckan.example.com"
        mock_config.to_dict.return_value = {"ckan_url": "http://test-ckan.example.com"}
        mock_auth_instance.config = mock_config

        client = UpstreamClient(
            username="test_user",
            password="test_pass",
            base_url="https://api.example.com",
            ckan_url="http://test-ckan.example.com",
        )

        # Test custom metadata parameters
        custom_dataset_metadata = {"project": "Test Project", "funding": "EPA"}
        custom_resource_metadata = {"quality": "Level 2", "version": "v1.0"}  
        custom_tags = ["research", "environmental"]

        with patch.object(client, "publish_station", return_value={"success": True}) as mock_publish:
            result = client.publish_to_ckan(
                campaign_id="test-campaign-123",
                station_id="test-station-456",
                dataset_metadata=custom_dataset_metadata,
                resource_metadata=custom_resource_metadata,
                custom_tags=custom_tags,
                auto_publish=False,
                license_id="cc-by-4.0",
            )

        mock_publish.assert_called_once_with(
            campaign_id="test-campaign-123",
            station_id="test-station-456",
            cascade=False,
            force=False,
            organization=None,
            tapis_token=None,
        )
        assert result["success"] is True
        assert "Custom CKAN metadata parameters are ignored" in caplog.text

    @patch("upstream.client.AuthManager")
    def test_publish_to_ckan_default_parameters(self, mock_auth):
        """Test publish_to_ckan works with default parameters (backward compatibility)."""
        mock_auth_instance = Mock()
        mock_auth.return_value = mock_auth_instance

        mock_config = Mock()
        mock_config.ckan_url = "http://test-ckan.example.com"
        mock_config.to_dict.return_value = {"ckan_url": "http://test-ckan.example.com"}
        mock_auth_instance.config = mock_config

        client = UpstreamClient(
            username="test_user",
            password="test_pass",
            base_url="https://api.example.com",
            ckan_url="http://test-ckan.example.com",
        )

        with patch.object(client, "publish_station", return_value={"success": True}) as mock_publish:
            result = client.publish_to_ckan(
                campaign_id="test-campaign-123",
                station_id="test-station-456",
            )

        mock_publish.assert_called_once_with(
            campaign_id="test-campaign-123",
            station_id="test-station-456",
            cascade=False,
            force=False,
            organization=None,
            tapis_token=None,
        )
        assert result["success"] is True
