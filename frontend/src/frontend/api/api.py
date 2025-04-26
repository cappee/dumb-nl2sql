import os
import requests
from urllib.parse import urljoin, quote

from frontend.api.models import APIResponse

BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000")

class API():

    @staticmethod
    def get_schema() -> APIResponse:
        url = urljoin(BASE_URL, "schema_summary")
        response = requests.get(url)
        return APIResponse(status_code=response.status_code, results=response.text)
        

    @staticmethod
    def search(question: str) -> APIResponse:
        url = urljoin(BASE_URL, f"search/{quote(question)}")
        response = requests.get(url)
        return APIResponse(status_code=response.status_code, results=response.text)
    

    @staticmethod
    def add(data_line: str) -> APIResponse:
        url = urljoin(BASE_URL, "add")
        response = requests.post(url, json={"data_line": data_line})
        return APIResponse(status_code=response.status_code, results=response.text)