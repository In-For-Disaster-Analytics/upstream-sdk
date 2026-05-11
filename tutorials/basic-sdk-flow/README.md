# Upstream SDK Two-Notebook Tutorial

This folder contains a two-step tutorial flow.

## Notebooks

1. `01_register_campaign_station_upload.ipynb`
2. `02_query_visualize_spatiotemporal.ipynb`

## Workflow

1. Run notebook 1 to:
   - connect to Upstream
   - create (or reuse) campaign/station
   - upload example data from `data/`
   - save `outputs/flow_context.json`
2. Run notebook 2 to:
   - load IDs from `outputs/flow_context.json`
   - query measurements
   - visualize spatial distribution with Folium
   - visualize spatiotemporal progression with a Folium time slider

## Data Location

Use:

- `data/sensors.csv`
- `data/measurements.csv`

## Run

```bash
cd /Users/wmobley/Documents/GitHub/upstream/upstream-sdk/tutorials/basic-sdk-flow
jupyter notebook
```

Open notebook `01_...` first, then `02_...`.

## SSL Certificate Issues

If notebook 1 fails with `SSLCertVerificationError: unable to get local issuer
certificate`, reinstall the current SDK in the notebook environment. The SDK
uses `certifi` as its default CA bundle for both direct requests and the
generated OpenAPI client, so no notebook code change is needed.

```bash
python -m pip install --upgrade --force-reinstall -e /Users/wmobley/Documents/GitHub/upstream/upstream-sdk
```

For custom institutional CA bundles, set the path once before starting Jupyter:

```bash
export UPSTREAM_SSL_CA_CERT="/path/to/institutional-ca-bundle.pem"
```

The SDK also honors `REQUESTS_CA_BUNDLE`, `CURL_CA_BUNDLE`, and
`SSL_CERT_FILE`. Avoid setting `verify_ssl=False` except as a temporary
diagnostic check.

## Other Files

- `utils.py`: shared notebook helpers
- `basic_sdk_flow.py`: older CLI flow (optional)
- `.env.example`: optional env template
