# MultiPolygon

MultiPolygon Model

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bbox** | [**Bbox**](Bbox.md) |  | [optional] 
**type** | **str** |  | 
**coordinates** | **List[List[List[LineStringCoordinatesInner]]]** |  | 

## Example

```python
from openapi_client.models.multi_polygon import MultiPolygon

# TODO update the JSON string below
json = "{}"
# create an instance of MultiPolygon from a JSON string
multi_polygon_instance = MultiPolygon.from_json(json)
# print the JSON string representation of the object
print(MultiPolygon.to_json())

# convert the object into a dict
multi_polygon_dict = multi_polygon_instance.to_dict()
# create an instance of MultiPolygon from a dict
multi_polygon_from_dict = MultiPolygon.from_dict(multi_polygon_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


