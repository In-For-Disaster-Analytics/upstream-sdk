"""
Campaign management for Upstream SDK.
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
class Campaign:
    """
    Represents an Upstream campaign.
    """
    id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: str = "active"
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


class CampaignManager:
    """
    Manages campaign operations for the Upstream API.
    """
    
    def __init__(self, config: ConfigManager, auth_manager: Any) -> None:
        """
        Initialize campaign manager.
        
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
        name: str,
        description: Optional[str] = None,
        **kwargs: Any,
    ) -> Campaign:
        """
        Create a new campaign.
        
        Args:
            name: Campaign name
            description: Campaign description
            **kwargs: Additional campaign parameters
            
        Returns:
            Created Campaign instance
            
        Raises:
            ValidationError: If campaign data is invalid
            UpstreamError: If creation fails
        """
        if not name or not name.strip():
            raise ValidationError("Campaign name is required")
        
        campaign_data = {
            "name": name.strip(),
            "description": description,
            **kwargs,
        }
        
        # Remove None values
        campaign_data = {k: v for k, v in campaign_data.items() if v is not None}
        
        url = f"{self.config.base_url}/campaigns"
        headers = self.auth.get_headers()
        
        try:
            response = self.session.post(url, json=campaign_data, headers=headers)
            response.raise_for_status()
            
            campaign_response = response.json()
            
            campaign = Campaign(
                id=campaign_response["id"],
                name=campaign_response["name"],
                description=campaign_response.get("description"),
                created_at=campaign_response.get("created_at"),
                updated_at=campaign_response.get("updated_at"),
                status=campaign_response.get("status", "active"),
                metadata=campaign_response.get("metadata", {}),
            )
            
            logger.info(f"Created campaign: {campaign.name} (ID: {campaign.id})")
            return campaign
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to create campaign: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                raise ValidationError(f"Invalid campaign data: {e}")
            else:
                raise UpstreamError(f"Campaign creation failed: {e}")
    
    def get(self, campaign_id: str) -> Campaign:
        """
        Get campaign by ID.
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Campaign instance
            
        Raises:
            UpstreamError: If campaign not found or retrieval fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required")
        
        url = f"{self.config.base_url}/campaigns/{campaign_id}"
        headers = self.auth.get_headers()
        
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            
            campaign_data = response.json()
            
            return Campaign(
                id=campaign_data["id"],
                name=campaign_data["name"],
                description=campaign_data.get("description"),
                created_at=campaign_data.get("created_at"),
                updated_at=campaign_data.get("updated_at"),
                status=campaign_data.get("status", "active"),
                metadata=campaign_data.get("metadata", {}),
            )
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to retrieve campaign: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise UpstreamError(f"Campaign not found: {campaign_id}")
            else:
                raise UpstreamError(f"Campaign retrieval failed: {e}")
    
    def list(self, limit: int = 100, offset: int = 0) -> List[Campaign]:
        """
        List campaigns.
        
        Args:
            limit: Maximum number of campaigns to return
            offset: Number of campaigns to skip
            
        Returns:
            List of Campaign instances
        """
        url = f"{self.config.base_url}/campaigns"
        headers = self.auth.get_headers()
        params = {"limit": limit, "offset": offset}
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            campaigns_data = response.json()
            
            campaigns = []
            for campaign_data in campaigns_data.get("campaigns", []):
                campaign = Campaign(
                    id=campaign_data["id"],
                    name=campaign_data["name"],
                    description=campaign_data.get("description"),
                    created_at=campaign_data.get("created_at"),
                    updated_at=campaign_data.get("updated_at"),
                    status=campaign_data.get("status", "active"),
                    metadata=campaign_data.get("metadata", {}),
                )
                campaigns.append(campaign)
            
            return campaigns
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to list campaigns: {e}")
    
    def update(self, campaign_id: str, **kwargs: Any) -> Campaign:
        """
        Update campaign.
        
        Args:
            campaign_id: Campaign ID
            **kwargs: Campaign fields to update
            
        Returns:
            Updated Campaign instance
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required")
        
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        
        if not update_data:
            raise ValidationError("No update data provided")
        
        url = f"{self.config.base_url}/campaigns/{campaign_id}"
        headers = self.auth.get_headers()
        
        try:
            response = self.session.patch(url, json=update_data, headers=headers)
            response.raise_for_status()
            
            campaign_data = response.json()
            
            return Campaign(
                id=campaign_data["id"],
                name=campaign_data["name"],
                description=campaign_data.get("description"),
                created_at=campaign_data.get("created_at"),
                updated_at=campaign_data.get("updated_at"),
                status=campaign_data.get("status", "active"),
                metadata=campaign_data.get("metadata", {}),
            )
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to update campaign: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise UpstreamError(f"Campaign not found: {campaign_id}")
            else:
                raise UpstreamError(f"Campaign update failed: {e}")
    
    def delete(self, campaign_id: str) -> bool:
        """
        Delete campaign.
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            True if deletion successful
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required")
        
        url = f"{self.config.base_url}/campaigns/{campaign_id}"
        headers = self.auth.get_headers()
        
        try:
            response = self.session.delete(url, headers=headers)
            response.raise_for_status()
            
            logger.info(f"Deleted campaign: {campaign_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            raise UpstreamError(f"Failed to delete campaign: {e}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise UpstreamError(f"Campaign not found: {campaign_id}")
            else:
                raise UpstreamError(f"Campaign deletion failed: {e}")