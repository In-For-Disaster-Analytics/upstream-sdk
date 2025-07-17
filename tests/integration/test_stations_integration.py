import os
import pytest
from datetime import datetime, timedelta
from upstream.client import UpstreamClient
from upstream_api_client.models import (
    CampaignsIn,
    CampaignUpdate,
    StationCreate,
    StationUpdate,
)
from upstream.exceptions import APIError

BASE_URL = "http://localhost:8000"
CKAN_URL = "http://ckan.tacc.cloud:5000"

USERNAME = os.environ.get("UPSTREAM_USERNAME")
PASSWORD = os.environ.get("UPSTREAM_PASSWORD")

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    not USERNAME or not PASSWORD,
    reason="UPSTREAM_USERNAME and UPSTREAM_PASSWORD must be set in env",
)
def test_station_lifecycle():
    client = UpstreamClient(
        username=USERNAME, password=PASSWORD, base_url=BASE_URL, ckan_url=CKAN_URL
    )

    # Create a campaign first
    campaign_name = (
        f"integration-test-campaign-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    campaign_in = CampaignsIn(
        name=campaign_name,
        description="Integration test campaign for stations",
        contact_name="Integration Tester",
        contact_email="integration@example.com",
        allocation="TACC",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
    )

    created_campaign = client.campaigns.create(campaign_in)
    assert created_campaign.id is not None
    print(f"Created campaign: {created_campaign.id}")

    try:
        # Create station
        station_name = (
            f"integration-test-station-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        station_create = StationCreate(
            name=station_name,
            description="Integration test station",
            contact_name="Station Tester",
            contact_email="station@example.com",
            start_date=datetime.now(),
            active=True,
        )

        created_station = client.stations.create(
            str(created_campaign.id), station_create
        )
        assert created_station.id is not None
        print(f"Created station: {created_station.id}")

        try:
            # Get station
            fetched_station = client.stations.get(
                str(created_station.id), str(created_campaign.id)
            )
            assert fetched_station.name == station_name
            assert fetched_station.description == "Integration test station"
            assert fetched_station.contact_name == "Station Tester"
            assert fetched_station.contact_email == "station@example.com"
            print(f"Fetched station: {fetched_station.id}")

            # Update station
            station_update = StationUpdate(
                description="Updated integration test station"
            )
            client.stations.update(
                str(created_station.id), str(created_campaign.id), station_update
            )

            # Fetch again to verify update
            fetched_again = client.stations.get(
                str(created_station.id), str(created_campaign.id)
            )
            assert fetched_again.description == "Updated integration test station"
            print(f"Updated station: {fetched_again.id}")

        finally:
            # Delete station
            deleted = client.stations.delete(
                str(created_station.id), str(created_campaign.id)
            )
            assert deleted is True
            print(f"Deleted station: {created_station.id}")

            # Check that the station is deleted
            with pytest.raises(APIError):
                client.stations.get(str(created_station.id), str(created_campaign.id))

    finally:
        # Delete campaign
        deleted_campaign = client.campaigns.delete(str(created_campaign.id))
        assert deleted_campaign is True
        print(f"Deleted campaign: {created_campaign.id}")

        # Check that the campaign is deleted
        with pytest.raises(APIError):
            client.campaigns.get(str(created_campaign.id))
