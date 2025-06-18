from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{items_id}")
def read_item(items_id: int, q: Optional[str] = None):
    return {"items_id": items_id, "q": q}
