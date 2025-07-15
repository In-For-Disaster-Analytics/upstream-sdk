# StationsListResponseItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**contact_name** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**active** | **bool** |  | [optional] 
**start_date** | **datetime** |  | 
**geometry** | [**GetCampaignResponseGeometry**](GetCampaignResponseGeometry.md) |  | [optional] 
**sensors** | [**List[SensorSummaryForStations]**](SensorSummaryForStations.md) |  | [optional] [default to []]

## Example

```python
from openapi_client.models.stations_list_response_item import StationsListResponseItem

# TODO update the JSON string below
json = "{}"
# create an instance of StationsListResponseItem from a JSON string
stations_list_response_item_instance = StationsListResponseItem.from_json(json)
# print the JSON string representation of the object
print(StationsListResponseItem.to_json())

# convert the object into a dict
stations_list_response_item_dict = stations_list_response_item_instance.to_dict()
# create an instance of StationsListResponseItem from a dict
stations_list_response_item_from_dict = StationsListResponseItem.from_dict(stations_list_response_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


