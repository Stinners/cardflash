from contextlib import closing
from sqlite3 import Connection
from typing import Optional, List
import logging
logging.basicConfig(level=logging.INFO)

from pydantic import BaseModel


class NewDeck(BaseModel):
    deck_name: str 
    deck_left: Optional[str]
    deck_right: Optional[str]


class Deck(BaseModel):
    deck_id: int 
    name: str 
    left: Optional[str]
    right: Optional[str]


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
        import pdb; pdb.set_trace()
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
