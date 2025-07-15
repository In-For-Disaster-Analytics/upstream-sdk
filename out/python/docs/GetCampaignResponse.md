# GetCampaignResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**contact_name** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**allocation** | **str** |  | 
**location** | [**Location**](Location.md) |  | [optional] 
**summary** | [**SummaryGetCampaign**](SummaryGetCampaign.md) |  | 
**geometry** | [**GetCampaignResponseGeometry**](GetCampaignResponseGeometry.md) |  | [optional] 
**stations** | [**List[StationsListResponseItem]**](StationsListResponseItem.md) |  | [optional] [default to []]

## Example

```python
from openapi_client.models.get_campaign_response import GetCampaignResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCampaignResponse from a JSON string
get_campaign_response_instance = GetCampaignResponse.from_json(json)
# print the JSON string representation of the object
print(GetCampaignResponse.to_json())

# convert the object into a dict
get_campaign_response_dict = get_campaign_response_instance.to_dict()
# create an instance of GetCampaignResponse from a dict
get_campaign_response_from_dict = GetCampaignResponse.from_dict(get_campaign_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


