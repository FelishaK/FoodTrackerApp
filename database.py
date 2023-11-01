from flask import g
import sqlite3

DATABASE = "C:\\FlaskProjects\\foodapp\\foodtracker.db"


def connect_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db