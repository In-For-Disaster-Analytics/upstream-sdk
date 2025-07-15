# GetCampaignResponseGeometry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bbox** | [**Bbox**](Bbox.md) |  | [optional] 
**type** | **str** |  | 
**coordinates** | **List[List[List[LineStringCoordinatesInner]]]** |  | 
**geometries** | [**List[GeometryCollectionGeometriesInner]**](GeometryCollectionGeometriesInner.md) |  | 

## Example

```python
from openapi_client.models.get_campaign_response_geometry import GetCampaignResponseGeometry

# TODO update the JSON string below
json = "{}"
# create an instance of GetCampaignResponseGeometry from a JSON string
get_campaign_response_geometry_instance = GetCampaignResponseGeometry.from_json(json)
# print the JSON string representation of the object
print(GetCampaignResponseGeometry.to_json())

# convert the object into a dict
get_campaign_response_geometry_dict = get_campaign_response_geometry_instance.to_dict()
# create an instance of GetCampaignResponseGeometry from a dict
get_campaign_response_geometry_from_dict = GetCampaignResponseGeometry.from_dict(get_campaign_response_geometry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


