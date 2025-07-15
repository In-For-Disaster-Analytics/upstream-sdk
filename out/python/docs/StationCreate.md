# StationCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**contact_name** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**active** | **bool** |  | [optional] 
**start_date** | **datetime** |  | 
**station_type** | [**StationType**](StationType.md) |  | [optional] 

## Example

```python
from openapi_client.models.station_create import StationCreate

# TODO update the JSON string below
json = "{}"
# create an instance of StationCreate from a JSON string
station_create_instance = StationCreate.from_json(json)
# print the JSON string representation of the object
print(StationCreate.to_json())

# convert the object into a dict
station_create_dict = station_create_instance.to_dict()
# create an instance of StationCreate from a dict
station_create_from_dict = StationCreate.from_dict(station_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


