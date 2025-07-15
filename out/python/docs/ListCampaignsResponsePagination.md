# ListCampaignsResponsePagination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[ListCampaignsResponseItem]**](ListCampaignsResponseItem.md) |  | 
**total** | **int** |  | 
**page** | **int** |  | 
**size** | **int** |  | 
**pages** | **int** |  | 

## Example

```python
from openapi_client.models.list_campaigns_response_pagination import ListCampaignsResponsePagination

# TODO update the JSON string below
json = "{}"
# create an instance of ListCampaignsResponsePagination from a JSON string
list_campaigns_response_pagination_instance = ListCampaignsResponsePagination.from_json(json)
# print the JSON string representation of the object
print(ListCampaignsResponsePagination.to_json())

# convert the object into a dict
list_campaigns_response_pagination_dict = list_campaigns_response_pagination_instance.to_dict()
# create an instance of ListCampaignsResponsePagination from a dict
list_campaigns_response_pagination_from_dict = ListCampaignsResponsePagination.from_dict(list_campaigns_response_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


