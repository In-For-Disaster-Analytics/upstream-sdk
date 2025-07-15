# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with modern Python packaging
- Core SDK structure with authentication, campaigns, stations, data upload, and CKAN integration
- Comprehensive test suite with pytest
- Development tooling (pre-commit, tox, GitHub Actions)
- Documentation structure with Sphinx
- Example usage and configuration files

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.0.0] - 2024-01-15

### Added
- Initial release of Upstream Python SDK
- Authentication manager with token handling and refresh
- Campaign management (create, read, update, delete)
- Station management with geolocation support
- Data upload functionality with CSV support and chunking for large files
- CKAN integration for dataset publication
- Comprehensive error handling and validation
- Type hints throughout the codebase
- Google-style docstrings for all public APIs
- Unit and integration test coverage
- CI/CD pipeline with GitHub Actions
- Development environment setup with modern tooling

### Features
- **Authentication**: Secure token-based authentication with automatic refresh
- **Campaign Management**: Full CRUD operations for environmental monitoring campaigns
- **Station Operations**: Create and manage monitoring stations with GPS coordinates
- **Data Upload**: Support for CSV data upload with automatic validation and chunking
- **CKAN Integration**: Automatic dataset publication to CKAN data portals
- **Configuration Management**: Flexible configuration via files, environment variables, or direct parameters
- **Error Handling**: Comprehensive exception hierarchy with detailed error messages
- **Async Support**: Ready for future async/await implementation
- **Type Safety**: Full type hint coverage for better IDE support and code quality

### Technical Details
- **Python Support**: Python 3.8+ compatibility
- **Dependencies**: Minimal core dependencies (requests, pyyaml, python-dateutil)
- **Testing**: 90%+ test coverage with pytest
- **Code Quality**: Automated formatting with Black, linting with flake8, type checking with mypy
- **Documentation**: Sphinx-based documentation with examples
- **Packaging**: Modern packaging with pyproject.toml and setuptools

### Documentation
- Complete API reference documentation
- Quick start guide with examples
- Configuration guide
- Contributing guidelines
- Security best practices
- Troubleshooting guide

[Unreleased]: https://github.com/In-For-Disaster-Analytics/upstream-python-sdk/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/In-For-Disaster-Analytics/upstream-python-sdk/releases/tag/v1.0.0