"""
Station management for Upstream SDK.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import logging

import requests

from .exceptions import UpstreamError, ValidationError
from .utils import ConfigManager

logger = logging.getLogger(__name__)


@dataclass
class Station:
    """
    Represents an Upstream monitoring station.
    """
    id: str
    campaign_id: str
    name: str
    latitude: float
    longitude: float
    description: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    altitude: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: str = "active"
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


class StationManager:
    """
    Manages station operations for the Upstream API.
    """
    
    def __init__(self, config: ConfigManager, auth_manager: Any) -> None:
        """
        Initialize station manager.
        
        Args:
            config: Configuration manager instance
            auth_manager: Authentication manager instance
        """
        self.config = config
        self.auth = auth_manager
        self.session = requests.Session()
        self.session.timeout = config.timeout
    
    def create(
        self,
        campaign_id: str,
        name: str,
        latitude: float,
        longitude: float,
        description: Optional[str] = None,
        contact_name: Optional[str] = None,
        contact_email: Optional[str] = None,
        altitude: Optional[float] = None,
        **kwargs: Any,
    ) -> Station:
        """
        Create a new station.
        
        Args:
            campaign_id: Parent campaign ID
            name: Station name
            latitude: Station latitude
            longitude: Station longitude
            description: Station description
            contact_name: Contact person name
            contact_email: Contact email
            altitude: Station altitude in meters
            **kwargs: Additional station parameters
            
        Returns:
            Created Station instance
            
        Raises:
            ValidationError: If station data is invalid
            UpstreamError: If creation fails
        """
        # Validate required fields
        if not campaign_id:
            raise ValidationError("Campaign ID is required")
        if not name or not name.strip():
            raise ValidationError("Station name is required")
        if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90")
        if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180")
        
        # Validate email if provided
        if contact_email and "@" not in contact_email:
            raise ValidationError("Invalid email format")
        
        station_data = {
            "campaign_id": campaign_id,
            "name": name.strip(),
            "latitude": latitude,
            "longitude": longitude,
            "description": description,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "altitude": altitude,
            **kwargs,
        }
        
        # Remove None values
        station_data = {k: v for k, v in station_data.items() if v is not None}
        
        url = f"{self.config.base_url}/stations"
        headers = self.auth.get_headers()
        
        try:
            response = self.session.post(url, json=station_data, headers=headers)
            response.raise_for_status()
            
            station_response = response.json()
            
            station = Station(
                id=station_response["id"],
                campaign_id=station_response["campaign_id"],
                name=station_response["name"],
                latitude=station_response["latitude"],
                longitude=station_response["longitude"],
                description=station_response.get("description"),
                contact_name=station_response.get("contact_name"),
                contact_email=station_response.get("contact_email"),
                altitude=station_response.get("altitude"),
                created_at=station_response.get("created_at"),
                updated_at=station_response.get("updated_at"),
                status=station_response.get("status", "active"),
                metadata=station_response.get("metadata", {}),
            )
            
            logger.info(f"Created station: {station.name} (ID: {station.id})")
            return station
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to create station: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                raise ValidationError(f"Invalid station data: {e}")
            else:
                raise UpstreamError(f"Station creation failed: {e}")
    
    def get(self, station_id: str) -> Station:
        """
        Get station by ID.
        
        Args:
            station_id: Station ID
            
        Returns:
            Station instance
            
        Raises:
            UpstreamError: If station not found or retrieval fails
        """
        if not station_id:
            raise ValidationError("Station ID is required")
        
        url = f"{self.config.base_url}/stations/{station_id}"
        headers = self.auth.get_headers()
        
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            
            station_data = response.json()
            
            return Station(
                id=station_data["id"],
                campaign_id=station_data["campaign_id"],
                name=station_data["name"],
                latitude=station_data["latitude"],
                longitude=station_data["longitude"],
                description=station_data.get("description"),
                contact_name=station_data.get("contact_name"),
                contact_email=station_data.get("contact_email"),
                altitude=station_data.get("altitude"),
                created_at=station_data.get("created_at"),
                updated_at=station_data.get("updated_at"),
                status=station_data.get("status", "active"),
                metadata=station_data.get("metadata", {}),
            )
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to retrieve station: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise UpstreamError(f"Station not found: {station_id}")
            else:
                raise UpstreamError(f"Station retrieval failed: {e}")
    
    def list(
        self,
        campaign_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Station]:
        """
        List stations.
        
        Args:
            campaign_id: Filter by campaign ID
            limit: Maximum number of stations to return
            offset: Number of stations to skip
            
        Returns:
            List of Station instances
        """
        url = f"{self.config.base_url}/stations"
        headers = self.auth.get_headers()
        params = {"limit": limit, "offset": offset}
        
        if campaign_id:
            params["campaign_id"] = campaign_id
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            stations_data = response.json()
            
            stations = []
            for station_data in stations_data.get("stations", []):
                station = Station(
                    id=station_data["id"],
                    campaign_id=station_data["campaign_id"],
                    name=station_data["name"],
                    latitude=station_data["latitude"],
                    longitude=station_data["longitude"],
                    description=station_data.get("description"),
                    contact_name=station_data.get("contact_name"),
                    contact_email=station_data.get("contact_email"),
                    altitude=station_data.get("altitude"),
                    created_at=station_data.get("created_at"),
                    updated_at=station_data.get("updated_at"),
                    status=station_data.get("status", "active"),
                    metadata=station_data.get("metadata", {}),
                )
                stations.append(station)
            
            return stations
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to list stations: {e}")
    
    def update(self, station_id: str, **kwargs: Any) -> Station:
        """
        Update station.
        
        Args:
            station_id: Station ID
            **kwargs: Station fields to update
            
        Returns:
            Updated Station instance
        """
        if not station_id:
            raise ValidationError("Station ID is required")
        
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        
        if not update_data:
            raise ValidationError("No update data provided")
        
        # Validate coordinates if provided
        if "latitude" in update_data:
            lat = update_data["latitude"]
            if not isinstance(lat, (int, float)) or not (-90 <= lat <= 90):
                raise ValidationError("Latitude must be between -90 and 90")
        
        if "longitude" in update_data:
            lon = update_data["longitude"]
            if not isinstance(lon, (int, float)) or not (-180 <= lon <= 180):
                raise ValidationError("Longitude must be between -180 and 180")
        
        # Validate email if provided
        if "contact_email" in update_data and "@" not in update_data["contact_email"]:
            raise ValidationError("Invalid email format")
        
        url = f"{self.config.base_url}/stations/{station_id}"
        headers = self.auth.get_headers()
        
        try:
            response = self.session.patch(url, json=update_data, headers=headers)
            response.raise_for_status()
            
            station_data = response.json()
            
            return Station(
                id=station_data["id"],
                campaign_id=station_data["campaign_id"],
                name=station_data["name"],
                latitude=station_data["latitude"],
                longitude=station_data["longitude"],
                description=station_data.get("description"),
                contact_name=station_data.get("contact_name"),
                contact_email=station_data.get("contact_email"),
                altitude=station_data.get("altitude"),
                created_at=station_data.get("created_at"),
                updated_at=station_data.get("updated_at"),
                status=station_data.get("status", "active"),
                metadata=station_data.get("metadata", {}),
            )
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to update station: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise UpstreamError(f"Station not found: {station_id}")
            else:
                raise UpstreamError(f"Station update failed: {e}")
    
    def delete(self, station_id: str) -> bool:
        """
        Delete station.
        
        Args:
            station_id: Station ID
            
        Returns:
            True if deletion successful
        """
        if not station_id:
            raise ValidationError("Station ID is required")
        
        url = f"{self.config.base_url}/stations/{station_id}"
        headers = self.auth.get_headers()
        
        try:
            response = self.session.delete(url, headers=headers)
            response.raise_for_status()
            
            logger.info(f"Deleted station: {station_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to delete station: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise UpstreamError(f"Station not found: {station_id}")
            else:
                raise UpstreamError(f"Station deletion failed: {e}")