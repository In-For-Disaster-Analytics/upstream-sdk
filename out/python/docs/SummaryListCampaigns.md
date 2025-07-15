# SummaryListCampaigns


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sensor_types** | **List[str]** |  | [optional] 
**variable_names** | **List[str]** |  | [optional] 

## Example

```python
from openapi_client.models.summary_list_campaigns import SummaryListCampaigns

# TODO update the JSON string below
json = "{}"
# create an instance of SummaryListCampaigns from a JSON string
summary_list_campaigns_instance = SummaryListCampaigns.from_json(json)
# print the JSON string representation of the object
print(SummaryListCampaigns.to_json())

# convert the object into a dict
summary_list_campaigns_dict = summary_list_campaigns_instance.to_dict()
# create an instance of SummaryListCampaigns from a dict
summary_list_campaigns_from_dict = SummaryListCampaigns.from_dict(summary_list_campaigns_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


