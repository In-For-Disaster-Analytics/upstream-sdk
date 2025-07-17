"""
CKAN integration tests for Upstream SDK.
"""

import os
import tempfile
from datetime import datetime
from pathlib import Path

import pytest
from upstream_api_client import GetCampaignResponse, SummaryGetCampaign

from upstream.ckan import CKANIntegration
from upstream.exceptions import APIError

# Test configuration - these should be set in environment for real CKAN testing
CKAN_URL = os.environ.get("CKAN_URL", "http://localhost:5000")
CKAN_API_KEY = os.environ.get("CKAN_API_KEY")
CKAN_ORGANIZATION = os.environ.get("CKAN_ORGANIZATION", "test-organization")

pytestmark = pytest.mark.integration


@pytest.fixture
def ckan_config():
    """CKAN configuration for testing."""
    config = {"timeout": 30, "ckan_organization": CKAN_ORGANIZATION}
    if CKAN_API_KEY:
        config["api_key"] = CKAN_API_KEY
    return config


@pytest.fixture
def ckan_client(ckan_config):
    """CKAN client for testing."""
    return CKANIntegration(ckan_url=CKAN_URL, config=ckan_config)


@pytest.fixture
def sample_dataset_data():
    """Sample dataset data for testing."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "name": f"test-dataset-{timestamp}",
        "title": f"Test Dataset {timestamp}",
        "description": "Integration test dataset",
        "tags": ["test", "integration", "upstream"],
    }


@pytest.fixture
def sample_campaign_response():
    """Sample campaign response for testing."""
    # Use unique ID based on timestamp to avoid conflicts
    unique_id = int(datetime.now().timestamp() * 1000) % 1000000
    return GetCampaignResponse(
        id=unique_id,
        name="Test Campaign",
        description="A test campaign for CKAN integration",
        contact_name="Test Contact",
        contact_email="test@example.com",
        allocation="TACC",
        start_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        end_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        summary=SummaryGetCampaign(
            station_count=2,
            sensor_count=5,
            sensor_types=["temperature", "humidity", "pressure"],
            sensor_variables=["temperature", "humidity", "pressure"],
        ),
    )


@pytest.fixture
def temp_sensor_csv():
    """Create a temporary sensor CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("alias,variablename,units\n")
        f.write("temp_01,Air Temperature,°C\n")
        f.write("humidity_01,Relative Humidity,%\n")
        temp_path = f.name

    yield Path(temp_path)
    Path(temp_path).unlink()


