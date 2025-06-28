from typing import Optional
from dotenv import dotenv_values
import logging

from fastapi import Request

from src.router import app, templates, DB_Conn
import src.deck as deck

CONFIG = dotenv_values(".env")
logging.basicConfig(level=logging.INFO)

@app.get("/card/create/deck/{deck_id}")
def create_card(req: Request, deck_id: int, conn = DB_Conn):
    deck_obj = deck.get_deck_by_id(conn, deck_id)
    return templates.TemplateResponse(request=req, name="deck_show_all.html",
                                      context={"deck": deck_obj})

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{items_id}")
def read_item(items_id: int, q: Optional[str] = None):
    return {"items_id": items_id, "q": q}
