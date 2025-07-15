# SensorItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**alias** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**postprocess** | **bool** |  | [optional] 
**postprocessscript** | **str** |  | [optional] 
**units** | **str** |  | [optional] 
**variablename** | **str** |  | [optional] 
**statistics** | [**SensorStatistics**](SensorStatistics.md) |  | [optional] 

## Example

```python
from openapi_client.models.sensor_item import SensorItem

# TODO update the JSON string below
json = "{}"
# create an instance of SensorItem from a JSON string
sensor_item_instance = SensorItem.from_json(json)
# print the JSON string representation of the object
print(SensorItem.to_json())

# convert the object into a dict
sensor_item_dict = sensor_item_instance.to_dict()
# create an instance of SensorItem from a dict
sensor_item_from_dict = SensorItem.from_dict(sensor_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


