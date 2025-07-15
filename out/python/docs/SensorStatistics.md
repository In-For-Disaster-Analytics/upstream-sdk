# SensorStatistics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_value** | **float** |  | [optional] 
**min_value** | **float** |  | [optional] 
**avg_value** | **float** |  | [optional] 
**stddev_value** | **float** |  | [optional] 
**percentile_90** | **float** |  | [optional] 
**percentile_95** | **float** |  | [optional] 
**percentile_99** | **float** |  | [optional] 
**count** | **int** |  | [optional] 
**first_measurement_value** | **float** |  | [optional] 
**first_measurement_collectiontime** | **datetime** |  | [optional] 
**last_measurement_time** | **datetime** |  | [optional] 
**last_measurement_value** | **float** |  | [optional] 
**stats_last_updated** | **datetime** |  | [optional] 

## Example

```python
from openapi_client.models.sensor_statistics import SensorStatistics

# TODO update the JSON string below
json = "{}"
# create an instance of SensorStatistics from a JSON string
sensor_statistics_instance = SensorStatistics.from_json(json)
# print the JSON string representation of the object
print(SensorStatistics.to_json())

# convert the object into a dict
sensor_statistics_dict = sensor_statistics_instance.to_dict()
# create an instance of SensorStatistics from a dict
sensor_statistics_from_dict = SensorStatistics.from_dict(sensor_statistics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


