"""
Integration tests for sensor management functionality.

These tests require valid credentials and a running API server.
Set UPSTREAM_USERNAME and UPSTREAM_PASSWORD environment variables.
"""

import os
import tempfile
from datetime import datetime, timedelta

import pytest

from upstream import UpstreamClient

BASE_URL = "http://localhost:8000"
CKAN_URL = "http://ckan.tacc.cloud:5000"

USERNAME = os.environ.get("UPSTREAM_USERNAME")
PASSWORD = os.environ.get("UPSTREAM_PASSWORD")
BASE_URL = os.environ.get("UPSTREAM_BASE_URL", "http://localhost:8000")
CKAN_URL = os.environ.get("CKAN_URL", "http://ckan.tacc.cloud:5000")


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


def sensor_file_content():
    """Create temporary CSV files for testing."""
    return """alias,variablename,units,postprocess,postprocessscript
temp_sensor_01,Air Temperature,°C,True,wind_correction_script
humidity_01,Relative Humidity,%,True,humidity_correction_script
pressure_01,Atmospheric Pressure,hPa,True,pressure_correction_script
wind_speed_01,Wind Speed,m/s,True,wind_correction_script"""


def measurements_file_content_empty():
    """Create temporary CSV files for testing."""
    return """collectiontime,Lat_deg,Lon_deg,temp_sensor_01,humidity_01,pressure_01,wind_speed_01\n"""


def measurements_file_content_filled():
    """Create temporary CSV files for testing."""
    return """collectiontime,Lat_deg,Lon_deg,temp_sensor_01,humidity_01,pressure_01,wind_speed_01
2024-01-15T10:30:00,30.2672,-97.7431,23.5,65.2,1013.25,2.3
2024-01-15T10:31:00,30.2673,-97.7432,23.7,64.8,1013.20,2.1
2024-01-15T10:32:00,30.2674,-97.7433,23.9,64.5,1013.15,1.8
2024-01-15T10:33:00,30.2675,-97.7434,,64.2,1013.10,1.9"""


def test_upload_csv_files(client):
    """Test uploading sensor and measurement CSV files."""
    # Create a campaign first
    from upstream_api_client.models import CampaignsIn

    campaign_data = CampaignsIn(
        name="Test Campaign for CSV Upload",
        description="Test campaign for CSV upload integration tests",
        contact_name="Integration Tester",
        contact_email="integration@example.com",
        allocation="TACC",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
    )

    campaign = client.create_campaign(campaign_data)
    campaign_id = campaign.id

    try:
        # Create a station
        from upstream_api_client.models import StationCreate

        station_data = StationCreate(
            name="Test Station for CSV Upload",
            description="Test station for CSV upload integration tests",
            contact_name="Station Tester",
            contact_email="station@example.com",
            start_date=datetime.now(),
            active=True,
        )

        station = client.create_station(campaign_id, station_data)
        station_id = station.id

        try:
            # Create temporary CSV files for testing using the correct format
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as sensors_file:
                sensors_file.write(sensor_file_content())
                sensors_file_path = sensors_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as measurements_file:
                measurements_file.write(measurements_file_content_filled())
                measurements_file_path = measurements_file.name

            try:
                # Test upload using file paths
                result = client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=sensors_file_path,
                    measurements_file=measurements_file_path,
                )

                # Verify the upload was successful
                assert isinstance(result, dict), "Upload should return a dictionary"
                print(f"Upload result: {result}")

                # Test upload using bytes
                with open(sensors_file_path, "rb") as f:
                    sensors_bytes = f.read()
                with open(measurements_file_path, "rb") as f:
                    measurements_bytes = f.read()

                result_bytes = client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=sensors_bytes,
                    measurements_file=measurements_bytes,
                )

                assert isinstance(
                    result_bytes, dict
                ), "Upload with bytes should return a dictionary"
                print(f"Upload with bytes result: {result_bytes}")

                # Test upload using tuple (filename, bytes)
                with open(sensors_file_path, "rb") as f:
                    sensors_bytes = f.read()
                with open(measurements_file_path, "rb") as f:
                    measurements_bytes = f.read()

                result_tuple = client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=("sensors.csv", sensors_bytes),
                    measurements_file=("measurements.csv", measurements_bytes),
                )

                assert isinstance(
                    result_tuple, dict
                ), "Upload with tuple should return a dictionary"
                print(f"Upload with tuple result: {result_tuple}")

                # Get all the sensors
                sensors = client.sensors.list(
                    campaign_id=campaign_id, station_id=station_id
                )
                assert len(sensors.items) > 0
                print(f"Sensors: {sensors.items}")

                # Check the sensors
                all_aliases = [sensor.alias for sensor in sensors.items]
                assert "temp_sensor_01" in all_aliases
                assert "humidity_01" in all_aliases
                assert "pressure_01" in all_aliases
                assert "wind_speed_01" in all_aliases

                all_variablenames = [sensor.variablename for sensor in sensors.items]
                assert "Air Temperature" in all_variablenames
                assert "Relative Humidity" in all_variablenames
                assert "Atmospheric Pressure" in all_variablenames
                assert "Wind Speed" in all_variablenames

                all_units = [sensor.units for sensor in sensors.items]
                assert "°C" in all_units
                assert "%" in all_units
                assert "hPa" in all_units
                assert "m/s" in all_units

                all_postprocesses = [sensor.postprocess for sensor in sensors.items]
                assert all(postprocess is True for postprocess in all_postprocesses)

                all_postprocessscripts = [
                    sensor.postprocessscript for sensor in sensors.items
                ]
                assert "wind_correction_script" in all_postprocessscripts
                assert "humidity_correction_script" in all_postprocessscripts
                assert "pressure_correction_script" in all_postprocessscripts
                assert "wind_correction_script" in all_postprocessscripts
            finally:
                # Clean up temporary files
                os.unlink(sensors_file_path)
                os.unlink(measurements_file_path)

        finally:
            for sensor in sensors.items:
                client.measurements.delete(campaign_id, station_id, sensor.id)

            for sensor in sensors.items:
                client.sensors.delete(sensor.id, station_id, campaign_id)

            client.stations.delete(station_id, campaign_id)

            # Check the sensors
            # sensors = client.sensors.list(campaign_id=campaign_id, station_id=station_id)
            # assert len(sensors.items) == 0
            # Clean up station
            # client.stations.delete(station_id, campaign_id)

    finally:
        # Clean up campaign
        client.campaigns.delete(campaign_id)


