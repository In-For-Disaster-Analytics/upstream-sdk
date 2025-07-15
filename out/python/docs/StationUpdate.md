# StationUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**contact_name** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**active** | **bool** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**station_type** | [**StationType**](StationType.md) |  | [optional] 

## Example

```python
from openapi_client.models.station_update import StationUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of StationUpdate from a JSON string
station_update_instance = StationUpdate.from_json(json)
# print the JSON string representation of the object
print(StationUpdate.to_json())

# convert the object into a dict
station_update_dict = station_update_instance.to_dict()
# create an instance of StationUpdate from a dict
station_update_from_dict = StationUpdate.from_dict(station_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


