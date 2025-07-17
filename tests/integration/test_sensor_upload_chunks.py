"""
Integration tests for sensor CSV upload with chunked measurements.
"""

import os
import tempfile
import pytest
from pathlib import Path
from datetime import datetime, timedelta

from upstream import UpstreamClient
from upstream.exceptions import ValidationError, APIError
from upstream_api_client.models import CampaignsIn, StationCreate

# Integration test configuration
BASE_URL = "http://localhost:8000"
CKAN_URL = "http://ckan.tacc.cloud:5000"

USERNAME = os.environ.get("UPSTREAM_USERNAME")
PASSWORD = os.environ.get("UPSTREAM_PASSWORD")


@pytest.fixture
def client():
    """Create authenticated client for testing."""
    username = os.environ.get("UPSTREAM_USERNAME")
    password = os.environ.get("UPSTREAM_PASSWORD")

    if not username or not password:
        pytest.skip(
            "UPSTREAM_USERNAME and UPSTREAM_PASSWORD environment variables required"
        )

    client = UpstreamClient(
        username=username, password=password, base_url=BASE_URL, ckan_url=CKAN_URL
    )

    # Ensure authentication
    assert client.authenticate(), "Authentication failed"
    return client


def test_upload_csv_files_chunked(client):
    """Test uploading CSV files with chunked measurements."""
    campaign_id = None
    station_id = None

    try:
        # Create campaign
        campaign_data = CampaignsIn(
            name="Test Campaign for Chunked Upload",
            description="Test campaign for chunked CSV upload",
            contact_name="Test User",
            contact_email="test@example.com",
            allocation="TACC",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
        )
        campaign = client.campaigns.create(campaign_data)
        campaign_id = campaign.id
        print(f"Created campaign: {campaign_id}")

        # Create station
        station_data = StationCreate(
            name="Test Station for Chunked Upload",
            description="Test station for chunked CSV upload",
            contact_name="Test User",
            contact_email="test@example.com",
            start_date=datetime.now(),
            active=True,
        )
        station = client.stations.create(campaign_id, station_data)
        station_id = station.id
        print(f"Created station: {station_id}")

        # Create sensors CSV file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as sensors_file:
            sensors_file.write(
                "alias,variablename,units,postprocess,postprocessscript\n"
            )
            sensors_file.write(
                "temp_sensor_01,Air Temperature,°C,True,wind_correction_script\n"
            )
            sensors_file.write(
                "humidity_sensor_01,Humidity,%,True,humidity_correction_script\n"
            )
            sensors_file_path = sensors_file.name

        # Create large measurements CSV file (more than 1000 lines to test chunking)
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as measurements_file:
            # Write header
            measurements_file.write(
                "collectiontime,Lat_deg,Lon_deg,temp_sensor_01,humidity_sensor_01\n"
            )

            # Write 2500 data lines (should create 3 chunks: 1000, 1000, 500)
            for i in range(2500):
                timestamp = (
                    f"2024-01-{(i % 30) + 1:02d}T{(i % 24):02d}:{(i % 60):02d}:00"
                )
                lat = 30.2672 + (i * 0.0001)  # Slight variation in coordinates
                lon = -97.7431 + (i * 0.0001)
                temp = 20.0 + (i % 10)  # Temperature between 20-30°C
                humidity = 50.0 + (i % 20)  # Humidity between 50-70%

                measurements_file.write(
                    f"{timestamp},{lat:.6f},{lon:.6f},{temp:.1f},{humidity:.1f}\n"
                )

            measurements_file_path = measurements_file.name

        try:
            # Upload with default chunk size (1000)
            response = client.sensors.upload_csv_files(
                campaign_id=campaign_id,
                station_id=station_id,
                sensors_file=sensors_file_path,
                measurements_file=measurements_file_path,
            )

            print(f"Upload response: {response}")

            # Verify sensors were created
            sensors = client.sensors.list(
                campaign_id=campaign_id, station_id=station_id
            )
            assert len(sensors.items) == 2
            print(f"Created {len(sensors.items)} sensors")
            # Delete all sensors
            for sensor in sensors.items:
                client.measurements.delete(campaign_id, station_id, sensor.id)

            for sensor in sensors.items:
                client.sensors.delete(sensor.id, station_id, campaign_id)

            # Verify measurements were uploaded (this would require checking the measurements API)
            # For now, we just verify the upload completed without errors

        finally:
            # Clean up temporary files
            Path(sensors_file_path).unlink(missing_ok=True)
            Path(measurements_file_path).unlink(missing_ok=True)

    finally:

        # Clean up station
        if station_id:
            try:
                client.stations.delete(station_id, campaign_id)
                print(f"Deleted station: {station_id}")
            except Exception as e:
                print(f"Failed to delete station: {e}")

        # Clean up campaign
        if campaign_id:
            try:
                client.campaigns.delete(campaign_id)
                print(f"Deleted campaign: {campaign_id}")
            except Exception as e:
                print(f"Failed to delete campaign: {e}")


