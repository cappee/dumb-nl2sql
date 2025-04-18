import csv
import mariadb
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from backend.db.mariadb import insert_data, db_connection
from backend.models.models import AddRequest, Data, AddResponse


router = APIRouter()


def csv2dict(line: str) -> Optional[dict[str, str]]:
    """Convert csv line to dictionary"""
    reader = csv.reader([line])
    row = next(reader)
    if len(row) != 7:
        return None
    keys = ["name", "director", "director_age", "release_year", "genre", "platform1", "platform2"]
    return dict(zip(keys, row))


@router.post(
    "/add",
    summary="Add a new movie from a CSV-formatted string"
)
def add(request: AddRequest, conn: mariadb.Connection = Depends(db_connection)) -> AddResponse:
    """
    Adds a new movie to the database.

    The input must be a **single line CSV string** in the following format:
    ```
    Name,Director,DirectorAge,ReleaseYear,Genre,Platform1,Platform2
    ```
    """
    data_line = request.data_line.strip()
    try:
        data = Data.model_validate(csv2dict(data_line))

        if insert_data(conn, data):
            return AddResponse(status="ok")
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