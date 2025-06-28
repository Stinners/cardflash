import sqlite3
from dotenv import dotenv_values

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


CONFIG = dotenv_values(".env")

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


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
