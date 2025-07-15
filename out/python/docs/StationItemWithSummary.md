# StationItemWithSummary


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
**sensor_count** | **int** |  | 
**sensor_types** | **List[str]** |  | 
**sensor_variables** | **List[str]** |  | 

## Example

```python
from openapi_client.models.station_item_with_summary import StationItemWithSummary

# TODO update the JSON string below
json = "{}"
# create an instance of StationItemWithSummary from a JSON string
station_item_with_summary_instance = StationItemWithSummary.from_json(json)
# print the JSON string representation of the object
print(StationItemWithSummary.to_json())

# convert the object into a dict
station_item_with_summary_dict = station_item_with_summary_instance.to_dict()
# create an instance of StationItemWithSummary from a dict
station_item_with_summary_from_dict = StationItemWithSummary.from_dict(station_item_with_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


