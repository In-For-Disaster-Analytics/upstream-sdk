#!/usr/bin/env python3
"""
Simple test script to verify chunked upload functionality.
"""

import tempfile
import os
from pathlib import Path

from upstream.sensors import SensorManager
from upstream.auth import AuthManager
from upstream.exceptions import ValidationError


def test_chunking_functionality():
    """Test the chunking functionality without API calls."""
    print("Testing chunking functionality...")

    # Create a mock auth manager
    auth_manager = None  # We don't need real auth for this test

    # Create sensor manager
    sensor_manager = SensorManager(auth_manager)

    # Create a temporary measurements file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write("collectiontime,Lat_deg,Lon_deg,temp_sensor,humidity_sensor\n")
        for i in range(2500):
            timestamp = f"2024-01-{(i % 30) + 1:02d}T{(i % 24):02d}:{(i % 60):02d}:00"
            lat = 30.2672 + (i * 0.0001)
            lon = -97.7431 + (i * 0.0001)
            temp = 20.0 + (i % 10)
            humidity = 50.0 + (i % 20)
            f.write(f"{timestamp},{lat:.6f},{lon:.6f},{temp:.1f},{humidity:.1f}\n")
        file_path = f.name

    try:
        # Test with default chunk size (1000)
        print(f"Testing with default chunk size (1000)...")
        chunks = sensor_manager._split_measurements_file(file_path, 1000)

        print(f"Created {len(chunks)} chunks:")
        for i, chunk in enumerate(chunks):
            chunk_content = chunk[1].decode('utf-8')
            chunk_lines = chunk_content.splitlines()
            print(f"  Chunk {i+1}: {chunk[0]} - {len(chunk_lines)} lines")

        # Test with custom chunk size (500)
        print(f"\nTesting with custom chunk size (500)...")
        chunks_custom = sensor_manager._split_measurements_file(file_path, 500)

        print(f"Created {len(chunks_custom)} chunks:")
        for i, chunk in enumerate(chunks_custom):
            chunk_content = chunk[1].decode('utf-8')
            chunk_lines = chunk_content.splitlines()
            print(f"  Chunk {i+1}: {chunk[0]} - {len(chunk_lines)} lines")

        # Test with bytes input
        print(f"\nTesting with bytes input...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content_bytes = content.encode('utf-8')

        chunks_bytes = sensor_manager._split_measurements_file(content_bytes, 750)

        print(f"Created {len(chunks_bytes)} chunks from bytes:")
        for i, chunk in enumerate(chunks_bytes):
            chunk_content = chunk[1].decode('utf-8')
            chunk_lines = chunk_content.splitlines()
            print(f"  Chunk {i+1}: {chunk[0]} - {len(chunk_lines)} lines")

        print("\n✅ All chunking tests passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise

    finally:
        # Clean up
        Path(file_path).unlink(missing_ok=True)


def test_error_handling():
    """Test error handling in chunking functionality."""
    print("\nTesting error handling...")

    auth_manager = None
    sensor_manager = SensorManager(auth_manager)

    # Test with nonexistent file
    try:
        sensor_manager._split_measurements_file("nonexistent_file.csv", 1000)
        print("❌ Should have raised ValidationError for nonexistent file")
    except ValidationError as e:
        print(f"✅ Correctly caught ValidationError: {e}")

    # Test with empty file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write("collectiontime,Lat_deg,Lon_deg,temp_sensor\n")
        file_path = f.name

    try:
        sensor_manager._split_measurements_file(file_path, 1000)
        print("❌ Should have raised ValidationError for empty file")
    except ValidationError as e:
        print(f"✅ Correctly caught ValidationError: {e}")
    finally:
        Path(file_path).unlink(missing_ok=True)

    # Test with invalid input type
    try:
        sensor_manager._split_measurements_file(123, 1000)
        print("❌ Should have raised ValidationError for invalid type")
    except ValidationError as e:
        print(f"✅ Correctly caught ValidationError: {e}")

    print("✅ All error handling tests passed!")


if __name__ == "__main__":
    print("=== Chunked Upload Functionality Test ===\n")

    test_chunking_functionality()
    test_error_handling()

    print("\n=== All tests completed successfully! ===")