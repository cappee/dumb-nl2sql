from pydantic import BaseModel


class Property(BaseModel):
    property_name: str
    propery_value: str


class SearchResponse(BaseModel):
    item_type: str
    properties: list[Property]