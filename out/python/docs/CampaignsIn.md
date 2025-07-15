# CampaignsIn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**contact_name** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**allocation** | **str** |  | 

## Example

```python
from openapi_client.models.campaigns_in import CampaignsIn

# TODO update the JSON string below
json = "{}"
# create an instance of CampaignsIn from a JSON string
campaigns_in_instance = CampaignsIn.from_json(json)
# print the JSON string representation of the object
print(CampaignsIn.to_json())

# convert the object into a dict
campaigns_in_dict = campaigns_in_instance.to_dict()
# create an instance of CampaignsIn from a dict
campaigns_in_from_dict = CampaignsIn.from_dict(campaigns_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


