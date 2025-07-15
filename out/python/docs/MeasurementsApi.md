# openapi_client.MeasurementsApi

All URIs are relative to */dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_measurement_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_post**](MeasurementsApi.md#create_measurement_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_post) | **POST** /api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/measurements | Create Measurement
[**delete_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_delete**](MeasurementsApi.md#delete_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_delete) | **DELETE** /api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/measurements | Delete Sensor Measurements
[**get_measurements_with_confidence_intervals_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_confidence_intervals_get**](MeasurementsApi.md#get_measurements_with_confidence_intervals_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_confidence_intervals_get) | **GET** /api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/measurements/confidence-intervals | Get Measurements With Confidence Intervals
[**get_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_get**](MeasurementsApi.md#get_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_get) | **GET** /api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/measurements | Get Sensor Measurements
[**partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_patch**](MeasurementsApi.md#partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_patch) | **PATCH** /api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/measurements/{measurement_id} | Partial Update Sensor
[**update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_put**](MeasurementsApi.md#update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_put) | **PUT** /api/v1/campaigns/{campaign_id}/stations/{station_id}/sensors/{sensor_id}/measurements/{measurement_id} | Update Sensor


# **create_measurement_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_post**
> MeasurementCreateResponse create_measurement_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_post(station_id, sensor_id, campaign_id, measurement_in)

Create Measurement

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.measurement_create_response import MeasurementCreateResponse
from openapi_client.models.measurement_in import MeasurementIn
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /dev
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "/dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.MeasurementsApi(api_client)
    station_id = 56 # int | 
    sensor_id = 56 # int | 
    campaign_id = 56 # int | 
    measurement_in = openapi_client.MeasurementIn() # MeasurementIn | 

    try:
        # Create Measurement
        api_response = api_instance.create_measurement_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_post(station_id, sensor_id, campaign_id, measurement_in)
        print("The response of MeasurementsApi->create_measurement_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MeasurementsApi->create_measurement_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **station_id** | **int**|  | 
 **sensor_id** | **int**|  | 
 **campaign_id** | **int**|  | 
 **measurement_in** | [**MeasurementIn**](MeasurementIn.md)|  | 

### Return type

[**MeasurementCreateResponse**](MeasurementCreateResponse.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_delete**
> delete_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_delete(campaign_id, station_id, sensor_id)

Delete Sensor Measurements

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /dev
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "/dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.MeasurementsApi(api_client)
    campaign_id = 56 # int | 
    station_id = 56 # int | 
    sensor_id = 56 # int | 

    try:
        # Delete Sensor Measurements
        api_instance.delete_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_delete(campaign_id, station_id, sensor_id)
    except Exception as e:
        print("Exception when calling MeasurementsApi->delete_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 
 **station_id** | **int**|  | 
 **sensor_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_measurements_with_confidence_intervals_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_confidence_intervals_get**
> List[AggregatedMeasurement] get_measurements_with_confidence_intervals_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_confidence_intervals_get(campaign_id, station_id, sensor_id, interval=interval, interval_value=interval_value, start_date=start_date, end_date=end_date, min_value=min_value, max_value=max_value)

Get Measurements With Confidence Intervals

Get sensor measurements with confidence intervals for visualization.

### Example


```python
import openapi_client
from openapi_client.models.aggregated_measurement import AggregatedMeasurement
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /dev
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "/dev"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.MeasurementsApi(api_client)
    campaign_id = 56 # int | 
    station_id = 56 # int | 
    sensor_id = 56 # int | 
    interval = 'hour' # str | Time interval for aggregation (minute, hour, day) (optional) (default to 'hour')
    interval_value = 1 # int | Multiple of interval (e.g., 15 for 15-minute intervals) (optional) (default to 1)
    start_date = '2013-10-20T19:20:30+01:00' # datetime | Start date for filtering measurements (optional)
    end_date = '2013-10-20T19:20:30+01:00' # datetime | End date for filtering measurements (optional)
    min_value = 3.4 # float | Minimum measurement value to include (optional)
    max_value = 3.4 # float | Maximum measurement value to include (optional)

    try:
        # Get Measurements With Confidence Intervals
        api_response = api_instance.get_measurements_with_confidence_intervals_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_confidence_intervals_get(campaign_id, station_id, sensor_id, interval=interval, interval_value=interval_value, start_date=start_date, end_date=end_date, min_value=min_value, max_value=max_value)
        print("The response of MeasurementsApi->get_measurements_with_confidence_intervals_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_confidence_intervals_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MeasurementsApi->get_measurements_with_confidence_intervals_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_confidence_intervals_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 
 **station_id** | **int**|  | 
 **sensor_id** | **int**|  | 
 **interval** | **str**| Time interval for aggregation (minute, hour, day) | [optional] [default to &#39;hour&#39;]
 **interval_value** | **int**| Multiple of interval (e.g., 15 for 15-minute intervals) | [optional] [default to 1]
 **start_date** | **datetime**| Start date for filtering measurements | [optional] 
 **end_date** | **datetime**| End date for filtering measurements | [optional] 
 **min_value** | **float**| Minimum measurement value to include | [optional] 
 **max_value** | **float**| Maximum measurement value to include | [optional] 

### Return type

[**List[AggregatedMeasurement]**](AggregatedMeasurement.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_get**
> ListMeasurementsResponsePagination get_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_get(campaign_id, station_id, sensor_id, start_date=start_date, end_date=end_date, min_measurement_value=min_measurement_value, max_measurement_value=max_measurement_value, limit=limit, page=page, downsample_threshold=downsample_threshold)

Get Sensor Measurements

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.list_measurements_response_pagination import ListMeasurementsResponsePagination
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /dev
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "/dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.MeasurementsApi(api_client)
    campaign_id = 56 # int | 
    station_id = 56 # int | 
    sensor_id = 56 # int | 
    start_date = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    end_date = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    min_measurement_value = 3.4 # float |  (optional)
    max_measurement_value = 3.4 # float |  (optional)
    limit = 1000 # int |  (optional) (default to 1000)
    page = 1 # int |  (optional) (default to 1)
    downsample_threshold = 56 # int |  (optional)

    try:
        # Get Sensor Measurements
        api_response = api_instance.get_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_get(campaign_id, station_id, sensor_id, start_date=start_date, end_date=end_date, min_measurement_value=min_measurement_value, max_measurement_value=max_measurement_value, limit=limit, page=page, downsample_threshold=downsample_threshold)
        print("The response of MeasurementsApi->get_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MeasurementsApi->get_sensor_measurements_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 
 **station_id** | **int**|  | 
 **sensor_id** | **int**|  | 
 **start_date** | **datetime**|  | [optional] 
 **end_date** | **datetime**|  | [optional] 
 **min_measurement_value** | **float**|  | [optional] 
 **max_measurement_value** | **float**|  | [optional] 
 **limit** | **int**|  | [optional] [default to 1000]
 **page** | **int**|  | [optional] [default to 1]
 **downsample_threshold** | **int**|  | [optional] 

### Return type

[**ListMeasurementsResponsePagination**](ListMeasurementsResponsePagination.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_patch**
> MeasurementCreateResponse partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_patch(campaign_id, station_id, sensor_id, measurement_id, measurement_update)

Partial Update Sensor

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.measurement_create_response import MeasurementCreateResponse
from openapi_client.models.measurement_update import MeasurementUpdate
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /dev
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "/dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.MeasurementsApi(api_client)
    campaign_id = 56 # int | 
    station_id = 56 # int | 
    sensor_id = 56 # int | 
    measurement_id = 56 # int | 
    measurement_update = openapi_client.MeasurementUpdate() # MeasurementUpdate | 

    try:
        # Partial Update Sensor
        api_response = api_instance.partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_patch(campaign_id, station_id, sensor_id, measurement_id, measurement_update)
        print("The response of MeasurementsApi->partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MeasurementsApi->partial_update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 
 **station_id** | **int**|  | 
 **sensor_id** | **int**|  | 
 **measurement_id** | **int**|  | 
 **measurement_update** | [**MeasurementUpdate**](MeasurementUpdate.md)|  | 

### Return type

[**MeasurementCreateResponse**](MeasurementCreateResponse.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_put**
> MeasurementCreateResponse update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_put(measurement_id, station_id, sensor_id, campaign_id, measurement_update)

Update Sensor

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.measurement_create_response import MeasurementCreateResponse
from openapi_client.models.measurement_update import MeasurementUpdate
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /dev
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "/dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.MeasurementsApi(api_client)
    measurement_id = 56 # int | 
    station_id = 56 # int | 
    sensor_id = 56 # int | 
    campaign_id = 56 # int | 
    measurement_update = openapi_client.MeasurementUpdate() # MeasurementUpdate | 

    try:
        # Update Sensor
        api_response = api_instance.update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_put(measurement_id, station_id, sensor_id, campaign_id, measurement_update)
        print("The response of MeasurementsApi->update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MeasurementsApi->update_sensor_api_v1_campaigns_campaign_id_stations_station_id_sensors_sensor_id_measurements_measurement_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **measurement_id** | **int**|  | 
 **station_id** | **int**|  | 
 **sensor_id** | **int**|  | 
 **campaign_id** | **int**|  | 
 **measurement_update** | [**MeasurementUpdate**](MeasurementUpdate.md)|  | 

### Return type

[**MeasurementCreateResponse**](MeasurementCreateResponse.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

