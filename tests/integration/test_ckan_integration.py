"""
CKAN integration tests for Upstream SDK.
"""

import io
import os
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from upstream_api_client import GetCampaignResponse, SummaryGetCampaign, GetStationResponse

from upstream.ckan import CKANIntegration
from upstream.client import UpstreamClient
from upstream.exceptions import APIError, ConfigurationError

# Test configuration - these should be set in environment for real CKAN testing
CKAN_URL = os.environ.get("CKAN_URL", "http://localhost:5000")
CKAN_API_KEY = os.environ.get("CKAN_API_KEY")
CKAN_ORGANIZATION = os.environ.get("CKAN_ORGANIZATION", "test-organization")
UPSTREAM_BASE_URL = os.environ.get("UPSTREAM_BASE_URL", "http://localhost:8000")
UPSTREAM_USERNAME = os.environ.get("UPSTREAM_USERNAME", "test")
UPSTREAM_PASSWORD = os.environ.get("UPSTREAM_PASSWORD", "test")

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
def mock_station_data():
    """Sample station data for testing."""
    return GetStationResponse(
        id=123,
        name="Test Station",
        description="A test station for CKAN integration",
        contact_name="Station Contact",
        contact_email="station@example.com",
        active=True,
        start_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        geometry={"type": "Point", "coordinates": [-97.7431, 30.2672]},
        sensors=[]
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

    def test_publish_campaign_with_streams(
        self,
        ckan_client: CKANIntegration,
        sample_campaign_response,
        mock_station_sensors_csv,
        mock_station_measurements_csv,
        mock_station_data,
    ):
        """Test publishing campaign data with stream uploads."""
        campaign_id = sample_campaign_response.id
        dataset_name = f"upstream-campaign-{campaign_id}"
        dataset_title = f"Test Campaign {campaign_id}"

        try:
            result = ckan_client.publish_campaign(
                campaign_id=campaign_id,
                campaign_data=sample_campaign_response,
                station_measurements=mock_station_measurements_csv,
                station_sensors=mock_station_sensors_csv,
                station_data=mock_station_data,
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
            assert dataset_title.startswith(dataset["title"])
            assert "environmental" in [tag["name"] for tag in dataset["tags"]]

            # Verify resources were created
            resources = result["resources"]
            resource_names = [r["name"] for r in resources]
            assert len(resources) == 2
            assert any("Test Station - Sensors Configuration" in name for name in resource_names)
            assert any("Test Station - Measurement Data" in name for name in resource_names)

            # Verify resource metadata
            for resource in resources:
                assert resource["format"] == "CSV"
                if "Sensors Configuration" in resource["name"]:
                    assert resource["description"] == "Sensor configuration and metadata"
                elif "Measurement Data" in resource["name"]:
                    assert resource["description"] == "Environmental sensor measurements"

            # Verify campaign metadata is stored in dataset extras
            dataset_extras = {extra["key"]: extra["value"] for extra in dataset.get("extras", [])}
            assert "campaign_id" in dataset_extras
            assert dataset_extras["campaign_id"] == str(campaign_id)
            assert "campaign_name" in dataset_extras
            assert dataset_extras["campaign_name"] == sample_campaign_response.name
            assert "campaign_contact_name" in dataset_extras
            assert dataset_extras["campaign_contact_name"] == sample_campaign_response.contact_name
            assert "campaign_contact_email" in dataset_extras
            assert dataset_extras["campaign_contact_email"] == sample_campaign_response.contact_email
            assert "campaign_allocation" in dataset_extras
            assert dataset_extras["campaign_allocation"] == sample_campaign_response.allocation
            assert "source" in dataset_extras
            assert dataset_extras["source"] == "Upstream Platform"
            assert "data_type" in dataset_extras
            assert dataset_extras["data_type"] == "environmental_sensor_data"

            # Verify station metadata is stored as direct resource fields
            for resource in resources:
                assert "station_id" in resource
                assert resource["station_id"] == str(mock_station_data.id)
                assert "station_name" in resource
                assert resource["station_name"] == mock_station_data.name
                assert "station_description" in resource
                assert resource["station_description"] == mock_station_data.description
                assert "station_contact_name" in resource
                assert resource["station_contact_name"] == mock_station_data.contact_name
                assert "station_contact_email" in resource
                assert resource["station_contact_email"] == mock_station_data.contact_email
                assert "station_active" in resource
                assert resource["station_active"] == str(mock_station_data.active)
                assert "station_geometry" in resource
                assert "station_sensors_count" in resource
                assert resource["station_sensors_count"] == str(len(mock_station_data.sensors))

        finally:
            try:
                ckan_client.delete_dataset(dataset_name)
            except APIError:
                pass

    def test_publish_campaign_update_existing(
        self, ckan_client: CKANIntegration, sample_campaign_response,
        mock_station_sensors_csv, mock_station_measurements_csv, mock_station_data
    ):
        """Test updating an existing campaign dataset."""
        campaign_id = sample_campaign_response.id
        dataset_name = f"upstream-campaign-{campaign_id}"

        try:
            # Create initial publication
            result1 = ckan_client.publish_campaign(
                campaign_id=campaign_id,
                campaign_data=sample_campaign_response,
                station_measurements=mock_station_measurements_csv,
                station_sensors=mock_station_sensors_csv,
                station_data=mock_station_data,
            )

            initial_dataset_id = result1["dataset"]["id"]

            # Create fresh streams for the update call
            sensors_data = "alias,variablename,units\ntemp_02,Air Temperature 2,°C\n"
            sensors_csv = io.BytesIO(sensors_data.encode('utf-8'))
            measurements_data = "collectiontime,Lat_deg,Lon_deg,temp_02\n2024-01-01T11:00:00Z,30.2672,-97.7431,26.0\n"
            measurements_csv = io.BytesIO(measurements_data.encode('utf-8'))

            # Update with different data
            updated_campaign = sample_campaign_response
            updated_campaign.description = "Updated campaign description"

            result2 = ckan_client.publish_campaign(
                campaign_id=campaign_id,
                campaign_data=updated_campaign,
                station_measurements=measurements_csv,
                station_sensors=sensors_csv,
                station_data=mock_station_data,
            )

            # Should update the same dataset
            assert result2["dataset"]["id"] == initial_dataset_id
            assert result2["dataset"]["notes"] == "Updated campaign description"

        finally:
            try:
                print(f"Deleting dataset: {dataset_name}")
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


@pytest.fixture
def mock_station_sensors_csv():
    """Mock station sensors CSV data as a stream."""
    csv_data = "alias,variablename,units\ntemp_01,Air Temperature,°C\nhumidity_01,Relative Humidity,%\n"
    return io.BytesIO(csv_data.encode('utf-8'))


@pytest.fixture
def mock_station_measurements_csv():
    """Mock station measurements CSV data as a stream."""
    csv_data = "collectiontime,Lat_deg,Lon_deg,temp_01,humidity_01\n2024-01-01T10:00:00Z,30.2672,-97.7431,25.5,65.2\n"
    return io.BytesIO(csv_data.encode('utf-8'))


class TestUpstreamClientCKANIntegration:
    """Test UpstreamClient publish_to_ckan functionality."""

    @pytest.fixture
    def mock_upstream_client(self):
        """Mock UpstreamClient with CKAN integration."""
        with patch('upstream.client.UpstreamClient') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # Mock CKAN integration
            mock_ckan = MagicMock()
            mock_client.ckan = mock_ckan

            # Mock station manager with export methods
            mock_stations = MagicMock()
            mock_client.stations = mock_stations

            yield mock_client

    def test_publish_to_ckan_with_station_streams(
        self, mock_station_sensors_csv, mock_station_measurements_csv
    ):
        """Test publish_to_ckan with station_id parameter and streaming data."""
        # Create a mock client and mock its dependencies
        mock_client = MagicMock()

        # Setup mock return values
        mock_client.stations.export_station_measurements.return_value = (
            mock_station_measurements_csv
        )
        mock_client.stations.export_station_sensors.return_value = (
            mock_station_sensors_csv
        )
        mock_client.campaigns.get.return_value = MagicMock()  # Mock campaign data
        mock_client.ckan = MagicMock()  # Mock CKAN integration

        expected_result = {
            "success": True,
            "dataset": {"id": "test-dataset", "name": "test-campaign"},
            "resources": [{"id": "resource1"}, {"id": "resource2"}]
        }
        mock_client.ckan.publish_campaign.return_value = expected_result

        # Import and call the real publish_to_ckan method
        from upstream.client import UpstreamClient

        # Call the method on the mock client
        result = UpstreamClient.publish_to_ckan(mock_client, campaign_id="123", station_id="456")

        # Verify station export methods were called
        mock_client.stations.export_station_measurements.assert_called_once_with(
            station_id="456", campaign_id="123"
        )
        mock_client.stations.export_station_sensors.assert_called_once_with(
            station_id="456", campaign_id="123"
        )
        mock_client.campaigns.get.assert_called_once_with(campaign_id="123")

        # Verify CKAN publish_campaign was called with streams
        mock_client.ckan.publish_campaign.assert_called_once()
        call_args = mock_client.ckan.publish_campaign.call_args

        assert call_args[1]['campaign_id'] == "123"
        assert 'station_measurements' in call_args[1]
        assert 'station_sensors' in call_args[1]
        assert 'campaign_data' in call_args[1]

        # Verify the result
        assert result == expected_result

    def test_publish_to_ckan_without_ckan_integration(self):
        """Test error when CKAN integration is not configured."""
        # Create mock client with no CKAN integration
        mock_client = MagicMock()
        mock_client.ckan = None  # No CKAN integration

        from upstream.client import UpstreamClient

        with pytest.raises(ConfigurationError, match="CKAN integration not configured"):
            UpstreamClient.publish_to_ckan(mock_client, campaign_id="123", station_id="456")

    def test_publish_to_ckan_station_export_error(self):
        """Test error handling when station export fails."""
        # Create mock client
        mock_client = MagicMock()

        # Set up the side_effect to raise an exception when export_station_measurements is called
        mock_client.stations.export_station_measurements.side_effect = APIError("Station export failed")
        mock_client.ckan = MagicMock()  # Has CKAN integration

        # Ensure ckan is truthy to pass the None check
        type(mock_client).ckan = MagicMock()

        from upstream.client import UpstreamClient

        with pytest.raises(APIError, match="Station export failed"):
            UpstreamClient.publish_to_ckan(mock_client, campaign_id="123", station_id="456")

    def test_publish_to_ckan_streams_contain_data(
        self, mock_station_sensors_csv, mock_station_measurements_csv
    ):
        """Test that station streams contain expected data format."""
        # Create mock client
        mock_client = MagicMock()
        mock_client.stations.export_station_measurements.return_value = (
            mock_station_measurements_csv
        )
        mock_client.stations.export_station_sensors.return_value = (
            mock_station_sensors_csv
        )
        mock_client.campaigns.get.return_value = MagicMock()
        mock_client.ckan = MagicMock()
        mock_client.ckan.publish_campaign.return_value = {"success": True}

        from upstream.client import UpstreamClient

        # Test the method
        UpstreamClient.publish_to_ckan(mock_client, campaign_id="123", station_id="456")

        # Verify CKAN was called with streams
        call_args = mock_client.ckan.publish_campaign.call_args[1]

        # Check that streams are BinaryIO objects
        station_measurements = call_args['station_measurements']
        station_sensors = call_args['station_sensors']

        # Reset stream positions to read content
        station_measurements.seek(0)
        station_sensors.seek(0)

        measurements_content = station_measurements.read().decode('utf-8')
        sensors_content = station_sensors.read().decode('utf-8')

        # Verify CSV content structure
        assert "collectiontime" in measurements_content
        assert "temp_01" in measurements_content
        assert "alias" in sensors_content
        assert "variablename" in sensors_content
