#!/usr/bin/env python3
"""
Automated Data Pipeline Example

This example demonstrates how to set up an automated data pipeline
for continuous sensor data collection and upload.
"""

import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

from upstream import UpstreamClient
from upstream.exceptions import UpstreamError, ValidationError, UploadError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class AutomatedPipeline:
    """Automated data pipeline for sensor data collection and upload."""

    def __init__(self, config_file: Path):
        """Initialize the pipeline with configuration."""
        self.client = UpstreamClient.from_config(config_file)
        self.campaign_id = None
        self.station_id = None
        self.upload_interval = 3600  # 1 hour in seconds
        self.max_retries = 3
        self.retry_delay = 300  # 5 minutes

    def setup_campaign_and_station(self) -> None:
        """Set up campaign and station for data collection."""
        try:
            # Create or get campaign
            campaign = self.client.create_campaign(
                name=f"Automated Monitoring {datetime.now().strftime('%Y-%m')}",
                description="Automated environmental monitoring campaign",
            )
            self.campaign_id = campaign.id
            logger.info(f"Campaign ready: {campaign.name} ({campaign.id})")

            # Create or get station
            station = self.client.create_station(
                campaign_id=self.campaign_id,
                name="Automated Weather Station",
                latitude=30.2672,
                longitude=-97.7431,
                description="Automated weather monitoring station",
                contact_name="Pipeline Manager",
                contact_email="pipeline@example.com",
            )
            self.station_id = station.id
            logger.info(f"Station ready: {station.name} ({station.id})")

        except UpstreamError as e:
            logger.error(f"Failed to setup campaign/station: {e}")
            raise

    def collect_sensor_data(self) -> List[Dict[str, Any]]:
        """Simulate sensor data collection."""
        # In a real implementation, this would interface with actual sensors
        current_time = datetime.now().isoformat() + "Z"

        # Simulate multiple sensor readings
        measurements = []
        for i in range(10):  # 10 data points
            timestamp = (datetime.now() - timedelta(minutes=i)).isoformat() + "Z"
            measurements.append(
                {
                    "collectiontime": timestamp,
                    "Lat_deg": 30.2672 + (i * 0.0001),  # Slight variation
                    "Lon_deg": -97.7431 + (i * 0.0001),
                    "temperature": 25.0 + (i * 0.1),
                    "humidity": 60.0 + (i * 0.5),
                    "pressure": 1013.25 + (i * 0.1),
                    "wind_speed": 5.0 + (i * 0.2),
                    "wind_direction": 180 + (i * 2),
                }
            )

        logger.info(f"Collected {len(measurements)} sensor readings")
        return measurements

    def upload_data_with_retry(self, measurements: List[Dict[str, Any]]) -> bool:
        """Upload data with retry logic."""
        for attempt in range(self.max_retries):
            try:
                result = self.client.upload_measurements(
                    campaign_id=self.campaign_id,
                    station_id=self.station_id,
                    data=measurements,
                )

                upload_id = result.get("upload_id")
                logger.info(f"Upload successful: {upload_id}")

                # Monitor upload status
                self.monitor_upload_status(upload_id)
                return True

            except ValidationError as e:
                logger.error(f"Data validation failed: {e}")
                return False  # Don't retry validation errors

            except UploadError as e:
                logger.warning(f"Upload attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("All upload attempts failed")
                    return False

            except Exception as e:
                logger.error(f"Unexpected error during upload: {e}")
                return False

        return False

    def monitor_upload_status(self, upload_id: str) -> None:
        """Monitor the status of an upload."""
        max_checks = 10
        check_interval = 30  # seconds

        for i in range(max_checks):
            try:
                status = self.client.get_upload_status(upload_id)
                upload_status = status.get("status", "unknown")

                logger.info(f"Upload {upload_id} status: {upload_status}")

                if upload_status in ["completed", "success"]:
                    logger.info("Upload processing completed successfully")
                    break
                elif upload_status in ["failed", "error"]:
                    logger.error("Upload processing failed")
                    break
                elif upload_status in ["processing", "pending"]:
                    time.sleep(check_interval)
                else:
                    logger.warning(f"Unknown upload status: {upload_status}")
                    break

            except Exception as e:
                logger.warning(f"Failed to check upload status: {e}")
                break

    def publish_to_ckan_if_configured(self) -> None:
        """Publish data to CKAN if configured."""
        if self.client.ckan:
            try:
                result = self.client.publish_to_ckan(
                    campaign_id=self.campaign_id, auto_publish=True
                )
                ckan_url = result.get("ckan_url")
                logger.info(f"Data published to CKAN: {ckan_url}")

            except Exception as e:
                logger.error(f"CKAN publication failed: {e}")

    def run_single_cycle(self) -> bool:
        """Run a single data collection and upload cycle."""
        try:
            logger.info("Starting data collection cycle...")

            # Collect sensor data
            measurements = self.collect_sensor_data()

            # Upload data
            if self.upload_data_with_retry(measurements):
                # Publish to CKAN if configured
                self.publish_to_ckan_if_configured()
                logger.info("Data cycle completed successfully")
                return True
            else:
                logger.error("Data cycle failed")
                return False

        except Exception as e:
            logger.error(f"Unexpected error in data cycle: {e}")
            return False

    def run_continuous(self) -> None:
        """Run the pipeline continuously."""
        logger.info(f"Starting continuous pipeline (interval: {self.upload_interval}s)")

        # Setup campaign and station
        self.setup_campaign_and_station()

        # Run continuous loop
        while True:
            try:
                cycle_start = time.time()

                # Run data collection cycle
                success = self.run_single_cycle()

                # Calculate next run time
                cycle_duration = time.time() - cycle_start
                sleep_time = max(0, self.upload_interval - cycle_duration)

                if success:
                    logger.info(
                        f"Cycle completed in {cycle_duration:.1f}s. "
                        f"Next cycle in {sleep_time:.1f}s"
                    )
                else:
                    logger.warning(
                        f"Cycle failed in {cycle_duration:.1f}s. "
                        f"Retrying in {sleep_time:.1f}s"
                    )

                time.sleep(sleep_time)

            except KeyboardInterrupt:
                logger.info("Pipeline stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in pipeline: {e}")
                logger.info(f"Continuing in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)

        # Cleanup
        try:
            self.client.logout()
            logger.info("Pipeline shutdown complete")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


def main():
    """Main function to run the automated pipeline."""
    config_file = Path("pipeline_config.yaml")

    if not config_file.exists():
        logger.error(f"Configuration file not found: {config_file}")
        logger.info("Please create a configuration file with your Upstream credentials")
        return

    try:
        pipeline = AutomatedPipeline(config_file)

        # Run a single cycle for testing
        logger.info("Running single test cycle...")
        pipeline.setup_campaign_and_station()
        success = pipeline.run_single_cycle()

        if success:
            logger.info("Test cycle successful!")

            # Ask user if they want to run continuously
            response = input("Run pipeline continuously? (y/N): ")
            if response.lower() in ["y", "yes"]:
                pipeline.run_continuous()
        else:
            logger.error("Test cycle failed!")

    except Exception as e:
        logger.error(f"Pipeline failed to start: {e}")


if __name__ == "__main__":
    main()
