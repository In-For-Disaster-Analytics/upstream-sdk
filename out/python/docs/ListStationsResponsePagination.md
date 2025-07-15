# ListStationsResponsePagination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[StationItemWithSummary]**](StationItemWithSummary.md) |  | 
**total** | **int** |  | 
**page** | **int** |  | 
**size** | **int** |  | 
**pages** | **int** |  | 

## Example

```python
from openapi_client.models.list_stations_response_pagination import ListStationsResponsePagination

# TODO update the JSON string below
json = "{}"
# create an instance of ListStationsResponsePagination from a JSON string
list_stations_response_pagination_instance = ListStationsResponsePagination.from_json(json)
# print the JSON string representation of the object
print(ListStationsResponsePagination.to_json())

# convert the object into a dict
list_stations_response_pagination_dict = list_stations_response_pagination_instance.to_dict()
# create an instance of ListStationsResponsePagination from a dict
list_stations_response_pagination_from_dict = ListStationsResponsePagination.from_dict(list_stations_response_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


