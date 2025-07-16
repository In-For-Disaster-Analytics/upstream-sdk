import os
from datetime import datetime, timedelta
import pytest
from upstream_api_client.models import CampaignsIn, CampaignUpdate
from upstream.client import UpstreamClient
from upstream.exceptions import APIError

BASE_URL = 'http://localhost:8008'
CKAN_URL = 'http://ckan.tacc.cloud:5000'

USERNAME = os.environ.get('UPSTREAM_USERNAME')
PASSWORD = os.environ.get('UPSTREAM_PASSWORD')

pytestmark = pytest.mark.integration

@pytest.mark.skipif(not USERNAME or not PASSWORD, reason="UPSTREAM_USERNAME and UPSTREAM_PASSWORD must be set in env")
def test_campaign_lifecycle():
    client = UpstreamClient(
        username=USERNAME,
        password=PASSWORD,
        base_url=BASE_URL,
        ckan_url=CKAN_URL
    )

    # Unique campaign name
    campaign_name = f"integration-test-campaign-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    description = "Integration test campaign"
    contact_name = "Integration Tester"
    contact_email = "integration@example.com"
    allocation = "TACC"
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=30)

    campaign_in = CampaignsIn(
        name=campaign_name,
        description=description,
        contact_name=contact_name,
        contact_email=contact_email,
        allocation=allocation,
        start_date=start_date,
        end_date=end_date
    )

    # Create
    created = client.campaigns.create(campaign_in)
    assert created.id is not None
    print(f"Created campaign: {created.id}")

    try:
        # Get
        fetched = client.campaigns.get(str(created.id))
        assert fetched.name == campaign_name
        assert fetched.description == description
        assert fetched.contact_name == contact_name
        assert fetched.contact_email == contact_email
        assert fetched.allocation == allocation
        assert fetched.start_date == start_date
        assert fetched.end_date == end_date
        print(f"Fetched campaign: {fetched.id}")

        # Update
        update = CampaignUpdate(description="Updated integration test campaign")
        client.campaigns.update(str(created.id), update)

        # Fetch again
        fetched_again = client.campaigns.get(str(created.id))
        assert fetched_again.description == "Updated integration test campaign"
        print(f"Updated campaign: {fetched_again.id}")

    finally:
        # Delete
        deleted = client.campaigns.delete(str(created.id))
        assert deleted is True
        print(f"Deleted campaign: {created.id}")

        # Check that the campaign is deleted
        with pytest.raises(APIError):
            client.campaigns.get(str(created.id))