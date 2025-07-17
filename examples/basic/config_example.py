#!/usr/bin/env python3
"""
Upstream SDK Configuration Example

This example demonstrates different ways to configure the Upstream SDK.
"""

import os
from pathlib import Path
import tempfile

from upstream import UpstreamClient
from upstream.utils import ConfigManager


def example_environment_config():
    """Example using environment variables."""
    print("📝 Configuration from environment variables:")

    # Set environment variables (in practice, these would be set in your shell)
    os.environ.update(
        {
            "UPSTREAM_USERNAME": "your_username",
            "UPSTREAM_PASSWORD": "your_password",
            "UPSTREAM_BASE_URL": "https://upstream-dso.tacc.utexas.edu/dev",
            "CKAN_URL": "https://ckan.tacc.utexas.edu",
        }
    )

    # Create client from environment
    client = UpstreamClient.from_environment()
    print(f"   Base URL: {client.auth_manager.config.base_url}")
    print(f"   Username: {client.auth_manager.config.username}")
    print(f"   CKAN URL: {client.auth_manager.config.ckan_url}")


def example_config_file():
    """Example using configuration file."""
    print("\n📄 Configuration from file:")

    # Create example config file
    config_content = """
upstream:
  username: your_username
  password: your_password
  base_url: https://upstream-dso.tacc.utexas.edu/dev

ckan:
  url: https://ckan.tacc.utexas.edu
  auto_publish: true
  default_organization: your-org

upload:
  chunk_size: 10000
  max_file_size_mb: 50
  timeout_seconds: 300
  retry_attempts: 3
"""

    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(config_content)
        config_path = f.name

    try:
        # Create client from config file
        client = UpstreamClient.from_config(config_path)
        print(f"   Base URL: {client.auth_manager.config.base_url}")
        print(f"   Username: {client.auth_manager.config.username}")
        print(f"   Chunk size: {client.auth_manager.config.chunk_size}")
        print(f"   Max retries: {client.auth_manager.config.max_retries}")

    finally:
        # Clean up temp file
        os.unlink(config_path)


def example_direct_config():
    """Example using direct configuration."""
    print("\n⚙️  Direct configuration:")

    client = UpstreamClient(
        username="your_username",
        password="your_password",
        base_url="https://upstream-dso.tacc.utexas.edu/dev",
        ckan_url="https://ckan.tacc.utexas.edu",
    )

    print(f"   Base URL: {client.auth_manager.config.base_url}")
    print(f"   Username: {client.auth_manager.config.username}")
    print(f"   CKAN URL: {client.auth_manager.config.ckan_url}")


def example_config_manager():
    """Example using ConfigManager directly."""
    print("\n🔧 Using ConfigManager:")

    # Create configuration manager
    config = ConfigManager(
        username="your_username",
        password="your_password",
        base_url="https://upstream-dso.tacc.utexas.edu/dev",
        ckan_url="https://ckan.tacc.utexas.edu",
        timeout=60,
        max_retries=5,
        chunk_size=5000,
    )

    print(f"   Base URL: {config.base_url}")
    print(f"   Username: {config.username}")
    print(f"   Timeout: {config.timeout}s")
    print(f"   Max retries: {config.max_retries}")
    print(f"   Chunk size: {config.chunk_size}")

    # Save configuration to file
    config_path = Path("example_config.yaml")
    config.save(config_path)
    print(f"   Configuration saved to: {config_path}")

    # Load configuration from file
    loaded_config = ConfigManager.from_file(config_path)
    print(f"   Loaded base URL: {loaded_config.base_url}")

    # Clean up
    config_path.unlink()


def main():
    """Main example function."""
    print("🚀 Upstream SDK Configuration Examples\n")

    try:
        example_environment_config()
        example_config_file()
        example_direct_config()
        example_config_manager()

        print("\n✅ All configuration examples completed!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
