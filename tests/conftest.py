"""
Pytest configuration and fixtures for Upstream SDK tests.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import json
import csv

from upstream.client import UpstreamClient
from upstream.auth import AuthManager
from upstream.utils import ConfigManager
from upstream_api_client.models import (
    CampaignsIn,
    StationCreate,
    GetCampaignResponse,
    GetStationResponse,
    StationCreateResponse,
    ListStationsResponsePagination,
)


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return ConfigManager(
        username="test_user",
        password="test_pass",
        base_url="https://test.example.com",
        ckan_url="https://test-ckan.example.com",
        timeout=30,
        max_retries=3,
        chunk_size=1000,
        max_chunk_size_mb=10,
    )


@pytest.fixture
def mock_auth_manager(mock_config):
    """Mock authentication manager."""
    auth_manager = Mock(spec=AuthManager)
    auth_manager.config = mock_config
    auth_manager.get_headers.return_value = {
        "Authorization": "Bearer test-token",
        "Content-Type": "application/json",
    }
    auth_manager.authenticate.return_value = True
    return auth_manager


@pytest.fixture
def mock_client(mock_config, mock_auth_manager):
    """Mock Upstream client."""
    with patch("upstream.client.AuthManager", return_value=mock_auth_manager):
        client = UpstreamClient(
            username="test_user",
            password="test_pass",
            base_url="https://test.example.com",
        )
        return client


@pytest.fixture
def sample_campaign_data():
    """Sample campaign data for testing."""
    return {
        "id": "test-campaign-123",
        "name": "Test Campaign",
        "description": "A test campaign for unit testing",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "metadata": {"test": "data"},
    }


@pytest.fixture
def sample_station_data():
    """Sample station data for testing."""
    return {
        "id": "test-station-456",
        "campaign_id": "test-campaign-123",
        "name": "Test Station",
        "latitude": 30.2672,
        "longitude": -97.7431,
        "description": "A test station",
        "contact_name": "Test Contact",
        "contact_email": "test@example.com",
        "altitude": 100.0,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "status": "active",
        "metadata": {"test": "data"},
    }


@pytest.fixture
def sample_sensors_data():
    """Sample sensors data for testing."""
    return [
        {
            "alias": "temp_01",
            "variablename": "Air Temperature",
            "units": "°C",
            "postprocess": "",
            "postprocessscript": "",
        },
        {
            "alias": "humidity_01",
            "variablename": "Relative Humidity",
            "units": "%",
            "postprocess": "",
            "postprocessscript": "",
        },
    ]


@pytest.fixture
def sample_measurements_data():
    """Sample measurements data for testing."""
    return [
        {
            "collectiontime": "2024-01-01T10:00:00Z",
            "Lat_deg": 30.2672,
            "Lon_deg": -97.7431,
            "temp_01": 25.5,
            "humidity_01": 65.2,
        },
        {
            "collectiontime": "2024-01-01T10:01:00Z",
            "Lat_deg": 30.2672,
            "Lon_deg": -97.7431,
            "temp_01": 25.7,
            "humidity_01": 64.8,
        },
    ]


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(["alias", "variablename", "units"])
        writer.writerow(["temp_01", "Air Temperature", "°C"])
        writer.writerow(["humidity_01", "Relative Humidity", "%"])
        temp_path = f.name

    yield Path(temp_path)

    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def temp_measurements_csv():
    """Create a temporary measurements CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(
            ["collectiontime", "Lat_deg", "Lon_deg", "temp_01", "humidity_01"]
        )
        writer.writerow(["2024-01-01T10:00:00Z", "30.2672", "-97.7431", "25.5", "65.2"])
        writer.writerow(["2024-01-01T10:01:00Z", "30.2672", "-97.7431", "25.7", "64.8"])
        temp_path = f.name

    yield Path(temp_path)

    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file for testing."""
    config_data = {
        "upstream": {
            "username": "test_user",
            "password": "test_pass",
            "base_url": "https://test.example.com",
        },
        "ckan": {"url": "https://test-ckan.example.com", "auto_publish": True},
        "upload": {
            "chunk_size": 1000,
            "max_file_size_mb": 10,
            "timeout_seconds": 30,
            "retry_attempts": 3,
        },
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name

    yield Path(temp_path)

    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def mock_requests_response():
    """Mock requests response."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"success": True, "data": {}}
    response.raise_for_status.return_value = None
    return response


@pytest.fixture
def mock_campaign(sample_campaign_data):
    """Mock Campaign object."""
    return GetCampaignResponse(**sample_campaign_data)


@pytest.fixture
def mock_station(sample_station_data):
    """Mock Station object."""
    return GetStationResponse(**sample_station_data)


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks after each test."""
    yield
    # Any cleanup code can go here


# Test markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "network: mark test as requiring network access")


# Skip network tests by default
def pytest_collection_modifyitems(config, items):
    """Modify test collection to skip network tests by default."""
    if config.getoption("--run-network"):
        return

    skip_network = pytest.mark.skip(reason="need --run-network option to run")
    for item in items:
        if "network" in item.keywords:
            item.add_marker(skip_network)


def pytest_addoption(parser):
    """Add command line options."""
    parser.addoption(
        "--run-network", action="store_true", default=False, help="run network tests"
    )
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )
