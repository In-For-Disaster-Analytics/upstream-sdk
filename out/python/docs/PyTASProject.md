# PyTASProject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**description** | **str** |  | 
**charge_code** | **str** |  | 
**gid** | **int** |  | 
**source** | **object** |  | 
**field_id** | **int** |  | 
**var_field** | **str** |  | 
**type_id** | **int** |  | 
**type** | **str** |  | 
**pi_id** | **int** |  | 
**pi** | [**PyTASPi**](PyTASPi.md) |  | 
**allocations** | [**List[PyTASAllocation]**](PyTASAllocation.md) |  | 
**nickname** | **object** |  | 

## Example

```python
from openapi_client.models.py_tas_project import PyTASProject

# TODO update the JSON string below
json = "{}"
# create an instance of PyTASProject from a JSON string
py_tas_project_instance = PyTASProject.from_json(json)
# print the JSON string representation of the object
print(PyTASProject.to_json())

# convert the object into a dict
py_tas_project_dict = py_tas_project_instance.to_dict()
# create an instance of PyTASProject from a dict
py_tas_project_from_dict = PyTASProject.from_dict(py_tas_project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


