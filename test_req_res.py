from __generated_api__.api_types import model_mapping
from pydantic import BaseModel, RootModel
from typing import Optional, List, Dict, Any, Union, Type

def validate_schema(schema: Type[BaseModel], data: Any):
    if isinstance(data, list):
        validated_data = schema(root=data)
    else:
        validated_data = schema(**data)
    return validated_data

# --------------------------------------------------------------------------------


out = validate_schema(
    model_mapping["/store/order"]["POST"]["parameters"],
    {
        "body": {
            "id": 3,
            "petId": 4,
            "quantity": 5,
            "shipDate": "x",
            "status": "delivered",
            "complete": True
        }
    }
)

print('---out---')
print(out)