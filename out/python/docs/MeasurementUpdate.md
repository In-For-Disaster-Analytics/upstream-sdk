# MeasurementUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sensorid** | **int** |  | [optional] 
**collectiontime** | **datetime** |  | [optional] 
**geometry** | **str** |  | [optional] 
**measurementvalue** | **float** |  | [optional] 
**variablename** | **str** |  | [optional] 
**variabletype** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.measurement_update import MeasurementUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of MeasurementUpdate from a JSON string
measurement_update_instance = MeasurementUpdate.from_json(json)
# print the JSON string representation of the object
print(MeasurementUpdate.to_json())

# convert the object into a dict
measurement_update_dict = measurement_update_instance.to_dict()
# create an instance of MeasurementUpdate from a dict
measurement_update_from_dict = MeasurementUpdate.from_dict(measurement_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


