from typing import Optional, Annotated
import sqlite3
from dotenv import dotenv_values
import logging

from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import src.deck as deck

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

CONFIG = dotenv_values(".env")
logging.basicConfig(level=logging.INFO)

app.mount("/static", StaticFiles(directory="static"), name="static")


###################### Get DB Connection ###################

def db_conn():
    raw_db_url = CONFIG["DATABASE_URL"]  
    db_url = raw_db_url.removeprefix("sqlite:")  #type: ignore
    conn = sqlite3.connect(db_url)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = 1")
        yield conn 
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()

DB_Conn = Depends(db_conn)


###################### Deck Routes #########################

@app.get("/deck/create")
def insert_deck_template(req: Request):
    return templates.TemplateResponse(request=req, name="deck_create.html")


@app.post("/deck/create")
def insert_deck(req: Request, data: Annotated[deck.NewDeck, Form()], conn = DB_Conn):
    logging.info("Got Create Deck Form")
    try:
        deck.create_deck(conn, data)
        return templates.TemplateResponse(request=req, name="deck_create.html")
    except Exception as ex:
        return templates.TemplateResponse(request=req, name="deck_create.html", 
                                          context={"error": str(ex)})


@app.get("/deck/show/all")
def show_all_decks(req: Request, conn = DB_Conn):
    logging.info("Getting all decks")
    decks = deck.get_decks(conn)
    return templates.TemplateResponse(request=req, name="deck_show_all.html",
                                      context={"decks": decks})

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
