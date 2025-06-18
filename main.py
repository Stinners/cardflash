from typing import Optional, Annotated

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import src.deck as deck

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.post("/deck/create")
def insert_deck(req: Request, data: Annotated[deck.NewDeck, Form()]):
    print(data)
    return templates.TemplateResponse(request=req, name="deck_create.html")

@app.get("/deck/create")
def insert_deck_template(req: Request):
    return templates.TemplateResponse(request=req, name="deck_create.html")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{items_id}")
def read_item(items_id: int, q: Optional[str] = None):
    return {"items_id": items_id, "q": q}
