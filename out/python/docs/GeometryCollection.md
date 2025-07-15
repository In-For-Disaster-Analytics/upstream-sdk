# GeometryCollection

GeometryCollection Model

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bbox** | [**Bbox**](Bbox.md) |  | [optional] 
**type** | **str** |  | 
**geometries** | [**List[GeometryCollectionGeometriesInner]**](GeometryCollectionGeometriesInner.md) |  | 

## Example

```python
from openapi_client.models.geometry_collection import GeometryCollection

# TODO update the JSON string below
json = "{}"
# create an instance of GeometryCollection from a JSON string
geometry_collection_instance = GeometryCollection.from_json(json)
# print the JSON string representation of the object
print(GeometryCollection.to_json())

# convert the object into a dict
geometry_collection_dict = geometry_collection_instance.to_dict()
# create an instance of GeometryCollection from a dict
geometry_collection_from_dict = GeometryCollection.from_dict(geometry_collection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