def test_sensor_statistics_update(client):
    """Test sensor statistics force update functionality."""
    # Create a campaign first
    from upstream_api_client.models import CampaignsIn, MeasurementIn

    campaign_data = CampaignsIn(
        name="Test Campaign for Statistics Update",
        description="Test campaign for sensor statistics update integration tests",
        contact_name="Integration Tester",
        contact_email="integration@example.com",
        allocation="TACC",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
    )

    campaign = client.create_campaign(campaign_data)
    campaign_id = campaign.id

    try:
        # Create a station
        from upstream_api_client.models import StationCreate

        station_data = StationCreate(
            name="Test Station for Statistics Update",
            description="Test station for sensor statistics update integration tests",
            contact_name="Station Tester",
            contact_email="station@example.com",
            start_date=datetime.now(),
            active=True,
        )

        station = client.create_station(campaign_id, station_data)
        station_id = station.id

        try:
            # Create temporary CSV files for testing with initial data
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as sensors_file:
                sensors_file.write(sensor_file_content())
                sensors_file_path = sensors_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as measurements_file:
                measurements_file.write(measurements_file_content_filled())
                measurements_file_path = measurements_file.name

            try:
                # Upload initial sensor and measurement data
                result = client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=sensors_file_path,
                    measurements_file=measurements_file_path,
                )

                print(f"Initial upload result: {result}")

                # Get the sensors and their initial statistics
                sensors = client.sensors.list(
                    campaign_id=campaign_id, station_id=station_id
                )
                assert len(sensors.items) > 0, "Should have sensors after upload"

                # Get a specific sensor for detailed testing
                temp_sensor = None
                for sensor in sensors.items:
                    if sensor.alias == "temp_sensor_01":
                        temp_sensor = sensor
                        break

                assert temp_sensor is not None, "temp_sensor_01 should exist"
                sensor_id = temp_sensor.id

                # Record initial statistics
                initial_stats = temp_sensor.statistics
                initial_count = initial_stats.count if initial_stats else 0
                print(f"Initial measurement count for temp_sensor_01: {initial_count}")

                # Add a new measurement manually
                measurement_data = MeasurementIn(
                    collectiontime=datetime.now(),
                    measurementvalue=25.5,
                    variablename="Air Temperature",
                    variabletype="temperature",
                    description="Test measurement for statistics update",
                    geometry="POINT(-97.7431 30.2672)",
                )

                created_measurement = client.measurements.create(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    measurement_in=measurement_data,
                )

                assert created_measurement.id is not None
                print(f"Created additional measurement: {created_measurement.id}")

                # Get sensor statistics before force update (should still show old count)
                sensors_before_update = client.sensors.list(
                    campaign_id=campaign_id, station_id=station_id
                )
                temp_sensor_before = None
                for sensor in sensors_before_update.items:
                    if sensor.alias == "temp_sensor_01":
                        temp_sensor_before = sensor
                        break

                before_update_count = temp_sensor_before.statistics.count if temp_sensor_before.statistics else 0
                print(f"Measurement count before statistics update: {before_update_count}")

                # Force update statistics for the specific sensor
                single_update_result = client.sensors.force_update_single_sensor_statistics(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                )

                print(f"Single sensor statistics update result: {single_update_result}")
                assert single_update_result is not None

                # Get sensor statistics after single sensor force update
                sensors_after_single_update = client.sensors.list(
                    campaign_id=campaign_id, station_id=station_id
                )
                temp_sensor_after_single = None
                for sensor in sensors_after_single_update.items:
                    if sensor.alias == "temp_sensor_01":
                        temp_sensor_after_single = sensor
                        break

                after_single_update_count = temp_sensor_after_single.statistics.count if temp_sensor_after_single.statistics else 0
                print(f"Measurement count after single sensor statistics update: {after_single_update_count}")

                # Verify that the count increased by 1
                assert after_single_update_count == initial_count + 1, f"Expected count to increase from {initial_count} to {initial_count + 1}, but got {after_single_update_count}"

                # Add another measurement
                measurement_data_2 = MeasurementIn(
                    collectiontime=datetime.now() + timedelta(minutes=1),
                    measurementvalue=26.0,
                    variablename="Air Temperature",
                    variabletype="temperature",
                    description="Second test measurement for statistics update",
                    geometry="POINT(-97.7431 30.2672)",
                )

                created_measurement_2 = client.measurements.create(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    measurement_in=measurement_data_2,
                )

                print(f"Created second additional measurement: {created_measurement_2.id}")

                # Force update statistics for all sensors in the station
                all_update_result = client.sensors.force_update_statistics(
                    campaign_id=campaign_id,
                    station_id=station_id,
                )

                print(f"All sensors statistics update result: {all_update_result}")
                assert all_update_result is not None

                # Get sensor statistics after force update of all sensors
                sensors_after_all_update = client.sensors.list(
                    campaign_id=campaign_id, station_id=station_id
                )
                temp_sensor_after_all = None
                for sensor in sensors_after_all_update.items:
                    if sensor.alias == "temp_sensor_01":
                        temp_sensor_after_all = sensor
                        break

                after_all_update_count = temp_sensor_after_all.statistics.count if temp_sensor_after_all.statistics else 0
                print(f"Measurement count after all sensors statistics update: {after_all_update_count}")

                # Verify that the count increased by 2 total (initial + 2 new measurements)
                assert after_all_update_count == initial_count + 2, f"Expected count to increase from {initial_count} to {initial_count + 2}, but got {after_all_update_count}"

                # Verify that statistics timestamps were updated
                final_stats = temp_sensor_after_all.statistics
                assert final_stats.stats_last_updated is not None
                print(f"Statistics last updated: {final_stats.stats_last_updated}")

                # Verify other statistics fields are present and reasonable
                assert final_stats.min_value is not None
                assert final_stats.max_value is not None
                assert final_stats.avg_value is not None
                assert final_stats.stddev_value is not None
                print(f"Final statistics - Count: {final_stats.count}, Min: {final_stats.min_value}, Max: {final_stats.max_value}, Avg: {final_stats.avg_value}")

            finally:
                # Clean up temporary files
                os.unlink(sensors_file_path)
                os.unlink(measurements_file_path)

        finally:
            # Clean up measurements and sensors
            try:
                sensors = client.sensors.list(campaign_id=campaign_id, station_id=station_id)
                for sensor in sensors.items:
                    try:
                        client.measurements.delete(campaign_id, station_id, sensor.id)
                    except Exception as e:
                        print(f"Error deleting measurements for sensor {sensor.id}: {e}")

                    try:
                        client.sensors.delete(sensor.id, station_id, campaign_id)
                    except Exception as e:
                        print(f"Error deleting sensor {sensor.id}: {e}")
            except Exception as e:
                print(f"Error during sensor cleanup: {e}")

            # Clean up station
            try:
                client.stations.delete(station_id, campaign_id)
            except Exception as e:
                print(f"Error deleting station: {e}")

    finally:
        # Clean up campaign
        try:
            client.campaigns.delete(campaign_id)
        except Exception as e:
            print(f"Error deleting campaign: {e}")
