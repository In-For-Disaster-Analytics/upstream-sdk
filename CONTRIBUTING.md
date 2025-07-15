# Contributing to Upstream Python SDK

Thank you for your interest in contributing to the Upstream Python SDK! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## Getting Started

### Development Environment Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/upstream-python-sdk.git
   cd upstream-python-sdk
   ```

2. **Set up development environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   make install-dev
   # or
   pip install -e ".[dev]"
   pip install -r requirements-dev.txt
   ```

3. **Install pre-commit hooks:**
   ```bash
   make pre-commit
   # or
   pre-commit install
   ```

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below.

3. **Run tests and checks:**
   ```bash
   make dev-check  # Runs lint, type-check, security, and tests
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Code Style

- **Python version:** Support Python 3.8+
- **Code formatting:** Use [Black](https://github.com/psf/black) with line length 88
- **Import sorting:** Use [isort](https://github.com/PyCQA/isort) with Black profile
- **Linting:** Follow [flake8](https://flake8.pycqa.org/) guidelines
- **Type hints:** All functions and methods must have type hints
- **Docstrings:** Use Google-style docstrings

### Code Quality Tools

Run these commands before submitting a PR:

```bash
# Format code
make format

# Check linting
make lint

# Type checking
make type-check

# Security checks
make security

# Run tests
make test
```

### Documentation

- **Docstrings:** All public functions, classes, and methods must have docstrings
- **Type hints:** All parameters and return values must be typed
- **Examples:** Include usage examples in docstrings where helpful
- **API changes:** Update documentation for any API changes

Example docstring format:
```python
def upload_data(self, campaign_id: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Upload sensor data to a campaign.
    
    Args:
        campaign_id: The ID of the target campaign
        data: List of measurement dictionaries
        
    Returns:
        Upload result containing status and metadata
        
    Raises:
        ValidationError: If data format is invalid
        UploadError: If upload fails
        
    Example:
        >>> client = UpstreamClient(username="user", password="pass")
        >>> result = client.upload_data("campaign-123", measurements)
        >>> print(result["upload_id"])
    """
```

## Testing

### Test Types

1. **Unit Tests:** Test individual functions and methods
2. **Integration Tests:** Test component interactions
3. **End-to-end Tests:** Test complete workflows

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names: `test_upload_data_validates_input_format`
- Use pytest fixtures for common test data
- Mock external dependencies in unit tests

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests only
make test-integration

# With coverage
make coverage
```

### Test Coverage

- Maintain minimum 90% test coverage
- New code must include appropriate tests
- Critical paths must have comprehensive test coverage

## Pull Request Process

### Before Submitting

1. **Run all checks:**
   ```bash
   make dev-check
   ```

2. **Update documentation** if needed

3. **Add tests** for new functionality

4. **Update CHANGELOG.md** following [Keep a Changelog](https://keepachangelog.com/) format

### PR Requirements

- **Clear description:** Explain what changes were made and why
- **Tests:** Include appropriate tests for new functionality
- **Documentation:** Update docs for API changes
- **No breaking changes** without discussion
- **Clean commit history:** Squash commits if necessary

### Review Process

1. All automated checks must pass
2. At least one maintainer review required
3. Address review feedback promptly
4. Maintain professional, constructive discussion

## Issue Reporting

### Bug Reports

When reporting bugs, include:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, SDK version)
- **Code example** that demonstrates the issue
- **Error messages** or stack traces

### Feature Requests

When requesting features, include:

- **Clear description** of the proposed feature
- **Use case** explaining why it's needed
- **Proposed API** if applicable
- **Alternative solutions** considered

## Development Guidelines

### API Design

- **Consistency:** Follow existing patterns and conventions
- **Backwards compatibility:** Avoid breaking changes when possible
- **Error handling:** Provide clear, actionable error messages
- **Documentation:** Include comprehensive examples

### Performance

- **Efficiency:** Consider performance implications of changes
- **Memory usage:** Avoid memory leaks and excessive allocations
- **Network calls:** Implement retry logic and rate limiting
- **Large datasets:** Support chunking and streaming where appropriate

### Security

- **Input validation:** Validate all user inputs
- **Authentication:** Handle credentials securely
- **Dependencies:** Keep dependencies up to date
- **Secrets:** Never commit secrets or credentials

## Release Process

### Version Management

- Follow [Semantic Versioning](https://semver.org/)
- Update version in `pyproject.toml`
- Update `CHANGELOG.md` with release notes

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Build and test package
5. Create release tag
6. Publish to PyPI

## Getting Help

- **Documentation:** Check the [documentation](https://upstream-python-sdk.readthedocs.io)
- **Issues:** Search existing issues before creating new ones
- **Discussions:** Use GitHub Discussions for questions
- **Email:** Contact maintainers for security issues

## Recognition

Contributors will be acknowledged in:
- CHANGELOG.md for significant contributions
- README.md contributors section
- GitHub releases

Thank you for contributing to the Upstream Python SDK!