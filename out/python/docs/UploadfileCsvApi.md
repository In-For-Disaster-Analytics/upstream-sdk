# openapi_client.UploadfileCsvApi

All URIs are relative to */dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post**](UploadfileCsvApi.md#post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post) | **POST** /api/v1/uploadfile_csv/campaign/{campaign_id}/station/{station_id}/sensor | Post Sensor And Measurement


# **post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post**
> Dict[str, object] post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post(campaign_id, station_id, upload_file_sensors, upload_file_measurements)

Post Sensor And Measurement

Process sensor and measurement files and store data in the database.

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
    api_instance = openapi_client.UploadfileCsvApi(api_client)
    campaign_id = 56 # int | 
    station_id = 56 # int | 
    upload_file_sensors = None # bytearray | File with sensors.
    upload_file_measurements = None # bytearray | File with measurements.

    try:
        # Post Sensor And Measurement
        api_response = api_instance.post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post(campaign_id, station_id, upload_file_sensors, upload_file_measurements)
        print("The response of UploadfileCsvApi->post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadfileCsvApi->post_sensor_and_measurement_api_v1_uploadfile_csv_campaign_campaign_id_station_station_id_sensor_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 
 **station_id** | **int**|  | 
 **upload_file_sensors** | **bytearray**| File with sensors. | 
 **upload_file_measurements** | **bytearray**| File with measurements. | 

### Return type

**Dict[str, object]**

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

