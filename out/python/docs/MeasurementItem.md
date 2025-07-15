# MeasurementItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**value** | **float** |  | 
**geometry** | [**Point**](Point.md) |  | 
**collectiontime** | **datetime** |  | 
**sensorid** | **int** |  | [optional] 
**variablename** | **str** |  | [optional] 
**variabletype** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.measurement_item import MeasurementItem

# TODO update the JSON string below
json = "{}"
# create an instance of MeasurementItem from a JSON string
measurement_item_instance = MeasurementItem.from_json(json)
# print the JSON string representation of the object
print(MeasurementItem.to_json())

# convert the object into a dict
measurement_item_dict = measurement_item_instance.to_dict()
# create an instance of MeasurementItem from a dict
measurement_item_from_dict = MeasurementItem.from_dict(measurement_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


