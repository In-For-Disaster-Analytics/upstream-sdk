# MeasurementIn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sensorid** | **int** |  | [optional] 
**collectiontime** | **datetime** |  | 
**geometry** | **str** |  | [optional] 
**measurementvalue** | **float** |  | 
**variablename** | **str** |  | [optional] 
**variabletype** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.measurement_in import MeasurementIn

# TODO update the JSON string below
json = "{}"
# create an instance of MeasurementIn from a JSON string
measurement_in_instance = MeasurementIn.from_json(json)
# print the JSON string representation of the object
print(MeasurementIn.to_json())

# convert the object into a dict
measurement_in_dict = measurement_in_instance.to_dict()
# create an instance of MeasurementIn from a dict
measurement_in_from_dict = MeasurementIn.from_dict(measurement_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


