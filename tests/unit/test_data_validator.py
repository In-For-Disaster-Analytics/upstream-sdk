from pathlib import Path

import pytest

from upstream.data import DataValidator
from upstream.exceptions import ValidationError


def _write_bom_sensors_csv(path: Path) -> None:
    content = "\ufeffalias,variablename,units\nsensor_01,Temperature,C\n"
    path.write_text(content, encoding="utf-8")


def test_validate_csv_file_accepts_utf8_bom_in_headers(tmp_path, mock_config):
    sensors_csv = tmp_path / "sensors.csv"
    _write_bom_sensors_csv(sensors_csv)

    validator = DataValidator(mock_config)
    result = validator.validate_csv_file(sensors_csv, "sensors")

    assert result["valid"] is True
    assert result["sensor_count"] == 1


def test_validate_csv_file_rejects_missing_required_fields(tmp_path, mock_config):
    sensors_csv = tmp_path / "sensors_missing.csv"
    sensors_csv.write_text("alias,variablename,units\n,Temperature,C\n", encoding="utf-8")

    validator = DataValidator(mock_config)
    with pytest.raises(ValidationError, match="Missing required field 'alias'"):
        validator.validate_csv_file(sensors_csv, "sensors")
