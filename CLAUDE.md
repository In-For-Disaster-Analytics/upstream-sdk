# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Configuration Memories

- Configuration with manual credential fallback should be implemented in Jupyter notebooks @UpstreamSDK_Core_Demo.ipynb and @UpstreamSDK_CKAN_Demo.ipynb
- BASE_URL can be dynamically set between production (https://api.upstream-dso.tacc.utexas.edu/dev) and local development (http://localhost:8000)
- Print statement for configuration settings suggests manual credential input fallback mechanism in Jupyter notebooks @UpstreamSDK_Core_Demo.ipynb @UpstreamSDK_CKAN_Demo.ipynb

## Development Commands

### Environment Setup
```bash
# Development installation (editable mode)
pip install -e .
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### Testing Commands
```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit                    # Unit tests only
pytest -m integration             # Integration tests only
pytest -m "not slow"              # Skip slow tests

# Run with coverage
pytest --cov=upstream --cov-report=html

# Run specific test file
pytest tests/unit/test_ckan_unit.py

# Run tests with network access (skipped by default)
pytest --run-network

# Run integration tests (requires credentials)
pytest --run-integration
```

### Code Quality Commands
```bash
# Format code
black .

# Check imports
isort --profile=black .

# Lint code
flake8 .
ruff check . --fix

# Type checking
mypy upstream

# Security check
bandit -r . -x tests

# Run all pre-commit hooks
pre-commit run --all-files
```

### Build and Documentation
```bash
# Build package
python -m build

# Build documentation
sphinx-build -b html docs docs/_build/html

# Test across Python versions
tox
```

## Core Architecture

### Client Architecture
The SDK follows a modular manager pattern centered around `UpstreamClient`:

- **UpstreamClient**: Main entry point with unified authentication and CKAN integration
- **Manager Classes**: Specialized managers for different API domains
  - `CampaignManager`: Campaign lifecycle management
  - `StationManager`: Station creation and management  
  - `SensorManager`: Sensor data operations
  - `MeasurementManager`: Measurement data handling
  - `DataUploader`: CSV data upload with chunking
- **CKANIntegration**: Separate module for CKAN portal publishing

### Authentication Flow
- `AuthManager` handles token-based authentication with automatic refresh
- `ConfigManager` supports multiple configuration sources (file, env vars, direct params)
- Client initialization can use config files, environment variables, or direct parameters

### Data Upload Architecture
The data upload system uses a chunked approach for handling large datasets:

- **DataUploader**: Manages CSV file processing and upload
- **DataValidator**: Validates CSV format and content
- Automatic chunking for large files (configurable chunk size)
- Progress tracking and error recovery

### CKAN Integration
- **CKANIntegration**: Complete CKAN portal integration
- Automatic dataset creation with rich metadata
- Custom metadata support for datasets and resources
- Resource management (sensors.csv, measurements.csv)
- JSON serialization with size limits for Solr compatibility

### Configuration System
Multi-layer configuration with precedence:
1. Direct constructor parameters
2. Configuration file (YAML/JSON)
3. Environment variables
4. Default values

Required environment variables for integration tests:
- `UPSTREAM_USERNAME`, `UPSTREAM_PASSWORD`, `UPSTREAM_BASE_URL`
- `CKAN_URL`, `CKAN_ORGANIZATION` (optional: `CKAN_API_KEY`)

### Exception Hierarchy
- `UpstreamError`: Base exception
- `APIError`: API communication errors
- `AuthenticationError`: Authentication failures
- `ValidationError`: Data validation errors
- `UploadError`: Data upload failures
- `ConfigurationError`: Configuration issues

### Demo Notebooks
- **UpstreamSDK_Core_Demo.ipynb**: Complete core functionality walkthrough
- **UpstreamSDK_CKAN_Demo.ipynb**: CKAN integration and publishing workflow

Both notebooks demonstrate production-ready patterns and include comprehensive error handling examples.

## Data Model Requirements

### CSV Format Expectations
**Sensors CSV**: `alias,variablename,units,postprocess,postprocessscript`
**Measurements CSV**: `collectiontime,Lat_deg,Lon_deg,<sensor_aliases>`

The system expects ISO format timestamps and geographic coordinates for all measurements.

## Integration Points

### Upstream API Client
Built on `upstream-api-client` OpenAPI-generated client with Pydantic models:
- `CampaignsIn`, `StationCreate` for input validation
- `GetCampaignResponse`, `GetStationResponse` for API responses
- Automatic type checking and validation

### CKAN Portal Integration
- Dataset creation with automatic metadata generation
- Resource upload with custom metadata
- Organization-based publishing
- Tag-based discovery and categorization

## Testing Strategy

- **Unit Tests**: Mock-based testing for individual components
- **Integration Tests**: Real API testing (requires credentials)
- **Fixtures**: Comprehensive test data in `conftest.py`
- **Network Tests**: Skipped by default, run with `--run-network`
- **Coverage**: Configured for 90%+ coverage excluding test files

## Special Configuration Notes

The notebooks use a fallback credential pattern:
1. Try loading from `config.yaml`
2. Fall back to environment variables
3. Final fallback to interactive input

This pattern should be preserved when modifying notebook configuration code.