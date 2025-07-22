"""
Unit tests for CKAN integration module.
"""

import io
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

import pytest
import requests
from upstream_api_client import GetCampaignResponse, SummaryGetCampaign, GetStationResponse

from upstream.ckan import CKANIntegration
from upstream.exceptions import APIError

pytestmark = pytest.mark.unit


@pytest.fixture
def mock_ckan_response():
    """Mock CKAN API response."""
    response = Mock()
    response.status_code = 200
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "success": True,
        "result": {
            "id": "test-dataset-id",
            "name": "test-dataset",
            "title": "Test Dataset",
            "notes": "Test description",
            "tags": [{"name": "test"}, {"name": "integration"}],
        },
    }
    return response


@pytest.fixture
def mock_ckan_error_response():
    """Mock CKAN API error response."""
    response = Mock()
    response.status_code = 400
    response.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request")
    response.json.return_value = {
        "success": False,
        "error": {"message": "Validation Error", "name": ["Missing value"]},
    }
    return response

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


@pytest.fixture
def sample_campaign_response():
    """Sample campaign response for testing."""
    return GetCampaignResponse(
        id=100,
        name="Test Campaign",
        description="A test campaign",
        contact_name="Test Contact",
        contact_email="test@example.com",
        allocation="TACC",
        start_date="2024-01-01T00:00:00Z",
        end_date="2024-12-31T23:59:59Z",
        summary=SummaryGetCampaign(
            station_count=2,
            sensor_count=5,
            sensor_types=["temperature", "humidity"],
            sensor_variables=["temperature", "humidity"],
        ),
    )


@pytest.fixture  
def mock_station_data():
    """Sample station data for testing."""
    return GetStationResponse(
        id=123,
        name="Test Station", 
        description="A test station",
        contact_name="Station Contact",
        contact_email="station@example.com",
        active=True,
        start_date="2024-01-01T00:00:00Z",
        geometry={"type": "Point", "coordinates": [-97.7431, 30.2672]},
        sensors=[]
    )


class TestCKANIntegrationInit:
    """Test CKAN integration initialization."""

    def test_init_basic(self):
        """Test basic initialization."""
        ckan = CKANIntegration("http://test.example.com")
        assert ckan.ckan_url == "http://test.example.com"
        assert ckan.config == {}
        assert ckan.session.timeout == 30

    def test_init_with_trailing_slash(self):
        """Test initialization with trailing slash removal."""
        ckan = CKANIntegration("http://test.example.com/")
        assert ckan.ckan_url == "http://test.example.com"

    def test_init_with_config(self):
        """Test initialization with configuration."""
        config = {"api_key": "test-key", "timeout": 60}
        ckan = CKANIntegration("http://test.example.com", config=config)

        assert ckan.config == config
        assert ckan.session.timeout == 60
        assert "Authorization" in ckan.session.headers
        assert ckan.session.headers["Authorization"] == "test-key"

    def test_init_with_access_token(self):
        """Test initialization with access token."""
        config = {"access_token": "test-token"}
        ckan = CKANIntegration("http://test.example.com", config=config)

        assert "Authorization" in ckan.session.headers
        assert ckan.session.headers["Authorization"] == "test-token"


