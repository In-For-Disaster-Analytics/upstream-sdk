"""
Unit tests for UpstreamClient.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from upstream.client import UpstreamClient
from upstream.exceptions import ConfigurationError


class TestUpstreamClient:
    """Test cases for UpstreamClient class."""
    
    def test_init_with_credentials(self):
        """Test client initialization with credentials."""
        with patch('upstream.client.AuthManager') as mock_auth:
            client = UpstreamClient(
                username="test_user",
                password="test_pass",
                base_url="https://test.example.com"
            )
            
            assert client is not None
            mock_auth.assert_called_once()
    
    def test_init_with_config_file(self, temp_config_file):
        """Test client initialization with config file."""
        with patch('upstream.client.AuthManager') as mock_auth:
            client = UpstreamClient(config_file=temp_config_file)
            
            assert client is not None
            mock_auth.assert_called_once()
    
    def test_from_config_classmethod(self, temp_config_file):
        """Test from_config class method."""
        with patch('upstream.client.AuthManager') as mock_auth:
            client = UpstreamClient.from_config(temp_config_file)
            
            assert client is not None
            mock_auth.assert_called_once()
    
    def test_from_environment_classmethod(self):
        """Test from_environment class method."""
        with patch.dict('os.environ', {
            'UPSTREAM_USERNAME': 'env_user',
            'UPSTREAM_PASSWORD': 'env_pass',
            'UPSTREAM_BASE_URL': 'https://env.example.com'
        }):
            with patch('upstream.client.AuthManager') as mock_auth:
                client = UpstreamClient.from_environment()
                
                assert client is not None
                mock_auth.assert_called_once()
    
    def test_authenticate(self, mock_client):
        """Test authentication method."""
        mock_client.auth_manager.authenticate.return_value = True
        
        result = mock_client.authenticate()
        
        assert result is True
        mock_client.auth_manager.authenticate.assert_called_once()
    
    def test_create_campaign(self, mock_client, sample_campaign_data):
        """Test campaign creation."""
        mock_campaign = Mock()
        mock_client.campaigns.create.return_value = mock_campaign
        
        result = mock_client.create_campaign(
            name="Test Campaign",
            description="Test Description"
        )
        
        assert result == mock_campaign
        mock_client.campaigns.create.assert_called_once_with(
            name="Test Campaign",
            description="Test Description"
        )
    
    def test_get_campaign(self, mock_client, sample_campaign_data):
        """Test campaign retrieval."""
        mock_campaign = Mock()
        mock_client.campaigns.get.return_value = mock_campaign
        
        result = mock_client.get_campaign("test-campaign-123")
        
        assert result == mock_campaign
        mock_client.campaigns.get.assert_called_once_with("test-campaign-123")
    
    def test_list_campaigns(self, mock_client):
        """Test campaign listing."""
        mock_campaigns = [Mock(), Mock()]
        mock_client.campaigns.list.return_value = mock_campaigns
        
        result = mock_client.list_campaigns()
        
        assert result == mock_campaigns
        mock_client.campaigns.list.assert_called_once()
    
    def test_create_station(self, mock_client, sample_station_data):
        """Test station creation."""
        mock_station = Mock()
        mock_client.stations.create.return_value = mock_station
        
        result = mock_client.create_station(
            campaign_id="test-campaign-123",
            name="Test Station",
            latitude=30.2672,
            longitude=-97.7431,
            description="Test Description"
        )
        
        assert result == mock_station
        mock_client.stations.create.assert_called_once_with(
            campaign_id="test-campaign-123",
            name="Test Station",
            latitude=30.2672,
            longitude=-97.7431,
            description="Test Description"
        )
    
    def test_get_station(self, mock_client):
        """Test station retrieval."""
        mock_station = Mock()
        mock_client.stations.get.return_value = mock_station
        
        result = mock_client.get_station("test-station-456")
        
        assert result == mock_station
        mock_client.stations.get.assert_called_once_with("test-station-456")
    
    def test_list_stations(self, mock_client):
        """Test station listing."""
        mock_stations = [Mock(), Mock()]
        mock_client.stations.list.return_value = mock_stations
        
        result = mock_client.list_stations(campaign_id="test-campaign-123")
        
        assert result == mock_stations
        mock_client.stations.list.assert_called_once_with(campaign_id="test-campaign-123")
    
    def test_upload_csv_data(self, mock_client, temp_csv_file, temp_measurements_csv):
        """Test CSV data upload."""
        mock_result = {"success": True, "upload_id": "test-upload-123"}
        mock_client.data.upload_csv_data.return_value = mock_result
        
        result = mock_client.upload_csv_data(
            campaign_id="test-campaign-123",
            station_id="test-station-456",
            sensors_file=temp_csv_file,
            measurements_file=temp_measurements_csv
        )
        
        assert result == mock_result
        mock_client.data.upload_csv_data.assert_called_once()
    
    def test_upload_measurements(self, mock_client, sample_measurements_data):
        """Test measurements upload."""
        mock_result = {"success": True, "upload_id": "test-upload-123"}
        mock_client.data.upload_measurements.return_value = mock_result
        
        result = mock_client.upload_measurements(
            campaign_id="test-campaign-123",
            station_id="test-station-456",
            data=sample_measurements_data
        )
        
        assert result == mock_result
        mock_client.data.upload_measurements.assert_called_once()
    
    def test_publish_to_ckan_with_integration(self, mock_client):
        """Test CKAN publication with integration configured."""
        mock_client.ckan = Mock()
        mock_result = {"success": True, "dataset_id": "test-dataset-123"}
        mock_client.ckan.publish_campaign.return_value = mock_result
        
        result = mock_client.publish_to_ckan(campaign_id="test-campaign-123")
        
        assert result == mock_result
        mock_client.ckan.publish_campaign.assert_called_once()
    
    def test_publish_to_ckan_without_integration(self, mock_client):
        """Test CKAN publication without integration configured."""
        mock_client.ckan = None
        
        with pytest.raises(ConfigurationError, match="CKAN integration not configured"):
            mock_client.publish_to_ckan(campaign_id="test-campaign-123")
    
    def test_get_upload_status(self, mock_client):
        """Test upload status retrieval."""
        mock_status = {"status": "completed", "progress": 100}
        mock_client.data.get_upload_status.return_value = mock_status
        
        result = mock_client.get_upload_status("test-upload-123")
        
        assert result == mock_status
        mock_client.data.get_upload_status.assert_called_once_with("test-upload-123")
    
    def test_logout(self, mock_client):
        """Test logout method."""
        mock_client.logout()
        
        mock_client.auth_manager.logout.assert_called_once()
    
    @pytest.mark.parametrize("missing_param", ["username", "password", "base_url"])
    def test_init_missing_required_params(self, missing_param):
        """Test client initialization with missing required parameters."""
        params = {
            "username": "test_user",
            "password": "test_pass",
            "base_url": "https://test.example.com"
        }
        params.pop(missing_param)
        
        with patch('upstream.client.AuthManager') as mock_auth:
            mock_auth.side_effect = ConfigurationError(f"{missing_param} is required")
            
            with pytest.raises(ConfigurationError):
                UpstreamClient(**params)