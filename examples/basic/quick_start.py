#!/usr/bin/env python3
"""
Upstream SDK Quick Start Example

This example demonstrates the basic usage of the Upstream Python SDK
for environmental sensor data management.
"""

import os
from pathlib import Path

from upstream import UpstreamClient
from upstream.exceptions import UpstreamError


def main() -> None:
    """Main example function."""

    # Initialize the client with credentials
    # In production, use environment variables or config files
    client = UpstreamClient(
        username=os.getenv("UPSTREAM_USERNAME", "your_username"),
        password=os.getenv("UPSTREAM_PASSWORD", "your_password"),
        base_url=os.getenv("UPSTREAM_BASE_URL", "https://upstream-dso.tacc.utexas.edu/dev"),
        ckan_url=os.getenv("CKAN_URL", "https://ckan.tacc.utexas.edu")
    )

    try:
        # Test authentication
        if client.authenticate():
            print("✅ Authentication successful!")
        else:
            print("❌ Authentication failed!")
            return

        # Create a new campaign
        print("\n📊 Creating campaign...")
        campaign = client.create_campaign(
            name="Example Air Quality Campaign",
            description="Demonstration campaign for SDK usage"
        )
        print(f"Created campaign: (ID: {campaign.id})")

        # Create a monitoring station
        print("\n📍 Creating station...")
        station = client.create_station(
            campaign_id=campaign.id,
            name="Downtown Monitor",
            latitude=30.2672,
            longitude=-97.7431,
            description="City center air quality monitoring station",
            contact_name="Dr. Jane Smith",
            contact_email="jane.smith@example.edu"
        )
        print(f"Created station: (ID: {station.id})")

        # Example data upload (if CSV files exist)
        sensors_file = Path("example_data/sensors.csv")
        measurements_file = Path("example_data/measurements.csv")

        if sensors_file.exists() and measurements_file.exists():
            print("\n📤 Uploading data...")
            result = client.upload_csv_data(
                campaign_id=campaign.id,
                station_id=station.id,
                sensors_file=sensors_file,
                measurements_file=measurements_file
            )
            print(f"Upload successful! Upload ID: {result.get('upload_id')}")

            # Publish to CKAN if configured
            if client.ckan:
                print("\n🌐 Publishing to CKAN...")
                ckan_result = client.publish_to_ckan(
                    campaign_id=campaign.id,
                    sensors_url=f"https://example.com/data/sensors.csv",
                    measurements_url=f"https://example.com/data/measurements.csv"
                )
                print(f"Published to CKAN: {ckan_result.get('ckan_url')}")
        else:
            print(f"\n⚠️  Example data files not found:")
            print(f"   {sensors_file}")
            print(f"   {measurements_file}")
            print("   Skipping data upload demonstration.")

        # List campaigns and stations
        print("\n📋 Listing campaigns...")
        campaigns = client.list_campaigns()
        for camp in campaigns.items[:3]:  # Show first 3
            print(f"  - {camp.id} {camp.name}")

        print(f"\n📋 Listing stations for campaign {campaign.id}...")
        stations = client.list_stations(campaign_id=campaign.id)
        for stat in stations.items:
            print(f"  - {stat.id} {stat.name}")

        print("\n🎉 Example completed successfully!")

    except UpstreamError as e:
        print(f"❌ Upstream SDK Error: {e}")
        if hasattr(e, 'details') and e.details:
            print(f"   Details: {e.details}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Clean up authentication
        client.logout()
        print("\n👋 Logged out successfully")


if __name__ == "__main__":
    main()