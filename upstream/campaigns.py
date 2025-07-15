"""
Campaign management module for the Upstream SDK using OpenAPI client.

This module handles creation, retrieval, and management of environmental
monitoring campaigns using the generated OpenAPI client.
"""

from typing import Optional
from datetime import datetime

from upstream.upstream_client.models.get_campaign_response import GetCampaignResponse
from upstream.upstream_client.models.list_campaigns_response_pagination import ListCampaignsResponsePagination

from .upstream_client.api import CampaignsApi
from .upstream_client.models import (
    CampaignsIn,
    CampaignCreateResponse,
    CampaignUpdate
)
from .auth import AuthManager
from .upstream_client.rest import ApiException

from .exceptions import APIError, ValidationError
from .utils import get_logger

logger = get_logger(__name__)



class CampaignManager:
    """Manages campaign operations using the OpenAPI client."""

    auth_manager: AuthManager
    def __init__(self, auth_manager: AuthManager) -> None:
        """Initialize campaign manager.

        Args:
            auth_manager: Authentication manager instance
        """
        self.auth_manager = auth_manager

    def create(self, name: str, description: str = "",
               contact_name: Optional[str] = None,
               contact_email: Optional[str] = None,
               allocation: str = "TACC",
               start_date: Optional[datetime] = None,
               end_date: Optional[datetime] = None,
               ) -> CampaignCreateResponse:
        """Create a new campaign.

        Args:
            name: Campaign name
            description: Campaign description
            contact_name: Contact person name
            contact_email: Contact email address
            allocation: Resource allocation (defaults to "TACC")
            start_date: Campaign start date
            end_date: Campaign end date

        Returns:
            Created Campaign object

        Raises:
            ValidationError: If campaign data is invalid
            APIError: If API request fails
        """
        if not name.strip():
            raise ValidationError("Campaign name cannot be empty", field="name")

        # Set default dates if not provided
        if start_date is None:
            start_date = datetime.now()
        if end_date is None:
            end_date = datetime.now().replace(year=datetime.now().year + 1)

        # Create campaign input model
        campaign_input = CampaignsIn(
            name=name.strip(),
            description=description.strip() if description else "",
            contact_name=contact_name,
            contact_email=contact_email,
            allocation=allocation,
            start_date=start_date,
            end_date=end_date
        )

        try:
            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)

                response: CampaignCreateResponse = campaigns_api.create_campaign_api_v1_campaigns_post(
                    campaigns_in=campaign_input
                )

                return response

        except ApiException as e:
            if e.status == 422:
                raise ValidationError(f"Campaign validation failed: {e}")
            else:
                raise APIError(f"Failed to create campaign: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to create campaign: {e}")

    def get(self, campaign_id: str) -> GetCampaignResponse:
        """Get campaign by ID.

        Args:
            campaign_id: Campaign ID

        Returns:
            Campaign object

        Raises:
            APIError: If API request fails or campaign not found
        """
        try:
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)

                response : GetCampaignResponse = campaigns_api.get_campaign_api_v1_campaigns_campaign_id_get(
                    campaign_id=campaign_id_int
                )
                return response

        except ValueError:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}")
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Campaign not found: {campaign_id}", status_code=404)
            else:
                raise APIError(f"Failed to get campaign: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to get campaign: {e}")

    def list(self, limit: int = 50, page: int = 1,
             search: Optional[str] = None) -> ListCampaignsResponsePagination:
        """List campaigns with optional filtering.

        Args:
            limit: Maximum number of campaigns to return
            page: Page number for pagination
            search: Search term for campaign names/descriptions

        Returns:
            List of Campaign objects

        Raises:
            APIError: If API request fails
        """
        try:
            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)
                response : ListCampaignsResponsePagination = campaigns_api.list_campaigns_api_v1_campaigns_get(
                    limit=limit,
                    page=page,
                )
                logger.info(f"Retrieved {response.total} campaigns")
                return response

        except ApiException as e:
            raise APIError(f"Failed to list campaigns: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to list campaigns: {e}")

    def update(self, campaign_id: str, name: Optional[str] = None,
               description: Optional[str] = None,
               contact_name: Optional[str] = None,
               contact_email: Optional[str] = None,
               ) -> CampaignCreateResponse:
        """Update an existing campaign.

        Args:
            campaign_id: Campaign ID
            name: New campaign name
            description: New campaign description
            contact_name: New contact name
            contact_email: New contact email

        Returns:
            Updated Campaign object

        Raises:
            ValidationError: If update data is invalid
            APIError: If API request fails
        """
        try:
            campaign_id_int = int(campaign_id)

            # Build update data
            update_data = {}
            if name is not None:
                if not name.strip():
                    raise ValidationError("Campaign name cannot be empty", field="name")
                update_data['name'] = name.strip()
            if description is not None:
                update_data['description'] = description.strip()
            if contact_name is not None:
                update_data['contact_name'] = contact_name
            if contact_email is not None:
                update_data['contact_email'] = contact_email

            if not update_data:
                raise ValidationError("No fields to update provided")

            campaign_update = CampaignUpdate(**update_data)

            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)

                response = campaigns_api.partial_update_campaign_api_v1_campaigns_campaign_id_patch_with_http_info(
                    campaign_id=campaign_id_int,
                    campaign_update=campaign_update
                )

                return response

        except ValueError:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}")
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Campaign not found: {campaign_id}", status_code=404)
            elif e.status == 422:
                raise ValidationError(f"Campaign validation failed: {e}")
            else:
                raise APIError(f"Failed to update campaign: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to update campaign: {e}")

    def delete(self, campaign_id: str) -> bool:
        """Delete a campaign.

        Args:
            campaign_id: Campaign ID

        Returns:
            True if successful

        Raises:
            APIError: If API request fails
        """
        try:
            campaign_id_int = int(campaign_id)

            with self.auth_manager.get_api_client() as api_client:
                campaigns_api = CampaignsApi(api_client)

                campaigns_api.delete_campaign_api_v1_campaigns_campaign_id_delete(
                    campaign_id=campaign_id_int
                )

                logger.info(f"Deleted campaign: {campaign_id}")
                return True

        except ValueError:
            raise ValidationError(f"Invalid campaign ID format: {campaign_id}")
        except ApiException as e:
            if e.status == 404:
                raise APIError(f"Campaign not found: {campaign_id}", status_code=404)
            else:
                raise APIError(f"Failed to delete campaign: {e}", status_code=e.status)
        except Exception as e:
            raise APIError(f"Failed to delete campaign: {e}")