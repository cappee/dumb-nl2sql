import csv
import mariadb
from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import ValidationError

from backend.db.mariadb import insert_data
from backend.models.models import AddRequest, Data, ErrorResponse, SuccessResponse
from backend.db.mariadb import get_connection


router = APIRouter()


def db_connection():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def csv2dict(line: str) -> Optional[dict[str, str]]:
    """Convert csv line to dictionary"""
    reader = csv.reader([line])
    row = next(reader)
    if len(row) != 7:
        return None
    keys = ["name", "director", "director_age", "release_year", "genre", "platform1", "platform2"]
    return dict(zip(keys, row))


@router.post(
    "/add/",
    summary="Add a new movie from a CSV-formatted string",
    response_description="Movie added successfully",
    responses={
        422: {
            "description": "Invalid input format or failed validation",
            "model": ErrorResponse
        },
        500: {
            "description": "Database error or internal server error",
            "model": ErrorResponse
        }
    }
)
def add(request: AddRequest, conn: mariadb.Connection = Depends(db_connection)) -> SuccessResponse:
    """
    Adds a new movie to the database.

    The input must be a **single line CSV string** in the following format:
    ```
    Name,Director,DirectorAge,ReleaseYear,Genre,Platform1,Platform2
    ```
    - Example:
      ```
      The Social Network,David Fincher,62,2010,Drama,Netflix,Amazon Prime Video
      ```

    Returns:
    - `200 OK` if the data was successfully added.
    - `422` if the input string is missing fields or fails validation.
    - `500` if there was an internal error while inserting into the database.
    """
    data_line = request.data_line.strip()
    print(f"Received data line: {data_line}")
    try:
        data = Data.model_validate(csv2dict(data_line))

        if insert_data(conn, data):
            return SuccessResponse(status="ok")
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to insert data into the database"
            )

    except(ValidationError, ValueError) as e:
        raise HTTPException(
            status_code=422,
            detail=f"Malformed input: {str(e)}"
        )