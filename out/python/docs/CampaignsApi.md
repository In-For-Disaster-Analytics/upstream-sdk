# openapi_client.CampaignsApi

All URIs are relative to */dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_campaign_api_v1_campaigns_post**](CampaignsApi.md#create_campaign_api_v1_campaigns_post) | **POST** /api/v1/campaigns | Create Campaign
[**delete_sensor_api_v1_campaigns_campaign_id_delete**](CampaignsApi.md#delete_sensor_api_v1_campaigns_campaign_id_delete) | **DELETE** /api/v1/campaigns/{campaign_id} | Delete Sensor
[**get_campaign_api_v1_campaigns_campaign_id_get**](CampaignsApi.md#get_campaign_api_v1_campaigns_campaign_id_get) | **GET** /api/v1/campaigns/{campaign_id} | Get Campaign
[**list_campaigns_api_v1_campaigns_get**](CampaignsApi.md#list_campaigns_api_v1_campaigns_get) | **GET** /api/v1/campaigns | List Campaigns
[**partial_update_campaign_api_v1_campaigns_campaign_id_patch**](CampaignsApi.md#partial_update_campaign_api_v1_campaigns_campaign_id_patch) | **PATCH** /api/v1/campaigns/{campaign_id} | Partial Update Campaign
[**update_campaign_api_v1_campaigns_campaign_id_put**](CampaignsApi.md#update_campaign_api_v1_campaigns_campaign_id_put) | **PUT** /api/v1/campaigns/{campaign_id} | Update Campaign


# **create_campaign_api_v1_campaigns_post**
> CampaignCreateResponse create_campaign_api_v1_campaigns_post(campaigns_in)

Create Campaign

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.campaign_create_response import CampaignCreateResponse
from openapi_client.models.campaigns_in import CampaignsIn
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
    api_instance = openapi_client.CampaignsApi(api_client)
    campaigns_in = openapi_client.CampaignsIn() # CampaignsIn | 

    try:
        # Create Campaign
        api_response = api_instance.create_campaign_api_v1_campaigns_post(campaigns_in)
        print("The response of CampaignsApi->create_campaign_api_v1_campaigns_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->create_campaign_api_v1_campaigns_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaigns_in** | [**CampaignsIn**](CampaignsIn.md)|  | 

### Return type

[**CampaignCreateResponse**](CampaignCreateResponse.md)

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

# **delete_sensor_api_v1_campaigns_campaign_id_delete**
> delete_sensor_api_v1_campaigns_campaign_id_delete(campaign_id)

Delete Sensor

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
    api_instance = openapi_client.CampaignsApi(api_client)
    campaign_id = 56 # int | 

    try:
        # Delete Sensor
        api_instance.delete_sensor_api_v1_campaigns_campaign_id_delete(campaign_id)
    except Exception as e:
        print("Exception when calling CampaignsApi->delete_sensor_api_v1_campaigns_campaign_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 

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

# **get_campaign_api_v1_campaigns_campaign_id_get**
> GetCampaignResponse get_campaign_api_v1_campaigns_campaign_id_get(campaign_id)

Get Campaign

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.get_campaign_response import GetCampaignResponse
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
    api_instance = openapi_client.CampaignsApi(api_client)
    campaign_id = 56 # int | 

    try:
        # Get Campaign
        api_response = api_instance.get_campaign_api_v1_campaigns_campaign_id_get(campaign_id)
        print("The response of CampaignsApi->get_campaign_api_v1_campaigns_campaign_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->get_campaign_api_v1_campaigns_campaign_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 

### Return type

[**GetCampaignResponse**](GetCampaignResponse.md)

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

# **list_campaigns_api_v1_campaigns_get**
> ListCampaignsResponsePagination list_campaigns_api_v1_campaigns_get(page=page, limit=limit, bbox=bbox, start_date=start_date, end_date=end_date, sensor_variables=sensor_variables)

List Campaigns

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.list_campaigns_response_pagination import ListCampaignsResponsePagination
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
    api_instance = openapi_client.CampaignsApi(api_client)
    page = 1 # int |  (optional) (default to 1)
    limit = 20 # int |  (optional) (default to 20)
    bbox = 'bbox_example' # str | Bounding box of the campaign west,south,east,north (optional)
    start_date = '2024-01-01' # datetime | Start date of the campaign (optional)
    end_date = '2025-01-01' # datetime | End date of the campaign (optional)
    sensor_variables = ['sensor_variables_example'] # List[Optional[str]] | List of sensor variables to filter by (optional)

    try:
        # List Campaigns
        api_response = api_instance.list_campaigns_api_v1_campaigns_get(page=page, limit=limit, bbox=bbox, start_date=start_date, end_date=end_date, sensor_variables=sensor_variables)
        print("The response of CampaignsApi->list_campaigns_api_v1_campaigns_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->list_campaigns_api_v1_campaigns_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**|  | [optional] [default to 1]
 **limit** | **int**|  | [optional] [default to 20]
 **bbox** | **str**| Bounding box of the campaign west,south,east,north | [optional] 
 **start_date** | **datetime**| Start date of the campaign | [optional] 
 **end_date** | **datetime**| End date of the campaign | [optional] 
 **sensor_variables** | [**List[Optional[str]]**](str.md)| List of sensor variables to filter by | [optional] 

### Return type

[**ListCampaignsResponsePagination**](ListCampaignsResponsePagination.md)

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

# **partial_update_campaign_api_v1_campaigns_campaign_id_patch**
> CampaignCreateResponse partial_update_campaign_api_v1_campaigns_campaign_id_patch(campaign_id, campaign_update)

Partial Update Campaign

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.campaign_create_response import CampaignCreateResponse
from openapi_client.models.campaign_update import CampaignUpdate
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
    api_instance = openapi_client.CampaignsApi(api_client)
    campaign_id = 56 # int | 
    campaign_update = openapi_client.CampaignUpdate() # CampaignUpdate | 

    try:
        # Partial Update Campaign
        api_response = api_instance.partial_update_campaign_api_v1_campaigns_campaign_id_patch(campaign_id, campaign_update)
        print("The response of CampaignsApi->partial_update_campaign_api_v1_campaigns_campaign_id_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->partial_update_campaign_api_v1_campaigns_campaign_id_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 
 **campaign_update** | [**CampaignUpdate**](CampaignUpdate.md)|  | 

### Return type

[**CampaignCreateResponse**](CampaignCreateResponse.md)

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

# **update_campaign_api_v1_campaigns_campaign_id_put**
> CampaignCreateResponse update_campaign_api_v1_campaigns_campaign_id_put(campaign_id, campaigns_in)

Update Campaign

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.campaign_create_response import CampaignCreateResponse
from openapi_client.models.campaigns_in import CampaignsIn
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
    api_instance = openapi_client.CampaignsApi(api_client)
    campaign_id = 56 # int | 
    campaigns_in = openapi_client.CampaignsIn() # CampaignsIn | 

    try:
        # Update Campaign
        api_response = api_instance.update_campaign_api_v1_campaigns_campaign_id_put(campaign_id, campaigns_in)
        print("The response of CampaignsApi->update_campaign_api_v1_campaigns_campaign_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->update_campaign_api_v1_campaigns_campaign_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **campaign_id** | **int**|  | 
 **campaigns_in** | [**CampaignsIn**](CampaignsIn.md)|  | 

### Return type

[**CampaignCreateResponse**](CampaignCreateResponse.md)

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

