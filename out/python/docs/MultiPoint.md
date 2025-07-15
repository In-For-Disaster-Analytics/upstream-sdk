# MultiPoint

MultiPoint Model

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bbox** | [**Bbox**](Bbox.md) |  | [optional] 
**type** | **str** |  | 
**coordinates** | [**List[LineStringCoordinatesInner]**](LineStringCoordinatesInner.md) |  | 

## Example

```python
from openapi_client.models.multi_point import MultiPoint

# TODO update the JSON string below
json = "{}"
# create an instance of MultiPoint from a JSON string
multi_point_instance = MultiPoint.from_json(json)
# print the JSON string representation of the object
print(MultiPoint.to_json())

# convert the object into a dict
multi_point_dict = multi_point_instance.to_dict()
# create an instance of MultiPoint from a dict
multi_point_from_dict = MultiPoint.from_dict(multi_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


