from typing import Optional, List, Dict, Any, Union, Type, Literal
from typing_extensions import TypedDict

class ApiResponse(TypedDict):
    code: Optional[int]
    type: Optional[str]
    message: Optional[str]


class Category(TypedDict):
    id: Optional[int]
    name: Optional[str]


class Tag(TypedDict):
    id: Optional[int]
    name: Optional[str]


class Pet(TypedDict):
    id: Optional[int]
    category: Optional[Category]
    name: str
    photoUrls: List[str]
    tags: Optional[List[Tag]]
    status: Optional[Literal["available", "pending", "sold"]]


class Order(TypedDict):
    id: Optional[int]
    petId: Optional[int]
    quantity: Optional[int]
    shipDate: Optional[str]
    status: Optional[Literal["placed", "approved", "delivered"]]
    complete: Optional[bool]


class User(TypedDict):
    id: Optional[int]
    username: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    userStatus: Optional[int]


class _pet_petId_uploadImage_POST_Response_Status200(TypedDict):
    code: Optional[int]
    type: Optional[str]
    message: Optional[str]


class _pet_petId_uploadImage_POST_Response_200(TypedDict):
    data: _pet_petId_uploadImage_POST_Response_Status200


class _pet_petId_uploadImage_POST_Method:
    response_200 = _pet_petId_uploadImage_POST_Response_200
    URL: Literal["/pet/{petId}/uploadImage"] = "/pet/{petId}/uploadImage"
    METHOD: Literal["POST"] = "POST"


class _pet_petId_uploadImage_API:
    POST = _pet_petId_uploadImage_POST_Method


class _pet_POST_RequestBody(TypedDict):
    id: Optional[int]
    category: Optional[Category]
    name: str
    photoUrls: List[str]
    tags: Optional[List[Tag]]
    status: Optional[Literal["available", "pending", "sold"]]


class _pet_POST_Method:
    request_body = _pet_POST_RequestBody
    URL: Literal["/pet"] = "/pet"
    METHOD: Literal["POST"] = "POST"


class _pet_PUT_RequestBody(TypedDict):
    id: Optional[int]
    category: Optional[Category]
    name: str
    photoUrls: List[str]
    tags: Optional[List[Tag]]
    status: Optional[Literal["available", "pending", "sold"]]


class _pet_PUT_Method:
    request_body = _pet_PUT_RequestBody
    URL: Literal["/pet"] = "/pet"
    METHOD: Literal["PUT"] = "PUT"


class _pet_API:
    POST = _pet_POST_Method
    PUT = _pet_PUT_Method


class _pet_findByStatus_GET_Response_Status200(TypedDict):
    items: List[Pet]


class _pet_findByStatus_GET_Response_200(TypedDict):
    data: _pet_findByStatus_GET_Response_Status200


class _pet_findByStatus_GET_Method:
    response_200 = _pet_findByStatus_GET_Response_200
    URL: Literal["/pet/findByStatus"] = "/pet/findByStatus"
    METHOD: Literal["GET"] = "GET"


class _pet_findByStatus_API:
    GET = _pet_findByStatus_GET_Method


class _pet_findByTags_GET_Response_Status200(TypedDict):
    items: List[Pet]


class _pet_findByTags_GET_Response_200(TypedDict):
    data: _pet_findByTags_GET_Response_Status200


class _pet_findByTags_GET_Method:
    response_200 = _pet_findByTags_GET_Response_200
    URL: Literal["/pet/findByTags"] = "/pet/findByTags"
    METHOD: Literal["GET"] = "GET"


class _pet_findByTags_API:
    GET = _pet_findByTags_GET_Method


class _pet_petId_GET_Response_Status200(TypedDict):
    id: Optional[int]
    category: Optional[Category]
    name: str
    photoUrls: List[str]
    tags: Optional[List[Tag]]
    status: Optional[Literal["available", "pending", "sold"]]


class _pet_petId_GET_Response_200(TypedDict):
    data: _pet_petId_GET_Response_Status200


class _pet_petId_GET_Method:
    response_200 = _pet_petId_GET_Response_200
    URL: Literal["/pet/{petId}"] = "/pet/{petId}"
    METHOD: Literal["GET"] = "GET"


class _pet_petId_POST_Method:
    URL: Literal["/pet/{petId}"] = "/pet/{petId}"
    METHOD: Literal["POST"] = "POST"


class _pet_petId_DELETE_Method:
    URL: Literal["/pet/{petId}"] = "/pet/{petId}"
    METHOD: Literal["DELETE"] = "DELETE"


class _pet_petId_API:
    GET = _pet_petId_GET_Method
    POST = _pet_petId_POST_Method
    DELETE = _pet_petId_DELETE_Method


class _store_inventory_GET_Response_Status200(TypedDict):
    pass


class _store_inventory_GET_Response_200(TypedDict):
    data: _store_inventory_GET_Response_Status200


class _store_inventory_GET_Method:
    response_200 = _store_inventory_GET_Response_200
    URL: Literal["/store/inventory"] = "/store/inventory"
    METHOD: Literal["GET"] = "GET"


class _store_inventory_API:
    GET = _store_inventory_GET_Method


class _store_order_POST_RequestBody(TypedDict):
    id: Optional[int]
    petId: Optional[int]
    quantity: Optional[int]
    shipDate: Optional[str]
    status: Optional[Literal["placed", "approved", "delivered"]]
    complete: Optional[bool]


