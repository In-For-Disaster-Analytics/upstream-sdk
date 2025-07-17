#!/usr/bin/env python3
"""
Example: Chunked CSV Upload for Large Measurement Files

This example demonstrates how to upload large measurement CSV files
in chunks to avoid HTTP timeouts. The upload_csv_files method now
supports chunked uploads with configurable chunk sizes.

Key Features:
- Uploads measurements in chunks of 1000 lines (default) or custom size
- Handles large files that would otherwise timeout
- Supports all input formats: file paths, bytes, or (filename, bytes) tuples
- Only uploads sensor metadata with the first chunk
- Provides progress logging for each chunk
"""

import tempfile
import time
from pathlib import Path
from datetime import datetime, timedelta
import random

from upstream import UpstreamClient
from upstream.exceptions import ValidationError, APIError


def create_large_measurements_file(file_path: str, num_lines: int = 5000):
    """
    Create a large measurements CSV file for testing chunked upload.

    Args:
        file_path: Path to the CSV file to create
        num_lines: Number of data lines to generate
    """
    print(f"Creating large measurements file with {num_lines} lines...")

    with open(file_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("collectiontime,Lat_deg,Lon_deg,temperature_sensor,humidity_sensor,pressure_sensor,wind_speed_sensor\n")

        # Generate data lines
        base_time = datetime(2024, 1, 1, 0, 0, 0)
        base_lat = 30.2672
        base_lon = -97.7431

        for i in range(num_lines):
            # Generate timestamp with slight variations
            timestamp = base_time + timedelta(hours=i % 24, minutes=i % 60, seconds=i % 60)

            # Generate coordinates with slight variations
            lat = base_lat + (i * 0.0001) % 0.01
            lon = base_lon + (i * 0.0001) % 0.01

            # Generate sensor readings with realistic variations
            temperature = 20.0 + 10 * random.random()  # 20-30°C
            humidity = 40.0 + 30 * random.random()     # 40-70%
            pressure = 1013.0 + 20 * random.random()   # 1013-1033 hPa
            wind_speed = 0.0 + 15 * random.random()    # 0-15 m/s

            f.write(f"{timestamp.isoformat()},{lat:.6f},{lon:.6f},{temperature:.2f},{humidity:.2f},{pressure:.2f},{wind_speed:.2f}\n")

    print(f"Created measurements file: {file_path}")


def create_sensors_file(file_path: str):
    """
    Create a sensors CSV file with multiple sensor definitions.

    Args:
        file_path: Path to the CSV file to create
    """
    print("Creating sensors file...")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("alias,variablename,units,postprocess,postprocessscript\n")
        f.write("temperature_sensor,Air Temperature,°C,True,temperature_correction_script\n")
        f.write("humidity_sensor,Relative Humidity,%,False,\n")
        f.write("pressure_sensor,Atmospheric Pressure,hPa,True,pressure_correction_script\n")
        f.write("wind_speed_sensor,Wind Speed,m/s,True,wind_correction_script\n")

    print(f"Created sensors file: {file_path}")


def demonstrate_chunked_upload():
    """Demonstrate chunked upload functionality."""
    print("=== Chunked CSV Upload Example ===\n")

    # Initialize client
    client = UpstreamClient()

    campaign_id = None
    station_id = None

    try:
        # Create campaign
        print("1. Creating campaign...")
        campaign = client.campaigns.create(
            name="Large Dataset Campaign",
            description="Campaign for testing chunked upload functionality",
            geometry="POINT(-97.7431 30.2672)"
        )
        campaign_id = campaign.id
        print(f"   Created campaign: {campaign_id}")

        # Create station
        print("\n2. Creating station...")
        station = client.stations.create(
            campaign_id=campaign_id,
            name="Multi-Sensor Station",
            description="Station with multiple sensors for chunked upload testing",
            geometry="POINT(-97.7431 30.2672)"
        )
        station_id = station.id
        print(f"   Created station: {station_id}")

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as sensors_file:
            sensors_path = sensors_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as measurements_file:
            measurements_path = measurements_file.name

        # Create the CSV files
        create_sensors_file(sensors_path)
        create_large_measurements_file(measurements_path, num_lines=3500)  # Will create 4 chunks with default size

        print(f"\n3. Uploading CSV files with chunked measurements...")
        print(f"   Sensors file: {sensors_path}")
        print(f"   Measurements file: {measurements_path}")
        print(f"   Expected chunks: 4 (1000, 1000, 1000, 500 lines each)")

        start_time = time.time()

        # Upload with default chunk size (1000)
        response = client.sensors.upload_csv_files(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_path,
            measurements_file=measurements_path
        )

        upload_time = time.time() - start_time
        print(f"   Upload completed in {upload_time:.2f} seconds")
        print(f"   Response: {response}")

        # Verify sensors were created
        print("\n4. Verifying uploaded sensors...")
        sensors = client.sensors.list(campaign_id=campaign_id, station_id=station_id)
        print(f"   Created {len(sensors.items)} sensors:")

        for sensor in sensors.items:
            print(f"     - {sensor.alias}: {sensor.variablename} ({sensor.units})")

        # Demonstrate custom chunk size
        print(f"\n5. Demonstrating custom chunk size...")
        print(f"   Creating smaller file for custom chunk size test...")

        # Create a smaller file for custom chunk size test
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as small_measurements_file:
            small_measurements_path = small_measurements_file.name
            create_large_measurements_file(small_measurements_path, num_lines=800)  # Will create 2 chunks with size=500

        print(f"   Uploading with custom chunk size (500 lines per chunk)...")

        start_time = time.time()

        response_custom = client.sensors.upload_csv_files(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_path,
            measurements_file=small_measurements_path,
            chunk_size=500  # Custom chunk size
        )

        upload_time = time.time() - start_time
        print(f"   Upload completed in {upload_time:.2f} seconds")
        print(f"   Response: {response_custom}")

        # Demonstrate bytes input
        print(f"\n6. Demonstrating bytes input with chunking...")

        # Create content as bytes
        sensors_content = (
            "alias,variablename,units,postprocess,postprocessscript\n"
            "bytes_temp_sensor,Air Temperature,°C,True,temp_correction\n"
        ).encode('utf-8')

        # Create measurements content as bytes
        measurements_lines = ["collectiontime,Lat_deg,Lon_deg,bytes_temp_sensor\n"]
        for i in range(1200):  # Will create 3 chunks with size=500
            timestamp = datetime(2024, 1, 1, 0, 0, 0) + timedelta(hours=i % 24)
            lat = 30.2672 + (i * 0.0001) % 0.01
            lon = -97.7431 + (i * 0.0001) % 0.01
            temp = 20.0 + 10 * random.random()
            measurements_lines.append(f"{timestamp.isoformat()},{lat:.6f},{lon:.6f},{temp:.2f}\n")

        measurements_content = ''.join(measurements_lines).encode('utf-8')

        print(f"   Uploading using bytes input with chunk size 500...")

        start_time = time.time()

        response_bytes = client.sensors.upload_csv_files(
            campaign_id=campaign_id,
            station_id=station_id,
            sensors_file=sensors_content,
            measurements_file=measurements_content,
            chunk_size=500
        )

        upload_time = time.time() - start_time
        print(f"   Upload completed in {upload_time:.2f} seconds")
        print(f"   Response: {response_bytes}")

        print(f"\n=== Chunked Upload Example Completed Successfully ===")

    except ValidationError as e:
        print(f"Validation error: {e}")
    except APIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        # Clean up temporary files
        for file_path in [sensors_path, measurements_path, small_measurements_path]:
            try:
                Path(file_path).unlink(missing_ok=True)
            except Exception:
                pass

        # Clean up station
        if station_id:
            try:
                client.stations.delete(station_id, campaign_id)
                print(f"\nCleaned up station: {station_id}")
            except Exception as e:
                print(f"Failed to clean up station: {e}")

        # Clean up campaign
        if campaign_id:
            try:
                client.campaigns.delete(campaign_id)
                print(f"Cleaned up campaign: {campaign_id}")
            except Exception as e:
                print(f"Failed to clean up campaign: {e}")


if __name__ == "__main__":
    demonstrate_chunked_upload()