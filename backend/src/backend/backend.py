from contextlib import asynccontextmanager
from fastapi import FastAPI
import mariadb

from backend.endpoints.search import search
from backend.endpoints.schema import schema
from backend.endpoints.add import add
from backend.db import mariadb as db


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = mariadb.connect(
        host="database",
        port=3306,
        user="py",
        password="esonero",
        database="movies_db"
    )
    db.populate_if_empty(conn)
    conn.close()

    yield

app = FastAPI(lifespan=lifespan)
app.title = "Movies API"
app.description = "API for managing movies and their details."

app.include_router(search.router)
app.include_router(schema.router)
app.include_router(add.router)