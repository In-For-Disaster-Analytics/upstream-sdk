# GetSensorResponse


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
from openapi_client.models.get_sensor_response import GetSensorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSensorResponse from a JSON string
get_sensor_response_instance = GetSensorResponse.from_json(json)
# print the JSON string representation of the object
print(GetSensorResponse.to_json())

# convert the object into a dict
get_sensor_response_dict = get_sensor_response_instance.to_dict()
# create an instance of GetSensorResponse from a dict
get_sensor_response_from_dict = GetSensorResponse.from_dict(get_sensor_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


