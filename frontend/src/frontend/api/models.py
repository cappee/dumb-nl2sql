from pydantic import BaseModel


class APIResponse(BaseModel):
    status_code: int
    results: str