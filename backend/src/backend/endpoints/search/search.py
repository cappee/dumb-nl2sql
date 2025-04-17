from fastapi import APIRouter, Depends, HTTPException

from backend.models.models import Property, SearchResponse
from backend.endpoints.search.nl2sql import Nl2SQL
from backend.db.mariadb import db_connection, execute_query


router = APIRouter()


@router.get(
    "/search/{question}",
    summary="Search for a movie based on a question"
)
def search(question: str, conn = Depends(db_connection)) -> list[SearchResponse]:
    """
    Search for a movie based on a question.

    This endpoint uses a dumb natural language processing to convert the question into a SQL query.
    """
    nl2sql = Nl2SQL(question)

    if not nl2sql.is_valid():
        raise HTTPException(status_code=422, detail="Invalid question, unable to generate SQL query.")
    
    response: list[SearchResponse] = []
    for row in execute_query(conn, nl2sql.get_sql_query()):
        properties = [
            Property(property_name=k, property_value=str(v)) 
            for k, v in zip(nl2sql.get_fields(), row)
        ]
        response.append(SearchResponse(item_type=nl2sql.get_item_type(), properties=properties))

    return response