@pytest.fixture
def temp_measurement_csv():
    """Create a temporary measurement CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("collectiontime,Lat_deg,Lon_deg,temp_01,humidity_01\n")
        f.write("2024-01-01T10:00:00Z,30.2672,-97.7431,25.5,65.2\n")
        f.write("2024-01-01T10:01:00Z,30.2672,-97.7431,25.7,64.8\n")
        temp_path = f.name

    yield Path(temp_path)
    Path(temp_path).unlink()


@pytest.mark.skipif(
    not CKAN_API_KEY,
    reason="CKAN_API_KEY must be set in environment for CKAN integration tests",
)
class TestCKANDatasetOperations:
    """Test CKAN dataset operations."""

    def test_dataset_lifecycle(self, ckan_client: CKANIntegration, sample_dataset_data):
        """Test complete dataset lifecycle: create, get, update, delete."""
        dataset_name = sample_dataset_data["name"]

        try:
            # Create dataset
            created_dataset = ckan_client.create_dataset(**sample_dataset_data)
            assert created_dataset["name"] == dataset_name
            assert created_dataset["title"] == sample_dataset_data["title"]
            assert created_dataset["notes"] == sample_dataset_data["description"]
            assert len(created_dataset["tags"]) == len(sample_dataset_data["tags"])

            # Get dataset
            retrieved_dataset = ckan_client.get_dataset(dataset_name)
            assert retrieved_dataset["name"] == dataset_name
            assert retrieved_dataset["id"] == created_dataset["id"]

            # Update dataset
            updated_title = "Updated Test Dataset"
            updated_dataset = ckan_client.update_dataset(
                dataset_name, title=updated_title
            )
            assert updated_dataset["title"] == updated_title

            # Verify update
            retrieved_updated = ckan_client.get_dataset(dataset_name)
            assert retrieved_updated["title"] == updated_title

        finally:
            # Clean up - delete dataset
            try:
                result = ckan_client.delete_dataset(dataset_name)
                assert result is True
            except APIError:
                pass  # Dataset might not exist or already deleted

    def test_get_nonexistent_dataset(self, ckan_client):
        """Test getting a dataset that doesn't exist."""
        with pytest.raises(APIError, match="not found"):
            ckan_client.get_dataset("nonexistent-dataset-12345")

    def test_create_dataset_minimal(self, ckan_client):
        """Test creating a dataset with minimal required fields."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        dataset_name = f"minimal-test-{timestamp}"

        try:
            dataset = ckan_client.create_dataset(
                name=dataset_name, title="Minimal Test Dataset"
            )
            assert dataset["name"] == dataset_name
            assert dataset["title"] == "Minimal Test Dataset"

        finally:
            try:
                ckan_client.delete_dataset(dataset_name)
            except APIError:
                pass


@pytest.mark.skipif(
    not CKAN_API_KEY,
    reason="CKAN_API_KEY must be set in environment for CKAN integration tests",
)
class TestCKANResourceOperations:
    """Test CKAN resource operations."""

    def test_create_file_resource(
        self, ckan_client, sample_dataset_data, temp_sensor_csv
    ):
        """Test creating a resource with file upload."""
        dataset_name = sample_dataset_data["name"]

        try:
            # Create dataset first
            dataset = ckan_client.create_dataset(**sample_dataset_data)

            # Create resource with file upload
            resource = ckan_client.create_resource(
                dataset_id=dataset["id"],
                name="Test Sensor Data",
                file_path=temp_sensor_csv,
                format="CSV",
                description="Test sensor configuration data",
            )

            assert resource["name"] == "Test Sensor Data"
            assert resource["format"] == "CSV"
            assert resource["description"] == "Test sensor configuration data"
            assert resource["package_id"] == dataset["id"]

        finally:
            try:
                ckan_client.delete_dataset(dataset_name)
            except APIError:
                pass

    def test_create_url_resource(self, ckan_client, sample_dataset_data):
        """Test creating a resource with URL."""
        dataset_name = sample_dataset_data["name"]

        try:
            # Create dataset first
            dataset = ckan_client.create_dataset(**sample_dataset_data)

            # Create resource with URL
            resource = ckan_client.create_resource(
                dataset_id=dataset["id"],
                name="Test Data URL",
                url="https://example.com/data2.csv",
                format="CSV",
                description="Test data from external URL",
            )

            assert resource["name"] == "Test Data URL"
            assert resource["url"] == "https://example.com/data2.csv"
            assert resource["format"] == "CSV"

        finally:
            try:
                ckan_client.delete_dataset(dataset_name)
            except APIError:
                pass

    def test_create_resource_missing_file(self, ckan_client, sample_dataset_data):
        """Test creating a resource with missing file."""
        dataset_name = sample_dataset_data["name"]

        try:
            dataset = ckan_client.create_dataset(**sample_dataset_data)

            with pytest.raises(APIError, match="File not found"):
                ckan_client.create_resource(
                    dataset_id=dataset["id"],
                    name="Missing File",
                    file_path="/nonexistent/file.csv",
                )

        finally:
            try:
                ckan_client.delete_dataset(dataset_name)
            except APIError:
                pass


@pytest.mark.skipif(
    not CKAN_API_KEY,
    reason="CKAN_API_KEY must be set in environment for CKAN integration tests",
)
class TestCKANCampaignPublishing:
    """Test CKAN campaign publishing functionality."""

    def test_publish_campaign_with_files(
        self,
        ckan_client,
        sample_campaign_response,
        temp_sensor_csv,
        temp_measurement_csv,
    ):
        """Test publishing campaign data with file uploads."""
        campaign_id = sample_campaign_response.id
        dataset_name = f"upstream-campaign-{campaign_id}"

        try:
            result = ckan_client.publish_campaign(
                campaign_id=campaign_id,
                campaign_data=sample_campaign_response,
                sensor_csv=str(temp_sensor_csv),
                measurement_csv=str(temp_measurement_csv),
                auto_publish=False,
            )

            assert result["success"] is True
            assert "dataset" in result
            assert "resources" in result
            assert "ckan_url" in result
            assert len(result["resources"]) == 2  # sensors + measurements

            # Verify dataset was created
            dataset = result["dataset"]
            assert dataset["name"] == dataset_name
            assert dataset["title"] == sample_campaign_response.name
            assert "environmental" in [tag["name"] for tag in dataset["tags"]]

            # Verify resources were created
            resources = result["resources"]
            resource_names = [r["name"] for r in resources]
            assert "Sensors Configuration" in resource_names
            assert "Measurement Data" in resource_names

        finally:
            try:
                ckan_client.delete_dataset(dataset_name)
            except APIError:
                pass

    def test_publish_campaign_with_urls(self, ckan_client, sample_campaign_response):
        """Test publishing campaign data with URLs."""
        campaign_id = sample_campaign_response.id
        dataset_name = f"upstream-campaign-{campaign_id}"

        try:
            result = ckan_client.publish_campaign(
                campaign_id=campaign_id,
                campaign_data=sample_campaign_response,
                sensors_url="https://example.com/sensors.csv",
                measurements_url="https://example.com/measurements.csv",
                auto_publish=False,
            )

            assert result["success"] is True
            assert len(result["resources"]) == 2

            # Verify resources have URLs
            resources = result["resources"]
            sensor_resource = next(r for r in resources if "Sensors" in r["name"])
            measurement_resource = next(
                r for r in resources if "Measurement" in r["name"]
            )

            assert sensor_resource["url"] == "https://example.com/sensors.csv"
            assert measurement_resource["url"] == "https://example.com/measurements.csv"

        finally:
            try:
                ckan_client.delete_dataset(dataset_name)
            except APIError:
                pass

    def test_publish_campaign_update_existing(
        self, ckan_client: CKANIntegration, sample_campaign_response, temp_sensor_csv
    ):
        """Test updating an existing campaign dataset."""
        campaign_id = sample_campaign_response.id
        dataset_name = f"upstream-campaign-{campaign_id}"

        try:
            # Create initial publication
            result1 = ckan_client.publish_campaign(
                campaign_id=campaign_id,
                campaign_data=sample_campaign_response,
                sensor_csv=str(temp_sensor_csv),
                auto_publish=False,
            )

            initial_dataset_id = result1["dataset"]["id"]

            # Update with different data
            updated_campaign = sample_campaign_response
            updated_campaign.description = "Updated campaign description"

            result2 = ckan_client.publish_campaign(
                campaign_id=campaign_id,
                campaign_data=updated_campaign,
                auto_publish=False,
            )

            # Should update the same dataset
            assert result2["dataset"]["id"] == initial_dataset_id
            assert result2["dataset"]["notes"] == "Updated campaign description"

        finally:
            try:
                ckan_client.delete_dataset(dataset_name)
            except APIError:
                pass


@pytest.mark.skipif(
    not CKAN_API_KEY,
    reason="CKAN_API_KEY must be set in environment for CKAN integration tests",
)
class TestCKANListOperations:
    """Test CKAN list operations."""

    def test_list_datasets(self, ckan_client):
        """Test listing datasets."""
        datasets = ckan_client.list_datasets(limit=10)
        assert isinstance(datasets, list)
        if datasets:
            dataset = datasets[0]
            assert "name" in dataset
            assert "title" in dataset

    def test_list_datasets_with_filters(self, ckan_client):
        """Test listing datasets with filters."""
        datasets = ckan_client.list_datasets(tags=["test"], limit=5)
        assert isinstance(datasets, list)

    def test_list_organizations(self, ckan_client):
        """Test listing organizations."""
        try:
            organizations = ckan_client.list_organizations()
            assert isinstance(organizations, list)
        except APIError:
            # Some CKAN instances might not allow listing organizations
            pytest.skip("Organization listing not allowed on this CKAN instance")


@pytest.mark.skipif(
    not CKAN_API_KEY,
    reason="CKAN_API_KEY must be set in environment for CKAN integration tests",
)
class TestCKANUtilities:
    """Test CKAN utility functions."""

    def test_sanitize_title(self, ckan_client):
        """Test title sanitization."""
        assert ckan_client.sanitize_title("Test Dataset") == "Test_Dataset"
        assert ckan_client.sanitize_title("Test-Dataset-Name") == "Test_Dataset_Name"
        assert (
            ckan_client.sanitize_title("Multiple Word Dataset Name")
            == "Multiple_Word_Dataset_Name"
        )


# Unit tests that don't require a real CKAN instance
class TestCKANUnitTests:
    """Unit tests for CKAN functionality."""

    def test_ckan_initialization(self):
        """Test CKAN client initialization."""
        client = CKANIntegration("http://test.example.com")
        assert client.ckan_url == "http://test.example.com"
        assert client.config == {}

        # Test with trailing slash removal
        client2 = CKANIntegration("http://test.example.com/")
        assert client2.ckan_url == "http://test.example.com"

    def test_ckan_initialization_with_config(self):
        """Test CKAN client initialization with configuration."""
        config = {"api_key": "test-key", "timeout": 60}
        client = CKANIntegration("http://test.example.com", config=config)

        assert client.config == config
        assert client.session.timeout == 60
        assert "Authorization" in client.session.headers

    def test_sanitize_title_edge_cases(self):
        """Test title sanitization edge cases."""
        client = CKANIntegration("http://test.example.com")

        assert client.sanitize_title("") == ""
        assert client.sanitize_title("NoSpaces") == "NoSpaces"
        assert client.sanitize_title("___") == "___"
        assert client.sanitize_title("Mix_of-Both Spaces") == "Mix_of_Both_Spaces"