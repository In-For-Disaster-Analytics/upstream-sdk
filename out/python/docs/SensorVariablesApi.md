# openapi_client.SensorVariablesApi

All URIs are relative to */dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_sensor_variables_api_v1_sensor_variables_get**](SensorVariablesApi.md#list_sensor_variables_api_v1_sensor_variables_get) | **GET** /api/v1/sensor_variables | List Sensor Variables


# **list_sensor_variables_api_v1_sensor_variables_get**
> List[Optional[str]] list_sensor_variables_api_v1_sensor_variables_get()

List Sensor Variables

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
    api_instance = openapi_client.SensorVariablesApi(api_client)

    try:
        # List Sensor Variables
        api_response = api_instance.list_sensor_variables_api_v1_sensor_variables_get()
        print("The response of SensorVariablesApi->list_sensor_variables_api_v1_sensor_variables_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SensorVariablesApi->list_sensor_variables_api_v1_sensor_variables_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[Optional[str]]**

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

