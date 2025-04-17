from fastapi import APIRouter, Depends, HTTPException

from backend.db.mariadb import execute_query, execute_query_columns, get_connection
from backend.models.models import Property, SearchResponse
from backend.endpoints.search.nl2sql import Nl2SQL


router = APIRouter()


def db_connection():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@router.get("/search/{question}")
def search(question: str, conn = Depends(db_connection)) -> list[SearchResponse]:
    """
    Search for a movie based on a question.
    
    Args:
        question (str): The question to search for.
        
    Returns:
        dict: A dictionary containing the search results.
    """
    nl2sql = Nl2SQL(question)
    query = nl2sql.get_sql_query()

    if not query:
        raise HTTPException(status_code=422, detail="Invalid question, unable to generate SQL query.")
    
    response: list[SearchResponse] = []
    for row in execute_query_columns(conn, query):
        properties = [
            Property(property_name=k, property_value=str(v)) 
            for k, v in row.items()
        ]
        response.append(SearchResponse(item_type=nl2sql.get_item_type(), properties=properties))

    return response