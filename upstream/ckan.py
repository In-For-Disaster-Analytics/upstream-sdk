"""
CKAN integration for Upstream SDK.
"""

from typing import Dict, Any, List, Optional, Union
import logging

import requests

from .exceptions import APIError, ConfigurationError
from .utils import ConfigManager

logger = logging.getLogger(__name__)


class CKANIntegration:
    """
    Handles CKAN data portal integration.
    """
    
    def __init__(self, ckan_url: str, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize CKAN integration.
        
        Args:
            ckan_url: CKAN portal URL
            config: Additional CKAN configuration
        """
        self.ckan_url = ckan_url.rstrip('/')
        self.config = config or {}
        self.session = requests.Session()
        self.session.timeout = self.config.get('timeout', 30)
        
        # Set up authentication if provided
        api_key = self.config.get('api_key')
        if api_key:
            self.session.headers.update({'Authorization': api_key})
    
    def create_dataset(self, 
                      name: str,
                      title: str,
                      description: str = "",
                      organization: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      **kwargs) -> Dict[str, Any]:
        """
        Create a new CKAN dataset.
        
        Args:
            name: Dataset name (URL-friendly)
            title: Dataset title
            description: Dataset description
            organization: Organization name
            tags: List of tags
            **kwargs: Additional dataset metadata
            
        Returns:
            Created dataset information
        """
        # Prepare dataset metadata
        dataset_data = {
            'name': name,
            'title': title,
            'notes': description,
            'owner_org': organization or self.config.get('default_organization'),
            'tags': [{'name': tag} for tag in (tags or [])],
            **kwargs
        }
        
        # Remove None values
        dataset_data = {k: v for k, v in dataset_data.items() if v is not None}
        
        try:
            response = self.session.post(
                f"{self.ckan_url}/api/3/action/package_create",
                json=dataset_data
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise APIError(f"CKAN dataset creation failed: {result.get('error')}")
            
            dataset = result['result']
            logger.info(f"Created CKAN dataset: {dataset['name']} (ID: {dataset['id']})")
            
            return dataset
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to create CKAN dataset: {e}")
    
    def get_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """
        Get CKAN dataset by ID or name.
        
        Args:
            dataset_id: Dataset ID or name
            
        Returns:
            Dataset information
        """
        try:
            response = self.session.get(
                f"{self.ckan_url}/api/3/action/package_show",
                params={'id': dataset_id}
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise APIError(f"CKAN dataset retrieval failed: {result.get('error')}")
            
            return result['result']
            
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response.status_code == 404:
                raise APIError(f"CKAN dataset not found: {dataset_id}")
            raise APIError(f"Failed to get CKAN dataset: {e}")
    
    def update_dataset(self, dataset_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update CKAN dataset.
        
        Args:
            dataset_id: Dataset ID or name
            **kwargs: Dataset fields to update
            
        Returns:
            Updated dataset information
        """
        # Get current dataset
        current_dataset = self.get_dataset(dataset_id)
        
        # Update with new values
        updated_data = {**current_dataset, **kwargs}
        
        try:
            response = self.session.post(
                f"{self.ckan_url}/api/3/action/package_update",
                json=updated_data
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise APIError(f"CKAN dataset update failed: {result.get('error')}")
            
            dataset = result['result']
            logger.info(f"Updated CKAN dataset: {dataset['name']}")
            
            return dataset
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to update CKAN dataset: {e}")
    
    def delete_dataset(self, dataset_id: str) -> bool:
        """
        Delete CKAN dataset.
        
        Args:
            dataset_id: Dataset ID or name
            
        Returns:
            True if successful
        """
        try:
            response = self.session.post(
                f"{self.ckan_url}/api/3/action/package_delete",
                json={'id': dataset_id}
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise APIError(f"CKAN dataset deletion failed: {result.get('error')}")
            
            logger.info(f"Deleted CKAN dataset: {dataset_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to delete CKAN dataset: {e}")
    
    def create_resource(self, 
                       dataset_id: str,
                       name: str,
                       url: str,
                       resource_type: str = "data",
                       format: str = "CSV",
                       description: str = "",
                       **kwargs) -> Dict[str, Any]:
        """
        Create a resource within a CKAN dataset.
        
        Args:
            dataset_id: Dataset ID or name
            name: Resource name
            url: Resource URL
            resource_type: Resource type
            format: Resource format
            description: Resource description
            **kwargs: Additional resource metadata
            
        Returns:
            Created resource information
        """
        resource_data = {
            'package_id': dataset_id,
            'name': name,
            'url': url,
            'resource_type': resource_type,
            'format': format,
            'description': description,
            **kwargs
        }
        
        try:
            response = self.session.post(
                f"{self.ckan_url}/api/3/action/resource_create",
                json=resource_data
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise APIError(f"CKAN resource creation failed: {result.get('error')}")
            
            resource = result['result']
            logger.info(f"Created CKAN resource: {resource['name']} (ID: {resource['id']})")
            
            return resource
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to create CKAN resource: {e}")
    
    def list_datasets(self, 
                     organization: Optional[str] = None,
                     tags: Optional[List[str]] = None,
                     limit: int = 50,
                     offset: int = 0) -> List[Dict[str, Any]]:
        """
        List CKAN datasets.
        
        Args:
            organization: Filter by organization
            tags: Filter by tags
            limit: Maximum number of datasets to return
            offset: Number of datasets to skip
            
        Returns:
            List of dataset information
        """
        params = {
            'rows': limit,
            'start': offset
        }
        
        # Build query
        query_parts = []
        
        if organization:
            query_parts.append(f'owner_org:"{organization}"')
        
        if tags:
            tag_query = ' OR '.join([f'tags:"{tag}"' for tag in tags])
            query_parts.append(f'({tag_query})')
        
        if query_parts:
            params['q'] = ' AND '.join(query_parts)
        
        try:
            response = self.session.get(
                f"{self.ckan_url}/api/3/action/package_search",
                params=params
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise APIError(f"CKAN dataset search failed: {result.get('error')}")
            
            return result['result']['results']
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to list CKAN datasets: {e}")
    
    def publish_campaign(self, 
                        campaign_id: str,
                        campaign_data: Dict[str, Any],
                        auto_publish: bool = True,
                        **kwargs) -> Dict[str, Any]:
        """
        Publish campaign data to CKAN.
        
        Args:
            campaign_id: Campaign ID
            campaign_data: Campaign information
            auto_publish: Whether to automatically publish the dataset
            **kwargs: Additional CKAN parameters
            
        Returns:
            CKAN publication result
        """
        # Create dataset name from campaign
        dataset_name = f"upstream-campaign-{campaign_id}"
        dataset_title = campaign_data.get('name', f'Campaign {campaign_id}')
        
        # Prepare dataset metadata
        dataset_metadata = {
            'name': dataset_name,
            'title': dataset_title,
            'notes': campaign_data.get('description', ''),
            'tags': ['environmental', 'sensors', 'upstream'],
            'extras': [
                {'key': 'campaign_id', 'value': campaign_id},
                {'key': 'source', 'value': 'Upstream Platform'},
                {'key': 'data_type', 'value': 'environmental_sensor_data'}
            ],
            **kwargs
        }
        
        try:
            # Create or update dataset
            try:
                dataset = self.get_dataset(dataset_name)
                # Update existing dataset
                dataset = self.update_dataset(dataset_name, **dataset_metadata)
            except APIError:
                # Create new dataset
                dataset = self.create_dataset(**dataset_metadata)
            
            # Add resources for different data types
            resources_created = []
            
            # Add sensors resource
            if 'sensors_url' in kwargs:
                sensors_resource = self.create_resource(
                    dataset_id=dataset['id'],
                    name='Sensors Configuration',
                    url=kwargs['sensors_url'],
                    format='CSV',
                    description='Sensor configuration and metadata'
                )
                resources_created.append(sensors_resource)
            
            # Add measurements resource
            if 'measurements_url' in kwargs:
                measurements_resource = self.create_resource(
                    dataset_id=dataset['id'],
                    name='Measurement Data',
                    url=kwargs['measurements_url'],
                    format='CSV',
                    description='Environmental sensor measurements'
                )
                resources_created.append(measurements_resource)
            
            # Publish dataset if requested
            if auto_publish and not dataset.get('private', True):
                self.update_dataset(dataset['id'], private=False)
            
            return {
                'success': True,
                'dataset': dataset,
                'resources': resources_created,
                'ckan_url': f"{self.ckan_url}/dataset/{dataset['name']}",
                'message': f'Campaign data published to CKAN: {dataset["name"]}'
            }
            
        except Exception as e:
            logger.error(f"Failed to publish campaign to CKAN: {e}")
            raise APIError(f"CKAN publication failed: {e}")
    
    def get_organization(self, org_id: str) -> Dict[str, Any]:
        """
        Get CKAN organization information.
        
        Args:
            org_id: Organization ID or name
            
        Returns:
            Organization information
        """
        try:
            response = self.session.get(
                f"{self.ckan_url}/api/3/action/organization_show",
                params={'id': org_id}
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise APIError(f"CKAN organization retrieval failed: {result.get('error')}")
            
            return result['result']
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to get CKAN organization: {e}")
    
    def list_organizations(self) -> List[Dict[str, Any]]:
        """
        List CKAN organizations.
        
        Returns:
            List of organization information
        """
        try:
            response = self.session.get(
                f"{self.ckan_url}/api/3/action/organization_list",
                params={'all_fields': True}
            )
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise APIError(f"CKAN organization listing failed: {result.get('error')}")
            
            return result['result']
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to list CKAN organizations: {e}")