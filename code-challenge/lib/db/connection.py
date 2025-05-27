# lib/db/connection.py
import sqlite3

def get_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def setup_database():
    with get_connection() as conn:
        with open('lib/db/schema.sql') as f:
            conn.executescript(f.read())