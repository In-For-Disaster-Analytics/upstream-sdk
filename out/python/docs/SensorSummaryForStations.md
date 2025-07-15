# SensorSummaryForStations


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**variable_name** | **str** |  | [optional] 
**measurement_unit** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.sensor_summary_for_stations import SensorSummaryForStations

# TODO update the JSON string below
json = "{}"
# create an instance of SensorSummaryForStations from a JSON string
sensor_summary_for_stations_instance = SensorSummaryForStations.from_json(json)
# print the JSON string representation of the object
print(SensorSummaryForStations.to_json())

# convert the object into a dict
sensor_summary_for_stations_dict = sensor_summary_for_stations_instance.to_dict()
# create an instance of SensorSummaryForStations from a dict
sensor_summary_for_stations_from_dict = SensorSummaryForStations.from_dict(sensor_summary_for_stations_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


