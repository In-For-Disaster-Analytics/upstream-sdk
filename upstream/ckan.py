"""
CKAN integration for Upstream SDK.
"""

from datetime import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Union

import requests
from upstream_api_client import GetStationResponse
from upstream_api_client.models.get_campaign_response import GetCampaignResponse

from .exceptions import APIError

logger = logging.getLogger(__name__)


def _serialize_for_json(value: Any) -> str:
    """
    Convert a value to a JSON-serializable string, with special handling for dates.

    Args:
        value: The value to serialize

    Returns:
        JSON-serializable string representation
    """
    if value is None:
        return ""
    elif isinstance(value, datetime):
        # Format datetime for Solr compatibility (ISO format without timezone suffix)
        # Solr expects format like: 2025-07-22T11:16:48Z
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif isinstance(value, (dict, list)):
        try:
            return json.dumps(value, default=str)
        except (TypeError, ValueError):
            return str(value)
    else:
        return str(value)



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
        self.ckan_url = ckan_url.rstrip("/")
        self.config = config or {}
        self.session = requests.Session()
        self.session.timeout = self.config.get("timeout", 30)

        # Set up authentication if provided
        api_key = self.config.get("api_key")
        if api_key:
            self.session.headers.update({"Authorization": api_key})

        access_token = self.config.get("access_token")
        if access_token:
            self.session.headers.update({"Authorization": access_token})

    def create_dataset(
        self,
        name: str,
        title: str,
        description: str = "",
        organization: Optional[str] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
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

        # Determine organization - use parameter or fall back to config
        owner_org = organization or self.config.get("ckan_organization")

        # Prepare dataset metadata
        dataset_data = {
            "name": name,
            "title": title,
            "notes": description,
            "tags": [{"name": tag} for tag in (tags or [])],
            **kwargs,
        }

        # Add owner_org if available
        if owner_org:
            dataset_data["owner_org"] = owner_org
        elif not name.startswith("test-"):
            # Only require organization for non-test datasets
            raise APIError("Organization is required for dataset creation. Please set CKAN_ORGANIZATION environment variable or pass organization parameter.")

        # Remove None values
        dataset_data = {k: v for k, v in dataset_data.items() if v is not None}

        try:
            print('Response', self.session.headers)
            response = self.session.post(
                f"{self.ckan_url}/api/3/action/package_create", json=dataset_data
            )
            response.raise_for_status()

            result = response.json()

            if not result.get("success"):
                raise APIError(f"CKAN dataset creation failed: {result.get('error')}")

            dataset = result["result"]
            logger.info(
                f"Created CKAN dataset: {dataset['name']} (ID: {dataset['id']})"
            )

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
                f"{self.ckan_url}/api/3/action/package_show", params={"id": dataset_id}
            )
            response.raise_for_status()

            result = response.json()

            if not result.get("success"):
                raise APIError(f"CKAN dataset retrieval failed: {result.get('error')}")

            return result["result"]

        except requests.exceptions.RequestException as e:
            if hasattr(e, "response") and e.response.status_code == 404:
                raise APIError(f"CKAN dataset not found: {dataset_id}")
            raise APIError(f"Failed to get CKAN dataset: {e}")

    def update_dataset(self, dataset_id: str, **kwargs: Any) -> Dict[str, Any]:
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

        # Ensure tags are properly formatted as list of dictionaries
        if "tags" in updated_data:
            tags = updated_data["tags"]
            if tags and isinstance(tags[0], str):
                # Convert string tags to dict format
                updated_data["tags"] = [{"name": tag} for tag in tags]

        try:
            response = self.session.post(
                f"{self.ckan_url}/api/3/action/package_update", json=updated_data
            )
            response.raise_for_status()

            result = response.json()

            if not result.get("success"):
                error_details = result.get('error', {})
                raise APIError(f"CKAN dataset update failed: {error_details}")

            dataset = result["result"]
            logger.info(f"Updated CKAN dataset: {dataset['name']}")

            return dataset

        except requests.exceptions.RequestException as e:
            # Log the response content for debugging
            error_msg = f"Failed to update CKAN dataset: {e}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_content = e.response.json()
                    error_msg += f" - Response: {error_content}"
                except:
                    error_msg += f" - Response text: {e.response.text[:500]}"
            raise APIError(error_msg)

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
                f"{self.ckan_url}/api/3/action/package_delete", json={"id": dataset_id}
            )
            response.raise_for_status()

            result = response.json()

            if not result.get("success"):
                raise APIError(f"CKAN dataset deletion failed: {result.get('error')}")

            logger.info(f"Deleted CKAN dataset: {dataset_id}")
            return True

        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to delete CKAN dataset: {e}")

    def create_resource(
        self,
        dataset_id: str,
        name: str,
        url: Optional[str] = None,
        file_path: Optional[Union[str, Path]] = None,
        file_obj: Optional[BinaryIO] = None,
        resource_type: str = "data",
        format: str = "CSV",
        description: str = "",
        metadata: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a resource within a CKAN dataset.

        Args:
            dataset_id: Dataset ID or name
            name: Resource name
            url: Resource URL (for URL-based resources)
            file_path: Path to file to upload
            file_obj: File object to upload
            resource_type: Resource type
            format: Resource format
            description: Resource description
            **kwargs: Additional resource metadata

        Returns:
            Created resource information
        """
        resource_data = {
            "package_id": dataset_id,
            "name": name,
            "resource_type": resource_type,
            "format": format,
            "description": description,
            **kwargs,
        }
        
        # Add metadata fields directly to resource (not in extras array)
        if metadata:
            for meta_item in metadata:
                if isinstance(meta_item, dict) and "key" in meta_item and "value" in meta_item:
                    resource_data[meta_item["key"]] = meta_item["value"]

        # Handle file upload vs URL
        if file_path or file_obj:
            # File upload
            files = {}
            if file_path:
                file_path = Path(file_path)
                if not file_path.exists():
                    raise APIError(f"File not found: {file_path}")
                files["upload"] = (file_path.name, open(file_path, "rb"))
            elif file_obj:
                filename = getattr(file_obj, "name", "uploaded_file")
                if hasattr(filename, "split"):
                    filename = os.path.basename(filename)
                files["upload"] = (filename, file_obj)

            try:
                response = self.session.post(
                    f"{self.ckan_url}/api/3/action/resource_create",
                    data=resource_data,
                    files=files,
                )
                response.raise_for_status()
            finally:
                # Close file if we opened it
                if file_path and "upload" in files:
                    files["upload"][1].close()
        else:
            # URL-based resource
            if not url:
                raise APIError("Either url, file_path, or file_obj must be provided")
            resource_data["url"] = url
            response = self.session.post(
                f"{self.ckan_url}/api/3/action/resource_create", json=resource_data
            )
            response.raise_for_status()

        try:
            result = response.json()

            if not result.get("success"):
                raise APIError(f"CKAN resource creation failed: {result.get('error')}")

            resource = result["result"]
            logger.info(
                f"Created CKAN resource: {resource['name']} (ID: {resource['id']})"
            )

            return resource

        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to create CKAN resource: {e}")

    def list_datasets(
        self,
        organization: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
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
        params = {"rows": limit, "start": offset}

        # Build query
        query_parts = []

        if organization:
            query_parts.append(f'owner_org:"{organization}"')

        if tags:
            tag_query = " OR ".join([f'tags:"{tag}"' for tag in tags])
            query_parts.append(f"({tag_query})")

        if query_parts:
            params["q"] = " AND ".join(query_parts)

        try:
            response = self.session.get(
                f"{self.ckan_url}/api/3/action/package_search", params=params
            )
            response.raise_for_status()

            result = response.json()

            if not result.get("success"):
                raise APIError(f"CKAN dataset search failed: {result.get('error')}")

            return result["result"]["results"]

        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to list CKAN datasets: {e}")

    def sanitize_title(self, title: str) -> str:
        """
        Sanitize a title to be used as a CKAN dataset title.
        """
        return title.replace(" ", "_").replace("-", "_")

    def publish_campaign(
        self,
        campaign_id: str,
        campaign_data: GetCampaignResponse,
        station_measurements: BinaryIO,
        station_sensors: BinaryIO,
        station_data: GetStationResponse,
        auto_publish: bool = True,
    ) -> Dict[str, Any]:
        """
        Publish campaign data to CKAN.

        Args:
            campaign_id: Campaign ID
            campaign_data: Campaign information
            station_measurements: BinaryIO stream of station measurements CSV
            station_sensors: BinaryIO stream of station sensors CSV
            auto_publish: Whether to automatically publish the dataset

        Returns:
            CKAN publication result
        """
        # Create dataset name from campaign
        dataset_name = f"upstream-campaign-{campaign_id}"
        dataset_title = campaign_data.name

        if campaign_data.description:
            description = campaign_data.description
        else:
            description = f"\nSensor Types: {', '.join(campaign_data.summary.sensor_types)}"

        # Prepare dataset metadata
        dataset_metadata = {
            "name": dataset_name,
            "title": dataset_title,
            "notes": description,
            "tags": ["environmental", "sensors", "upstream"],
            "extras": [
                {"key": "source", "value": "Upstream Platform"},
                {"key": "data_type", "value": "environmental_sensor_data"},
                {"key": "campaign", "value": _serialize_for_json(campaign_data.to_dict())},
                {"key": "campaign_id", "value": campaign_id},
                {"key": "campaign_name", "value": campaign_data.name or ""},
                {"key": "campaign_description", "value": campaign_data.description or ""},
                {"key": "campaign_contact_name", "value": campaign_data.contact_name or ""},
                {"key": "campaign_contact_email", "value": campaign_data.contact_email or ""},
                {"key": "campaign_allocation", "value": campaign_data.allocation or ""},
            ],
        }

        try:
            # Create or update dataset
            should_update = False
            try:
                dataset = self.get_dataset(dataset_name)
                should_update = True
            except APIError:
                should_update = False

            if should_update:
                dataset = self.update_dataset(dataset_name, **dataset_metadata)
            else:
                dataset = self.create_dataset(**dataset_metadata)

            # Add resources for different data types
            resources_created = []


            station_metadata = [
                {"key": "station_id", "value": str(station_data.id)},
                {"key": "station_name", "value": station_data.name or ""},
                {"key": "station_description", "value": station_data.description or ""},
                {"key": "station_contact_name", "value": station_data.contact_name or ""},
                {"key": "station_contact_email", "value": station_data.contact_email or ""},
                {"key": "station_active", "value": str(station_data.active)},
                {"key": "station_geometry", "value": _serialize_for_json(station_data.geometry)},
                {"key": "station_sensors", "value": _serialize_for_json([sensor.to_dict() for sensor in station_data.sensors])},
                {"key": "station_sensors_count", "value": str(len(station_data.sensors))},
                {"key": "station_sensors_aliases", "value": _serialize_for_json([sensor.alias for sensor in station_data.sensors])},
                {"key": "station_sensors_units", "value": _serialize_for_json([sensor.units for sensor in station_data.sensors])},
                {"key": "station_sensors_descriptions", "value": _serialize_for_json([sensor.description for sensor in station_data.sensors])},
                {"key": "station_sensors_variablename", "value": _serialize_for_json([sensor.variablename for sensor in station_data.sensors])},
            ]


            # Add sensors resource (file upload or URL)
            published_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            sensors_resource = self.create_resource(
                dataset_id=dataset["id"],
                name=f"{station_data.name} - Sensors Configuration - {published_at}",
                file_obj=station_sensors,
                format="CSV",
                description="Sensor configuration and metadata",
                metadata=station_metadata,
            )
            resources_created.append(sensors_resource)

            # Add measurements resource (file upload or URL)
            measurements_resource = self.create_resource(
                    dataset_id=dataset["id"],
                    name=f"{station_data.name} - Measurement Data - {published_at}",
                    file_obj=station_measurements,
                    format="CSV",
                    description="Environmental sensor measurements",
                    metadata=station_metadata,
                )
            resources_created.append(measurements_resource)

            # Publish dataset if requested
            if auto_publish and not dataset.get("private", True):
                self.update_dataset(dataset["id"], private=False)

            return {
                "success": True,
                "dataset": dataset,
                "resources": resources_created,
                "ckan_url": f"{self.ckan_url}/dataset/{dataset['name']}",
                "message": f'Campaign data published to CKAN: {dataset["name"]}',
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
                f"{self.ckan_url}/api/3/action/organization_show", params={"id": org_id}
            )
            response.raise_for_status()

            result = response.json()

            if not result.get("success"):
                raise APIError(
                    f"CKAN organization retrieval failed: {result.get('error')}"
                )

            return result["result"]

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
                params={"all_fields": True},
            )
            response.raise_for_status()

            result = response.json()

            if not result.get("success"):
                raise APIError(
                    f"CKAN organization listing failed: {result.get('error')}"
                )

            return result["result"]

        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to list CKAN organizations: {e}")
