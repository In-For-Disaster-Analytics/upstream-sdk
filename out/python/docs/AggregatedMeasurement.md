# AggregatedMeasurement


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measurement_time** | **datetime** |  | 
**value** | **float** |  | 
**median_value** | **float** |  | 
**point_count** | **int** |  | 
**lower_bound** | **float** |  | 
**upper_bound** | **float** |  | 
**parametric_lower_bound** | **float** |  | 
**parametric_upper_bound** | **float** |  | 
**std_dev** | **float** |  | 
**min_value** | **float** |  | 
**max_value** | **float** |  | 
**percentile_25** | **float** |  | 
**percentile_75** | **float** |  | 
**ci_method** | **str** |  | 
**confidence_level** | **float** |  | 

## Example

```python
from openapi_client.models.aggregated_measurement import AggregatedMeasurement

# TODO update the JSON string below
json = "{}"
# create an instance of AggregatedMeasurement from a JSON string
aggregated_measurement_instance = AggregatedMeasurement.from_json(json)
# print the JSON string representation of the object
print(AggregatedMeasurement.to_json())

# convert the object into a dict
aggregated_measurement_dict = aggregated_measurement_instance.to_dict()
# create an instance of AggregatedMeasurement from a dict
aggregated_measurement_from_dict = AggregatedMeasurement.from_dict(aggregated_measurement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


