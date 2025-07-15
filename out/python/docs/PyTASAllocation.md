# PyTASAllocation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**start** | **str** |  | 
**end** | **str** |  | 
**status** | **str** |  | 
**justification** | **str** |  | 
**decision_summary** | **str** |  | 
**date_requested** | **str** |  | 
**date_reviewed** | **str** |  | 
**compute_requested** | **int** |  | 
**compute_allocated** | **int** |  | 
**storage_requested** | **int** |  | 
**storage_allocated** | **int** |  | 
**memory_requested** | **int** |  | 
**memory_allocated** | **int** |  | 
**resource_id** | **int** |  | 
**resource** | **str** |  | 
**project_id** | **int** |  | 
**project** | **str** |  | 
**requestor_id** | **int** |  | 
**requestor** | **str** |  | 
**reviewer_id** | **int** |  | 
**reviewer** | **object** |  | 
**compute_used** | **float** |  | 

## Example

```python
from openapi_client.models.py_tas_allocation import PyTASAllocation

# TODO update the JSON string below
json = "{}"
# create an instance of PyTASAllocation from a JSON string
py_tas_allocation_instance = PyTASAllocation.from_json(json)
# print the JSON string representation of the object
print(PyTASAllocation.to_json())

# convert the object into a dict
py_tas_allocation_dict = py_tas_allocation_instance.to_dict()
# create an instance of PyTASAllocation from a dict
py_tas_allocation_from_dict = PyTASAllocation.from_dict(py_tas_allocation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