def test_upload_csv_files_custom_chunk_size(client):
    """Test uploading CSV files with custom chunk size."""
    campaign_id = None
    station_id = None

    try:
        # Create campaign
        campaign_data = CampaignsIn(
            name="Test Campaign for Custom Chunk Size",
            description="Test campaign for custom chunk size CSV upload",
            contact_name="Test User",
            contact_email="test@example.com",
            allocation="TACC",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
        )
        campaign = client.campaigns.create(campaign_data)
        campaign_id = campaign.id
        print(f"Created campaign: {campaign_id}")

        # Create station
        station_data = StationCreate(
            name="Test Station for Custom Chunk Size",
            description="Test station for custom chunk size CSV upload",
            contact_name="Test User",
            contact_email="test@example.com",
            start_date=datetime.now(),
            active=True,
        )
        station = client.stations.create(campaign_id, station_data)
        station_id = station.id
        print(f"Created station: {station_id}")

        # Create sensors CSV file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as sensors_file:
            sensors_file.write(
                "alias,variablename,units,postprocess,postprocessscript\n"
            )
            sensors_file.write(
                "temp_sensor_02,Air Temperature,°C,True,wind_correction_script\n"
            )
            sensors_file_path = sensors_file.name

        # Create measurements CSV file with 500 lines (should create 2 chunks with chunk_size=300)
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as measurements_file:
            # Write header
            measurements_file.write("collectiontime,Lat_deg,Lon_deg,temp_sensor_02\n")

            # Write 500 data lines (should create 2 chunks: 300, 200)
            for i in range(500):
                timestamp = (
                    f"2024-01-{(i % 30) + 1:02d}T{(i % 24):02d}:{(i % 60):02d}:00"
                )
                lat = 30.2672 + (i * 0.0001)
                lon = -97.7431 + (i * 0.0001)
                temp = 20.0 + (i % 10)

                measurements_file.write(f"{timestamp},{lat:.6f},{lon:.6f},{temp:.1f}\n")

            measurements_file_path = measurements_file.name

        try:
            # Upload with custom chunk size (300)
            response = client.sensors.upload_csv_files(
                campaign_id=campaign_id,
                station_id=station_id,
                sensors_file=sensors_file_path,
                measurements_file=measurements_file_path,
                chunk_size=300,
            )

            print(f"Upload response: {response}")

            # Verify sensors were created
            sensors = client.sensors.list(
                campaign_id=campaign_id, station_id=station_id
            )
            print(f"Created {len(sensors.items)} sensors")
            for sensor in sensors.items:
                client.measurements.delete(campaign_id, station_id, sensor.id)
                client.sensors.delete(sensor.id, station_id, campaign_id)

        finally:
            # Clean up temporary files
            Path(sensors_file_path).unlink(missing_ok=True)
            Path(measurements_file_path).unlink(missing_ok=True)

    finally:
        # Clean up station
        if station_id:
            try:
                client.stations.delete(station_id, campaign_id)
                print(f"Deleted station: {station_id}")
            except Exception as e:
                print(f"Failed to delete station: {e}")

        # Clean up campaign
        if campaign_id:
            try:
                client.campaigns.delete(campaign_id)
                print(f"Deleted campaign: {campaign_id}")
            except Exception as e:
                print(f"Failed to delete campaign: {e}")


def test_upload_csv_files_bytes_input(client):
    """Test uploading CSV files using bytes input with chunking."""
    campaign_id = None
    station_id = None

    try:
        # Create campaign
        campaign_data = CampaignsIn(
            name="Test Campaign for Bytes Input",
            description="Test campaign for bytes input CSV upload",
            contact_name="Test User",
            contact_email="test@example.com",
            allocation="TACC",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
        )
        campaign = client.campaigns.create(campaign_data)
        campaign_id = campaign.id
        print(f"Created campaign: {campaign_id}")

        # Create station
        station_data = StationCreate(
            name="Test Station for Bytes Input",
            description="Test station for bytes input CSV upload",
            contact_name="Test User",
            contact_email="test@example.com",
            start_date=datetime.now(),
            active=True,
        )
        station = client.stations.create(campaign_id, station_data)
        station_id = station.id
        print(f"Created station: {station_id}")

        # Create sensors CSV content as bytes
        sensors_content = (
            "alias,variablename,units,postprocess,postprocessscript\n"
            "temp_sensor_03,Air Temperature,°C,True,wind_correction_script\n"
        ).encode("utf-8")

        # Create measurements CSV content as bytes (1500 lines)
        measurements_lines = ["collectiontime,Lat_deg,Lon_deg,temp_sensor_03\n"]
        for i in range(1500):
            timestamp = f"2024-01-{(i % 30) + 1:02d}T{(i % 24):02d}:{(i % 60):02d}:00"
            lat = 30.2672 + (i * 0.0001)
            lon = -97.7431 + (i * 0.0001)
            temp = 20.0 + (i % 10)
            measurements_lines.append(f"{timestamp},{lat:.6f},{lon:.6f},{temp:.1f}\n")

        measurements_content = "".join(measurements_lines).encode("utf-8")

        # Upload using bytes input
        response = client.sensors.upload_csv_files(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_content,
            measurements_file=measurements_content,
            chunk_size=500,  # Should create 3 chunks: 500, 500, 500
        )

        print(f"Upload response: {response}")

        # Verify sensors were created
        sensors = client.sensors.list(campaign_id=campaign_id, station_id=station_id)
        print(f"Created {len(sensors.items)} sensors")

        # Delete all sensors
        for sensor in sensors.items:
            client.measurements.delete(campaign_id, station_id, sensor.id)
            client.sensors.delete(sensor.id, station_id, campaign_id)

    finally:
        # Clean up station
        if station_id:
            try:
                client.stations.delete(station_id, campaign_id)
                print(f"Deleted station: {station_id}")
            except Exception as e:
                print(f"Failed to delete station: {e}")

        # Clean up campaign
        if campaign_id:
            try:
                client.campaigns.delete(campaign_id)
                print(f"Deleted campaign: {campaign_id}")
            except Exception as e:
                print(f"Failed to delete campaign: {e}")
