# GetStationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**contact_name** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**active** | **bool** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**geometry** | [**GetCampaignResponseGeometry**](GetCampaignResponseGeometry.md) |  | [optional] 
**sensors** | [**List[SensorItem]**](SensorItem.md) |  | [optional] 

## Example

```python
from openapi_client.models.get_station_response import GetStationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetStationResponse from a JSON string
get_station_response_instance = GetStationResponse.from_json(json)
# print the JSON string representation of the object
print(GetStationResponse.to_json())

# convert the object into a dict
get_station_response_dict = get_station_response_instance.to_dict()
# create an instance of GetStationResponse from a dict
get_station_response_from_dict = GetStationResponse.from_dict(get_station_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


