# openapi_client.ProjectsApi

All URIs are relative to */dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_project_members_for_user_api_v1_projects_project_id_members_get**](ProjectsApi.md#get_project_members_for_user_api_v1_projects_project_id_members_get) | **GET** /api/v1/projects/{project_id}/members | Get Project Members For User
[**get_projects_api_v1_projects_get**](ProjectsApi.md#get_projects_api_v1_projects_get) | **GET** /api/v1/projects | Get Projects


# **get_project_members_for_user_api_v1_projects_project_id_members_get**
> List[PyTASUser] get_project_members_for_user_api_v1_projects_project_id_members_get(project_id)

Get Project Members For User

### Example


```python
import openapi_client
from openapi_client.models.py_tas_user import PyTASUser
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
    api_instance = openapi_client.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Get Project Members For User
        api_response = api_instance.get_project_members_for_user_api_v1_projects_project_id_members_get(project_id)
        print("The response of ProjectsApi->get_project_members_for_user_api_v1_projects_project_id_members_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_project_members_for_user_api_v1_projects_project_id_members_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**List[PyTASUser]**](PyTASUser.md)

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

# **get_projects_api_v1_projects_get**
> List[PyTASProject] get_projects_api_v1_projects_get()

Get Projects

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import openapi_client
from openapi_client.models.py_tas_project import PyTASProject
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
    api_instance = openapi_client.ProjectsApi(api_client)

    try:
        # Get Projects
        api_response = api_instance.get_projects_api_v1_projects_get()
        print("The response of ProjectsApi->get_projects_api_v1_projects_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_projects_api_v1_projects_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[PyTASProject]**](PyTASProject.md)

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

