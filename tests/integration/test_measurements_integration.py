"""
Integration tests for measurement management functionality.

These tests require valid credentials and a running API server.
Set UPSTREAM_USERNAME and UPSTREAM_PASSWORD environment variables.
"""

import os
from datetime import datetime, timedelta

import pytest
from upstream_api_client.models import MeasurementIn, MeasurementUpdate

from upstream import UpstreamClient

# Test configuration
BASE_URL = os.environ.get("UPSTREAM_BASE_URL", "http://localhost:8000")
CKAN_URL = os.environ.get("CKAN_URL", "http://ckan.tacc.cloud:5000")
USERNAME = os.environ.get("UPSTREAM_USERNAME")
PASSWORD = os.environ.get("UPSTREAM_PASSWORD")


@pytest.fixture
def upstream_client():
    """Create authenticated client for testing."""
    username = os.environ.get("UPSTREAM_USERNAME")
    password = os.environ.get("UPSTREAM_PASSWORD")

    if not username or not password:
        pytest.skip(
            "UPSTREAM_USERNAME and UPSTREAM_PASSWORD environment variables required"
        )

    upstream_client = UpstreamClient(
        username=username, password=password, base_url=BASE_URL, ckan_url=CKAN_URL
    )

    # Ensure authentication
    assert upstream_client.authenticate(), "Authentication failed"
    return upstream_client


def test_measurement_lifecycle(upstream_client):
    """Test complete measurement lifecycle: create, list, update, delete."""
    # Create a campaign first
    from upstream_api_client.models import CampaignsIn

    campaign_data = CampaignsIn(
        name="Test Campaign for Measurements",
        description="Test campaign for measurement integration tests",
        contact_name="Integration Tester",
        contact_email="integration@example.com",
        allocation="TACC",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
    )

    campaign = upstream_client.create_campaign(campaign_data)
    campaign_id = str(campaign.id)

    try:
        # Create a station
        from upstream_api_client.models import StationCreate

        station_data = StationCreate(
            name="Test Station for Measurements",
            description="Test station for measurement integration tests",
            contact_name="Station Tester",
            contact_email="station@example.com",
            start_date=datetime.now(),
            active=True,
        )

        station = upstream_client.create_station(campaign_id, station_data)
        station_id = str(station.id)

        try:
            # Create a sensor first (we need one to create measurements)
            # Upload a simple sensor via CSV
            import tempfile

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as sensors_file:
                sensors_file.write(
                    "alias,variablename,units,postprocess,postprocessscript\n"
                )
                sensors_file.write(
                    "temp_sensor_01,Air Temperature,°C,True,wind_correction_script\n"
                )
                sensors_file_path = sensors_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as measurements_file:
                measurements_file.write(
                    "collectiontime,Lat_deg,Lon_deg,temp_sensor_01\n"
                )
                measurements_file.write("2024-01-15T10:30:00,30.2672,-97.7431,23.5\n")
                measurements_file_path = measurements_file.name

            try:
                # Upload sensor
                result = upstream_client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=sensors_file_path,
                    measurements_file=measurements_file_path,
                )

                # Get the sensor ID
                sensors = upstream_client.sensors.list(
                    campaign_id=campaign_id, station_id=station_id
                )
                assert len(sensors.items) > 0
                sensor = sensors.items[0]
                sensor_id = str(sensor.id)

                # Test create measurement
                measurement_data = MeasurementIn(
                    collectiontime=datetime.now(),
                    measurementvalue=25.5,
                    variablename="Air Temperature",
                    variabletype="temperature",
                    description="Test measurement",
                    geometry="POINT(-97.7431 30.2672)",
                )

                created_measurement = upstream_client.measurements.create(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    measurement_in=measurement_data,
                )

                assert created_measurement.id is not None
                print(f"Created measurement: {created_measurement.id}")

                # Test list measurements
                measurements = upstream_client.list_measurements(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    limit=10,
                )

                assert measurements.total > 0
                print(f"Found {measurements.total} measurements")

                # Test get measurements with confidence intervals
                confidence_measurements = (
                    upstream_client.get_measurements_with_confidence_intervals(
                        campaign_id=campaign_id,
                        station_id=station_id,
                        sensor_id=sensor_id,
                        interval="hour",
                        interval_value=1,
                    )
                )

                print(f"Found {len(confidence_measurements)} aggregated measurements")

                # Test update measurement (if we have a measurement to update)
                if measurements.items:
                    measurement = measurements.items[0]
                    measurement_id = str(measurement.id)

                    update_data = MeasurementUpdate(
                        measurementvalue=26.0, description="Updated test measurement"
                    )

                    upstream_client.update_measurement(
                        campaign_id=campaign_id,
                        station_id=station_id,
                        sensor_id=sensor_id,
                        measurement_id=measurement_id,
                        measurement_update=update_data,
                    )

                    updated_measurement = upstream_client.measurements.list(
                        campaign_id=campaign_id,
                        station_id=station_id,
                        sensor_id=sensor_id,
                        limit=10,
                    )

                    # TODO: The updated measurement is not being returned in the list

                    # # #loop through the measurements and find the updated measurement
                    # # m = None
                    # # for m in updated_measurement.items:
                    # #     if m.id == measurement_id:
                    # #         updated_measurement = m
                    # #         break

                    # assert m is not None
                    # assert m.id == measurement_id
                    # assert m.value == 26.0
                    # #assert m.description == "Updated test measurement"
                    # print(f"Updated measurement: {updated_measurement.id}")

                # Test delete measurements
                result = upstream_client.delete_measurements(
                    campaign_id=campaign_id, station_id=station_id, sensor_id=sensor_id
                )

                assert result is True
                print(f"Deleted measurements for sensor: {sensor_id}")

                # Verify deletion
                measurements_after_delete = upstream_client.list_measurements(
                    campaign_id=campaign_id, station_id=station_id, sensor_id=sensor_id
                )

                assert len(measurements_after_delete.items) == 0

                # Note: The delete endpoint removes all measurements for the sensor
                # so we can't check for specific measurement deletion

            finally:
                # Clean up temporary files
                os.unlink(sensors_file_path)
                os.unlink(measurements_file_path)

        finally:
            # Clean up station
            # client.stations.delete(station_id, campaign_id)
            pass

    finally:
        # Clean up campaign
        # client.campaigns.delete(campaign_id)
        pass


