from pydantic import BaseModel, RootModel
from typing import Optional, List, Dict, Any, Union
from enum import Enum

class Pet_Status(Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


class Order_Status(Enum):
    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"


class _pet_POST_BodyParam_Status(Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


class _pet_PUT_BodyParam_Status(Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


class _store_order_POST_BodyParam_Status(Enum):
    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"


class ApiResponse(BaseModel):
    code: int = None
    type: str = None
    message: str = None


class Category(BaseModel):
    id: int = None
    name: str = None


class Pet(BaseModel):
    id: int = None
    category: Category = None
    name: str
    photoUrls: List[str]
    tags: List[Any] = None
    status: Pet_Status = None


class Tag(BaseModel):
    id: int = None
    name: str = None


class Order(BaseModel):
    id: int = None
    petId: int = None
    quantity: int = None
    shipDate: str = None
    status: Order_Status = None
    complete: bool = None


class User(BaseModel):
    id: int = None
    username: str = None
    firstName: str = None
    lastName: str = None
    email: str = None
    password: str = None
    phone: str = None
    userStatus: int = None


class _pet_POST_BodyParam(BaseModel):
    id: int = None
    category: Category = None
    name: str
    photoUrls: List[str]
    tags: List[Any] = None
    status: _pet_POST_BodyParam_Status = None


class _pet_POST_Params(BaseModel):
    body: _pet_POST_BodyParam


class _pet_PUT_BodyParam(BaseModel):
    id: int = None
    category: Category = None
    name: str
    photoUrls: List[str]
    tags: List[Any] = None
    status: _pet_PUT_BodyParam_Status = None


class _pet_PUT_Params(BaseModel):
    body: _pet_PUT_BodyParam


class _store_order_POST_BodyParam(BaseModel):
    id: int = None
    petId: int = None
    quantity: int = None
    shipDate: str = None
    status: _store_order_POST_BodyParam_Status = None
    complete: bool = None


class _store_order_POST_Params(BaseModel):
    body: _store_order_POST_BodyParam


class _user_createWithList_POST_BodyParam(BaseModel):
    pass


class _user_createWithList_POST_Params(BaseModel):
    body: _user_createWithList_POST_BodyParam


class _user_username_PUT_BodyParam(BaseModel):
    id: int = None
    username: str = None
    firstName: str = None
    lastName: str = None
    email: str = None
    password: str = None
    phone: str = None
    userStatus: int = None


class _user_username_PUT_Params(BaseModel):
    body: _user_username_PUT_BodyParam


class _user_createWithArray_POST_BodyParam(BaseModel):
    pass


class _user_createWithArray_POST_Params(BaseModel):
    body: _user_createWithArray_POST_BodyParam


class _user_POST_BodyParam(BaseModel):
    id: int = None
    username: str = None
    firstName: str = None
    lastName: str = None
    email: str = None
    password: str = None
    phone: str = None
    userStatus: int = None


class _user_POST_Params(BaseModel):
    body: _user_POST_BodyParam


model_mapping = {
    "/pet/{petId}/uploadImage": {
        "POST": {
            "responses": {
            },
        },
    },
    "/pet": {
        "POST": {
            "parameters": _pet_POST_Params,
            "responses": {
            },
        },
        "PUT": {
            "parameters": _pet_PUT_Params,
            "responses": {
            },
        },
    },
    "/pet/findByStatus": {
        "GET": {
            "responses": {
            },
        },
    },
    "/pet/findByTags": {
        "GET": {
            "responses": {
            },
        },
    },
    "/pet/{petId}": {
        "GET": {
            "responses": {
            },
        },
        "POST": {
            "responses": {
            },
        },
        "DELETE": {
            "responses": {
            },
        },
    },
    "/store/inventory": {
        "GET": {
            "responses": {
            },
        },
    },
    "/store/order": {
        "POST": {
            "parameters": _store_order_POST_Params,
            "responses": {
            },
        },
    },
    "/store/order/{orderId}": {
        "GET": {
            "responses": {
            },
        },
        "DELETE": {
            "responses": {
            },
        },
    },
    "/user/createWithList": {
        "POST": {
            "parameters": _user_createWithList_POST_Params,
            "responses": {
            },
        },
    },
    "/user/{username}": {
        "GET": {
            "responses": {
            },
        },
        "PUT": {
            "parameters": _user_username_PUT_Params,
            "responses": {
            },
        },
        "DELETE": {
            "responses": {
            },
        },
    },
    "/user/login": {
        "GET": {
            "responses": {
            },
        },
    },
    "/user/logout": {
        "GET": {
            "responses": {
            },
        },
    },
    "/user/createWithArray": {
        "POST": {
            "parameters": _user_createWithArray_POST_Params,
            "responses": {
            },
        },
    },
    "/user": {
        "POST": {
            "parameters": _user_POST_Params,
            "responses": {
            },
        },
    },
}
