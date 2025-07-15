.PHONY: help install install-dev clean test test-unit test-integration coverage lint format type-check security docs docs-serve build publish pre-commit

# Default target
help:
	@echo "Available targets:"
	@echo "  install       Install package in development mode"
	@echo "  install-dev   Install package with development dependencies"
	@echo "  clean         Clean build artifacts"
	@echo "  test          Run all tests"
	@echo "  test-unit     Run unit tests only"
	@echo "  test-integration  Run integration tests only"
	@echo "  coverage      Run tests with coverage report"
	@echo "  lint          Run linting checks"
	@echo "  format        Format code with black and isort"
	@echo "  type-check    Run type checking with mypy"
	@echo "  security      Run security checks"
	@echo "  docs          Build documentation"
	@echo "  docs-serve    Serve documentation with auto-reload"
	@echo "  build         Build package"
	@echo "  publish       Publish package to PyPI"
	@echo "  pre-commit    Install pre-commit hooks"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	pytest

test-unit:
	pytest tests/unit/

test-integration:
	pytest tests/integration/

coverage:
	pytest --cov=upstream --cov-report=html --cov-report=term-missing

lint:
	flake8 upstream tests
	black --check upstream tests
	isort --check-only upstream tests

format:
	black upstream tests
	isort upstream tests

type-check:
	mypy upstream

security:
	bandit -r upstream
	safety check

docs:
	cd docs && make html

docs-serve:
	cd docs && make livehtml

build:
	python -m build

publish:
	twine upload dist/*

pre-commit:
	pre-commit install
	pre-commit run --all-files

# Development workflow targets
dev-setup: install-dev pre-commit
	@echo "Development environment setup complete!"

dev-check: lint type-check security test
	@echo "All development checks passed!"

# CI-like targets
ci-test:
	pytest --cov=upstream --cov-report=xml --cov-report=term-missing

ci-build: clean build
	twine check dist/*

# Release workflow
release-check: clean dev-check docs build
	@echo "Release checks complete!"

# Utility targets
show-deps:
	pip list

show-outdated:
	pip list --outdated

update-deps:
	pip install --upgrade pip
	pip install --upgrade -r requirements-dev.txt