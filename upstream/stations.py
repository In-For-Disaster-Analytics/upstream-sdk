"""
Station management module for the Upstream SDK using OpenAPI client.

This module handles creation, retrieval, and management of monitoring stations
using the generated OpenAPI client.
"""

from typing import Optional, Any

from upstream.upstream_client.models.campaign_create_response import CampaignCreateResponse

from .upstream_client.api import StationsApi
from .upstream_client.models import (
    StationCreate,
    StationUpdate,
    GetStationResponse,
    StationCreateResponse,
    ListStationsResponsePagination
)
from .upstream_client.rest import ApiException

from .exceptions import APIError, ValidationError
from .utils import get_logger

logger = get_logger(__name__)


class StationManager:
    """
    Manages station operations using the OpenAPI client.
    """

    def __init__(self, auth_manager) -> None:
        """
        Initialize station manager.

        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager

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
    ) -> CampaignCreateResponse:
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
            APIError: If creation fails
        """
        # Validate required fields
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")
        if not name or not name.strip():
            raise ValidationError("Station name is required", field="name")
        if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90", field="latitude")
        if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180", field="longitude")

        # Validate email if provided
        if contact_email and "@" not in contact_email:
            raise ValidationError("Invalid email format", field="contact_email")

        # Create station input model
        station_input = StationCreate(
            name=name.strip(),
            latitude=latitude,
            longitude=longitude,
            description=description,
            contact_name=contact_name,
            contact_email=contact_email,
            altitude=altitude
        )

        try:
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                response = stations_api.create_station_api_v1_campaigns_campaign_id_stations_post(
                    campaign_id=campaign_id_int,
                    station_create=station_input
                )
                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}") from exc
        except ApiException as e:
            if e.status == 422:
                raise ValidationError(f"Station validation failed: {e}") from e
            else:
                raise APIError(f"Failed to create station: {e}", status_code=e.status) from e
        except Exception as e:
            raise APIError(f"Failed to create station: {e}") from e

    def get(self, station_id: str, campaign_id: str) -> GetStationResponse:
        """
        Get station by ID.

        Args:
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            Station instance

        Raises:
            ValidationError: If IDs are invalid
            APIError: If station not found or retrieval fails
        """
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                response = stations_api.get_station_api_v1_campaigns_campaign_id_stations_station_id_get(
                    station_id=station_id_int,
                    campaign_id=campaign_id_int
                )

                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid ID format: station_id={station_id}, campaign_id={campaign_id}") from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Station not found: {station_id}", status_code=404)
            else:
                raise APIError(f"Failed to get station: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to get station: {e}")

    def list(
        self,
        campaign_id: str,
        limit: int = 100,
        page: int = 1,
    ) -> ListStationsResponsePagination:
        """
        List stations for a campaign.

        Args:
            campaign_id: Campaign ID to filter by
            limit: Maximum number of stations to return
            page: Page number for pagination

        Returns:
            List of Station instances

        Raises:
            ValidationError: If campaign_id is invalid
            APIError: If listing fails
        """
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                response = stations_api.list_stations_api_v1_campaigns_campaign_id_stations_get(
                    campaign_id=campaign_id_int,
                    limit=limit,
                    page=page
                )

                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}") from exc
        except ApiException as e:
            raise APIError(f"Failed to list stations: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to list stations: {e}")

    def update(self, station_id: str, campaign_id: str, **kwargs: Any) -> StationCreateResponse:
        """
        Update station.

        Args:
            station_id: Station ID
            campaign_id: Campaign ID
            **kwargs: Station fields to update

        Returns:
            Updated Station instance

        Raises:
            ValidationError: If IDs are invalid or no update data provided
            APIError: If update fails
        """
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            raise ValidationError("No update data provided")

        # Validate coordinates if provided
        if "latitude" in update_data:
            lat = update_data["latitude"]
            if not isinstance(lat, (int, float)) or not (-90 <= lat <= 90):
                raise ValidationError("Latitude must be between -90 and 90", field="latitude")

        if "longitude" in update_data:
            lon = update_data["longitude"]
            if not isinstance(lon, (int, float)) or not (-180 <= lon <= 180):
                raise ValidationError("Longitude must be between -180 and 180", field="longitude")

        # Validate email if provided
        if "contact_email" in update_data and "@" not in update_data["contact_email"]:
            raise ValidationError("Invalid email format", field="contact_email")

        try:
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            station_update = StationUpdate(**update_data)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                response = stations_api.partial_update_station_api_v1_campaigns_campaign_id_stations_station_id_patch(
                    campaign_id=campaign_id_int,
                    station_id=station_id_int,
                    station_update=station_update
                )

                return response

        except ValueError as exc:
            raise ValidationError(f"Invalid ID format: station_id={station_id}, campaign_id={campaign_id}") from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Station not found: {station_id}", status_code=404) from e
            elif e.status == 422:
                raise ValidationError(f"Station validation failed: {e}") from e
            else:
                raise APIError(f"Failed to update station: {e}", status_code=e.status) from e
        except Exception as e:
            raise APIError(f"Failed to update station: {e}") from e

    def delete(self, station_id: str, campaign_id: str) -> bool:
        """
        Delete station.

        Args:
            station_id: Station ID
            campaign_id: Campaign ID

        Returns:
            True if deletion successful

        Raises:
            ValidationError: If IDs are invalid
            APIError: If deletion fails
        """
        if not station_id:
            raise ValidationError("Station ID is required", field="station_id")
        if not campaign_id:
            raise ValidationError("Campaign ID is required", field="campaign_id")

        try:
            station_id_int = int(station_id)
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                stations_api = StationsApi(api_client)

                # Note: The OpenAPI spec shows delete_sensor method, but this appears to be
                # for deleting stations based on the endpoint path structure
                stations_api.delete_sensor_api_v1_campaigns_campaign_id_stations_delete(
                    campaign_id=campaign_id_int
                )

                logger.info(f"Deleted station: {station_id}")
                return True

        except ValueError as exc:
            raise ValidationError(f"Invalid ID format: station_id={station_id}, campaign_id={campaign_id}") from exc
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Station not found: {station_id}", status_code=404)
            else:
                raise APIError(f"Failed to delete station: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to delete station: {e}")