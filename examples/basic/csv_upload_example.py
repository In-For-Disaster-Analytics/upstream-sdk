#!/usr/bin/env python3
"""
Example: Upload Sensor and Measurement CSV Files

This example demonstrates how to upload sensor metadata and measurement data
using the correct CSV format for the Upstream API.

CSV Format Requirements:
- Sensors CSV: alias,variablename,units,postprocess,postprocessscript
- Measurements CSV: collectiontime,Lat_deg,Lon_deg,{sensor_aliases...}
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

from upstream import UpstreamClient


def create_sample_sensors_csv(file_path: str) -> None:
    """Create a sample sensors CSV file with the correct format."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("alias,variablename,units,postprocess,postprocessscript\n")
        f.write("temp_sensor_01,Air Temperature,°C,,\n")
        f.write("humidity_01,Relative Humidity,%,,\n")
        f.write("pressure_01,Atmospheric Pressure,hPa,,\n")
        f.write("wind_speed_01,Wind Speed,m/s,true,wind_correction_script\n")
        f.write("wind_direction_01,Wind Direction,degrees,,\n")
        f.write("rainfall_01,Rainfall,mm,,\n")


def create_sample_measurements_csv(file_path: str) -> None:
    """Create a sample measurements CSV file with the correct format."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(
            "collectiontime,Lat_deg,Lon_deg,temp_sensor_01,humidity_01,pressure_01,wind_speed_01,wind_direction_01,rainfall_01\n"
        )

        # Generate sample data for the last 24 hours
        base_time = datetime.now() - timedelta(hours=24)
        base_lat = 30.2672
        base_lon = -97.7431

        for i in range(24):
            timestamp = base_time + timedelta(hours=i)
            lat = base_lat + (i * 0.0001)  # Slight variation
            lon = base_lon + (i * 0.0001)  # Slight variation

            # Generate realistic sensor values
            temp = 20 + (i % 12) * 0.5  # Temperature variation
            humidity = 60 + (i % 8) * 2  # Humidity variation
            pressure = 1013.25 + (i % 6) * 0.1  # Pressure variation
            wind_speed = 2 + (i % 4) * 0.5  # Wind speed variation
            wind_direction = (i * 15) % 360  # Wind direction variation
            rainfall = 0 if i < 20 else (i - 19) * 0.1  # Some rain at the end

            f.write(
                f"{timestamp.strftime('%Y-%m-%dT%H:%M:%S')},{lat:.4f},{lon:.4f},{temp:.1f},{humidity:.1f},{pressure:.2f},{wind_speed:.1f},{wind_direction:.0f},{rainfall:.1f}\n"
            )


def main():
    """Main function demonstrating CSV upload functionality."""

    # Initialize client (you'll need to set these environment variables)
    username = os.environ.get("UPSTREAM_USERNAME")
    password = os.environ.get("UPSTREAM_PASSWORD")

    if not username or not password:
        print(
            "❌ Please set UPSTREAM_USERNAME and UPSTREAM_PASSWORD environment variables"
        )
        return

    client = UpstreamClient(
        username=username,
        password=password,
        base_url="https://upstream-dev.tacc.utexas.edu",
    )

    # Authenticate
    if not client.authenticate():
        print("❌ Authentication failed")
        return

    print("✅ Authentication successful")

    # Create a campaign for testing
    from upstream_api_client.models import CampaignsIn
    from datetime import datetime, timedelta

    campaign_data = CampaignsIn(
        name="CSV Upload Example Campaign",
        description="Example campaign for demonstrating CSV upload functionality",
        contact_name="Example User",
        contact_email="example@tacc.utexas.edu",
        allocation="TACC",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
    )

    try:
        campaign = client.create_campaign(campaign_data)
        campaign_id = str(campaign.id)
        print(f"✅ Created campaign: {campaign_id}")

        # Create a station
        from upstream_api_client.models import StationCreate

        station_data = StationCreate(
            name="CSV Upload Example Station",
            description="Example station for CSV upload testing",
            contact_name="Example User",
            contact_email="example@tacc.utexas.edu",
            start_date=datetime.now(),
            active=True,
        )

        station = client.create_station(campaign_id, station_data)
        station_id = str(station.id)
        print(f"✅ Created station: {station_id}")

        try:
            # Create temporary CSV files
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as sensors_file:
                create_sample_sensors_csv(sensors_file.name)
                sensors_path = sensors_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as measurements_file:
                create_sample_measurements_csv(measurements_file.name)
                measurements_path = measurements_file.name

            try:
                print("📤 Uploading sensor and measurement files...")

                # Upload using file paths
                result = client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=sensors_path,
                    measurements_file=measurements_path,
                )

                print("✅ Upload successful!")
                print(f"📊 Upload result: {result}")

                # Demonstrate different upload methods
                print("\n🔄 Testing different upload methods...")

                # Method 1: Using bytes
                with open(sensors_path, "rb") as f:
                    sensors_bytes = f.read()
                with open(measurements_path, "rb") as f:
                    measurements_bytes = f.read()

                result_bytes = client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=sensors_bytes,
                    measurements_file=measurements_bytes,
                )
                print("✅ Bytes upload successful")

                # Method 2: Using tuples (filename, bytes)
                result_tuple = client.upload_sensor_measurement_files(
                    campaign_id=campaign_id,
                    station_id=station_id,
                    sensors_file=("sensors.csv", sensors_bytes),
                    measurements_file=("measurements.csv", measurements_bytes),
                )
                print("✅ Tuple upload successful")

            finally:
                # Clean up temporary files
                os.unlink(sensors_path)
                os.unlink(measurements_path)
                print("🧹 Cleaned up temporary files")

        finally:
            # Clean up station
            client.stations.delete(station_id, campaign_id)
            print(f"🗑️ Deleted station: {station_id}")

    finally:
        # Clean up campaign
        client.campaigns.delete(campaign_id)
        print(f"🗑️ Deleted campaign: {campaign_id}")

    print("\n🎉 CSV upload example completed successfully!")


if __name__ == "__main__":
    main()
