from contextlib import closing
from sqlite3 import Connection
from typing import Optional, List
import logging
from typing import Annotated

from pydantic import BaseModel
from fastapi import Request, Form

from src.router import app, templates, DB_Conn

logging.basicConfig(level=logging.INFO)

class NewDeck(BaseModel):
    deck_name: str 
    deck_left: Optional[str]
    deck_right: Optional[str]


class Deck(BaseModel):
    deck_id: int 
    name: str 
    left: Optional[str]
    right: Optional[str]

################### Routes ##########################33

@app.get("/deck/create")
def insert_deck_template(req: Request):
    return templates.TemplateResponse(request=req, name="deck_create.html")


@app.post("/deck/create")
def insert_deck(req: Request, data: Annotated[NewDeck, Form()], conn = DB_Conn):
    logging.info("Got Create Deck Form")
    try:
        create_deck(conn, data)
        return templates.TemplateResponse(request=req, name="deck_create.html")
    except Exception as ex:
        return templates.TemplateResponse(request=req, name="deck_create.html", 
                                          context={"error": str(ex)})


@app.get("/deck/show/all")
def show_all_decks(req: Request, conn = DB_Conn):
    logging.info("Getting all decks")
    decks = get_decks(conn)
    return templates.TemplateResponse(request=req, name="deck_show_all.html",
                                      context={"decks": decks})

@app.get("/card/create/deck/{deck_id}")
def create_card(req: Request, deck_id: int, conn = DB_Conn):
    deck = get_deck_by_id(conn, deck_id)
    return templates.TemplateResponse(request=req, name="deck_show_all.html",
                                      context={"deck": deck})

################### Handlers ##########################33

def create_deck(conn: Connection, new_deck: NewDeck):
    sql = """insert into deck(deck_name, left_name, right_name) 
             values(?,?,?);"""
    logging.info("Executing create_deck")

    with closing(conn.cursor()) as cur:
        cur.execute(sql, (
            new_deck.deck_name,
            new_deck.deck_left,
            new_deck.deck_right
        ))


def get_decks(conn: Connection) -> List[Deck]:
    sql = """select
                deck_id,
                deck_name as name,
                left_name as left, 
                right_name as right 
            from deck;"""


    with closing(conn.cursor()) as cur:
        cur.execute(sql)
        rows = cur.fetchall() 
        decks = [Deck(**row) for row in rows]
        return decks

def get_deck_by_id(conn: Connection, deck_id: int) -> Optional[Deck]:
    sql = """select
                deck_id,
                deck_name as name,
                left_name as left, 
                right_name as right 
            from deck
            where deck_id = ?;"""

    with closing(conn.cursor()) as cur:
        cur.execute(sql, (deck_id,))
        row = cur.fetchone() 
        if row != None:
            return Deck(**row)


def delete_deck(conn: Connection, deck_id: int):
    sql = """delete from deck where deck_id = ?;"""

    with closing(conn.cursor()) as cur:
        cur.execute(sql, (deck_id,))
