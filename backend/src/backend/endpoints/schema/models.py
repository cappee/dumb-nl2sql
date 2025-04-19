from pydantic import BaseModel


class DatabaseSchema(BaseModel):
    table_name: str
    table_column: str