class TestCKANDatasetOperations:
    """Test CKAN dataset operations."""

    @patch("upstream.ckan.requests.Session.post")
    def test_create_dataset_success(self, mock_post, mock_ckan_response):
        """Test successful dataset creation."""
        mock_post.return_value = mock_ckan_response
        ckan = CKANIntegration("http://test.example.com")

        result = ckan.create_dataset(
            name="test-dataset", title="Test Dataset", description="Test description"
        )

        assert result["name"] == "test-dataset"
        assert result["title"] == "Test Dataset"
        mock_post.assert_called_once()

    @patch("upstream.ckan.requests.Session.post")
    def test_create_dataset_with_organization(self, mock_post, mock_ckan_response):
        """Test dataset creation with organization."""
        mock_post.return_value = mock_ckan_response
        ckan = CKANIntegration("http://test.example.com")

        result = ckan.create_dataset(
            name="test-dataset",
            title="Test Dataset",
            organization="test-org",
            tags=["test", "data"],
        )

        # Check that the call was made with the right data
        call_args = mock_post.call_args
        data = call_args[1]["json"]
        assert data["owner_org"] == "test-org"
        assert data["tags"] == [{"name": "test"}, {"name": "data"}]

    @patch("upstream.ckan.requests.Session.post")
    def test_create_dataset_failure(self, mock_post, mock_ckan_error_response):
        """Test dataset creation failure."""
        mock_post.return_value = mock_ckan_error_response
        ckan = CKANIntegration("http://test.example.com")

        with pytest.raises(APIError, match="Failed to create CKAN dataset"):
            ckan.create_dataset(name="test-dataset", title="Test Dataset")

    @patch("upstream.ckan.requests.Session.post")
    def test_create_dataset_api_error(self, mock_post):
        """Test dataset creation with API error response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": False,
            "error": {"message": "Validation failed"},
        }
        mock_post.return_value = mock_response

        ckan = CKANIntegration("http://test.example.com")

        with pytest.raises(APIError, match="CKAN dataset creation failed"):
            ckan.create_dataset(name="test-dataset", title="Test Dataset")

    @patch("upstream.ckan.requests.Session.get")
    def test_get_dataset_success(self, mock_get, mock_ckan_response):
        """Test successful dataset retrieval."""
        mock_get.return_value = mock_ckan_response
        ckan = CKANIntegration("http://test.example.com")

        result = ckan.get_dataset("test-dataset")

        assert result["name"] == "test-dataset"
        mock_get.assert_called_once()

    @patch("upstream.ckan.requests.Session.get")
    def test_get_dataset_not_found(self, mock_get):
        """Test dataset not found."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_response.response.status_code = 404
        mock_get.return_value = mock_response

        # Need to set the response attribute for the hasattr check
        error = requests.exceptions.HTTPError()
        error.response = mock_response
        mock_response.raise_for_status.side_effect = error

        ckan = CKANIntegration("http://test.example.com")

        with pytest.raises(APIError, match="CKAN dataset not found"):
            ckan.get_dataset("nonexistent-dataset")

    @patch("upstream.ckan.requests.Session.post")
    @patch("upstream.ckan.CKANIntegration.get_dataset")
    def test_update_dataset_success(self, mock_get, mock_post, mock_ckan_response):
        """Test successful dataset update."""
        # Mock getting current dataset
        mock_get.return_value = {
            "id": "test-id",
            "name": "test-dataset",
            "title": "Old Title",
        }

        # Mock update response
        updated_response = mock_ckan_response
        updated_response.json.return_value["result"]["title"] = "New Title"
        mock_post.return_value = updated_response

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.update_dataset("test-dataset", title="New Title")

        assert result["title"] == "New Title"
        mock_get.assert_called_once_with("test-dataset")
        mock_post.assert_called_once()

    @patch("upstream.ckan.requests.Session.post")
    def test_delete_dataset_success(self, mock_post):
        """Test successful dataset deletion."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.delete_dataset("test-dataset")

        assert result is True
        mock_post.assert_called_once()


class TestCKANResourceOperations:
    """Test CKAN resource operations."""

    @patch("upstream.ckan.requests.Session.post")
    def test_create_resource_with_url(self, mock_post):
        """Test creating a resource with URL."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": {
                "id": "resource-id",
                "name": "Test Resource",
                "url": "https://example.com/data.csv",
                "format": "CSV",
            },
        }
        mock_post.return_value = mock_response

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.create_resource(
            dataset_id="dataset-id",
            name="Test Resource",
            url="https://example.com/data.csv",
            format="CSV",
        )

        assert result["name"] == "Test Resource"
        assert result["url"] == "https://example.com/data.csv"
        mock_post.assert_called_once()

    @patch("upstream.ckan.requests.Session.post")
    @patch("builtins.open", new_callable=mock_open, read_data="test,data\n1,2\n")
    @patch("pathlib.Path.exists")
    def test_create_resource_with_file(self, mock_exists, mock_file, mock_post):
        """Test creating a resource with file upload."""
        mock_exists.return_value = True
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": {
                "id": "resource-id",
                "name": "Test Resource",
                "format": "CSV",
            },
        }
        mock_post.return_value = mock_response

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.create_resource(
            dataset_id="dataset-id",
            name="Test Resource",
            file_path="/path/to/test.csv",
            format="CSV",
        )

        assert result["name"] == "Test Resource"
        mock_post.assert_called_once()

    @patch("pathlib.Path.exists")
    def test_create_resource_file_not_found(self, mock_exists):
        """Test creating a resource with missing file."""
        mock_exists.return_value = False
        ckan = CKANIntegration("http://test.example.com")

        with pytest.raises(APIError, match="File not found"):
            ckan.create_resource(
                dataset_id="dataset-id",
                name="Test Resource",
                file_path="/nonexistent/file.csv",
            )

    def test_create_resource_no_source(self):
        """Test creating a resource with no URL or file."""
        ckan = CKANIntegration("http://test.example.com")

        with pytest.raises(APIError, match="Either url, file_path, or file_obj must be provided"):
            ckan.create_resource(dataset_id="dataset-id", name="Test Resource")

    @patch("upstream.ckan.requests.Session.post")
    def test_create_resource_with_file_obj(self, mock_post):
        """Test creating a resource with file object."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": {"id": "resource-id", "name": "Test Resource"},
        }
        mock_post.return_value = mock_response

        # Create a mock file object
        file_obj = Mock()
        file_obj.name = "test.csv"

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.create_resource(
            dataset_id="dataset-id", name="Test Resource", file_obj=file_obj
        )

        assert result["name"] == "Test Resource"
        mock_post.assert_called_once()


class TestCKANListOperations:
    """Test CKAN list operations."""

    @patch("upstream.ckan.requests.Session.get")
    def test_list_datasets(self, mock_get):
        """Test listing datasets."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": {
                "results": [
                    {"name": "dataset1", "title": "Dataset 1"},
                    {"name": "dataset2", "title": "Dataset 2"},
                ]
            },
        }
        mock_get.return_value = mock_response

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.list_datasets(limit=10)

        assert len(result) == 2
        assert result[0]["name"] == "dataset1"
        mock_get.assert_called_once()

    @patch("upstream.ckan.requests.Session.get")
    def test_list_datasets_with_filters(self, mock_get):
        """Test listing datasets with organization and tag filters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": {"results": []},
        }
        mock_get.return_value = mock_response

        ckan = CKANIntegration("http://test.example.com")

        ckan.list_datasets(organization="test-org", tags=["tag1", "tag2"])

        # Check that the query was properly constructed
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert 'owner_org:"test-org"' in params["q"]
        assert 'tags:"tag1"' in params["q"]
        assert 'tags:"tag2"' in params["q"]

    @patch("upstream.ckan.requests.Session.get")
    def test_list_organizations(self, mock_get):
        """Test listing organizations."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": [
                {"name": "org1", "title": "Organization 1"},
                {"name": "org2", "title": "Organization 2"},
            ],
        }
        mock_get.return_value = mock_response

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.list_organizations()

        assert len(result) == 2
        assert result[0]["name"] == "org1"
        mock_get.assert_called_once()


