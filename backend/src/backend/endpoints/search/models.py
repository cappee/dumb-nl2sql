from typing import Callable, TypedDict
from pydantic import BaseModel


class Query(TypedDict):
    sql: Callable[..., str]
    item_type: str
    fields: list[str]


class Property(BaseModel):
    property_name: str
    property_value: str


class SearchResponse(BaseModel):
    item_type: str
    properties: list[Property]