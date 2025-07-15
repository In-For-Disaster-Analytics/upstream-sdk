"""
Main client class for the Upstream SDK.

This module provides the primary interface for interacting with the Upstream API
and CKAN data platform.
"""

import os
from typing import Optional, Dict, Any, List, Union
from pathlib import Path

from .auth import AuthManager
from .campaigns import CampaignManager
from .stations import StationManager
from .data import DataUploader
from .ckan import CKANIntegration
from .utils import get_logger, load_config
from .exceptions import ConfigurationError


logger = get_logger(__name__)


class UpstreamClient:
    """Main client class for interacting with the Upstream API."""
    
    def __init__(self, 
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 base_url: Optional[str] = None,
                 ckan_url: Optional[str] = None,
                 config_file: Optional[Union[str, Path]] = None,
                 config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the Upstream client.
        
        Args:
            username: Username for authentication
            password: Password for authentication
            base_url: Base URL for the Upstream API
            ckan_url: URL for CKAN integration
            config_file: Path to configuration file
            config: Configuration dictionary
            
        Raises:
            ConfigurationError: If required configuration is missing
        """
        # Load configuration from file if provided
        if config_file:
            config = load_config(config_file)
        elif config is None:
            config = {}
            
        # Initialize authentication manager
        self.auth_manager = AuthManager(
            username=username,
            password=password,
            base_url=base_url,
            config=config.get('upstream', {})
        )
        
        # Initialize component managers
        self.campaigns = CampaignManager(self.auth_manager)
        self.stations = StationManager(self.auth_manager)
        self.data = DataUploader(self.auth_manager)
        
        # Initialize CKAN integration if URL provided
        ckan_config = config.get('ckan', {})
        if ckan_url or ckan_config.get('url'):
            self.ckan = CKANIntegration(
                ckan_url=ckan_url or ckan_config.get('url'),
                config=ckan_config
            )
        else:
            self.ckan = None
            
        logger.info("Upstream client initialized successfully")
        
    @classmethod
    def from_config(cls, config_file: Union[str, Path]) -> 'UpstreamClient':
        """Create client from configuration file.
        
        Args:
            config_file: Path to configuration file (JSON or YAML)
            
        Returns:
            Configured UpstreamClient instance
        """
        return cls(config_file=config_file)
        
    @classmethod
    def from_environment(cls) -> 'UpstreamClient':
        """Create client from environment variables.
        
        Environment variables:
        - UPSTREAM_USERNAME: Username for authentication
        - UPSTREAM_PASSWORD: Password for authentication
        - UPSTREAM_BASE_URL: Base URL for the Upstream API
        - CKAN_URL: URL for CKAN integration
        
        Returns:
            Configured UpstreamClient instance
        """
        return cls(
            username=os.environ.get('UPSTREAM_USERNAME'),
            password=os.environ.get('UPSTREAM_PASSWORD'),
            base_url=os.environ.get('UPSTREAM_BASE_URL'),
            ckan_url=os.environ.get('CKAN_URL')
        )
        
    def authenticate(self) -> bool:
        """Test authentication with the API.
        
        Returns:
            True if authentication successful, False otherwise
        """
        return self.auth_manager.authenticate()
        
    def create_campaign(self, name: str, description: str = "", 
                       **kwargs) -> 'Campaign':
        """Create a new monitoring campaign.
        
        Args:
            name: Campaign name
            description: Campaign description
            **kwargs: Additional campaign parameters
            
        Returns:
            Created Campaign object
        """
        return self.campaigns.create(name=name, description=description, **kwargs)
        
    def get_campaign(self, campaign_id: str) -> 'Campaign':
        """Get campaign by ID.
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Campaign object
        """
        return self.campaigns.get(campaign_id)
        
    def list_campaigns(self, **kwargs) -> List['Campaign']:
        """List all campaigns.
        
        Args:
            **kwargs: Additional filtering parameters
            
        Returns:
            List of Campaign objects
        """
        return self.campaigns.list(**kwargs)
        
    def create_station(self, campaign_id: str, name: str, 
                      latitude: float, longitude: float,
                      description: str = "", **kwargs) -> 'Station':
        """Create a new monitoring station.
        
        Args:
            campaign_id: ID of the campaign
            name: Station name
            latitude: Station latitude
            longitude: Station longitude
            description: Station description
            **kwargs: Additional station parameters
            
        Returns:
            Created Station object
        """
        return self.stations.create(
            campaign_id=campaign_id,
            name=name,
            latitude=latitude,
            longitude=longitude,
            description=description,
            **kwargs
        )
        
    def get_station(self, station_id: str) -> 'Station':
        """Get station by ID.
        
        Args:
            station_id: Station ID
            
        Returns:
            Station object
        """
        return self.stations.get(station_id)
        
    def list_stations(self, campaign_id: Optional[str] = None, 
                     **kwargs) -> List['Station']:
        """List stations, optionally filtered by campaign.
        
        Args:
            campaign_id: Campaign ID to filter by
            **kwargs: Additional filtering parameters
            
        Returns:
            List of Station objects
        """
        return self.stations.list(campaign_id=campaign_id, **kwargs)
        
    def upload_csv_data(self, campaign_id: str, station_id: str,
                       sensors_file: Union[str, Path],
                       measurements_file: Union[str, Path],
                       **kwargs) -> Dict[str, Any]:
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
            **kwargs
        )
        
    def upload_measurements(self, campaign_id: str, station_id: str,
                           data: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """Upload measurement data directly.
        
        Args:
            campaign_id: Campaign ID
            station_id: Station ID
            data: List of measurement dictionaries
            **kwargs: Additional upload parameters
            
        Returns:
            Upload result dictionary
        """
        return self.data.upload_measurements(
            campaign_id=campaign_id,
            station_id=station_id,
            data=data,
            **kwargs
        )
        
    def publish_to_ckan(self, campaign_id: str, **kwargs) -> Dict[str, Any]:
        """Publish campaign data to CKAN.
        
        Args:
            campaign_id: Campaign ID
            **kwargs: Additional CKAN parameters
            
        Returns:
            CKAN publication result
            
        Raises:
            ConfigurationError: If CKAN integration not configured
        """
        if not self.ckan:
            raise ConfigurationError("CKAN integration not configured")
            
        return self.ckan.publish_campaign(campaign_id=campaign_id, **kwargs)
        
    def get_upload_status(self, upload_id: str) -> Dict[str, Any]:
        """Get status of a data upload.
        
        Args:
            upload_id: Upload ID
            
        Returns:
            Upload status dictionary
        """
        return self.data.get_upload_status(upload_id)
        
    def logout(self) -> None:
        """Logout and invalidate authentication."""
        self.auth_manager.logout()
        logger.info("Client logged out successfully")