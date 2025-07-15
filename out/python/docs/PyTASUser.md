# PyTASUser


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**username** | **str** |  | 
**role** | **str** |  | [optional] 
**first_name** | **str** |  | [optional] 
**last_name** | **str** |  | [optional] 
**email** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.py_tas_user import PyTASUser

# TODO update the JSON string below
json = "{}"
# create an instance of PyTASUser from a JSON string
py_tas_user_instance = PyTASUser.from_json(json)
# print the JSON string representation of the object
print(PyTASUser.to_json())

# convert the object into a dict
py_tas_user_dict = py_tas_user_instance.to_dict()
# create an instance of PyTASUser from a dict
py_tas_user_from_dict = PyTASUser.from_dict(py_tas_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


