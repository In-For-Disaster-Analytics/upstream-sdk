# ListCampaignsResponseItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**location** | [**Location**](Location.md) |  | [optional] 
**description** | **str** |  | [optional] 
**contact_name** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**allocation** | **str** |  | [optional] 
**summary** | [**SummaryListCampaigns**](SummaryListCampaigns.md) |  | 
**geometry** | [**GetCampaignResponseGeometry**](GetCampaignResponseGeometry.md) |  | [optional] 

## Example

```python
from openapi_client.models.list_campaigns_response_item import ListCampaignsResponseItem

# TODO update the JSON string below
json = "{}"
# create an instance of ListCampaignsResponseItem from a JSON string
list_campaigns_response_item_instance = ListCampaignsResponseItem.from_json(json)
# print the JSON string representation of the object
print(ListCampaignsResponseItem.to_json())

# convert the object into a dict
list_campaigns_response_item_dict = list_campaigns_response_item_instance.to_dict()
# create an instance of ListCampaignsResponseItem from a dict
list_campaigns_response_item_from_dict = ListCampaignsResponseItem.from_dict(list_campaigns_response_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


