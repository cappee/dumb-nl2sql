from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from frontend.models.schema import TableSchema

app = FastAPI(title="nl2sql HTML Interface")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Project home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/search/")
def search(question: str):
    pass
    

@app.get("/schema_summmary")
def schema_summary() -> list[TableSchema]:
    return list()