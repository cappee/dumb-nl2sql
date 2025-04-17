from fastapi import FastAPI

from backend.endpoints.search import search
from backend.endpoints.schema import schema
from backend.endpoints.add import add


app = FastAPI()
app.title = "Movies API"
app.description = "API for managing movies and their details."

app.include_router(search.router)
app.include_router(schema.router)
app.include_router(add.router)