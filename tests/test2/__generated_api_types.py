from typing import Optional, List, Dict, Any, Union, Type, Literal
from typing_extensions import TypedDict

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


class ModelMapping:

    # /pet
    _pet = _pet_API
