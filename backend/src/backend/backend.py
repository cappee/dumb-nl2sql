from fastapi import Depends, FastAPI

from backend.db.mariadb import db_connection, get_schema
from backend.models.models import TableSchema
from backend.endpoints.add import add


app = FastAPI()
app.title = "Movies API"


@app.get("/search/")
def search(question: str):
    pass


@app.get("/schema_summary/")
def schema_summmary(conn = Depends(db_connection)) -> list[TableSchema]:
    return get_schema(conn)

app.include_router(add.router)