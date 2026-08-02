import sqlite3

DATABASE = "sparkvault.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn



