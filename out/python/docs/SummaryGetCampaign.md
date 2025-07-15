# SummaryGetCampaign


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**station_count** | **int** |  | 
**sensor_count** | **int** |  | 
**sensor_types** | **List[str]** |  | 
**sensor_variables** | **List[str]** |  | 

## Example

```python
from openapi_client.models.summary_get_campaign import SummaryGetCampaign

# TODO update the JSON string below
json = "{}"
# create an instance of SummaryGetCampaign from a JSON string
summary_get_campaign_instance = SummaryGetCampaign.from_json(json)
# print the JSON string representation of the object
print(SummaryGetCampaign.to_json())

# convert the object into a dict
summary_get_campaign_dict = summary_get_campaign_instance.to_dict()
# create an instance of SummaryGetCampaign from a dict
summary_get_campaign_from_dict = SummaryGetCampaign.from_dict(summary_get_campaign_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


