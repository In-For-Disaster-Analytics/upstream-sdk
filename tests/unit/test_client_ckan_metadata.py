"""
Unit tests for UpstreamClient CKAN custom metadata functionality.
"""

from unittest.mock import Mock, patch
import pytest
from upstream.client import UpstreamClient
from upstream.exceptions import ConfigurationError

pytestmark = pytest.mark.unit


class TestUpstreamClientCKANMetadata:
    """Test UpstreamClient CKAN custom metadata functionality."""

    def test_publish_to_ckan_no_ckan_integration(self):
        """Test publish_to_ckan raises error when CKAN integration not configured."""
        # Create client without CKAN integration by setting ckan to None
        client = UpstreamClient(
            username="test_user",
            password="test_pass",
            base_url="https://api.example.com"
        )
        # Manually set ckan to None to simulate no CKAN integration
        client.ckan = None
        
        with pytest.raises(ConfigurationError, match="CKAN integration not configured"):
            client.publish_to_ckan("campaign123", "station456")

    @patch("upstream.client.CKANIntegration")
    @patch("upstream.client.CampaignManager")
    @patch("upstream.client.StationManager") 
    @patch("upstream.client.AuthManager")
    def test_publish_to_ckan_with_custom_metadata(
        self, mock_auth, mock_station_mgr, mock_campaign_mgr, mock_ckan_integration
    ):
        """Test publish_to_ckan passes custom metadata to CKAN integration."""
        # Setup mocks
        mock_auth_instance = Mock()
        mock_auth.return_value = mock_auth_instance
        
        mock_station_mgr_instance = Mock()
        mock_station_mgr.return_value = mock_station_mgr_instance
        
        mock_campaign_mgr_instance = Mock()
        mock_campaign_mgr.return_value = mock_campaign_mgr_instance
        
        mock_ckan_instance = Mock()
        mock_ckan_integration.return_value = mock_ckan_instance
        
        # Mock the CKAN configuration
        mock_config = Mock()
        mock_config.ckan_url = "http://test-ckan.example.com"
        mock_config.to_dict.return_value = {"ckan_url": "http://test-ckan.example.com"}
        mock_auth_instance.config = mock_config
        
        # Create client with CKAN URL to trigger CKAN integration
        client = UpstreamClient(
            username="test_user",
            password="test_pass", 
            base_url="https://api.example.com",
            ckan_url="http://test-ckan.example.com"
        )
        
        # Mock the required data methods
        mock_station_data = Mock()
        mock_station_mgr_instance.get.return_value = mock_station_data
        mock_station_mgr_instance.export_station_measurements.return_value = Mock()
        mock_station_mgr_instance.export_station_sensors.return_value = Mock()
        
        mock_campaign_data = Mock()
        mock_campaign_mgr_instance.get.return_value = mock_campaign_data
        
        mock_ckan_instance.publish_campaign.return_value = {"success": True}
        
        # Test custom metadata parameters
        custom_dataset_metadata = {"project": "Test Project", "funding": "EPA"}
        custom_resource_metadata = {"quality": "Level 2", "version": "v1.0"}  
        custom_tags = ["research", "environmental"]
        
        result = client.publish_to_ckan(
            campaign_id="test-campaign-123",
            station_id="test-station-456",
            dataset_metadata=custom_dataset_metadata,
            resource_metadata=custom_resource_metadata,
            custom_tags=custom_tags,
            auto_publish=False,
            license_id="cc-by-4.0"
        )
        
        # Verify the CKAN integration publish_campaign was called with correct parameters
        mock_ckan_instance.publish_campaign.assert_called_once_with(
            campaign_id="test-campaign-123",
            campaign_data=mock_campaign_data,
            station_measurements=mock_station_mgr_instance.export_station_measurements.return_value,
            station_sensors=mock_station_mgr_instance.export_station_sensors.return_value,
            station_data=mock_station_data,
            dataset_metadata=custom_dataset_metadata,
            resource_metadata=custom_resource_metadata,
            custom_tags=custom_tags,
            auto_publish=False,
            license_id="cc-by-4.0"
        )
        
        assert result["success"] is True

    @patch("upstream.client.CKANIntegration")
    @patch("upstream.client.CampaignManager")
    @patch("upstream.client.StationManager")
    @patch("upstream.client.AuthManager")
    def test_publish_to_ckan_default_parameters(
        self, mock_auth, mock_station_mgr, mock_campaign_mgr, mock_ckan_integration
    ):
        """Test publish_to_ckan works with default parameters (backward compatibility)."""
        # Setup mocks
        mock_auth_instance = Mock()
        mock_auth.return_value = mock_auth_instance
        
        mock_station_mgr_instance = Mock()
        mock_station_mgr.return_value = mock_station_mgr_instance
        
        mock_campaign_mgr_instance = Mock()
        mock_campaign_mgr.return_value = mock_campaign_mgr_instance
        
        mock_ckan_instance = Mock()
        mock_ckan_integration.return_value = mock_ckan_instance
        
        # Mock the CKAN configuration
        mock_config = Mock()
        mock_config.ckan_url = "http://test-ckan.example.com"
        mock_config.to_dict.return_value = {"ckan_url": "http://test-ckan.example.com"}
        mock_auth_instance.config = mock_config
        
        # Create client
        client = UpstreamClient(
            username="test_user",
            password="test_pass",
            base_url="https://api.example.com",
            ckan_url="http://test-ckan.example.com"
        )
        
        # Mock the required data methods
        mock_station_data = Mock()
        mock_station_mgr_instance.get.return_value = mock_station_data
        mock_station_mgr_instance.export_station_measurements.return_value = Mock()
        mock_station_mgr_instance.export_station_sensors.return_value = Mock()
        
        mock_campaign_data = Mock()
        mock_campaign_mgr_instance.get.return_value = mock_campaign_data
        
        mock_ckan_instance.publish_campaign.return_value = {"success": True}
        
        # Test with default parameters (backward compatibility)
        result = client.publish_to_ckan(
            campaign_id="test-campaign-123",
            station_id="test-station-456"
        )
        
        # Verify the CKAN integration publish_campaign was called with default values
        mock_ckan_instance.publish_campaign.assert_called_once_with(
            campaign_id="test-campaign-123",
            campaign_data=mock_campaign_data,
            station_measurements=mock_station_mgr_instance.export_station_measurements.return_value,
            station_sensors=mock_station_mgr_instance.export_station_sensors.return_value,
            station_data=mock_station_data,
            dataset_metadata=None,
            resource_metadata=None,
            custom_tags=None,
            auto_publish=True
        )
        
        assert result["success"] is True