class TestCKANCampaignPublishing:
    """Test CKAN campaign publishing functionality."""

    @patch("upstream.ckan.CKANIntegration.create_resource")
    @patch("upstream.ckan.CKANIntegration.create_dataset")
    @patch("upstream.ckan.CKANIntegration.get_dataset")
    def test_publish_campaign_success(
        self, mock_get, mock_create, mock_create_resource, sample_campaign_response, mock_station_data
    ):
        """Test successful campaign publishing."""
        # Mock get_dataset to raise APIError (dataset doesn't exist)
        mock_get.side_effect = APIError("Dataset not found")

        # Mock create_dataset
        mock_create.return_value = {
            "id": "dataset-id",
            "name": "upstream-campaign-test-campaign-123",
            "title": "Test_Campaign",
        }

        # Mock create_resource
        mock_create_resource.return_value = {
            "id": "resource-id",
            "name": "Test Resource",
        }

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.publish_campaign(
            campaign_id="test-campaign-123",
            campaign_data=sample_campaign_response,
            station_measurements=mock_station_measurements_csv,
            station_sensors=mock_station_sensors_csv,
            station_data=mock_station_data
        )

        assert result["success"] is True
        assert "dataset" in result
        assert "resources" in result
        assert len(result["resources"]) == 2

        mock_create.assert_called_once()
        assert mock_create_resource.call_count == 2
        
        # Verify dataset metadata structure (back to extras array format)
        create_call_args = mock_create.call_args[1]  # Get keyword arguments
        assert "extras" in create_call_args
        extras = create_call_args["extras"]
        
        # Convert extras list to dict for easier testing
        extras_dict = {extra["key"]: extra["value"] for extra in extras}
        
        # Verify required campaign metadata fields
        assert extras_dict["source"] == "Upstream Platform"
        assert extras_dict["data_type"] == "environmental_sensor_data"
        assert extras_dict["campaign_id"] == "test-campaign-123"
        assert extras_dict["campaign_name"] == sample_campaign_response.name
        assert extras_dict["campaign_contact_name"] == sample_campaign_response.contact_name
        assert extras_dict["campaign_contact_email"] == sample_campaign_response.contact_email
        assert extras_dict["campaign_allocation"] == sample_campaign_response.allocation
        
        # Verify resource metadata structure (station data added as direct fields)
        resource_calls = mock_create_resource.call_args_list
        assert len(resource_calls) == 2
        
        # Check that both resources have station metadata as direct fields
        for call in resource_calls:
            call_kwargs = call[1]  # Get keyword arguments
            assert "metadata" in call_kwargs
            metadata = call_kwargs["metadata"]
            
            # Convert metadata to dict for easier testing
            metadata_dict = {meta["key"]: meta["value"] for meta in metadata}
            assert metadata_dict["station_id"] == str(mock_station_data.id)
            assert metadata_dict["station_name"] == mock_station_data.name
            assert metadata_dict["station_active"] == str(mock_station_data.active)

    @patch("upstream.ckan.CKANIntegration.create_resource")
    @patch("upstream.ckan.CKANIntegration.update_dataset")
    @patch("upstream.ckan.CKANIntegration.get_dataset")
    def test_publish_campaign_update_existing(
        self, mock_get, mock_update, mock_create_resource, sample_campaign_response, mock_station_data
    ):
        """Test updating existing campaign dataset."""
        # Mock get_dataset to return existing dataset
        mock_get.return_value = {
            "id": "dataset-id",
            "name": "upstream-campaign-test-campaign-123",
            "title": "Old Title",
        }

        # Mock update_dataset
        mock_update.return_value = {
            "id": "dataset-id",
            "name": "upstream-campaign-test-campaign-123",
            "title": "Test_Campaign",
        }

        # Mock create_resource
        mock_create_resource.return_value = {
            "id": "resource-id",
            "name": "Test Resource",
        }

        ckan = CKANIntegration("http://test.example.com")

        result = ckan.publish_campaign(
            campaign_id="test-campaign-123",
            campaign_data=sample_campaign_response,
            station_measurements=mock_station_measurements_csv,
            station_sensors=mock_station_sensors_csv,
            station_data=mock_station_data
        )

        assert result["success"] is True
        mock_update.assert_called_once()

    @patch("upstream.ckan.CKANIntegration.create_dataset")
    @patch("upstream.ckan.CKANIntegration.get_dataset")
    def test_publish_campaign_creation_failure(
        self, mock_get, mock_create, sample_campaign_response, mock_station_data
    ):
        """Test campaign publishing with dataset creation failure."""
        mock_get.side_effect = APIError("Dataset not found")
        mock_create.side_effect = APIError("Creation failed")

        ckan = CKANIntegration("http://test.example.com")

        with pytest.raises(APIError, match="CKAN publication failed"):
            ckan.publish_campaign(
                campaign_id="test-campaign-123",
                campaign_data=sample_campaign_response,
                station_measurements=mock_station_measurements_csv,
                station_sensors=mock_station_sensors_csv,
                station_data=mock_station_data
            )


