from contextlib import closing
from sqlite3 import Connection
from typing import Optional, List

from pydantic import BaseModel


class NewDeck(BaseModel):
    deck_name: str 
    deck_left: Optional[str]
    deck_right: Optional[str]


class Deck(BaseModel):
    id: int 
    name: str 
    left: Optional[str]
    right: Optional[str]


def create_deck(conn: Connection, new_deck: NewDeck):
    sql = """insert into deck(deck_name, left, right) 
             values(?,?,?);"""

    with closing(conn.cursor()) as cur:
        cur.execute(sql, (
            new_deck.deck_name,
            new_deck.deck_left,
            new_deck.deck_right
        ))


def get_decks(conn: Connection) -> List[Deck]:
    sql = "select deck_id as id, deck_name as name, left, right from deck;"

    with closing(conn.cursor()) as cur:
        cur.execute(sql)
        rows = cur.fetchall() 
        decks = [Deck(**row) for row in rows]
        return decks

