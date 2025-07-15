# MultiLineString

MultiLineString Model

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bbox** | [**Bbox**](Bbox.md) |  | [optional] 
**type** | **str** |  | 
**coordinates** | **List[List[LineStringCoordinatesInner]]** |  | 

## Example

```python
from openapi_client.models.multi_line_string import MultiLineString

# TODO update the JSON string below
json = "{}"
# create an instance of MultiLineString from a JSON string
multi_line_string_instance = MultiLineString.from_json(json)
# print the JSON string representation of the object
print(MultiLineString.to_json())

# convert the object into a dict
multi_line_string_dict = multi_line_string_instance.to_dict()
# create an instance of MultiLineString from a dict
multi_line_string_from_dict = MultiLineString.from_dict(multi_line_string_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


