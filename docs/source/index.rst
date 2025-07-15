Upstream Python SDK Documentation
==================================

Welcome to the Upstream Python SDK documentation! This package provides a comprehensive Python interface for interacting with the Upstream environmental sensor data platform and CKAN data portals.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api/index
   configuration
   examples/index
   contributing
   changelog

Overview
--------

The Upstream Python SDK enables environmental researchers and organizations to:

* **Authenticate** with Upstream API and CKAN data portals
* **Manage** environmental monitoring campaigns and stations
* **Upload** sensor data efficiently with automatic chunking for large datasets
* **Publish** datasets automatically to CKAN for discoverability
* **Automate** data pipelines for continuous sensor networks

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install upstream-sdk

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from upstream import UpstreamClient

   # Initialize client
   client = UpstreamClient(
       username="your_username",
       password="your_password",
       base_url="https://upstream-dso.tacc.utexas.edu/dev"
   )

   # Create campaign and station
   campaign = client.create_campaign("Hurricane Monitoring 2024")
   station = client.create_station(
       campaign.id, 
       name="Galveston Pier", 
       latitude=29.3, 
       longitude=-94.8
   )

   # Upload sensor data
   result = client.upload_csv_data(
       campaign_id=campaign.id,
       station_id=station.id,
       sensors_file="sensors.csv",
       measurements_file="measurements.csv"
   )

   print(f"Data uploaded successfully: {result['upload_id']}")

Key Features
------------

🔐 **Unified Authentication**
   Seamless integration with Upstream API and Tapis/CKAN with automatic token management

📊 **Complete Data Workflow**
   From campaign creation to data publication, handle the entire workflow

🚀 **Production-Ready**
   Automatic chunking, retry mechanisms, comprehensive error handling, and progress tracking

🔄 **Automation-Friendly**
   Perfect for automated sensor networks and scheduled data uploads

API Reference
-------------

.. autosummary::
   :toctree: api/
   :recursive:

   upstream

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`