from contextlib import closing
from sqlite3 import Connection
from typing import List

from pydantic import BaseModel

class NewTag(BaseModel):
    tag_name: str 
    deck_id: int 

class Tag(NewTag):
    id: int


def create_tag(conn: Connection, tag: NewTag): 
    sql = """insert into tag(tag_name, deck_id)
           values (?,?);"""

    with closing(conn.cursor()) as cur:
        cur.execute(sql, (
            tag.tag_name,
            tag.deck_id
        ))

def read_by_deck(conn: Connection, deck_id) -> List[Tag]:
    sql = """select 
                tag_id as id,
                tag_name,
                deck_id
            from tag
            where deck_id = ?;"""


    with closing(conn.cursor()) as cur:
        cur.execute(sql, (deck_id,))
        rows = cur.fetchall()
        tags = [Tag(**row) for row in rows]
        return tags


def delete_by_id(conn: Connection, tag_id: int):
    sql = "delete from tag where tag_id = ?;"

    with closing(conn.cursor()) as cur:
        cur.execute(sql, (tag_id,))
