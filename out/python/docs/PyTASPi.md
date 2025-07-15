# PyTASPi


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**username** | **str** |  | 
**email** | **str** |  | 
**first_name** | **str** |  | 
**last_name** | **str** |  | 
**institution** | **str** |  | 
**institution_id** | **int** |  | 
**department** | **str** |  | 
**department_id** | **int** |  | 
**citizenship** | **str** |  | 
**citizenship_id** | **int** |  | 
**source** | **str** |  | 
**uid** | **int** |  | 
**home_directory** | **str** |  | 
**gid** | **int** |  | 

## Example

```python
from openapi_client.models.py_taspi import PyTASPi

# TODO update the JSON string below
json = "{}"
# create an instance of PyTASPi from a JSON string
py_taspi_instance = PyTASPi.from_json(json)
# print the JSON string representation of the object
print(PyTASPi.to_json())

# convert the object into a dict
py_taspi_dict = py_taspi_instance.to_dict()
# create an instance of PyTASPi from a dict
py_taspi_from_dict = PyTASPi.from_dict(py_taspi_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


