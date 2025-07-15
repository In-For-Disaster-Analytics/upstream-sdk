# CampaignUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**contact_name** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**allocation** | **str** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**end_date** | **datetime** |  | [optional] 

## Example

```python
from openapi_client.models.campaign_update import CampaignUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of CampaignUpdate from a JSON string
campaign_update_instance = CampaignUpdate.from_json(json)
# print the JSON string representation of the object
print(CampaignUpdate.to_json())

# convert the object into a dict
campaign_update_dict = campaign_update_instance.to_dict()
# create an instance of CampaignUpdate from a dict
campaign_update_from_dict = CampaignUpdate.from_dict(campaign_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


