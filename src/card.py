from contextlib import closing
from sqlite3 import Connection
from typing import Optional, List
from enum import Enum 

from pydantic import BaseModel

class CardDirection(Enum):
    Left = 0
    Right = 1
    Both = 2

class NewCard(BaseModel):
    left: str 
    right: str
    direction: CardDirection
    deck_id: int


class Card(NewCard):
    card_id: int 


def create_card(conn: Connection, new_card: NewCard, tag_ids: List[int]):
    card_sql = """insert into card(left, right, direction, deck_id)
                  values (?,?,?,?)
                  returning card_id;"""
    tag_sql = """insert into card_tag(card_id, tag_id)
                 values (?,?);"""


    with closing(conn.cursor()) as cur:
        cur.execute(card_sql, (
            new_card.left,
            new_card.right,
            new_card.direction,
            new_card.deck_id
        ))

        card_id = cur.fetchone()[0]

        for tag_id in tag_ids:
            cur.execute(tag_sql, (
                card_id,
                tag_id
            ))

def read_card_by_id(conn: Connection, card_id: int) -> Optional[Card]:
    sql = """select 
                card_id,
                left, 
                right,
                direction,
                deck_id 
            from card 
            where card_id = ?;"""

    with closing(conn.cursor()) as cur:
        cur.execute(sql, (card_id,))
        row = cur.fetchone() 
        
        if row is not None:
            return Card(**row)
