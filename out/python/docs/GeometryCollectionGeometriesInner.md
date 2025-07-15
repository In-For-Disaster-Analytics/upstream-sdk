# GeometryCollectionGeometriesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bbox** | [**Bbox**](Bbox.md) |  | [optional] 
**type** | **str** |  | 
**coordinates** | **List[List[List[LineStringCoordinatesInner]]]** |  | 
**geometries** | [**List[GeometryCollectionGeometriesInner]**](GeometryCollectionGeometriesInner.md) |  | 

## Example

```python
from openapi_client.models.geometry_collection_geometries_inner import GeometryCollectionGeometriesInner

# TODO update the JSON string below
json = "{}"
# create an instance of GeometryCollectionGeometriesInner from a JSON string
geometry_collection_geometries_inner_instance = GeometryCollectionGeometriesInner.from_json(json)
# print the JSON string representation of the object
print(GeometryCollectionGeometriesInner.to_json())

# convert the object into a dict
geometry_collection_geometries_inner_dict = geometry_collection_geometries_inner_instance.to_dict()
# create an instance of GeometryCollectionGeometriesInner from a dict
geometry_collection_geometries_inner_from_dict = GeometryCollectionGeometriesInner.from_dict(geometry_collection_geometries_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


