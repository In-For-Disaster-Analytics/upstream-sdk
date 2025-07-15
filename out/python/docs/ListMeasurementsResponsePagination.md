# ListMeasurementsResponsePagination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[MeasurementItem]**](MeasurementItem.md) |  | 
**total** | **int** |  | 
**page** | **int** |  | 
**size** | **int** |  | 
**pages** | **int** |  | 
**min_value** | **float** |  | 
**max_value** | **float** |  | 
**average_value** | **float** |  | 
**downsampled** | **bool** |  | 
**downsampled_total** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.list_measurements_response_pagination import ListMeasurementsResponsePagination

# TODO update the JSON string below
json = "{}"
# create an instance of ListMeasurementsResponsePagination from a JSON string
list_measurements_response_pagination_instance = ListMeasurementsResponsePagination.from_json(json)
# print the JSON string representation of the object
print(ListMeasurementsResponsePagination.to_json())

# convert the object into a dict
list_measurements_response_pagination_dict = list_measurements_response_pagination_instance.to_dict()
# create an instance of ListMeasurementsResponsePagination from a dict
list_measurements_response_pagination_from_dict = ListMeasurementsResponsePagination.from_dict(list_measurements_response_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


