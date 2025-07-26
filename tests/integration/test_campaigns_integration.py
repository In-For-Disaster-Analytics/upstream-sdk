import os
from datetime import datetime, timedelta

import pytest
from upstream_api_client.models import CampaignsIn, CampaignUpdate

from upstream.client import UpstreamClient
from upstream.exceptions import APIError
from upstream.ckan import CKANIntegration

BASE_URL = os.environ.get("UPSTREAM_BASE_URL", "http://localhost:8000")
CKAN_URL = os.environ.get("CKAN_URL", "http://ckan.tacc.cloud:5000")

USERNAME = os.environ.get("UPSTREAM_USERNAME")
PASSWORD = os.environ.get("UPSTREAM_PASSWORD")
CKAN_API_KEY = os.environ.get("CKAN_API_KEY", "")
ORGANIZATION = os.environ.get("CKAN_ORGANIZATION", "")

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    not USERNAME or not PASSWORD,
    reason="UPSTREAM_USERNAME and UPSTREAM_PASSWORD must be set in env",
)
def test_campaign_lifecycle():
    client = UpstreamClient(
        username=USERNAME, password=PASSWORD, base_url=BASE_URL, ckan_url=CKAN_URL
    )

    # Unique campaign name
    campaign_name = (
        f"integration-test-campaign-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
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
        end_date=end_date,
    )

    # Create
    created = client.campaigns.create(campaign_in)
    assert created.id is not None
    print(f"Created campaign: {created.id}")

    try:
        # Get
        fetched = client.campaigns.get(created.id)
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
        client.campaigns.update(created.id, update)

        # Fetch again
        fetched_again = client.campaigns.get(created.id)
        assert fetched_again.description == "Updated integration test campaign"
        print(f"Updated campaign: {fetched_again.id}")

    finally:
        # Delete
        deleted = client.campaigns.delete(created.id)
        assert deleted is True
        print(f"Deleted campaign: {created.id}")

        # Check that the campaign is deleted
        with pytest.raises(APIError):
            client.campaigns.get(created.id)