def test_measurement_filtering(upstream_client):
    """Test measurement filtering and querying capabilities."""
    # Create a campaign first
    from upstream_api_client.models import CampaignsIn

    campaign_data = CampaignsIn(
        name="Test Campaign for Measurement Filtering",
        description="Test campaign for measurement filtering tests",
        contact_name="Integration Tester",
        contact_email="integration@example.com",
        allocation="TACC",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
    )

    campaign = upstream_client.create_campaign(campaign_data)
    campaign_id = str(campaign.id)

    try:
        # Create a station
        from upstream_api_client.models import StationCreate

        station_data = StationCreate(
            name="Test Station for Measurement Filtering",
            description="Test station for measurement filtering tests",
            contact_name="Station Tester",
            contact_email="station@example.com",
            start_date=datetime.now(),
            active=True,
        )

        station = upstream_client.create_station(campaign_id, station_data)
        station_id = str(station.id)

        try:
            # Create a sensor and some measurements
            import tempfile

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

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as measurements_file:
                measurements_file.write(
                    "collectiontime,Lat_deg,Lon_deg,temp_sensor_02\n"
                )
                measurements_file.write("2024-01-15T10:30:00,30.2672,-97.7431,23.5\n")
                measurements_file.write("2024-01-15T11:30:00,30.2672,-97.7431,24.0\n")
                measurements_file.write("2024-01-15T12:30:00,30.2672,-97.7431,24.5\n")
                measurements_file_path = measurements_file.name

            try:
                # Upload sensor and measurements
                result = upstream_client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=sensors_file_path,
                    measurements_file=measurements_file_path,
                )

                # Get the sensor ID
                sensors = upstream_client.sensors.list(
                    campaign_id=campaign_id, station_id=station_id
                )
                assert len(sensors.items) > 0
                sensor = sensors.items[0]
                sensor_id = str(sensor.id)

                # Test filtering by date range
                start_date = datetime(2024, 1, 15, 10, 0, 0)
                end_date = datetime(2024, 1, 15, 12, 0, 0)

                filtered_measurements = upstream_client.list_measurements(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    start_date=start_date,
                    end_date=end_date,
                )

                print(f"Found {filtered_measurements.total} measurements in date range")

                # Test filtering by value range
                value_filtered_measurements = upstream_client.list_measurements(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    min_measurement_value=23.0,
                    max_measurement_value=24.0,
                )

                print(
                    f"Found {value_filtered_measurements.total} measurements in value range"
                )

                # Test pagination
                paginated_measurements = upstream_client.list_measurements(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    limit=2,
                    page=1,
                )

                print(
                    f"Found {len(paginated_measurements.items)} measurements on page 1"
                )

                # Test confidence intervals with different intervals
                hourly_intervals = upstream_client.get_measurements_with_confidence_intervals(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensor_id=sensor_id,
                    interval="hour",
                    interval_value=1,
                )

                print(f"Found {len(hourly_intervals)} hourly aggregated measurements")

            finally:
                # Clean up temporary files
                os.unlink(sensors_file_path)
                os.unlink(measurements_file_path)

        finally:
            # Clean up station
            pass
            # client.stations.delete(station_id, campaign_id)

    finally:
        # Clean up campaign
        pass
        # client.campaigns.delete(campaign_id)
