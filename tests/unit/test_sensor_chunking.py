"""
Unit tests for sensor chunking functionality.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from upstream.auth import AuthManager
from upstream.data import DataUploader
from upstream.exceptions import ValidationError


class TestSensorChunking:
    """Test sensor chunking functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.auth_manager = Mock(spec=AuthManager)
        self.auth_manager.config = Mock()
        self.data_uploader = DataUploader(self.auth_manager)

    def test_split_measurements_file_path(self):
        """Test splitting measurements file from file path."""
        # Create a temporary file with 2500 lines
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write("collectiontime,Lat_deg,Lon_deg,temp_sensor\n")
            for i in range(2500):
                f.write(f"2024-01-01T{i%24:02d}:00:00,30.2672,-97.7431,{20.0 + i%10}\n")
            file_path = f.name

        try:
            # Test with default chunk size (1000)
            chunks = self.data_uploader._split_measurements_file(file_path, 1000)

            assert len(chunks) == 3  # Should create 3 chunks: 1000, 1000, 500
            assert "_1.csv" in chunks[0][0]
            assert "_2.csv" in chunks[1][0]
            assert "_3.csv" in chunks[2][0]

            # Verify chunk contents
            chunk1_content = chunks[0][1].decode("utf-8")
            chunk1_lines = chunk1_content.splitlines()
            assert len(chunk1_lines) == 1001  # Header + 1000 data lines

            chunk2_content = chunks[1][1].decode("utf-8")
            chunk2_lines = chunk2_content.splitlines()
            assert len(chunk2_lines) == 1001  # Header + 1000 data lines

            chunk3_content = chunks[2][1].decode("utf-8")
            chunk3_lines = chunk3_content.splitlines()
            assert len(chunk3_lines) == 501  # Header + 500 data lines

            # Verify headers are present in all chunks
            assert chunk1_lines[0] == "collectiontime,Lat_deg,Lon_deg,temp_sensor"
            assert chunk2_lines[0] == "collectiontime,Lat_deg,Lon_deg,temp_sensor"
            assert chunk3_lines[0] == "collectiontime,Lat_deg,Lon_deg,temp_sensor"

        finally:
            Path(file_path).unlink(missing_ok=True)

    def test_split_measurements_file_bytes(self):
        """Test splitting measurements file from bytes input."""
        # Create content as bytes
        content_lines = ["collectiontime,Lat_deg,Lon_deg,temp_sensor\n"]
        for i in range(1500):
            content_lines.append(
                f"2024-01-01T{i%24:02d}:00:00,30.2672,-97.7431,{20.0 + i%10}\n"
            )

        content_bytes = "".join(content_lines).encode("utf-8")

        # Test with custom chunk size (500)
        chunks = self.data_uploader._split_measurements_file(content_bytes, 500)

        assert len(chunks) == 3  # Should create 3 chunks: 500, 500, 500
        assert "_1.csv" in chunks[0][0]
        assert "_2.csv" in chunks[1][0]
        assert "_3.csv" in chunks[2][0]

        # Verify chunk contents
        for i, chunk in enumerate(chunks):
            chunk_content = chunk[1].decode("utf-8")
            chunk_lines = chunk_content.splitlines()
            assert len(chunk_lines) == 501  # Header + 500 data lines
            assert chunk_lines[0] == "collectiontime,Lat_deg,Lon_deg,temp_sensor"

    def test_split_measurements_file_tuple(self):
        """Test splitting measurements file from tuple input."""
        # Create content as tuple (filename, bytes)
        content_lines = ["collectiontime,Lat_deg,Lon_deg,temp_sensor\n"]
        for i in range(800):
            content_lines.append(
                f"2024-01-01T{i%24:02d}:00:00,30.2672,-97.7431,{20.0 + i%10}\n"
            )

        content_bytes = "".join(content_lines).encode("utf-8")
        file_tuple = ("test_measurements.csv", content_bytes)

        # Test with custom chunk size (300)
        chunks = self.data_uploader._split_measurements_file(file_tuple, 300)

        assert len(chunks) == 3  # Should create 3 chunks: 300, 300, 200
        assert "_1.csv" in chunks[0][0]
        assert "_2.csv" in chunks[1][0]
        assert "_3.csv" in chunks[2][0]

        # Verify chunk contents
        chunk1_content = chunks[0][1].decode("utf-8")
        chunk1_lines = chunk1_content.splitlines()
        assert len(chunk1_lines) == 301  # Header + 300 data lines

        chunk2_content = chunks[1][1].decode("utf-8")
        chunk2_lines = chunk2_content.splitlines()
        assert len(chunk2_lines) == 301  # Header + 300 data lines

        chunk3_content = chunks[2][1].decode("utf-8")
        chunk3_lines = chunk3_content.splitlines()
        assert len(chunk3_lines) == 201  # Header + 200 data lines

    def test_split_measurements_file_empty(self):
        """Test splitting empty measurements file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write("collectiontime,Lat_deg,Lon_deg,temp_sensor\n")
            file_path = f.name

        try:
            assert self.data_uploader._split_measurements_file(file_path, 1000) == [
                ("", b"")
            ]
        finally:
            Path(file_path).unlink(missing_ok=True)

    def test_split_measurements_file_invalid_format(self):
        """Test splitting measurements file with invalid format."""
        with pytest.raises(ValidationError, match="Invalid measurements file format"):
            self.data_uploader._split_measurements_file(123, 1000)  # Invalid type

    def test_split_measurements_file_nonexistent(self):
        """Test splitting nonexistent measurements file."""
        with pytest.raises(ValidationError, match="Measurements file not found"):
            self.data_uploader._split_measurements_file("nonexistent_file.csv", 1000)

    def test_split_measurements_file_invalid_encoding(self):
        """Test splitting measurements file with invalid encoding."""
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
            f.write(b"collectiontime,Lat_deg,Lon_deg,temp_sensor\n")
            f.write(b"2024-01-01T00:00:00,30.2672,-97.7431,20.0\n")
            # Add some invalid UTF-8 bytes
            f.write(b"\xff\xfe\xfd\n")
            file_path = f.name

        try:
            with pytest.raises(
                ValidationError, match="Failed to decode measurements file"
            ):
                self.data_uploader._split_measurements_file(file_path, 1000)
        finally:
            Path(file_path).unlink(missing_ok=True)

    def test_split_measurements_file_small_chunk_size(self):
        """Test splitting with very small chunk size."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write("collectiontime,Lat_deg,Lon_deg,temp_sensor\n")
            for i in range(10):
                f.write(f"2024-01-01T{i%24:02d}:00:00,30.2672,-97.7431,{20.0 + i%10}\n")
            file_path = f.name

        try:
            # Test with chunk size smaller than total lines
            chunks = self.data_uploader._split_measurements_file(file_path, 3)

            assert len(chunks) == 4  # Should create 4 chunks: 3, 3, 3, 1
            assert "_1.csv" in chunks[0][0]
            assert "_2.csv" in chunks[1][0]
            assert "_3.csv" in chunks[2][0]
            assert "_4.csv" in chunks[3][0]

            # Verify chunk contents
            for i, chunk in enumerate(chunks[:-1]):
                chunk_content = chunk[1].decode("utf-8")
                chunk_lines = chunk_content.splitlines()
                assert len(chunk_lines) == 4  # Header + 3 data lines

            # Last chunk should have 1 data line
            last_chunk_content = chunks[-1][1].decode("utf-8")
            last_chunk_lines = last_chunk_content.splitlines()
            assert len(last_chunk_lines) == 2  # Header + 1 data line

        finally:
            Path(file_path).unlink(missing_ok=True)
