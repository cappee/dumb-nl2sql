from typing import Self
from pydantic import BaseModel, Field, model_validator


class DatabaseSchema(BaseModel):
    table_name: str
    table_column: str


class Data(BaseModel):
    name: str = Field(..., min_length=1)
    director: str = Field(..., min_length=1)
    director_age: int = Field(..., gt=0)
    release_year: int
    genre: str = Field(..., min_length=1)
    platform1: str
    platform2: str

    @model_validator(mode="after")
    def platform2_require_platform1(self) -> Self:
        if self.platform2 and not self.platform1:
            raise ValueError("Field 'platform2' requires 'platform1' to be present")
        return self


class Property(BaseModel):
    property_name: str
    property_value: str


class SearchResponse(BaseModel):
    item_type: str
    properties: list[Property]


class AddResponse(BaseModel):
    status: str = Field("OK")
    

class AddRequest(BaseModel):
    data_line: str = Field(..., description="CSV formatted string containing movie data")