# ListSensorsResponsePagination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[SensorItem]**](SensorItem.md) |  | 
**total** | **int** |  | 
**page** | **int** |  | 
**size** | **int** |  | 
**pages** | **int** |  | 

## Example

```python
from openapi_client.models.list_sensors_response_pagination import ListSensorsResponsePagination

# TODO update the JSON string below
json = "{}"
# create an instance of ListSensorsResponsePagination from a JSON string
list_sensors_response_pagination_instance = ListSensorsResponsePagination.from_json(json)
# print the JSON string representation of the object
print(ListSensorsResponsePagination.to_json())

# convert the object into a dict
list_sensors_response_pagination_dict = list_sensors_response_pagination_instance.to_dict()
# create an instance of ListSensorsResponsePagination from a dict
list_sensors_response_pagination_from_dict = ListSensorsResponsePagination.from_dict(list_sensors_response_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


