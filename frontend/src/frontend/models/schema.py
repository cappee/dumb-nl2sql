from pydantic import BaseModel


class TableSchema(BaseModel):
    table_name: str
    table_column: str