# SensorUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**postprocess** | **bool** |  | [optional] 
**postprocessscript** | **str** |  | [optional] 
**units** | **str** |  | [optional] 
**variablename** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.sensor_update import SensorUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of SensorUpdate from a JSON string
sensor_update_instance = SensorUpdate.from_json(json)
# print the JSON string representation of the object
print(SensorUpdate.to_json())

# convert the object into a dict
sensor_update_dict = sensor_update_instance.to_dict()
# create an instance of SensorUpdate from a dict
sensor_update_from_dict = SensorUpdate.from_dict(sensor_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


