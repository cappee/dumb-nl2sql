from fastapi import APIRouter, Depends

from backend.db.mariadb import db_connection, execute_query
from backend.models.models import DatabaseSchema


router = APIRouter()


@router.get(
    "/schema_summary/", 
    summary="Get DB schema summary"
)
def schema_summmary(conn = Depends(db_connection)) -> list[DatabaseSchema]:
    """
    Returns a summary of the database schema.

    This endpoint provides a list of all tables and their corresponding columns.
    """
    schema: list[DatabaseSchema] = list()

    tables = execute_query(conn, "SHOW tables;")
    for table in tables:
        columns = execute_query(conn, f"SHOW columns FROM {table[0]}")
        for column in columns:
            schema.append(DatabaseSchema(table_name=table[0], table_column=column[0]))

    return schema