@pytest.mark.skipif(
    not USERNAME or not PASSWORD,
    reason="UPSTREAM_USERNAME and UPSTREAM_PASSWORD must be set in env",
)
def test_ckan_dataset_update_integration():
    """
    Integration test for updating CKAN dataset with custom metadata and tags.

    This test verifies the enhanced update_dataset functionality by:
    1. Creating an initial dataset with tags and metadata
    2. Updating the dataset using merge mode (preserving existing data)
    3. Verifying all changes using get_dataset()
    4. Testing replace mode (replacing all existing data)
    5. Verifying replace mode behavior
    6. Cleaning up the test dataset

    Tests both merge and replace modes for tags and metadata to ensure
    the update_dataset method works correctly in real CKAN environments.

    Requires:
        - UPSTREAM_USERNAME and UPSTREAM_PASSWORD environment variables
        - Running CKAN instance at CKAN_URL
        - Valid CKAN API credentials
    """
    client = UpstreamClient(
        username=USERNAME, password=PASSWORD, base_url=BASE_URL, ckan_url=CKAN_URL
    )
    ckan_config = {"timeout": 30}
    if not CKAN_API_KEY:
        pytest.skip("CKAN API key not set (required for dataset creation)")

    if not ORGANIZATION:
        pytest.skip("CKAN organization not set (required for dataset creation)")

    ckan_config["api_key"] = CKAN_API_KEY
    client.ckan = CKANIntegration(ckan_url=CKAN_URL, config=ckan_config)

    if not client.ckan:
        pytest.skip("CKAN integration not available")

    # Create a unique test dataset name
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    dataset_name = f"test-dataset-update-{timestamp}"

    print(f"Testing CKAN dataset update integration with: {dataset_name}")

    # Step 1: Create initial dataset with organization
    initial_dataset = client.ckan.create_dataset(
        name=dataset_name,
        title="Initial Test Dataset",
        description="This is a test dataset for update integration testing",
        organization=ORGANIZATION,
        tags=["test", "initial"],
        extras=[
            {"key": "test_phase", "value": "initial"},
            {"key": "created_by", "value": "integration_test"}
        ]
    )

    print(f"✅ Created initial dataset: {initial_dataset['name']}")

    try:
        # Step 2: Verify initial state
        fetched_initial = client.ckan.get_dataset(dataset_name)
        initial_tags = [tag["name"] for tag in fetched_initial["tags"]]
        initial_extras = {extra["key"]: extra["value"] for extra in fetched_initial.get("extras", [])}

        assert "test" in initial_tags
        assert "initial" in initial_tags
        assert initial_extras["test_phase"] == "initial"
        assert initial_extras["created_by"] == "integration_test"
        print(f"✅ Verified initial dataset state")

        # Step 3: Update dataset - Add new tag and metadata
        print("🔄 Updating dataset with new tag and metadata...")

        updated_dataset = client.ckan.update_dataset(
            dataset_name,
            # Add new custom metadata
            dataset_metadata={
                "test_phase": "updated",  # Update existing field
                "update_timestamp": datetime.now().isoformat(),  # Add new field
                "integration_status": "passed"  # Add another new field
            },
            # Add new custom tags
            custom_tags=["updated", "integration-test"],
            # Use merge mode to preserve existing data
            merge_extras=True,
            merge_tags=True,
            # Also update the title
            title="Updated Test Dataset"
        )

        print(f"✅ Updated dataset: {updated_dataset['name']}")

        # Step 4: Verify updates using get_dataset
        print("🔍 Verifying updates...")

        verified_dataset = client.ckan.get_dataset(dataset_name)

        # Verify title update
        assert verified_dataset["title"] == "Updated Test Dataset"
        print("  ✓ Title updated successfully")

        # Verify tags (should include both old and new)
        updated_tags = [tag["name"] for tag in verified_dataset["tags"]]
        expected_tags = ["test", "initial", "updated", "integration-test"]

        for tag in expected_tags:
            assert tag in updated_tags, f"Expected tag '{tag}' not found in {updated_tags}"

        # Also verify we have the right number of tags (no extras)
        assert len(updated_tags) == len(expected_tags), f"Expected {len(expected_tags)} tags, got {len(updated_tags)}: {updated_tags}"
        print(f"  ✓ Tags updated successfully: {sorted(updated_tags)}")

        # Verify metadata/extras (should include both old and new)
        updated_extras = {extra["key"]: extra["value"] for extra in verified_dataset.get("extras", [])}

        # Check preserved fields
        assert updated_extras["created_by"] == "integration_test"
        print("  ✓ Original metadata preserved")

        # Check updated fields
        assert updated_extras["test_phase"] == "updated"
        print("  ✓ Existing metadata updated")

        # Check new fields
        assert "update_timestamp" in updated_extras
        assert updated_extras["integration_status"] == "passed"
        print("  ✓ New metadata added")

        print(f"✅ All updates verified successfully!")

        # Step 5: Test replace mode
        print("🔄 Testing replace mode...")

        client.ckan.update_dataset(
            dataset_name,
            dataset_metadata={
                "final_phase": "replace_test",
                "mode": "replace"
            },
            custom_tags=["replaced", "final"],
            merge_extras=False,  # Replace all extras
            merge_tags=False,    # Replace all tags
            title="Replaced Test Dataset"
        )

        # Verify replace mode
        verified_replace = client.ckan.get_dataset(dataset_name)

        # Check that old tags are gone and only new ones remain
        final_tags = [tag["name"] for tag in verified_replace["tags"]]
        expected_final_tags = ["replaced", "final"]
        assert set(final_tags) == set(expected_final_tags), f"Expected {expected_final_tags}, got {final_tags}"
        assert len(final_tags) == len(expected_final_tags), f"Expected {len(expected_final_tags)} tags, got {len(final_tags)}"
        print("  ✓ Tags replaced successfully")

        # Check that old extras are gone and only new ones remain
        final_extras = {extra["key"]: extra["value"] for extra in verified_replace.get("extras", [])}
        assert "created_by" not in final_extras  # Should be gone
        assert "test_phase" not in final_extras  # Should be gone
        assert final_extras["final_phase"] == "replace_test"
        assert final_extras["mode"] == "replace"
        print("  ✓ Metadata replaced successfully")

        print("✅ Replace mode test passed!")

    finally:
        # Cleanup: Delete the test dataset
        try:
            client.ckan.delete_dataset(dataset_name)
            print(f"🧹 Cleaned up test dataset: {dataset_name}")
        except Exception as e:
            print(f"⚠️  Warning: Could not delete test dataset {dataset_name}: {e}")

    print("🎉 CKAN dataset update integration test completed successfully!")
