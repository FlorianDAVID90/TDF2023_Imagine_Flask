import pymysql.cursors
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host="localhost",
            user="flodavid",
            password="#Apoal75",
            database="bdd_fdavid5",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    return db