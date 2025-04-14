from fastapi import FastAPI

app = FastAPI()

@app.get("/search/")
def search(question: str):
    pass

