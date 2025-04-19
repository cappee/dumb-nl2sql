from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from frontend.api.api import API

app = FastAPI(title="nl2sql HTML Interface")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Project home page"""
    return templates.TemplateResponse("index.html", {"request": request, "results": []})


@app.get("/search", response_class=HTMLResponse)
def search(request: Request, question: str = Query(...)):
    response = API.search(question)
    results = json.loads(response.results)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "results": json.dumps(results, indent=2), 
        "status_code": response.status_code
        })
    

@app.get("/schema_summary", response_class=HTMLResponse)
def schema_summary(request: Request):
    response = API.get_schema()
    results = json.loads(response.results)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "results": json.dumps(results, indent=2), 
        "status_code": response.status_code
        })



@app.post("/add", response_class=HTMLResponse)
def add(request: Request, data_line: str = Form(...)):
    response = API.add(data_line)
    results = json.loads(response.results)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "results": json.dumps(results, indent=2), 
        "status_code": response.status_code
        })