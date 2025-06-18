from contextlib import closing
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Optional, List


@dataclass
class Deck:
    id: int 
    name: str 
    left: Optional[str]
    right: Optional[str]



def create_deck(conn: Connection, name: str, left: Optional[str], right: Optional[str]):
    sql = """insert into deck(deck_name, left, right) 
             values(?,?,?);"""

    with closing(conn.cursor()) as cur:
        cur.execute(sql, (name, left, right))


def get_decks(conn: Connection) -> List[Deck]:
    sql = "select deck_id as id, deck_name as name, left, right from deck;"

    with closing(conn.cursor()) as cur:
        cur.execute(sql)
        rows = cur.fetchall() 
        decks = [Deck(**row) for row in rows]
        return decks