class _store_order_POST_Response_Status200(TypedDict):
    id: Optional[int]
    petId: Optional[int]
    quantity: Optional[int]
    shipDate: Optional[str]
    status: Optional[Literal["placed", "approved", "delivered"]]
    complete: Optional[bool]


class _store_order_POST_Response_200(TypedDict):
    data: _store_order_POST_Response_Status200


class _store_order_POST_Method:
    request_body = _store_order_POST_RequestBody
    response_200 = _store_order_POST_Response_200
    URL: Literal["/store/order"] = "/store/order"
    METHOD: Literal["POST"] = "POST"


class _store_order_API:
    POST = _store_order_POST_Method


class _store_order_orderId_GET_Response_Status200(TypedDict):
    id: Optional[int]
    petId: Optional[int]
    quantity: Optional[int]
    shipDate: Optional[str]
    status: Optional[Literal["placed", "approved", "delivered"]]
    complete: Optional[bool]


class _store_order_orderId_GET_Response_200(TypedDict):
    data: _store_order_orderId_GET_Response_Status200


class _store_order_orderId_GET_Method:
    response_200 = _store_order_orderId_GET_Response_200
    URL: Literal["/store/order/{orderId}"] = "/store/order/{orderId}"
    METHOD: Literal["GET"] = "GET"


class _store_order_orderId_DELETE_Method:
    URL: Literal["/store/order/{orderId}"] = "/store/order/{orderId}"
    METHOD: Literal["DELETE"] = "DELETE"


class _store_order_orderId_API:
    GET = _store_order_orderId_GET_Method
    DELETE = _store_order_orderId_DELETE_Method


class _user_createWithList_POST_RequestBody(TypedDict):
    items: List[User]


class _user_createWithList_POST_Method:
    request_body = _user_createWithList_POST_RequestBody
    URL: Literal["/user/createWithList"] = "/user/createWithList"
    METHOD: Literal["POST"] = "POST"


class _user_createWithList_API:
    POST = _user_createWithList_POST_Method


class _user_username_GET_Response_Status200(TypedDict):
    id: Optional[int]
    username: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    userStatus: Optional[int]


class _user_username_GET_Response_200(TypedDict):
    data: _user_username_GET_Response_Status200


class _user_username_GET_Method:
    response_200 = _user_username_GET_Response_200
    URL: Literal["/user/{username}"] = "/user/{username}"
    METHOD: Literal["GET"] = "GET"


class _user_username_PUT_RequestBody(TypedDict):
    id: Optional[int]
    username: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    userStatus: Optional[int]


class _user_username_PUT_Method:
    request_body = _user_username_PUT_RequestBody
    URL: Literal["/user/{username}"] = "/user/{username}"
    METHOD: Literal["PUT"] = "PUT"


class _user_username_DELETE_Method:
    URL: Literal["/user/{username}"] = "/user/{username}"
    METHOD: Literal["DELETE"] = "DELETE"


class _user_username_API:
    GET = _user_username_GET_Method
    PUT = _user_username_PUT_Method
    DELETE = _user_username_DELETE_Method


class _user_login_GET_Response_Status200(TypedDict):
    pass


class _user_login_GET_Response_200(TypedDict):
    data: _user_login_GET_Response_Status200


class _user_login_GET_Method:
    response_200 = _user_login_GET_Response_200
    URL: Literal["/user/login"] = "/user/login"
    METHOD: Literal["GET"] = "GET"


class _user_login_API:
    GET = _user_login_GET_Method


class _user_logout_GET_Method:
    URL: Literal["/user/logout"] = "/user/logout"
    METHOD: Literal["GET"] = "GET"


class _user_logout_API:
    GET = _user_logout_GET_Method


class _user_createWithArray_POST_RequestBody(TypedDict):
    items: List[User]


class _user_createWithArray_POST_Method:
    request_body = _user_createWithArray_POST_RequestBody
    URL: Literal["/user/createWithArray"] = "/user/createWithArray"
    METHOD: Literal["POST"] = "POST"


class _user_createWithArray_API:
    POST = _user_createWithArray_POST_Method


class _user_POST_RequestBody(TypedDict):
    id: Optional[int]
    username: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    userStatus: Optional[int]


class _user_POST_Method:
    request_body = _user_POST_RequestBody
    URL: Literal["/user"] = "/user"
    METHOD: Literal["POST"] = "POST"


class _user_API:
    POST = _user_POST_Method


class ModelMapping:

    # /pet/{petId}/uploadImage
    _pet_petId_uploadImage = _pet_petId_uploadImage_API

    # /pet
    _pet = _pet_API

    # /pet/findByStatus
    _pet_findByStatus = _pet_findByStatus_API

    # /pet/findByTags
    _pet_findByTags = _pet_findByTags_API

    # /pet/{petId}
    _pet_petId = _pet_petId_API

    # /store/inventory
    _store_inventory = _store_inventory_API

    # /store/order
    _store_order = _store_order_API

    # /store/order/{orderId}
    _store_order_orderId = _store_order_orderId_API

    # /user/createWithList
    _user_createWithList = _user_createWithList_API

    # /user/{username}
    _user_username = _user_username_API

    # /user/login
    _user_login = _user_login_API

    # /user/logout
    _user_logout = _user_logout_API

    # /user/createWithArray
    _user_createWithArray = _user_createWithArray_API

    # /user
    _user = _user_API