class TestCKANUtilities:
    """Test CKAN utility functions."""

    def test_sanitize_title(self):
        """Test title sanitization."""
        ckan = CKANIntegration("http://test.example.com")

        assert ckan.sanitize_title("Test Dataset") == "Test_Dataset"
        assert ckan.sanitize_title("Test-Dataset-Name") == "Test_Dataset_Name"
        assert ckan.sanitize_title("Multiple Word Dataset") == "Multiple_Word_Dataset"
        assert ckan.sanitize_title("Mixed-Case_and Space") == "Mixed_Case_and_Space"

    def test_sanitize_title_edge_cases(self):
        """Test title sanitization with edge cases."""
        ckan = CKANIntegration("http://test.example.com")

        assert ckan.sanitize_title("") == ""
        assert ckan.sanitize_title("NoSpacesOrDashes") == "NoSpacesOrDashes"
        assert ckan.sanitize_title("___") == "___"
        assert ckan.sanitize_title("   ") == "___"
        assert ckan.sanitize_title("---") == "___"


class TestCKANErrorHandling:
    """Test CKAN error handling."""

    @patch("upstream.ckan.requests.Session.post")
    def test_network_error_handling(self, mock_post):
        """Test network error handling."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Network error")

        ckan = CKANIntegration("http://test.example.com")

        with pytest.raises(APIError, match="Failed to create CKAN dataset"):
            ckan.create_dataset(name="test-dataset", title="Test")

    @patch("upstream.ckan.requests.Session.post")
    def test_timeout_error_handling(self, mock_post):
        """Test timeout error handling."""
        mock_post.side_effect = requests.exceptions.Timeout("Request timeout")

        ckan = CKANIntegration("http://test.example.com")

        with pytest.raises(APIError, match="Failed to create CKAN dataset"):
            ckan.create_dataset(name="test-dataset", title="Test")