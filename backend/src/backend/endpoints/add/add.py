import csv
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from backend.db.mariadb import add_data_to_db, db_connection
from backend.models.models import Data


router = APIRouter()


def csv2dict(line: str) -> Optional[dict[str, str]]:
    """Convert csv line to dictionary"""
    reader = csv.reader([line])
    row = next(reader)
    if len(row) != 7:
        return None
    keys = ["title", "director", "director_age", "release_year", "genre", "platform1", "platform2"]
    return dict(zip(keys, row))


@router.post("/add/")
def add(data_line: str, conn = Depends(db_connection)):
    """Validate input string and add line to db"""
    try:
        data = Data.model_validate(csv2dict(data_line))

        if add_data_to_db(conn, data):
            return {"status": "OK"}

    except(ValidationError, ValueError) as e:
        raise HTTPException(
            status_code=422,
            detail=f"Malformed input: {str(e)}"
        )