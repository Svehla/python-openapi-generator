OpenAPI Model Generator Documentation
=====================================
  
This documentation describes the usage of the OpenAPI Model Generator function, which generates Pydantic models from an OpenAPI specification.

Function: `generate_models`
---------------------------

The `generate_models` function generates Pydantic models from an OpenAPI specification dictionary. The generated models are returned as a string.

### Parameters

*   `openapi_spec`: `Dict[str, Any]` - The OpenAPI specification dictionary.

### Returns

*   `str` - The generated Pydantic models as a string.

### Usage Example

```py
from typing import Dict, Any
from pydantic import BaseModel
from your_module import generate_models

openapi_spec: Dict[str, Any] = {
    "openapi": "3.0.0",
    "info": {
        "title": "Sample API",
        "version": "1.0.0"
    },
    "paths": {
        "/users": {
            "get": {
                "responses": {
                    "200": {
                        "description": "A list of users",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/User"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "required": ["id", "name"]
            }
        }
    }
}

models_code = generate_models(openapi_spec)
print(models_code)
```

### Output Example

```py
from pydantic import BaseModel, RootModel
from typing import Optional, List, Dict, Any, Union

class User(BaseModel):
    id: int
    name: str

model_mapping = {
    "/users": {
        "GET": {
            "responses": {
                "200": List[User],
            },
        },
    },
}
```